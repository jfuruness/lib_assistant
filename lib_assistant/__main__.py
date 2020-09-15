#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module runs all command line arguments."""

__authors__ = ["Justin Furuness"]
__credits__ = ["Justin Furuness"]
__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"

from argparse import ArgumentParser, Action
from logging import DEBUG
from sys import argv

from .assistant import Assistant
from .utils import config_logging


def main():
    """Does all the command line options available
    See top of file for in depth description"""

    parser = ArgumentParser(description="lib_assistant, see github")
    parser.add_argument("--assistant", dest="assistant", default=False, action='store_true')
    parser.add_argument("--debug", dest="debug", default=False, action='store_true')

    args = parser.parse_args()
    if args.debug:
        config_logging(DEBUG)

    if args.assistant:
        Assistant().run()


if __name__ == "__main__":
    main()
