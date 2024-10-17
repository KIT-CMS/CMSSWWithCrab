#! /usr/bin/env python3

import yaml
import os
import glob
import asyncio
import logging
import argparse
import pathlib
import importlib.util
import json
import time

import CRABClient
from CRABAPI.RawCommand import crabCommand

def parse_args():
    parser = argparse.ArgumentParser(
        description="Script to manage a CMSSW production with crab",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Main options

    ## Necessary arguments
    parser.add_argument("--crab-config-pattern",required=True,help="Path pattern to the crab configration files, processed with glob")
    parser.add_argument("--maxmemory",default=None,help="Maximum memory threshold in MB for resubmission passed to crab")
    parser.add_argument("--maxjobruntime",default=None,help="Maximum job runtime threshold in minutes for resubmission passed to crab")

    return parser.parse_args()

def load_config(config_path):
    spec = importlib.util.spec_from_file_location("crab_config_module",config_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.config

async def submit(config):
    loop = asyncio.get_event_loop()
    try:
        return await loop.run_in_executor(None,crabCommand,'submit',config=config)
    except Exception as e:
        print(f"Failed submitting task:\n{e}")

async def status(cfg_dir):
    loop = asyncio.get_event_loop()
    try:
        return await loop.run_in_executor(None, crabCommand, 'status',dir=cfg_dir)
    except Exception as e:
        print(f"Failed querying status of task:\n{e}")

async def resubmit(cfg_dir, **kwargs):
    loop = asyncio.get_event_loop()
    try:
        return await loop.run_in_executor(None,crabCommand,'resubmit',dir=cfg_dir,**kwargs)
    except Exception as e:
        print(f"Failed resubmitting task:\n{e}")

async def worker(queue, args):
    while True:
        cfgpath = await queue.get()
        if cfgpath is None:
            break

        cfg = load_config(cfgpath)
        cfg_directory = os.path.join(cfg.General.workArea, "crab_" + cfg.General.requestName)
        if not os.path.isdir(cfg_directory):
            print(f"Submitting {cfgpath}")
            await submit(cfg)
            await asyncio.sleep(600)

        n_published = -1
        n_finished = -2
        n_all = -3
        while n_all != n_finished or n_all != n_published:
            print(f"Checking task status for {cfg_directory}")
            res = await status(cfg_directory)
            #json.dump(res, open("res.json", "w"), indent=2, sort_keys=True)
            n_all = sum([res["jobsPerStatus"][state] for state in res["jobsPerStatus"].keys()])
            n_intermediate = res["jobsPerStatus"].get("idle", 0) + res["jobsPerStatus"].get("running", 0)
            n_finished = res["jobsPerStatus"].get("finished", 0)
            n_failed = res["jobsPerStatus"].get("failed", 0)
            n_published = res["publication"].get("done", 0)
            print(f"Number of jobs: all = {n_all}, intermediate = {n_intermediate}, finished = {n_finished}, failed = {n_failed}, published = {n_published}")
            kwargs = {k: v for k, v in {
                "maxmemory": args.maxmemory,
                "maxjobruntime": args.maxjobruntime,
            }.items() if v is not None}
            if n_intermediate == 0 and n_failed > 0 and kwargs:
                await resubmit(cfg_directory, **kwargs)
            await asyncio.sleep(60)

        queue.task_done()

async def main():
    args = parse_args()

    config_paths = glob.glob(args.crab_config_pattern)
    queue = asyncio.Queue()

    # Create worker tasks
    num_workers = min(len(config_paths), 5)  # Adjust the number of workers as needed
    workers = [asyncio.create_task(worker(queue, args)) for _ in range(num_workers)]

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