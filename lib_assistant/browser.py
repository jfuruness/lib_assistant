from enum import Enum
from os.path import expanduser
import os
import subprocess
import time

from pynput.keyboard import Key, Controller
import selenium
from selenium import webdriver
from selenium.webdriver import ChromeOptions as Options
from selenium.webdriver.common.keys import Keys


from . import utils

class Browser:
    driver_path = os.path.join(expanduser("~"), "/usr/local/bin/chromedriver")

    def __init__(self):
        if not os.path.exists(self.driver_path):
            self.install()
        self.in_iframe = False
        self.pdf = False

    @property
    def url(self):
        return self.browser.current_url

    def open(self, side=None):
        width, height = self._get_dims()
        print(side)
        if side in [Side.LEFT, Side.RIGHT]:
            # Get chrome options
            opts = Options()

            # Set new width and hieght
            new_width = width // 2
            new_height = height * .9
            # https://stackoverflow.com/a/37151037/8903959
            opts.add_argument(f"--window-size={new_width},{new_height}")

            # Set new position
            if side == Side.LEFT:
                opts.add_argument("--window-position=0,0")
            elif side == Side.RIGHT:
                opts.add_argument(f"--window-position={new_width + 1},0")
        else:
            assert False, "Not implimented"
            
        self.browser = webdriver.Chrome(self.driver_path,
                                        chrome_options=opts)
    def get(self, url):
        self.browser.get(url)

    def get_el(self, _id=None, name=None, tag=None, xpath=None, plural=False):
        if _id:
            return self.browser.find_element_by_id(_id)
        if name:
            return self.browser.find_element_by_name(name)
        if tag:
            if plural:
                return self.browser.find_elements_by_tag_name(tag)
            else:
                return self.browser.find_element_by_tag_name(tag)
        if xpath:
            if plural:
                return self.browser.find_elements_by_xpath(xpath)
            else:
                return self.browser.find_element_by_xpath(xpath)

    def get_clickable(self):
        a_tags = self.get_el(tag="a", plural=True)
        # https://stackoverflow.com/a/48365300/8903959
        submit_buttons = self.get_el(xpath="//input[@type='submit']", plural=True)
        other_buttons = self.get_el(xpath="//input[@type='button']", plural=True)
        standard_buttons = [x for x in submit_buttons + other_buttons
                            if (x.get_attribute("value")
                                and "Lucky" not in x.get_attribute("value"))]

        radio_buttons = self.get_el(xpath="//input[@type='radio']", plural=True)
        clickables = a_tags + standard_buttons + radio_buttons
        
        return [elem for elem in clickables if self.valid_elem(elem)]

    def valid_elem(self, elem):
        if elem.is_displayed() and elem.is_enabled():
            return True
        else:
            return False

    def add_number(self, num, elem):
        if elem.get_attribute("type").lower() in ["submit", "button"]:
            self.add_number_to_button(num, elem)
        elif elem.get_attribute("type").lower() == "radio":
            self.add_number_to_radio(num, elem)
        else:
            self.add_number_to_elem(num, elem)

    def add_number_to_radio(self, num, button):
        # https://stackoverflow.com/a/18079918
        # https://www.edureka.co/community/4032/how-get-next-sibling-element-using-xpath-and-selenium-for-java
        #next_elem = button.find_element_by_xpath("following-sibling::*")
        parent_elem = button.find_element_by_xpath("..")
        num_str = self._format_number(num)
        # https://www.quora.com/How-do-I-add-an-HTML-element-using-Selenium-WebDriver
        javascript_str = (f"text = document.createTextNode('{num_str}');"
                          f"arguments[0].appendChild(text);")
        # https://stackoverflow.com/a/14052682
        #child_elems = parent_elem.find_elements_by_xpath(".//*")
        #for i, elem in enumerate(child_elems):
        #    if elem.get_attribute("type").lower() == "radio":
        #        next_elem = child_elems[i + 1]
        self.browser.execute_script(javascript_str, parent_elem)
        #self.add_number_to_elem(num, next_elem)

    def add_number_to_button(self, num, button):
        #print(button.get_attribute("outerHTML"))
        #input()
        button_value = button.get_attribute("value")
        num_str = f"{self._format_number(num)}{button_value}"
        self.browser.execute_script(f"arguments[0].value = '{num_str}'",
                                    button)

    def add_number_to_elem(self, num, elem):
        # https://stackoverflow.com/a/18079918
        # https://www.edureka.co/community/4032/how-get-next-sibling-element-using-xpath-and-selenium-for-java
        #next_elem = button.find_element_by_xpath("following-sibling::*")
        parent_elem = elem.find_element_by_xpath("..")
        num_str = self._format_number(num)
        # https://www.quora.com/How-do-I-add-an-HTML-element-using-Selenium-WebDriver
        javascript_str = (f"text = document.createTextNode('{num_str}');"
                          f"arguments[0].appendChild(text);")
        # https://stackoverflow.com/a/14052682
        #child_elems = parent_elem.find_elements_by_xpath(".//*")
        #for i, elem in enumerate(child_elems):
        #    if elem.get_attribute("type").lower() == "radio":
        #        next_elem = child_elems[i + 1]
        self.browser.execute_script(javascript_str, parent_elem)
        return
        # https://stackoverflow.com/a/26947299
        #print(elem.text)
        #print(elem.get_attribute("innerHTML"))
        #input(self.valid_elem(elem))
        # https://stackoverflow.com/a/41553384/8903959
        # https://stackoverflow.com/a/49071078/8903959
        #num_str = (f"""<div style="color:blue;"""
        #           f"float:left;height:20px;"
        #           f"width:20px;margin-bottom:15px;"
        #           f"border: 1px solid black;"
        #           f"""clear: both;background:red">:{num}:{elem.text}</div>""")
        num_str = f"{self._format_number(num)}{elem.text}"
#        self.browser.execute_script(f"arguments[0].style.backgroundColor = 'white'",
#                                    elem)
        self.browser.execute_script(f"arguments[0].innerText = '{num_str}'",
                                    elem)

    def remove_number(self, num, elem):
        return
        remove_str = self._format_number(num)
        num_str = elem.text.replace(remove_str, "")
        self.browser.execute_script(f"arguments[0].innerText = '{num_str}'",
                                    elem)
        if elem.get_attribute("type").lower() in ["submit", "button"]:
            num_str = elem.get_attribute("value").replace(remove_str, "")
            self.browser.execute_script(f"arguments[0].value = '{num_str}'",
                                        elem)


    def _format_number(self, num):
        return f"__{num}__"

    def _get_dims(self):
        """Gets width and height of monitor"""

        # https://stackoverflow.com/a/3598320/8903959
        output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',
                                  shell=True,
                                  stdout=subprocess.PIPE).communicate()[0]
        output = output.decode('utf-8').split("\n")[0]
        # 1920x1080
        return [int(x) for x in output.split("x")]

    def install(self):
        """Installs chromedriver to driverpath"""


        # https://gist.github.com/mikesmullin/2636776#gistcomment-2608206
        cmd = ("LATEST_VERSION=$(curl -s "
               "https://chromedriver.storage.googleapis.com/LATEST_RELEASE) &&"
               " wget -O /tmp/chromedriver.zip "
               "https://chromedriver.storage.googleapis.com/$LATEST_VERSION/"
               "chromedriver_linux64.zip && "
               "sudo unzip /tmp/chromedriver.zip "
               f"chromedriver -d {driverpath};")
        utils.run_cmds(cmd)

    def scroll_up(self):
        # https://www.reddit.com/r/learnpython/comments/6yrcee/use_selenium_to_repeatedly_send_arrowuprightdown/
#        el = self.get_el(tag="body")
#        action = webdriver.common.action_chains.ActionChains(self.browser)
#        action.move_to_element_with_offset(el, 5, 5)
#        action.click()
#        action.perform()
        for _ in range(3):
            self.get_el(tag="body").send_keys(Keys.ARROW_UP)
        if self.pdf:
            keyboard = Controller()
            for key_type in ["up"] * 6:
                print(f"Sending key: {key_type}")
                keyboard.press(getattr(Key, key_type))
                keyboard.release(getattr(Key, key_type))
                time.sleep(.2)

    def scroll_down(self):
        el = self.get_el(tag="body")
 #       action = webdriver.common.action_chains.ActionChains(self.browser)
 #       action.move_to_element_with_offset(el, 5, 5)
 #       action.click()
 #       action.perform()
        for _ in range(3):
            self.get_el(tag="body").send_keys(Keys.ARROW_DOWN)
        if self.pdf:
            keyboard = Controller()
            for key_type in ["down"] * 6:
                print(f"Sending key: {key_type}")
                keyboard.press(getattr(Key, key_type))
                keyboard.release(getattr(Key, key_type))
                time.sleep(.2)

    def page_up(self):
        print(self.url)
        for _ in range(3):
            self.get_el(tag="body").send_keys(Keys.PAGE_UP)
        if self.pdf:
            keyboard = Controller()
            for key_type in ["page_up"]:
                print(f"Sending key: {key_type}")
                keyboard.press(getattr(Key, key_type))
                keyboard.release(getattr(Key, key_type))
                time.sleep(.2)


    def page_down(self):
        print(self.url)
        for _ in range(3):
            self.get_el(tag="body").send_keys(Keys.PAGE_DOWN)
        if self.pdf:

            keyboard = Controller()
            for key_type in ["page_down"]:
                print(f"Sending key: {key_type}")
                keyboard.press(getattr(Key, key_type))
                keyboard.release(getattr(Key, key_type))
                time.sleep(.2)


    def right_click_tag(self, tag):
        action = selenium.webdriver.ActionChains(self.browser)
        action.context_click(self.get_el(tag=tag)).perform()

class Side(Enum):
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"
