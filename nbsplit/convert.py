#!/usr/bin/env python3

import os
import textwrap
import argparse
import subprocess


def main():
    parser = argparse.ArgumentParser(description=textwrap.dedent("""
		Convert a notebook containing both solutions and tasks into two more notebooks. Solution and task cells need to be marked with the metadata {"exercise": "solution"} and {"exercise": "task"}.
        """), formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('infile', type=argparse.FileType('r'), help="Input file to convert.")
    parser.add_argument('--output-task', nargs='?', type=argparse.FileType('w'), default=None, help="Output file for task version.")
    parser.add_argument('--output-solution', nargs='?', type=argparse.FileType('w'), default=None, help="Output file for solution version.")
    parser.add_argument('--basekey', type=str, help="Basekey to use for discriminating the tags (default: exercise)", default="exercise")
    args = parser.parse_args()
    
    inpath, inext = os.path.splitext(args.infile.name)
    if inext != ".ipynb":
            exit("files must have .ipynb extension")
    
    if args.output_task is None:
        args.output_task = open(inpath+"_task"+inext, "w", encoding="utf-8")
    if args.output_solution is None:
        args.output_solution = open(inpath+"_solution"+inext, "w", encoding="utf-8")
    
    lines = [r"%%skip", r"%load_ext skip_kernel_extension"]
	
    subprocess.call(
          ["nbsplitter", args.infile.name, "--output", args.output_task.name]
        + ["--keep", "task", "--remove", "solution"]
        + [i for line in lines for i in ["--line", line]], shell=True)

    subprocess.call(
          ["nbsplitter", args.infile.name, "--output", args.output_solution.name]
        + ["--keep", "solution", "--remove", "task"]
        + [i for line in lines for i in ["--line", line]], shell=True)

if __name__ == '__main__':
    main()

