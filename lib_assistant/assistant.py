import logging
import time

from pocketsphinx import LiveSpeech
import selenium
from selenium.webdriver.common.keys import Keys

from .browser import Browser, Side

class Assistant:
    keywords_path = "/tmp/keywords.list"
    def __init__(self):
        # track
        # bye
        # yes
        # 
        # hello
        # hi
        # brown
        # laptop

        #! school!
        # 

        # move (up, on out)


        self.callbacks = {
            "Apple": self.google_mode_huskyct,
            "login": self.google_mode_huskyct,
            "log in": self.google_mode_huskyct,
            "go to school": self.google_mode_huskyct,
            "Orange": self.show_links,
            "Show numbers": self.show_links,
            "Show the numbers": self.show_links,
            "sure members": self.show_links,
            "sure numbers": self.show_links,
            "show of numbers": self.show_links,
            "Accept": self.accept_pop_up,
            "except": self.accept_pop_up,
            "Move up": self.scroll_up,
            "Move op": self.scroll_up,
            "Move on": self.scroll_up,
            "Move out": self.scroll_up,
            "Move down": self.scroll_down,
            "Moved down": self.scroll_down,
            "scroll up": self.scroll_up,
            "Scroll down": self.scroll_down,
            "Swipe up": self.scroll_up,
            "Swipe down": self.scroll_down,
            "Page up": self.page_up,
            "Page down": self.page_down,
            "Paige up": self.page_up,
            "Paige cop": self.page_up,
            "Go back to the top": self.page_up,
            "Go back to the bottom": self.page_up,
            "Paige down": self.page_down,
            "School": self.focus_left,
            "Right": self.focus_right,
            "tap number twelve": self.click,
            "Tap number thirteen": self.click,
            "tap number fourteen": self.click,
            "Tap number fifteen": self.click,
            "Tap number sixteen": self.click,
            "search": self.search,
        }
        self.callbacks = {k.lower(): v for k, v in self.callbacks.items()}
        with open(self.keywords_path, "w") as f:
            for keyword in self.callbacks:
                f.write(f"{keyword} /-100/")

    def run(self):
        logging.info("Running")
        Speech = LiveSpeech(kws=self.keywords_path)
        for phrase in Speech:
#        while True:
            speech = phrase.hypothesis().lower()
#            speech = input("Enter word here while Christina is sleeping: ")
            callback = self.callbacks.get(speech, False)
            if callback is not False:
                print(f"Executing: {speech}")
                callback(speech)
            elif "number" in speech:
                print(f"Executing: {speech}")
                self.click(speech)
            elif "search" in speech or "section" in speech or "said" in speech:
                print(f"Executing: {speech}")
                self.search(speech)
            else:
                print(speech)

    def google_mode_huskyct(self, *args):
        """Open up two browsers side by side for googling.

        Left browser will login to huskyct
        The right browser will be able to google with
        """

        # Init browsers        
        self.left_browser = Browser()
        self.right_browser = Browser()
        # Open left browser and align left
        self.left_browser.open(side=Side.LEFT)
        # Open right browser and align right
        self.right_browser.open(side=Side.RIGHT)

        # Right browser goes to google
        self.right_browser.get("http://www.google.com")

        # Left browser login to huskyct
        self._login_to_huskyct()

    def _login_to_huskyct(self):
        # left browser goes to huskyct
        self.left_browser.get("https://lms.uconn.edu/")
        # Wait for privacy agreement to pop up
        time.sleep(3)
        # Clicks privacy agreement
        self.left_browser.get_el(_id="agree_button").click()
        # Go away privacy agreement!!
        time.sleep(1)
        # click login button
        self.left_browser.get_el(_id="cas-login").click()

        # Wait for login to appear
        time.sleep(2)
        # Send in username
        self.left_browser.get_el(_id="username").send_keys("chg16109")
        # Send in password
        with open("/tmp/password.txt", "r") as f:
            password = f.read().strip()
        self.left_browser.get_el(_id="password").send_keys(password)
        # Click login
        self.left_browser.get_el(name="submit").click()
        self.left_browser.get("https://lms.uconn.edu/ultra/course")
        self.focused_browser = self.left_browser
        time.sleep(2)
        self.show_links()

    def show_links(self, side=None):
        # https://stackoverflow.com/a/21898701/8903959
        if side == Side.LEFT:
            browser = self.left_browser
        elif side == Side.RIGHT:
            browser = self.right_browser
        else:
            browser = self.focused_browser

        self.switch_to_iframe(browser)

        # Get all links within the page
        for i, tag in enumerate(browser.get_clickable()):
            # Add a number next to all of the links
            browser.add_number(i, tag)

    def switch_to_iframe(self, browser):
        # Switches in and out of iframe
        if browser.in_iframe:
            browser.browser.switch_to.default_content()

        # https://stackoverflow.com/a/24286392
        if "https://lms.uconn.edu/ultra/courses" in browser.url:
            # Everything from here on in operates from within an iframe
            # Wait for iframe to load
            time.sleep(2)
            # Switch to iframe, life is good
            iframe_name = "classic-learn-iframe"
            browser.browser.switch_to.frame(browser.get_el(name=iframe_name))
            browser.in_iframe = True


    def click(self, text):
        try:
            number = text.replace("numbers", "number").split("number")[-1].strip()
        except ValueError:
            return


        if len(number) == 0:
            return
        number = self.text2int(number)
        if number == 30:
            number = 13

        tag_to_click = None

        # Get all links within the page
        for i, tag in enumerate(self.focused_browser.get_clickable()):
            # Add a number next to all of the links
            if i == number:
                tag_to_click = tag
                break
            #browser.remove_number(i, tag)

#        for j, tag in enumerate(other_browser.get_clickable()):
#            other_browser.remove_number(j, tag)

        try:
            old_url = self.focused_browser.url
            tag_to_click.click()
        except selenium.common.exceptions.ElementClickInterceptedException:
            if i <=3:
                if i == 1:
                    num = "two"
                elif i == 2:
                    num = "three"
                elif i == 3:
                    num = "four"
                print("Element unclickable, trying again with next element")
                self.click(f"number {num}")

        if self.focused_browser.url != old_url:
            time.sleep(2)
            self.show_links()

    def search(self, speech):
        self.focused_browser = self.right_browser
        self.right_browser.get("https://www.google.com/")
        speech = speech.replace("search", "").replace("section", "").replace("said", "").strip()
        time.sleep(2)
        search_bar_opts = self.right_browser.get_el(tag="input", plural=True)
        for bar in search_bar_opts:
            if "earch" in bar.get_attribute("title"):
                search_bar = bar
        search_bar.send_keys(speech)
        time.sleep(.5)
        search_bar.send_keys(Keys.ENTER)

    def text2int(self, textnum, numwords={}):
        try:
            return int(textnum)
        except ValueError:
            pass
        # https://stackoverflow.com/a/493788/8903959
        if not numwords:
          units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
          ]
    
          tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
          scales = ["hundred", "thousand", "million", "billion", "trillion"]
    
          numwords["and"] = (1, 0)
          for idx, word in enumerate(units):    numwords[word] = (1, idx)
          for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
          for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)
    
        current = result = 0
        for word in textnum.split():
            if word not in numwords:
              raise Exception("Illegal word: " + word)
    
            scale, increment = numwords[word]
            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0
    
        return result + current

    def accept_pop_up(self, *args):
        for browser in [self.focused_browser]:#, self.right_browser]:
            try:
                browser.browser.switch_to.alert.accept()
                browser.browser.switch_to.default_content()
            except Exception as e:
                print(e)

    def scroll_up(self, *args, browser=None):
        if not browser:
            browser = self.focused_browser

        browser.scroll_up()

    def scroll_down(self, *args, browser=None):
        if not browser:
            browser = self.focused_browser

        browser.scroll_down()

    def page_up(self, *args, browser=None):
        if not browser:
            browser = self.focused_browser
        browser.page_up()

    def page_down(self, *args, browser=None):
        if not browser:
            browser = self.focused_browser
        browser.page_down()

    def focus_left(self, *args):
        self.focused_browser = self.left_browser

    def focus_right(self, *args):
        self.focused_browser = self.right_browser
