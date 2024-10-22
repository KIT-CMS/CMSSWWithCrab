#! /usr/bin/env python3

# TODO:
# Add a check of for the input and output datasets about number of events.
# This would allow to justify, that the production was completely successful.
# Possible tool: DBS client bindings

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

import CRABClient
from CRABAPI.RawCommand import crabCommand

def parse_args():
    parser = argparse.ArgumentParser(
        description="Script to manage a CMSSW production with crab",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Main options

    ## Necessary arguments
    parser.add_argument("--crab-config-patterns", nargs='+', required=True, help="List of path patterns to the crab configuration files, processed with glob")
    parser.add_argument("--maxmemory", default=None, help="Maximum memory threshold in MB for resubmission passed to crab")
    parser.add_argument("--maxjobruntime", default=None, help="Maximum job runtime threshold in minutes for resubmission passed to crab")
    parser.add_argument("--nworkers", default=5, help="Number of workers to manage the crab tasks simultaneously")

    return parser.parse_args()

def load_config(config_path):
    spec = importlib.util.spec_from_file_location("crab_config_module", config_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.config

async def submit(config, logger):
    loop = asyncio.get_event_loop()
    try:
        sleep_duration = random.randint(0,12*nworkers)
        await asyncio.sleep(sleep_duration)
        return await loop.run_in_executor(None, lambda: crabCommand('submit', config=config))
    except Exception as e:
        logger.error(f"Failed submitting task:\n{e}")
        cfg_directory = os.path.join(config.General.workArea, "crab_" + config.General.requestName)
        logger.debug(f"Cleaning up config directory {cfg_directory}")
        shutil.rmtree(cfg_directory)
        return None

async def status(cfg_dir, logger, nworkers):
    loop = asyncio.get_event_loop()
    try:
        sleep_duration = random.randint(0,12*nworkers)
        await asyncio.sleep(sleep_duration)
        return await loop.run_in_executor(None, lambda: crabCommand('status', dir=cfg_dir))
    except Exception as e:
        logger.error(f"Failed querying status of task:\n{e}")
        return None

async def resubmit(cfg_dir, logger, nworkers, **kwargs):
    loop = asyncio.get_event_loop()
    try:
        sleep_duration = random.randint(0,12*nworkers)
        await asyncio.sleep(sleep_duration)
        return await loop.run_in_executor(None, lambda: crabCommand('resubmit', dir=cfg_dir, **kwargs))
    except Exception as e:
        logger.error(f"Failed resubmitting task:\n{e}")
        return None

async def worker(queue, args, worker_id, nworkers):
    # Set up logging for this worker
    logs_directory = pathlib.Path("logs")
    logs_directory.mkdir(mode=0o755,parents=True,exist_ok=True)
    logs_path = logs_directory / f'worker_{worker_id}.log'

    logger = logging.getLogger(f'worker_{worker_id}')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(str(logs_path))
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    while True:
        cfgpath = await queue.get()
        if cfgpath is None:
            break

        cfg = load_config(cfgpath)
        cfg_directory = os.path.join(cfg.General.workArea, "crab_" + cfg.General.requestName)
        res = None
        if not os.path.isdir(cfg_directory):
            logger.info(f"Submitting {cfgpath}")
            while not res:
                res = await submit(cfg, logger, nworkers)
                await asyncio.sleep(10)
            await asyncio.sleep(600)

        n_published = -1
        n_finished = -2
        n_all = -3
        while n_all != n_finished or n_all != n_published:
            logger.info(f"Checking task status for {cfg_directory}")
            res = await status(cfg_directory, logger, nworkers)
            if res:
                #json.dump(res, open("res.json", "w"), indent=2, sort_keys=True)
                n_all = sum([res["jobsPerStatus"][state] for state in res["jobsPerStatus"].keys()])
                n_intermediate = res["jobsPerStatus"].get("idle", 0) + res["jobsPerStatus"].get("running", 0)
                n_finished = res["jobsPerStatus"].get("finished", 0)
                n_failed = res["jobsPerStatus"].get("failed", 0)
                n_published = res["publication"].get("done", 0)
                logger.info(f"Number of jobs: all = {n_all}, intermediate = {n_intermediate}, finished = {n_finished}, failed = {n_failed}, published = {n_published}")
                kwargs = {k: v for k, v in {
                    "maxmemory": args.maxmemory,
                    "maxjobruntime": args.maxjobruntime,
                }.items() if v is not None}
                if n_intermediate == 0 and n_failed > 0 and kwargs:
                    logger.info(f"Resubmitting task for {cfg_directory}")
                    resub = None
                    while not resub:
                        resub = await resubmit(cfg_directory, logger, nworkers, **kwargs)
                        await asyncio.sleep(10)
            await asyncio.sleep(900)
        logger.info(f"Task {cfg_directory} finished. Output datasets:")
        for dataset in ast.literal_eval(res["outdatasets"]):
            logger.info(f"\t{dataset}")
        queue.task_done()

async def main():
    args = parse_args()

    # Process the list of patterns and create a flat list of config paths
    config_paths = []
    for pattern in args.crab_config_patterns:
        config_paths.extend(glob.glob(pattern))

    queue = asyncio.Queue()

    # Create worker tasks
    nworkers = min(len(config_paths), args.nworkers)
    workers = [asyncio.create_task(worker(queue, args, i, nworkers)) for i in range(nworkers)]

    # Enqueue config paths
    for cfgpath in config_paths:
        await queue.put(cfgpath)

    # Wait until the queue is fully processed
    await queue.join()

    # Stop workers
    for _ in range(num_workers):
        await queue.put(None)
    await asyncio.gather(*workers)

if __name__ == "__main__":
    asyncio.run(main())
