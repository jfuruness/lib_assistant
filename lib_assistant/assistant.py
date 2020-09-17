import logging
import time

from pocketsphinx import LiveSpeech
from pynput.keyboard import Key, Controller
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
            "go to Europe": self.google_mode_mimir,
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
            "Back to the top": self.page_up,
            "Go back to the bottom": self.page_down,
            "Back to the bottom": self.page_down,
            "Paige down": self.page_down,
            "School": self.focus_left,
            "Right": self.focus_right,
            "tap number twelve": self.click,
            "Tap number thirteen": self.click,
            "tap number fourteen": self.click,
            "Tap number fifteen": self.click,
            "Tap number sixteen": self.click,
            "search": self.search,
            "Download file": self.download_mimir_pdf,
            "Downvote a file": self.download_mimir_pdf,
            "Downvote file": self.download_mimir_pdf,
            "Download a file": self.download_mimir_pdf,
            "move over": self.switch_tab,
            "Quit": self.quit,
            "shut down": self.quit,
            "Shut us down": self.quit,
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

    def google_mode_mimir(self, *args):
        """Opens up mimir with google"""

        # Open google
        self._open_google()
        # Left browser login to mimir
        self._login_to_mimir()


    def google_mode_huskyct(self, *args):
        """Open up two browsers side by side for googling.

        Left browser will login to huskyct
        The right browser will be able to google with
        """

        # Open google
        self._open_google()
        # Left browser login to huskyct
        self._login_to_huskyct()

    def _open_google(self):
        self.right_browser = Browser()
        # Open right browser and align right
        self.right_browser.open(side=Side.RIGHT)
        # Right browser goes to google
        self.right_browser.get("http://www.google.com")

    def _login_to_huskyct(self):
        self.left_browser = Browser()
        # Open left browser and align left
        self.left_browser.open(side=Side.LEFT)
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
        time.sleep(3)
        self.show_links()

    def _login_to_mimir(self):
        self.left_browser = Browser()
        # Open left browser and align left
        self.left_browser.open(side=Side.LEFT)
        # left browser goes to huskyct
        self.left_browser.get("https://class.mimir.io/login")
        # Load site
        time.sleep(1)
        # Send in username
        email = "christina.gorbenko@uconn.edu"
        self.left_browser.get_el(_id="LoginForm--emailInput").send_keys(email)
        # Send in password
        with open("/tmp/password.txt", "r") as f:
            password = f.read().strip()
        pword_id = "LoginForm--passwordInput"
        self.left_browser.get_el(_id=pword_id).send_keys(password)
        # Click login
        submit_id = "LoginForm--submitButton"
        time.sleep(1)
        self.left_browser.get_el(_id=submit_id).click()
        time.sleep(3)
        url = ("https://class.mimir.io/courses/"
               "01268b2b-9903-442e-8310-9bc462c41929")
        self.left_browser.get(url)
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

        iframe_links = {"https://lms.uconn.edu/ultra/courses":
                            "classic-learn-iframe",
                        "https://class.mimir.io/projects/":
                            "main.pdf"}

        # https://stackoverflow.com/a/24286392
        for iframe_link, iframe_name in iframe_links.items():
            if iframe_link in browser.url:
                # Everything from here on in operates from within an iframe
                # Wait for iframe to load
                time.sleep(2)
                # Switch to iframe, life is good
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

    def download_mimir_pdf(self, *args):
        self.focused_browser.right_click_tag(tag="embed")
        time.sleep(.5)
        embed = self.focused_browser.get_el(tag="embed")
        action = selenium.webdriver.ActionChains(self.focused_browser.browser)
        keyboard = Controller()
        for key_type in ["down", "enter", "enter"]:
            print(f"Sending key: {key_type}")
            keyboard.press(getattr(Key, key_type))
            keyboard.release(getattr(Key, key_type))
            time.sleep(1)

        # https://stackoverflow.com/a/43921765
#        input("WORKS")
        time.sleep(1)
        # Open downloads page
        with keyboard.pressed(Key.ctrl):
            print(f"Sending key: Control + j")
            keyboard.press("j")
            keyboard.release("j")
            time.sleep(.2)

        time.sleep(1)
        for _ in range(2):
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
            time.sleep(.2)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(.25)
        self.focused_browser.browser.switch_to.active_element
        self.focused_browser.pdf = True
        #self.focused_browser.get_el(_id="file-link").click()

    def switch_tab(self, *args):
        keyboard = Controller()
        with keyboard.pressed(Key.ctrl):
            for key_type in ["tab"]:
                print(f"Sending key: {key_type}")
                keyboard.press(getattr(Key, key_type))
                keyboard.release(getattr(Key, key_type))
                time.sleep(.2)
        self.focused_browser.browser.switch_to.active_element

    def quit(self, *args):
        self.left_browser.browser.quit()
        self.right_browser.browser.quit()
