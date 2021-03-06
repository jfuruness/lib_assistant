#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This package contains all the commands for the personal voice assistant"""

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"

from .command import Command, Link_Command, Number_Command, Directional_Command
from .command import Mode_Command

commands = [
Link_Command(["ice", "ice man"],
             func_name="go_to_ice_man",
             name="Ice Man/Wim Hof"),
Link_Command(["meet", "event", "events", "meeting", "meetings",
              "event links", "meeting links"],
             func_name="go_to_zoom",
             name="Zoom links"),
Link_Command(["husky", "cause the", "cause he", "plus he",
              "blackboard", "black", "classes", "school",
              "black board", "blood poured"],
             func_name="go_to_blackboard",
             name="Huskyct"),
Link_Command(["software", "software engineering",
              "software class", "software engineering class"],
             func_name="go_to_software_engineering",
             name="CSE2102: Software Engineering"),
Link_Command(["cyber",
              "security",
              "cyber security",
              "cyber class",
              "security class",
              "cyber security class"],
             func_name="go_to_cyber_security",
             name="Cybersecurity"),
Link_Command(["philosophy",
              "ethics",
              "philosophy class",
              "ethics class"],
             func_name="go_to_ethics",
             name="CSE300: Ethics"),
Link_Command(["history", "history class", "his story", "his theory",
              "a mystery"],
             func_name="go_to_history",
             name="HIST1502: History"),
Link_Command(["education", "education class",
              "teaching", "teaching class"],
             func_name="go_to_education",
             name=("EPSY3010: "
                   "Educational Psychology")),
Link_Command(["math", "math class"],
             func_name="go_to_math",
             name="MATH2210Q: Linear Algebra"),
Link_Command(["linear", "linear algebra", "algebra",
              "linear class", "linear algebra class",
              "algebra class"],
             func_name="go_to_math_website",
             name="Math website"),
Command(["show numbers",
         "numbers",
         "show links",
         "links"],
        func_name="show_numbers",
        _help="Displays numbers on browser"),
Command(["close"],
        func_name="close",
        _help="Close all browsers"),
Command(["turn off", "turnoff", "stop", "go to sleep", "die", "tear off",
         "turnout", "turned off"],
        func_name="end",
        _help="Closes all browsers and ends session"),
Command(["show commands", "show help", "show hope", "help", "commands",
         "list commands", "list help", "display commands", "display help"],
        func_name="help",
        _help="Displays all commands"),
Command(["show websites", "websites", "display websites"],
        func_name="show_websites",
        _help="Show website commands"),
Directional_Command(["left", "laughed", "laugh"], func_name="focus_left"),
Directional_Command(["right", "bright"], func_name="focus_right"),
Directional_Command(["center", "middle", "censor"], func_name="focus_center"),
Command(["scroll down", "move down", "down", "world around",
         "swirled around", "scrawled on", "swirled once",
         "scrawled are", "damn", "dow", "move beyond",
         "scroll town", "scroll brown", "scroll noun"],
        func_name="scroll_down",
        _help="Scroll down"),
Command(["scroll up", "move up", "up", "go up", "scroll all"],
        func_name="scroll_up",
        _help="Scroll up"),
Command(["lower", "page down", "go lower", "page town", "page noun",
         "page brown", "lauer", "lore", "laurie", "p g down", "low were",
         "glow were", "lol were", "pitch down"],
        func_name="page_down",
        _help="Scroll down"),
Command(["upper", "higher", "page up", "high", "hire"],
        func_name="page_up",
        _help="Scroll up"),
Command(["go back", "reverse", "back"],
        func_name="back",
        _help="Go back a page"),
Command(["accept", "except", "okay", "accept pop", "accept pop up",
         "accept pop up window"],
        func_name="accept_pop_up",
        _help="Accepts pop up window"),
Command(["maximize", "maximus", "max", "enlarge"],
        func_name="maximize"),
Command(["reset", "start over", "listen", "star over", "recess"],
        func_name="reset"),

###########################
### Unfinished commands ###
###########################

Mode_Command(["safe", "said"],
             func_name="start_safe_mode",
             name="safe",
             end_func_name="end_safe_mode"),
Mode_Command(["google", "hey google", "search", "sarge"],
             func_name="start_google_mode",
             name="google",
             end_func_name="end_google_mode"),
Command(["retrieve", "click latest", "latest", "show files", "go to latest",
         "go to wait it's"],
        func_name="go_to_downloads",
        _help="Download huskyct pop ups as html"),
Command(["shift tab", "move over", "move tab", "move tabs",
         "tap over", "move or", "moveable for", "move pulver",
         "move full ver", "moves over", "moveable", "move will for"],
         func_name="tab_over",
         _help="Moves tabs"),
Command(["new tab", "open new tab", "open a new tab",
         "pop open new tab", "pop open a new tab",
         "open tab", "you dab", "new jab", "new tad",
         "new tout", "new to add", "new town", "new to",
         "open and new to"],
         func_name="new_tab",
         _help="Opens a new tab"),
Command(["show dog", "show our future dog"],
         func_name="show_dog",
         _help="Shows dogs"),
Command(["unfinished", "list unfinished", "show unfinished",
         "display unfinished", "show incomplete", "incomplete",
         "display incomplete", "i'm finished", "show on finished",
         "incomplete"],
         func_name="show_unfinished_functions"),]
