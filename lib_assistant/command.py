#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains a command"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"

from num2words import num2words


class Command:
    def __init__(self, keyword_list, callback_func, _help=None):
        self.keyword_list = keyword_list
        self.callback_func = callback_func
        if _help:
            self._help = _help
        else:
            self._help = callback_func.__name__.replace("_", " ")

    def __str__(self):
        return " ".join(self.keyword_list) + f" {self.callback_func.__name__}"

class Link_Command(Command):
    def __init__(self, ways_to_call_link, callback_func, link_name):
        # First get all the ways we can call the website
        keywords_list = []
        for way_to_call_website in ways_to_call_website:
            keywords_list.append(way_to_call_website)
            for prepend in ["open", "go to"]:
                keywords_list.append(f"{prepend} {way_to_call_website}")
        super(Link_Command, self).__init__(keywords_list=keywords_list,
                                           callback_func=callback_func,
                                           _help=f"Goes to {link_name}")

class Number_Command(Command):
    def __init__(self, num: int, callback_func):
        num_str = num2words(num).replace("-", " ")
        keywords_list = [num_str]
        for prepend in ["tap ", "click "]:
            for prepend_2 in ["", "number "]
                keywords_list.append(f"{prepend}{prepend_2}{num_str}")
        super(Number_Command, self).__init__(keywords_list=keywords_list,
                                             callback_func=callback_func,
                                             _help=f"Click {num_str}")
