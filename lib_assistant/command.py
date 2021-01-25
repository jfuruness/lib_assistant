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

    directions = ["",
                  "left ",
                  "on the left ",
                  "right ",
                  "on the right ",
                  "center ",
                  "in the center ",]

    def __init__(self, keyword_list, callback_func, _help=None):
        self.keyword_list = [x.lower() for x in keyword_list]
        self.callback_func = callback_func
        if _help:
            self._help = _help
        else:
            self._help = callback_func.__name__.replace("_", " ")

    def __str__(self):
        return (f"Desc: {self._help}\n"
                "\tOptions:\n\t\t") + "\n\t\t".join(self.keyword_list) + "\n"

class Link_Command(Command):
    def __init__(self, ways_to_call_link, callback_func, name):
        # First get all the ways we can call the website
        keyword_list = []
        for way_to_call_link in ways_to_call_link:
            for direction in self.directions:
                keyword_list.append(direction + way_to_call_link)
                for prepend in ["open", "go to"]:
                    keyword_list.append(f"{direction}{prepend} {way_to_call_link}")
        super(Link_Command, self).__init__(keyword_list=keyword_list,
                                           callback_func=callback_func,
                                           _help=f"Goes to {name}")

class Number_Command(Command):
    def __init__(self, num: int, callback_func):
        num_str = num2words(num).replace("-", " ")
        keyword_list = []
        for direction in self.directions:
            keyword_list.append(direction + num_str)
            for prepend in ["tap ", "click "]:
                for prepend_2 in ["", "number "]:
                    keyword_list.append(f"{direction}{prepend}{prepend_2}{num_str}")
        super(Number_Command, self).__init__(keyword_list=keyword_list,
                                             callback_func=callback_func,
                                             _help=f"Click {num_str}")
