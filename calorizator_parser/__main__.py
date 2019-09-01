""" Calorizator parser application. """

import argparse

from calorizator_parser.parser import main as parser_main


def run() -> None:
    """ CLI for the app. """
    parser = argparse.ArgumentParser(prog="calorizator_parser", description="Parser for calorizator site")
    parser.add_argument("--output", type=str, help="name of the output file", required=True)

    args = parser.parse_args()

    parser_main(args)


if __name__ == "__main__":
    run()
