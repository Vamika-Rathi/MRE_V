#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename    :  main.py
Date        :  2024/05/21 09:23:41
Author      :  Tung Thai
"""

import argparse

import pack_core


def run(args: list = None):
    """Just run. Don't ask, but parse"""
    parser = argparse.ArgumentParser(
        description="Convert text data to compact data for easier distribution."
    )
    parser.add_argument(
        "input", metavar="FILE", type=str, nargs="+", help="The input file"
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="FILE",
        type=str,
        default="",
        help="Specify custom path for output. If not set, output in current folder",
    )
    parser.add_argument("-t", type=str, default=".mat", help="Output file type")
    parser.add_argument("-s", type=str, default="_mat", help="Output file suffix")

    args = parser.parse_args(args)
    my_worker = pack_core.PackCore()

    for a_path in args.input:
        if my_worker.load(a_path) == 0:

            # Do something with the data
            # For example
            #
            # my_array = my_worker.data["poi"][:10]  # get first 10 coordinates of data

            my_worker.save_lst(args.s, args.t, False, args.output)

    print("Done")


if __name__ == "__main__":
    run()
