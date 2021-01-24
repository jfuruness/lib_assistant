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

from word2number import w2n

from .command import Command, Link_Command, Number_Command

class Assistant:
    def __init__(self):
        self.commands = [Link_Command(["husky", "blackboard"],
                                      self.go_to_blackboard,
                                      name="Huskyct"),
                         Link_Command(["software", "software engineering"],
                                      self.go_to_software_engineering,
                                      name="CSE2102: Software Engineering"),
                         Link_Command(["cyber",
                                       "security",
                                       "cyber security",
                                       "cybersecurity"],
                                      self.go_to_cyber_security,
                                      name="Cybersecurity"),
                         Link_Command(["philosophy"],
                                      self.go_to_ethics,
                                      name="CSE300: Ethics"),
                         Link_Command(["history"],
                                      self.go_to_history,
                                      name="HIST1502: History"),
                         Link_Command(["education"],
                                      self.go_to_education,
                                      name=("EPSY3010: "
                                            "Educational Psychology")),
                         Link_Command(["math"],
                                      self.go_to_math,
                                      name="MATH2210Q: Linear Algebra"),
                         Command(["show numbers",
                                  "numbers"],
                                 self.show_numbers,
                                 _help="Displays numbers on browser"),
                         Command(["close"],
                                 self.close,
                                 _help="Close all browsers"),
                         Command(["off", "stop", "go to sleep"],
                                 self.end,
                                 _help="Closes all browsers and ends session"),
                         Command(["show commands"],
                                 self.help,
                                 _help="Displays all commands"),
                         Command(["Show websites", "websites"],
                                 self.show_websites,
                                 _help="Show website commands"),
                         Command(["on the left", "left"],
                                 self.focus_left,
                                 _help="Commands left browser"),
                         Command(["on the right", "right"],
                                 self.focus_right,
                                 _help="Commands right browser"),
                         Command(["in the center", "center", "middle", "in the middle"],
                                 self.focus_center,
                                 _help="Commands center browser"),
                         Command(["scroll down", "move down", "down"],
                                 self.scroll_down,
                                 _help="Scroll down"),
                         Command(["scroll up", "move up", "up"],
                                 self.scroll_up,
                                 _help="Scroll up"),
                         Command(["page down"],
                                 self.page_down,
                                 _help="Scroll down"),
                         Command(["page up"],
                                 self.page_up,
                                 _help="Scroll up"),]

        # Add number commands
        nums_to_exclude = set([1, 2, 4, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90,
                               21, 31, 41, 51, 61, 71, 81, 91,
                               22, 32, 42, 52, 62, 72, 82, 92,
                               24, 34, 44, 54, 64, 74, 84, 94])
        # Reverse it so that if user says 21, doesn't conflict with 1
        for i in reversed(list(range(99))):
            if i not in nums_to_exclude:
                self.commands.append(Number_Command(i, self.click_number))

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
                if isinstance(command, Number_Command):
                    keywords_dict[keyword] = -1
                else:
                    keywords_dict[keyword] = -10000000
                # Set the callback func for the keyword
                callbacks_dict[keyword] = command.callback_func
            keywords_dict["ethics"] = -100000000000
            keywords_dict["eleven"] = -100
            keywords_dict["fourteen"] = -10000
        # right
        removed_words = ["ray", "great", "write", "both", "but", "red", "direct",
                         "rate", "rates", "we're"]
        # scroll
        removed_words += ["gone", "swirl", "lot", "squirrel", "scrawled"
                          "screw"]
        # Up
        removed_words += ["of", "oh", "op", "ah", "out"]
        # Page
        removed_words += ["joe", "job", "hey", "they", "jump", "if", "joke",
                          "ma", "jar", "jobs", "theirs", "their", "paige",
                          "punjab", "ninja", "purjure", "courage", "pigeon",
                          "de", "jo", "they'd", "bridge", "i'll", "paid",
                          "could", "perjure", "good", "jeff", "just", "interrupt",
                          "java", "that", "they've"]
        # Eleven
        removed_words += ["obama", "love"]

        return Speech_Recognition_Wrapper(keywords_dict=keywords_dict,
                                          callback_dict=callbacks_dict,
                                          removed_words=removed_words)

    def run(self, test=False):
        if test:
            self.test()
            input("Done w test")
        self.cmd_executor.run()

##################
### Test funcs ###
##################

    def test(self):
        """Tests funcs and leaves browser open for further testing

        Better than pytest because it leaves browser open for this case
        """

        self.help()
        self.test_click_func()
        self.test_link_funcs()

    def test_click_func(self):
        logging.info("Testing click func")
        self.go_to_math("go to math")
        self.click_number("click eight")

    def test_link_funcs(self):
        for func in [self.go_to_blackboard,
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

    def focus_right(self, speech):
        self.focused_side = Side.RIGHT

    def focus_left(self, speech):
        self.focused_side = Side.LEFT

    def focus_center(self, speech):
        self.focused_side = Side.CENTER

    def show_numbers(self, speech=""):
        browser, open_new = self.get_browser_and_open_status(speech)
        browser.show_links(open_new)

    def click_number(self, speech):
        num = None
        # Remove word by word until you are just left with nums
        for i in range(len(speech.split())):
            number_str = "".join(speech.split()[i:])
            try:
                num = w2n.word_to_num(number_str)
            except ValueError:
                pass
        assert num is not None, "There was no number in text?"
        try:
            self.browsers[self.focused_side].click_number(num)
            self.browsers[self.focused_side].show_links()
        except AttributeError:
            print("You tried to click a number when the browser wasn't open")

    def close(self, speech=""):
        for side, browser in self.browsers.items():
            if browser is not None:
                browser.close()
                self.browsers[side] = None

    def end(self, speech=""):
        # Close browsers
        self.close()
        sys.exit(0)

    def help(self, speech=""):
        for command in self.standard_commands:
            print(command)
            time.sleep(2)
        self.show_websites()
        print("num command ex:")
        print(Number_Command(1, self.click_number))

    def show_websites(self, speech=""):
        for link_command in self.link_commands:
            print(link_command)
            time.sleep(2)

    def scroll_down(self, speech):
        browser, open_new = self.get_browser_and_open_status(speech)
        if open_new:
            browser.open()
        browser.scroll_down()

    def scroll_up(self, speech):
        browser, open_new = self.get_browser_and_open_status(speech)
        if open_new:
            browser.open()
        browser.scroll_up()

    def page_down(self, speech):
        browser, open_new = self.get_browser_and_open_status(speech)
        if open_new:
            browser.open()
        browser.page_down()

    def page_up(self, speech):
        browser, open_new = self.get_browser_and_open_status(speech)
        if open_new:
            browser.open()
        browser.page_up()

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

    def go_to_shit(self, speech: str):
        browser, open_new = self.get_browser_and_open_status(speech)
        if open_new:
            browser.open()
        browser.get("http://www2.math.uconn.edu/"
                    "~olshevsky/classes/2021_Spring/math2210/math2210.php")
        browser.wait_send_keys(name="txtUsername", "math2210")
        browser.wait_send_keys(name="txtPassword", "Gauss")

########################
### Helper Functions ###
### ONLY for helping ###
########################

    @property
    def standard_commands(self):
        return [x for x in self.commands if x.__class__ == Command]

    @property
    def link_commands(self):
        return [x for x in self.commands if x.__class__ == Link_Command]

    @property
    def focused_browser(self):
        assert self.focused_side is not None, "No browser is in focus"
        return self.browsers[self.focused_side]

    def get_browser_and_open_status(self, speech):
        """Gets the browser side from speech and returns browser

        If there is no browser there, creates a new browser object"""

        side = self.get_browser_side(speech)

        if self.browsers[side] is None:
            self.browsers[side] = Convenience_Browser(side=side)
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
