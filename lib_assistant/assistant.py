import logging
import time

from pocketsphinx import LiveSpeech

from .browser import Browser, Side

class Assistant:
    def __init__(self):
        self.callbacks = {
            "Apple": self.google_mode_huskyct,
            "login": self.google_mode_huskyct,
            "log in": self.google_mode_huskyct,
            "Orange": self.show_links,
            "Show numbers": self.show_links
        }
        self.callbacks = {k.lower(): v for k, v in self.callbacks.items()}

    def run(self):
        logging.info("Running")
        #for phrase in LiveSpeech():
        while True:
#            speech = phrase.hypothesis()
            speech = input("Enter word here while Christina is sleeping: ")
            callback = self.callbacks.get(speech, False)
            if callback is not False:
                callback()
            elif "tap number" in speech:
                self.click(speech)
            else:
                print(speech)

    def google_mode_huskyct(self):
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

    def show_links_left(self):
        self.show_links(side=Side.LEFT)

    def show_links_right(self):
        self.show_links(side=Side.RIGHT)

    def show_links(self, side=None):
        # https://stackoverflow.com/a/21898701/8903959
        if side == Side.LEFT:
            browser = self.left_browser
        elif side == Side.RIGHT:
            browser = self.right_browser
        else:
            self.show_links(side=Side.LEFT)
            self.show_links(side=Side.RIGHT)
            # Don't run the code below
            return

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

        # Get all links within the page
        for i, tag in enumerate(browser.get_el(tag="a", plural=True)):
            # Add a number next to all of the links
            browser.add_number(i, tag)

    def click(self, text):
        number, side = text.replace("tap number", "").strip().split("on the")
        if "left" in side.lower():
            browser = self.left_browser
        else:
            browser = self.right_browser

        number = self.text2int(number)

        tag_to_click = None

        # Get all links within the page
        for i, tag in enumerate(browser.get_el(tag="a", plural=True)):
            # Add a number next to all of the links
            if i == number:
                tag_to_click = tag
            browser.remove_number(i, tag)

        tag_to_click.click()


    def text2int(self, textnum, numwords={}):
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
