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
import os

import re
import smtplib
import time
import os
import email
import imaplib
import traceback
from urllib.parse import unquote

from lib_browser import Convenience_Browser, Side
from lib_config import Config
from lib_speech_recognition_wrapper import Speech_Recognition_Wrapper

from word2number import w2n

from .command import Command, Link_Command, Number_Command
from .commands import commands

class Assistant:

    html_file = "/tmp/assistant.html"

    def __init__(self, test=False, train=False, quiet=False):
        self.test = test
        self.commands = []
        for command in commands:
            try:
                callback = getattr(self, command.func_name)
            except AttributeError:
                def placeholder_func(speech):
                    print(f"Placeholder for {command.func_name}")
                callback = placeholder_func

            command.add_callback_func(callback)
            self.commands.append(command)

        # Add number commands
        nums_to_exclude = set([1, 2, 4, 6, 7, 8, 9, 10, 11, 13, 14, 20, 30, 40, 50, 60, 70, 80, 90,
                               21, 31, 41, 51, 61, 71, 81, 91,
                               22, 32, 42, 52, 62, 72, 82, 92,
                               24, 34, 44, 54, 64, 74, 84, 94])
        # Reverse it so that if user says 21, doesn't conflict with 1
        for i in reversed(list(range(99))):
            if i not in nums_to_exclude:
                self.commands.append(Number_Command(i, self.click_number))

        self.cmd_executor = self.init_speech_recognizer(train, quiet)

        self.browsers = {x: None for x in Side}
        # Default to the left side for opening
        self.focused_side = Side.RIGHT

    def init_speech_recognizer(self, train, quiet):
        keywords_dict = {}
        callbacks_dict = {}
        for command in self.commands:
            for keyword in command.keyword_list:
                # https://stackoverflow.com/a/41536754/8903959
                # Threshold is 10 ** whatever we set here
                if isinstance(command, Number_Command):
                    # Max is 1
                    keywords_dict[keyword] = 0
                else:
                    # Best case is -50
                    keywords_dict[keyword] = -50

                # Set the callback func for the keyword
                callbacks_dict[keyword] = command.callback_func
            keywords_dict["ethics"] = -10000000000
            keywords_dict["fourteen"] = -10000

        removed_words = []
        # math
        removed_words += ["mouth"]
        # linear
        removed_words += ["lanier", "year", "when", "your", "you're", "ear"]
        # right
        removed_words += ["ray", "great", "write", "both", "but", "red", "direct",
                         "rate", "rates", "we're", "birds", "burt"]
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

        # Third
        removed_words += ["third"]
        # back
        removed_words += ["yeah"]
        # meeting
        removed_words += ["me", "him"]
        # Event
        removed_words += ["resent"]

        tuning_phrases = []
        for command in self.commands:
            if not isinstance(command, Number_Command):
                tuning_phrases.extend(command.keyword_list)
        for i in range(99):
            tuning_phrases.extend(Number_Command(i, self.click_number).keyword_list)


        return Speech_Recognition_Wrapper(keywords_dict=keywords_dict,
                                          callback_dict=callbacks_dict,
                                          removed_words=removed_words,
                                          tuning_phrases=tuning_phrases,
                                          test=self.test,
                                          train=train,
                                          quiet=quiet)

    def run(self):
        if self.test:
            self.test_funcs()
            input("Done w test")
        self.cmd_executor.run()

##################
### Test funcs ###
##################

    def test_funcs(self):
        """Tests funcs and leaves browser open for further testing

        Better than pytest because it leaves browser open for this case
        """

        self.go_to_ice_man()
        self.go_to_zoom("")
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

    def tab_over(self, speech):
        browser, open_new = self.browser.open_a_new_tab()
        if open_new:
            browser.open()
        else:
            browser.tab_over()

    def open_tab(self, speech):
        browser, open_new = self.browser.open_a_new_tab()
        if open_new:
            browser.open()
        else:
            browser.open_new_tab()

    def focus_right(self, speech):
        self.focused_side = Side.RIGHT

    def focus_left(self, speech):
        self.focused_side = Side.LEFT

    def focus_center(self, speech):
        self.focused_side = Side.CENTER

    def maximize(self, speech):
        if self.focused_side == Side.CENTER:
            pass
        else:
            browser, open_new = self.get_browser_and_open_status(speech)
            if self.browsers[Side.CENTER]:
                self.browsers[Side.CENTER].close()
                self.browsers[Side.CENTER] = None
            if open_new:
                browser.open()
            side = browser.side
            self.browsers[side] = None
            self.browsers[Side.CENTER] = browser
            browser.side = Side.CENTER
            browser.maximize()
            self.focused_side = Side.CENTER

    def show_numbers(self, speech=""):
        browser, open_new = self.get_browser_and_open_status(speech)
        browser.show_links(open_new)

    def click_number(self, speech):
        os.system('notify-send "'+callback.__name__+'" "'+speech+'"')
        num = None
        # Remove word by word until you are just left with nums
        for i in range(len(speech.split())):
            number_str = "".join(speech.split()[i:])
            try:
                num = w2n.word_to_num(number_str)
            except ValueError:
                pass
        try:
            assert num is not None, "There was no number in text?"
        except AssertionError:
            logging.warning("no num in text, not executing")
            return
        try:
            self.browsers[self.focused_side].click_number(num)
            self.browsers[self.focused_side].show_links()
        except AttributeError:
            print("You tried to click a number when the browser wasn't open")

    def back(self, speech=""):
        browser, open_new = self.get_browser_and_open_status(speech)
        if open_new:
            browser.open()
        browser.back()

    def accept_pop_up(self, speech=""):
        browser, open_new = self.get_browser_and_open_status(speech)
        if open_new:
           browser.open()
        try:
            browser.accept_pop_up()
        except Exception as e:
            logging.warning(e)


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

    def go_to_ice_man(self, speech=""):
        browser, open_new = self.get_browser_and_open_status(speech)
        if open_new:
            browser.open()
        browser.open_ice_man()
 
    def go_to_zoom(self, speech):
        browser, open_new = self.get_browser_and_open_status(speech)
        if open_new:
            browser.open()
        self._write_zoom_links()
        browser.get("file:///" + self.html_file)
        self.show_numbers()


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

    def go_to_math_website(self, speech: str):
        browser, open_new = self.get_browser_and_open_status(speech)
        browser.open_math_website(open_new=open_new)
        browser.show_links()

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
        try:
            browser.wait_click(_id="menuPuller")
        except selenium.common.exceptions.TimeoutException:
            logging.warning("Couldn't pull out menu")
        browser.show_links()

    def _write_zoom_links(self):

        logging.info("Getting emails")

        # https://www.geeksforgeeks.org/python-fetch-your-gmail-emails-from-a-particular-user/
        _email, password = Config().webull_email_creds()
        SMTP_SERVER = "imap.gmail.com" 
        SMTP_PORT = 993

        html = ["<DOCTYPE html>",
                "<html>",
                "<head><title>Zoom links</title></head>",
                "<body>",
                "<h1>Zoom Links</h1>"]

        try:
            mail = imaplib.IMAP4_SSL(SMTP_SERVER)
            mail.login(str(_email), str(password))
            mail.select('inbox')

            data = mail.search(None, 'ALL')
            mail_ids = data[1]
            id_list = mail_ids[0].split()   
            first_email_id = int(id_list[0])
            latest_email_id = int(id_list[-1])

            max_links = 10

            for i in range(latest_email_id, first_email_id, -1):
                data = mail.fetch(str(i), '(RFC822)' )
                for response_part in data:
                    arr = response_part[0]
                    if isinstance(arr, tuple):
                        msg = email.message_from_string(str(arr[1], 'utf-8'))
                        email_subject = msg['subject']
                        email_from = msg['from']
                        msg = str(msg).replace("\n", "").replace(" ", "")
                        zoom_links = re.findall("https%3A%2F%2F=us02web.zoom.us%2Fj%2F\d+?%3Fpwd%3D.*?&", str(msg))
                        if len(zoom_links) == 0:
                            zoom_links = re.findall("https.*?/j/\d+\-", str(msg))
                            if len(zoom_links) == 0:
                                zoom_links = re.findall("https://zoom.us/j/\d+\?pwd=\w+\W", str(msg))
                        if zoom_links:
                            zoom_link = zoom_links[0].replace("=", "")[:-1]
                            html.append(f"<div><a href='{unquote(zoom_link)}'>{email_subject}</a></div><br>")
                            max_links -= 1
                if max_links <= 0:
                    break
        except Exception as e:
            logging.warning(e)

        html.append("</body></html>")
        with open(self.html_file, "w") as f:
            for html_line in html:
                f.write(html_line + "\n")
