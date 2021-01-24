#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains a command"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"


class Command:
    def __init__(self, keyword_list, callback_func, _help=None):
        self.keyword_list = keyword_list
        self.keyword_set = set(keyword_list)
        self.callback_func = callback_func
        if _help:
            self._help = _help
        else:
            self._help = callback_func.__name__.replace("_", " ")

    def __str__(self):
        return " ".join(self.keyword_list) + f" {self.callback_func.__name__}"
