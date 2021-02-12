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

    def __init__(self, keyword_list, func_name, _help=None):
        self.keyword_list = [x.lower() for x in keyword_list]
        self.func_name = func_name
        if _help:
            self._help = _help
        else:
            self._help = func_name.replace("_", " ")

    def add_callback_func(self, callback_func):
        self.callback_func = callback_func

    def __str__(self):
        return (f"Desc: {self._help}\n"
                "\tOptions:\n\t\t") + "\n\t\t".join(self.keyword_list) + "\n"


class Link_Command(Command):
    def __init__(self, ways_to_call_link, func_name, name):
        # First get all the ways we can call the website
        keyword_list = []
        for way_to_call_link in ways_to_call_link:
            keyword_list.append(way_to_call_link)
            for prepend in ["open", "go to"]:
                keyword_list.append(f"{prepend} {way_to_call_link}")
        super(Link_Command, self).__init__(keyword_list=keyword_list,
                                           func_name=func_name,
                                           _help=f"Goes to {name}")


class Mode_Command(Command):
    def __init__(self, ways_to_call, func_name, name, end_func_name):
        keyword_list = []
        for way_to_call in ways_to_call:
            for prepend in ["", "enter ", "begin ", "start ", "activate "]:
                for _append in ["", " mode"]:
                    keyword_list.append(f"{prepend}{way_to_call}{_append}")
        self.end_func_name = end_func_name
        super(Mode_Command, self).__init__(keyword_list=keyword_list,
                                           func_name=func_name,
                                           _help=f"Starts {name} mode")


class Directional_Command(Command):
    def __init__(self, directions: list, func_name):
        keyword_list = []
        for direction in directions:
            for focus in ["", "focus "]:
                for prepend in ["", "on the ", "in the "]:
                    for _append in ["",
                                    " browser",
                                    " side",
                                    " window",
                                    " browser window"]:
                        keyword_list.append((f"{focus}{prepend}"
                                             f"{direction}{_append}"))
        _help = "Focus on the {directions[0]} browser"
        super(Directional_Command, self).__init__(keyword_list=keyword_list,
                                                  func_name=func_name,
                                                  _help=_help)


class Number_Command(Command):
    def __init__(self, num: int, callback_func):
        num_str = num2words(num).replace("-", " ")
        num_strs = [num_str]
        if num == 12:
            num_strs.append("twelfth")
        elif num == 18:
            num_strs.append("the dean")
        keyword_list = []
        for _num_str in num_strs:
            for prepend in ["tap ", "click ", "press ", "quick ", ""]:
                for prepend_2 in ["", "number "]:
                    keyword_list.append(f"{prepend}{prepend_2}{_num_str}")
        self.callback_func = callback_func
        super(Number_Command, self).__init__(keyword_list=keyword_list,
                                             func_name=callback_func.__name__,
                                             _help=f"Click {num_str}")
