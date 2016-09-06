#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
@author: ttlttl
@contact: wangmingape@gmail.com
@site: https://github.com/ttlttl
@file: whatsnew-q.py
@time: 9/6/2016 2:11 PM
"""

import argparse
import multiprocessing
import os
import queue
import tempfile
import threading
import webbrowser
import Feed
import Qtrac


def main():
    limit, concurrency = handle_commandline()
    Qtrac.report("starting...")
    filename = os.path.join(os.path.dirname(__file__), "whatsnew.dat")
    jobs = queue.Queue()
    results = queue.Queue()
    create_threads(limit, jobs, results, concurrency)
    todo = add_jobs(filename, jobs)
    process(todo, jobs, results, concurrency)


def handle_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--limit", type=int, default=0,
            help="the maximum items per feed [default: unlimited]")
    parser.add_argument("-c", "--concurrency", type=int,
            default=multiprocessing.cpu_count() * 4,
            help="specify the concurrency (for debugging and "
                "timing) [default: %(default)d]")
    args = parser.parse_args()
    return args.limit, args.concurrency


def create_threads(limit, jobs, results, concurrency):
    for _ in range(concurrency):
        thread = threading.Thread(target=worker, args=(limit, jobs,
                results))
        thread.daemon = True
        thread.start()


def worker(limit, jobs, results):
    while True:
        try:
            feed = jobs.get()
            ok, result = Feed.read(feed, limit)
            if not ok:
                Qtrac.report(result, True)
            elif result is not None:
                Qtrac.report("read {}".format(result[0][4:-6]))
                results.put(result)
        finally:
            jobs.task_done()


def add_jobs(filename, jobs):
    for todo, feed in enumerate(Feed.iter(filename), start=1):
        jobs.put(feed)
    return todo


def process(todo, jobs, results, concurrency):
    canceled = False
    try:
        jobs.join() # Wait for all the work to be done
    except KeyboardInterrupt: # May not work on Windows
        Qtrac.report("canceling...")
        canceled = True
    if canceled:
        done = results.qsize()
    else:
        done, filename = output(results)
    Qtrac.report("read {}/{} feeds using {} threads{}".format(done, todo,
            concurrency, " [canceled]" if canceled else ""))
    print()
    if not canceled:
        webbrowser.open(filename)


def output(results):
    done = 0
    filename = os.path.join(tempfile.gettempdir(), "whatsnew.html")
    with open(filename, "wt", encoding="utf-8") as file:
        file.write("<!doctype html>\n")
        file.write("<html><head><title>What's New</title></head>\n")
        file.write("<body><h1>What's New</h1>\n")
        while not results.empty(): # Safe because all jobs have finished
            result = results.get_nowait()
            done += 1
            for item in result:
                file.write(item)
        file.write("</body></html>\n")
    return done, filename


if __name__ == "__main__":
    main()

