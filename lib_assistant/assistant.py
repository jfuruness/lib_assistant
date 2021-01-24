#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This package contains a personal voice assistant

Functionality:
    1. Searching
    2. blackboard
    3. click numbers
    4. accepting pop ups
    5. scroll up
    6. scroll down
    7. switch tabs
"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"

import logging
import time
import sys

from lib_browser import Convenience_Browser, Side
from lib_speech_recognition_wrapper import Speech_Recognition_Wrapper

from .command import Command

def website_permutations(ways_to_call_website: list) -> list:
    """Gets ways to say how to go to a website"""

    commands = []
    for way_to_call_website in ways_to_call_website:
        commands.append(way_to_call_website)
        for prepend in ["go to", "open"]:
            commands.append(prepend + " " + way_to_call_website)
    return commands

class Assistant:
    def __init__(self):
        self.commands = [Command(website_permutations(["husky",
                                                     "blackboard"]),
                                 self.go_to_blackboard,
                                 _help="Goes to Huskyct"),
                         Command(website_permutations(["software",
                                                       "software engineering"]),
                                 self.go_to_software_engineering,
                                 _help="Goes to CSE2102: Software Engineering"),
                         Command(website_permutations(["cyber",
                                                       "security",
                                                       "cyber security",
                                                       "cybersecurity"]),
                                 self.go_to_cyber_security,
                                 _help="Goes to CSE3140: Cybersecurity"),
                         Command(website_permutations(["ethics"]),
                                 self.go_to_ethics,
                                 _help="Goes to CSE300: Ethics"),
                         Command(website_permutations(["history"]),
                                 self.go_to_history,
                                 _help="Goes to HIST1502: History"),
                         Command(website_permutations(["education"]),
                                 self.go_to_education,
                                 _help="Goes to EPSY3010: Educational Psychology"),
                          Command(website_permutations(["math"]),
                                 self.go_to_math,
                                 _help="Goes to MATH2210Q: Linear Algebra"),
                         Command(["show numbers",
                                  "show links",
                                  "numbers",
                                  "links"],
                                 self.show_numbers,
                                 _help="Displays numbers on browser"),
                         Command(["close"],
                                 self.close,
                                 _help="Close all browsers"),
                         Command(["end", "off"],
                                 self.end,
                                 _help="Closes all browsers and ends session")]

        self.cmd_executor = self.init_speech_recognizer()

        self.browsers = {x: None for x in Side}
        # Default to the left side for opening
        self.focused_side = Side.LEFT

    def init_speech_recognizer(self):
        keywords_dict = {}
        callbacks_dict = {}
        for command in self.commands:
            for keyword in command.keyword_list:
                # Threshold is 10 ** whatever we set here
                keywords_dict[keyword] = -10
                # Set the callback func for the keyword
                callbacks_dict[keyword] = command.callback_func

        return Speech_Recognition_Wrapper(keywords_dict=keywords_dict,
                                          callback_dict=callbacks_dict)

    def run(self, test=False):
        if test:
            self.test()
            input("Done w test")
        self.cmd_executor.run()

    def test(self):
        """Tests funcs and leaves browser open for further testing

        Better than pytest because it leaves browser open for this case
        """

        for func in [self.go_to_blackboard,
                     self.go_to_math,
                     self.go_to_software_engineering,
                     self.go_to_ethics,
                     self.go_to_cyber_security,
                     self.go_to_education,
                     self.go_to_history,
                     self.go_to_math,
                     self.close]:
            logging.info(f"Running test func {func.__name__}")
            func(func.__name__.replace("_", " "))
            time.sleep(1)

################
### Commands ###
################

    def show_numbers(self, speech):
        browser, open_new = self.get_browser_and_open_status(speech)
        browser.show_links()

    def close(self, speech):
        for side, browser in self.browsers:
            if browser is not None:
                browser.close()

    def end(self, speech):
        # Close browsers
        self.close()
        sys.exit(0)

    def go_to_blackboard(self, speech: str):
        browser, open_new = self.get_browser_and_open_status(speech)
        browser.open_blackboard(open_new=open_new)

########################
### Blackboard links ###
########################

    def go_to_software_engineering(self, speech: str):
        self.open_blackboard_course(speech, course_id="_87669_1")

    def go_to_ethics(self, speech: str):
        self.open_blackboard_course(speech, course_id="_93434_1")

    def go_to_cyber_security(self, speech: str):
        self.open_blackboard_course(speech, course_id="_92554_1")

    def go_to_education(self, speech: str):
        self.open_blackboard_course(speech, course_id="_94421_1")

    def go_to_history(self, speech: str):
        self.open_blackboard_course(speech, course_id="_89027_1")

    def go_to_math(self, speech: str):
        self.open_blackboard_course(speech, course_id="_89692_1")

########################
### Helper Functions ###
### ONLY for helping ###
########################

    @property
    def focused_browser(self):
        assert self.focused_side is not None, "No browser is in focus"
        return self.browsers[self.focused_side]

    def get_browser_and_open_status(self, speech):
        """Gets the browser side from speech and returns browser

        If there is no browser there, creates a new browser object"""

        side = self.get_browser_side(speech)

        if self.browsers[side] is None:
            self.browsers[side] = Convenience_Browser()
            open_new = True
        else:
            open_new = False

        return self.browsers[side], open_new

    def get_browser_side(self, speech):
        """Gets the side to open the browser on"""

        words = speech.split()

        if "center" in words or "middle" in words:
            return Side.CENTER
        elif "left" in words:
            return Side.LEFT
        elif "right" in words:
            return Side.RIGHT
        else:
            return self.focused_side

############################
### Command Helper Funcs ###
############################

    def open_blackboard_course(self, speech, course_id=None):
        browser, open_new = self.get_browser_and_open_status(speech)
        if not browser.blackboard_logged_in or open_new:
            browser.open_blackboard(open_new)
        base_url = "https://lms.uconn.edu/ultra/courses/"
        browser.get(base_url + f"{course_id}/cl/outline")
        browser.switch_to_iframe()
        browser.wait_click(_id="menuPuller")
        browser.show_links()
