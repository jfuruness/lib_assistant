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
import logging
from logging import DEBUG
from sys import argv

from lib_utils import utils

from .assistant import Assistant


def main():
    """Does all the command line options available
    See top of file for in depth description"""

    parser = ArgumentParser(description="lib_assistant, see github")

    for arg in ["run", "debug", "test"]:
        parser.add_argument(f"--{arg}", default=False, action='store_true')

    args = parser.parse_args()
    if args.debug:
        utils.config_logging(DEBUG if args.debug else logging.info, "assistant")

    if args.run:
        Assistant().run(args.test)
