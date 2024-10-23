#! /usr/bin/env python3

import os
import glob
import asyncio
import logging
import argparse
import pathlib
import importlib.util
import shutil
import random
import ast
import json

import CRABClient
from CRABAPI.RawCommand import crabCommand


def parse_args():
    parser = argparse.ArgumentParser(
        description="Script to manage a CMSSW production with crab",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Main options

    ## Necessary arguments
    parser.add_argument(
        "--crab-config-patterns",
        nargs="+",
        required=True,
        help="List of path patterns to the crab configuration files, processed with glob",
    )
    parser.add_argument(
        "--maxmemory",
        default=None,
        help="Maximum memory threshold in MB for resubmission passed to crab",
    )
    parser.add_argument(
        "--maxjobruntime",
        default=None,
        help="Maximum job runtime threshold in minutes for resubmission passed to crab",
    )
    parser.add_argument(
        "--nworkers",
        default=5,
        type=int,
        help="Number of workers to manage the crab tasks simultaneously",
    )
    parser.add_argument(
        "--sitewhitelist",
        default=None,
        help="Comma-separated list of sites to exclusively run your jobs on.",
    )
    parser.add_argument(
        "--siteblacklist",
        default=None,
        help="Comma-separated list of sites to avoid running your jobs there.",
    )

    return parser.parse_args()


def load_config(config_path):
    spec = importlib.util.spec_from_file_location("crab_config_module", config_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.config


async def submit(config, logger, nworkers):
    loop = asyncio.get_event_loop()
    try:
        sleep_duration = random.randint(0, 12 * nworkers)
        await asyncio.sleep(sleep_duration)
        return await loop.run_in_executor(
            None, lambda: crabCommand("submit", config=config)
        )
    except Exception as e:
        logger.error(f"Failed submitting task:\n{e}")
        cfg_directory = os.path.join(
            config.General.workArea, "crab_" + config.General.requestName
        )
        logger.debug(f"Cleaning up config directory {cfg_directory}")
        shutil.rmtree(cfg_directory)
        return None


async def status(cfg_dir, logger, nworkers):
    loop = asyncio.get_event_loop()
    try:
        sleep_duration = random.randint(0, 12 * nworkers)
        await asyncio.sleep(sleep_duration)
        return await loop.run_in_executor(
            None, lambda: crabCommand("status", dir=cfg_dir)
        )
    except Exception as e:
        logger.error(f"Failed querying status of task:\n{e}")
        return None


async def resubmit(cfg_dir, logger, nworkers, **kwargs):
    loop = asyncio.get_event_loop()
    try:
        sleep_duration = random.randint(0, 12 * nworkers)
        await asyncio.sleep(sleep_duration)
        return await loop.run_in_executor(
            None, lambda: crabCommand("resubmit", dir=cfg_dir, **kwargs)
        )
    except Exception as e:
        logger.error(f"Failed resubmitting task:\n{e}")
        return None


async def run_dasgoclient_query(dataset, instance):
    command = [
        "dasgoclient",
        "-query",
        f"dataset dataset={dataset} instance={instance}",
        "-json",
    ]
    process = await asyncio.create_subprocess_exec(
        *command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        raise RuntimeError(f"Failed to query DAS: {stderr.decode().strip()}")
    return json.loads(stdout.decode().strip())


async def worker(
    submission_queue, status_queue, args, worker_id, nworkers, is_submission_worker
):
    # Set up logging for this worker
    logs_directory = pathlib.Path("logs")
    logs_directory.mkdir(mode=0o755, parents=True, exist_ok=True)
    logs_path = logs_directory / f"worker_{worker_id}.log"

    logger = logging.getLogger(f"worker_{worker_id}")
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(str(logs_path))
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    while True:
        queue = submission_queue if is_submission_worker else status_queue
        cfgpath = await queue.get()
        if cfgpath is None:
            break

        cfg = load_config(cfgpath)
        cfg_directory = os.path.join(
            cfg.General.workArea, "crab_" + cfg.General.requestName
        )
        res = None

        if is_submission_worker:
            if not os.path.isdir(cfg_directory):
                logger.info(f"Submitting {cfgpath}")
                res = await submit(cfg, logger, nworkers)
            else:
                logger.info(
                    f"Task directory exists: {cfg_directory}. Considering as submitted."
                )
            # Enqueue the task for status checking
            await status_queue.put(cfgpath)

        else:
            n_published = -1
            n_finished = -2
            n_all = -3
            while n_all != n_finished or n_all != n_published:
                logger.info(f"Checking task status for {cfg_directory}")
                res = await status(cfg_directory, logger, nworkers)
                if res:
                    n_all = sum(
                        [
                            res["jobsPerStatus"][state]
                            for state in res["jobsPerStatus"].keys()
                        ]
                    )
                    n_intermediate = res["jobsPerStatus"].get("idle", 0) + res[
                        "jobsPerStatus"
                    ].get("running", 0)
                    n_finished = res["jobsPerStatus"].get("finished", 0)
                    n_failed = res["jobsPerStatus"].get("failed", 0)
                    n_published = res["publication"].get("done", 0)
                    logger.info(
                        f"Number of jobs: all = {n_all}, intermediate = {n_intermediate}, finished = {n_finished}, failed = {n_failed}, published = {n_published}"
                    )
                    kwargs = {
                        k: v
                        for k, v in {
                            "maxmemory": args.maxmemory,
                            "maxjobruntime": args.maxjobruntime,
                            "sitewhitelist": args.sitewhitelist,
                            "siteblacklist": args.siteblacklist,
                        }.items()
                        if v is not None
                    }
                    if n_intermediate == 0 and n_failed > 0 and kwargs:
                        logger.info(f"Resubmitting task for {cfg_directory}")
                        resub = None
                        while not resub:
                            resub = await resubmit(
                                cfg_directory, logger, nworkers, **kwargs
                            )
                            await asyncio.sleep(10)
                await asyncio.sleep(
                    0 if n_all == n_finished and n_all == n_published else 900
                )
            logger.info(f"Task {cfg_directory} finished. Output datasets:")
            for dataset in ast.literal_eval(res["outdatasets"]):
                try:
                    das_output = await run_dasgoclient_query(dataset, "prod/phys03")
                    das_input = await run_dasgoclient_query(
                        cfg.Data.inputDataset, "prod/global"
                    )
                    nevents_output = None
                    nevents_input = None
                    for o in das_output:
                        for do in o["dataset"]:
                            if "nevents" in do:
                                nevents_output = do["nevents"]
                                break
                    for i in das_input:
                        for di in i["dataset"]:
                            if "nevents" in di:
                                nevents_input = di["nevents"]
                                break
                    if (
                        nevents_input is None
                        or nevents_output is None
                        or nevents_input != nevents_output
                    ):
                        logger.error(
                            f"Numbers of events in input {cfg.Data.inputDataset} ({nevents_input}) does not match output {dataset}: {nevents_output}. Crab task FAILED."
                        )
                    else:
                        logger.info(
                            f"\t{dataset}: {nevents_output} events, consistent with input dataset"
                        )
                except Exception as e:
                    logger.error(
                        f"Failed to query DAS for dataset {dataset} and its parent:\n{e}"
                    )

        queue.task_done()


async def main():
    args = parse_args()

    # Process the list of patterns and create a flat list of config paths
    config_paths = []
    for pattern in args.crab_config_patterns:
        config_paths.extend(glob.glob(pattern))

    submission_queue = asyncio.Queue()
    status_queue = asyncio.Queue()

    # Create a single submission worker
    submission_worker = asyncio.create_task(
        worker(
            submission_queue,
            status_queue,
            args,
            "submission",
            1,
            is_submission_worker=True,
        )
    )

    # Create multiple status workers
    nworkers = min(len(config_paths), args.nworkers)
    status_workers = [
        asyncio.create_task(
            worker(
                submission_queue,
                status_queue,
                args,
                i,
                nworkers,
                is_submission_worker=False,
            )
        )
        for i in range(nworkers)
    ]

    # Enqueue config paths for submission
    for cfgpath in config_paths:
        await submission_queue.put(cfgpath)

    # Wait until the submission queue is fully processed
    await submission_queue.join()

    # Stop the submission worker:
    await submission_queue.put(None)
    await submission_worker

    # Wait until the status queue is fully processed
    await status_queue.join()

    # Stop workers
    for _ in range(nworkers):
        await status_queue.put(None)
    await asyncio.gather(*status_workers)


if __name__ == "__main__":
    asyncio.run(main())
