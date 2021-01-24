from datetime import datetime
import sys
import time

from pocketsphinx import LiveSpeech
from pynput.keyboard import Key, Controller
import selenium
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .browser import Browser, Side

class Command:
    def __init__(self, cmd, related_words, wrong_words, func):
        self.cmd = cmd
        self.related_words = related_words
        self.wrong_words = wrong_words
        self.func = func


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
            "go to thirty five hundred": self.thirty_five_hundred,
            "go to the quizzes": self.thirty_five_hundred,
            "go to Europe": self.google_mode_mimir,
            "Orange": self.show_links,
            "Show numbers": self.show_links,
            "Show the numbers": self.show_links,
            "sure members": self.show_links,
            "sure numbers": self.show_links,
            "show of numbers": self.show_links,
            "joe numbers": self.show_links,
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
            "Page about": self.page_up,
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
            "Downloaded file": self.download_mimir_pdf,
            "move over": self.switch_tab,
            "switch tab": self.switch_tab,
            "switch have": self.switch_tab,
            "switched have": self.switch_tab,
            "switch to tell one": self.switch_tab,
            "switch to tap want": self.switch_tab,
            "switch to tab one": self.switch_tab,
            "switch to tab two": self.switch_tab,
            "switch to tab to": self.switch_tab,
            "switch to tab three": self.switch_tab,
            "switch to tab four": self.switch_tab,
            "switch to tab five": self.switch_tab,
            "switch to tab six": self.switch_tab,
            "switch to tab seven": self.switch_tab,
            "switch to tab eight": self.switch_tab,
            "switch to tab nine": self.switch_tab,
            "Quit": self.quit,
            "shut down": self.quit,
            "Shut us down": self.quit,
            "Turn off": self.turn_off,
            "start a test": self.start_test,
            "start the test": self.start_test,
            "go to the car": self.start_test,
            "Go to their car": self.start_test,
            "Go to the store": self.start_test,
            "European homework": self.mimir_homework,
            "European work": self.mimir_homework,
            "European workshop": self.mimir_workshop,
            "New tab": self.new_tab,
            "Open a new tab": self.new_tab,
            "watch the lecture": self.discord_youtube,
            "pause": self.send_k,
            "play": self.send_k,
            "Start watching": self.send_k,
            "Stop watching": self.send_k,
            "started watching": self.send_k,
            "Stopped watching": self.send_k,
            "refocus": self.refocus,
        }
        self.callbacks = {k.lower(): v for k, v in self.callbacks.items()}
        with open(self.keywords_path, "w") as f:
            for keyword in self.callbacks:
                f.write(f"{keyword} /-100/")
        self.right_browser = None
        self.left_browser = None

    def run(self):
        print("Running")
        if "--test" in sys.argv:
            test1 = ["go to school",
                           "show numbers",
                           "show numbers",
                           "tap number thirteen",
                           "tap number one",
                           "scroll down",
                           "scroll down",
                           "tap number fifteen",
                           "tap number seven",
                           "tap number four",
                           "tap number five",
                           "scroll down",
                           "scroll down",
                           "tap number eleven",
                           "scroll down",
                           "scroll down"]
            test2 = ["search hello world",
                           "show numbers",
                           "page down", "page down", "page down", "page down", "page down", "tap number thirty six"]
            test3 = ["go to school", "scroll down"]
            test4 = ["european homework one", "scroll down", "scroll down", "scroll down", "switch tab"]
            test5 = ["search amazon vitamins", "scroll down", "go to thirty five hundred", "shut down", "go to school"]
            test6 = ["watch the lecture"]
            all_tests = test1 + test2 + test3 + test4 + test5 + test6 + ["quit"]
            for speech in all_tests:
                self.deal_with_speech(speech.lower())
            input("!")
            while True:
                self.deal_with_speech(input("ENTER SPEECH: ").lower())
        elif "--quiet" in sys.argv:
            while True:
                self.deal_with_speech(input("ENTER SPEECH: ").lower())
        else:
            Speech = LiveSpeech(kws=self.keywords_path)
            for phrase in Speech:
                self.deal_with_speech(phrase.hypothesis().lower())

    def refocus(self):
        self.focused_browser.refocus()

    def deal_with_speech(self, speech):
        callback = self.callbacks.get(speech, False)
        if callback is not False:
            self.execute(callback, speech)
        elif "number" in speech:
            self.execute(self.click, speech)
        elif "search" in speech or "section" in speech or "said" in speech:
            self.execute(self.search, speech)
        elif "european homework" in speech or "european work " in speech:
            self.execute(self.mimir_homework, speech)
        elif "european workshop" in speech:
            self.execute(self.mimir_workshop,speech)
        else:
            self.execute(None, speech)

    def execute(self, func, speech):
        with open("/tmp/transcript.txt", "w+") as f:
            if func is None:
                print(speech)
                f.write(speech)
            else:
                print(f"Executing: {speech}")
                f.write(f"Executing: {speech}")
        if func is not None:
            try:
                func(speech)
            except Exception as e:
                print(e)
            with open("/tmp/transcript.txt", "w+") as f:
                print(f"Done executing {speech}")
                f.write(f"Done executing {speech}")
            

    def start_test(self, *args):
        self._open_google()

    def new_tab(self, *args):
        self.focused_browser.open_new_tab()

    def google_mode_mimir(self, *args):
        """Opens up mimir with google"""

        # Open google
        # self._open_google()
        # Left browser login to mimir
        self._login_to_mimir()

    def get_num(self, speech):
        if "one" in speech or "while" in speech or "want" in speech or '1' in speech:
            return 1
        elif "to" in speech or "two" in speech or "too" in speech:
            return 2
        elif "three" in speech:
            return 3
        elif "for" in speech or "floor" in speech or "four" in speech:
            return 4
        elif "five" in speech:
            return 5
        elif "six" in speech:
            return 6
        elif "seven" in speech:
            return 7
        elif "eight" in speech:
            return 8
        elif "nine" in speech:
            return 9
        elif "ten" in speech:
            return 10
        else:
            print("Contact Justin for adjustment")

    def mimir_homework(self, speech, *args):
        self._login_to_mimir(show_links=False)
        desired_text = f"PS {self.get_num(speech)}"
        self.focused_browser.wait_click(xpath=f"//*[contains(text(), '{desired_text}')]")
        self.download_mimir_pdf()

    def mimir_workshop(self, speech, *args):
        self._login_to_mimir(show_links=False)
        desired_text = f"Lab {self.get_num(speech)}"
        self.focused_browser.wait_click(xpath=f"//*[contains(text(), '{desired_text}')]")
        self.download_mimir_pdf()

    def thirty_five_hundred(self, speech, *args):
        self.google_mode_huskyct(show_links=False)
        self.left_browser.get("https://lms.uconn.edu/ultra/courses/_80636_1/cl/outline")
        self.left_browser.switch_to_iframe()
        self.left_browser.wait_click(_id="menuPuller")
        for _ in range(2):
            self.scroll_down()
        self.show_links()

    def google_mode_huskyct(self, *args, show_links=True):
        """Open up two browsers side by side for googling.

        Left browser will login to huskyct
        The right browser will be able to google with
        """

        # Open google
        # self._open_google()
        # Left browser login to huskyct
        self._login_to_huskyct(show_links)

    def _open_google(self):
        self.right_browser = Browser()
        # Open right browser and align right
        self.right_browser.open(side=Side.RIGHT)
        # Right browser goes to google
        self.right_browser.get("http://www.google.com")
        self.focused_browser = self.right_browser

    def _login_to_huskyct(self, show_links):
        if self.left_browser is None:
            self.left_browser = Browser()
            # Open left browser and align left
            self.left_browser.open(side=Side.LEFT)
        else:
            self.focus_left()
        # left browser goes to huskyct
        self.left_browser.get("https://lms.uconn.edu/")
        try:
            if "https://lms.uconn.edu/ultra/institution-page" in self.left_browser.url:
                print("NO")
                raise Exception("Already logged in")
            # Wait for privacy agreement to pop up and click
            self.left_browser.wait_click(_id="agree_button")
            # click login button
            self.left_browser.wait_click(_id="cas-login")
            # Send in username
            self.left_browser.wait_send_keys(_id="username",
                                             keys="chg16109")
            # Send in password
            with open("/tmp/password.txt", "r") as f:
                password = f.read().strip()
            self.left_browser.wait_send_keys(_id="password",
                                             keys=password)
            # Click login
            self.left_browser.get_el(name="submit").click()
        except Exception as e:
            print(e)
            print("Already logged in?")
        self.focused_browser = self.left_browser
        if show_links:
            self.left_browser.get("https://lms.uconn.edu/ultra/course")
            self.focused_browser = self.left_browser
            self.focused_browser.switch_to_iframe()
            self.focused_browser.wait('//*[@id="course-columns-current"]/div', By.XPATH)
            self.show_links()

    def _login_to_mimir(self, show_links=True):
        if self.left_browser is None:
            self.left_browser = Browser()
            # Open left browser and align left
            self.left_browser.open(side=Side.LEFT)
        else:
            self.focus_left()
        try:
            # left browser goes to huskyct
            self.left_browser.get("https://class.mimir.io/login")
            # Send in username
            email = "christina.gorbenko@uconn.edu"
            self.left_browser.wait_send_keys(_id="LoginForm--emailInput",
                                             keys=email)
            # Send in password
            with open("/tmp/password.txt", "r") as f:
                password = f.read().strip()
            pword_id = "LoginForm--passwordInput"
            self.left_browser.get_el(_id=pword_id).send_keys(password)
            # Click login
            submit_id = "LoginForm--submitButton"
            self.left_browser.get_el(_id=submit_id).click()
            time.sleep(.2)
        except Exception as e:
            print("Already logged in?")
        url = ("https://class.mimir.io/courses/"
               "01268b2b-9903-442e-8310-9bc462c41929")
        self.left_browser.wait("Dashboard--courseworkCard-0", By.ID)
        self.focused_browser = self.left_browser
        if show_links:
            self.left_browser.get(url)
            self.left_browser.wait("Coursework--collapseLive", By.ID)
            self.show_links()

    def discord_youtube(self, *args):
        if self.left_browser is None:
            self.left_browser = Browser()
            # Open left browser and align left
            self.left_browser.open(side=Side.LEFT)
        else:
            self.focus_left()
        # left browser goes to huskyct
        self.left_browser.get("https://discord.com/login")
        email = self.left_browser.get_el(name="email")
        while email is None:
            email = self.left_browser.get_el(name="email")
            time.sleep(.1)
        email.send_keys("christina.gorbenko@uconn.edu")
        try:
            with open("/tmp/password.txt", "r") as f:
                password = f.read()
        except FileNotFoundError:
            assert False, "Password!"
        self.left_browser.get_el(name="password").send_keys(password)
        xpath = "//button[@type='submit']"
        self.left_browser.wait_click(xpath=xpath)
        self.left_browser.wait("private-channels", By.ID)
        lecture_url = ("https://discord.com/channels/720663056962813972/"
                        "746373437567664239")
        self.left_browser.get(lecture_url)

        last_yt_link = None
        while last_yt_link is None:
            try:
                elems = self.left_browser.get_el(xpath="//a[@href]", plural=True)
                for elem in elems:
                    href = elem.get_attribute("href")
                    if "youtube" in href:
                        last_yt_link = href
            except selenium.common.exceptions.StaleElementReferenceException:
                continue

        self.focused_browser = self.left_browser
        self.focused_browser.open_new_tab(url=last_yt_link)

    def send_k(self, *args):
        time.sleep(2)
        self.focused_browser.get_el(tag="body").send_keys("k")

    def show_links(self, side=None):
        # https://stackoverflow.com/a/21898701/8903959
        self.focused_browser.switch_to_iframe()

        # https://stackoverflow.com/a/24595952
        removal_javascript_str = ("""var ele = document.getElementsByName("furuness");"""
                                  """for(var i=ele.length-1;i>=0;i--)"""
                                  """{ele[i].parentNode.removeChild(ele[i]);}""")
        self.focused_browser.browser.execute_script(removal_javascript_str)


        javascript_strs = []
        elems = []
        # Get all links within the page
        for i, tag in enumerate(self.focused_browser.get_clickable()):
            # Add a number next to all of the links
            javascript_str, elem = self.focused_browser.add_number(i, tag)
            javascript_strs.append(javascript_str)
            elems.append(elem)
        self.focused_browser.browser.execute_script(" ".join(javascript_strs), *elems)

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

        old_clickables = self.focused_browser.get_clickable()

        # Get all links within the page
#        for i, tag in enumerate(old_clickables):
#            try:
#                print(tag.text)
#                print(tag.get_attribute("innerHTML"))
#            except Exception as e:
#                print(e)
#            # Add a number next to all of the links
#            if i == number:
#                tag_to_click = tag
#                break
#        tag_to_click.click()
#        old_clickables = self.focused_browser.get_clickable()
        num_str = self.focused_browser._format_number(number)
        xpath = f"//*[contains(., '{num_str}')]"
        """function getElementByXpath(path) {
  return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

getElementByXpath("//*[contains(., '__13__')]").childNodes;"""
        # childNodes - get the one directly after the one whos textContent is the number.
#        xpath='//*[@id="course-list-course-_80636_1"]/div[2]/preceding::text()'
        #parent = self.focused_browser.get_el(xpath=xpath, plural=True)[-1]
        javascript_str = ("""var mylist = document.evaluate"""
                          f"""("//*[contains(., '{num_str}')]", document,"""
                          """null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);"""
                          """var mynode = mylist.snapshotItem(mylist.snapshotLength - 1);"""
                          """for (index = 0; index < mynode.childNodes.length; index++) {"""
                          f"""if(mynode.childNodes[index].nodeValue == "{num_str}")"""
                          """{mynode.childNodes[index + 1].click();"""
                          """break;"""
                          """}}""")
        javascript_str = ("""var mylist = document.evaluate"""
                          f"""("//*[contains(., '{num_str}')]", document,"""
                          """null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);"""
                          """var mynode = mylist.snapshotItem(mylist.snapshotLength - 1);"""
                          """for (index = 0; index < mynode.childNodes.length; index++) {"""
                          f"""if(mynode.childNodes[index].nodeValue == "{num_str}")"""
                          """{mynode.childNodes[index + 1].click();"""
                          """break;"""
                          """}}""")
        javascript_str = (f"""document.evaluate("//*[@id='furuness_{num_str}']","""
                          """ document, null, XPathResult.FIRST_ORDERED_NODE_TYPE,"""
                          """ null).singleNodeValue.nextSibling.click();""")
        try:
            self.focused_browser.browser.execute_script(javascript_str)
        except selenium.common.exceptions.JavascriptException as e:
            # This is a button
            if "nextSibling" in str(e):
                javascript_str = (f"""document.evaluate("//*[@id='furuness_{num_str}']","""
                          """ document, null, XPathResult.FIRST_ORDERED_NODE_TYPE,"""
                          """ null).singleNodeValue.nextSibling.click();""")
            print(e)

        # Sometimes it opens in a new tab, we must refocus
        self.focused_browser.switch_to_iframe()
        # Wait until clickables change
        for i in range(3):
            clickables = self.focused_browser.get_clickable()
            if clickables != old_clickables:
                break
            else:
                # NOTE: just check if it was a radio button pressed
                # OR store that radio buttons exist on the page when adding numbers
                # Just a simple bool. And if radios on page, wait a lot less if at all
                print("Waiting for change - remind me and I'll fix this later")
                time.sleep(.2)
        self.show_links()

    def search(self, speech):
        if self.right_browser is None:
            self._open_google()
        else:
            self.focus_right()
        self.right_browser.get("https://www.google.com/")
        speech = speech.replace("search", "").replace("section", "").replace("said", "").strip()
        time.sleep(.1)
        search_bar_opts = self.right_browser.get_el(tag="input", plural=True)
        for bar in search_bar_opts:
            if "earch" in bar.get_attribute("title"):
                search_bar = bar
        search_bar.send_keys(speech)
        time.sleep(.01)
        search_bar.send_keys(Keys.ENTER)
        self.show_links()

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
                browser.switch_to_iframe()
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
        self.focused_browser.refocus()

    def focus_right(self, *args):
        self.focused_browser = self.right_browser
        self.focused_browser.refocus()

    def download_mimir_pdf(self, *args):
        pdf_url = "blank"
        while "pdf" not in pdf_url:
            pdf = self.focused_browser.get_el(tag="iframe")
            pdf_url = pdf.get_attribute("src")
            time.sleep(.1)
        self.focused_browser.open_new_tab(url=pdf_url)

    def switch_tab(self, speech, *args):
        tab_num = self.get_num(speech)

        handles = self.focused_browser.browser.window_handles
        current_handle = self.focused_browser.browser.current_window_handle
        handle_num = handles.index(current_handle) + 1
        if tab_num is None:
            tab_num = handle_num + 1
            if tab_num > len(handles):
                tab_num = 1
        # https://www.techbeamers.com/switch-between-windows-selenium-python/
        self.focused_browser.browser.switch_to_window(handles[tab_num - 1])
        text = "__1__"
        if self.focused_browser.get_el(xpath="//*[contains(text(),'" + text + "')]") is not None:
            print("Found numbers!")
        else:
            self.show_links()

    def quit(self, *args):
        for attr in ["left_browser", "right_browser"]:
            try:
                getattr(self, attr).browser.quit()
                setattr(self, attr, None)
            except AttributeError as e:
                pass

    def turn_off(self, *args):
        try:
            self.quit()
        except Exception as e:
            print(e)
        sys.exit(0)
