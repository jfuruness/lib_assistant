from enum import Enum
from os.path import expanduser
import os
import subprocess

from selenium import webdriver
from selenium.webdriver import ChromeOptions as Options

from . import utils

class Browser:
    driver_path = os.path.join(expanduser("~"), "/usr/local/bin/chromedriver")

    def __init__(self):
        if not os.path.exists(self.driver_path):
            self.install()
        self.in_iframe = False

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

    def get_el(self, _id=None, name=None, tag=None, plural=False):
        if _id:
            return self.browser.find_element_by_id(_id)
        if name:
            return self.browser.find_element_by_name(name)
        if tag:
            if plural:
                return self.browser.find_elements_by_tag_name(tag)
            else:
                return self.browser.find_element_by_tag_name(tag)

    def valid_elem(self, elem):
        if elem.is_displayed() and elem.is_enabled():
            return True
        else:
            return False

    def add_number(self, num, elem):
        # https://stackoverflow.com/a/26947299
        print(elem.text)
        print(elem.get_attribute("innerHTML"))
        input(self.valid_elem(elem))
        if not self.valid_elem(elem):
            return
        # https://stackoverflow.com/a/41553384/8903959
        # https://stackoverflow.com/a/49071078/8903959
        #num_str = (f"""<div style="color:blue;"""
        #           f"float:left;height:20px;"
        #           f"width:20px;margin-bottom:15px;"
        #           f"border: 1px solid black;"
        #           f"""clear: both;background:red">:{num}:{elem.text}</div>""")
        num_str = f"{self._format_number(num)}{elem.text}"
#        print(num_str)
#        input(elem.get_attribute("outerHTML"))
        # Change to innerHtml or textContent? Potentially inline css style?
#        self.browser.execute_script(f"arguments[0].style.backgroundColor = 'white'",
#                                    elem)
        self.browser.execute_script(f"arguments[0].innerText = '{num_str}'",
                                    elem)

    def remove_number(self, num, elem):
        if not self.valid_elem(elem):
            return
        num_str = elem.text.replace(self._format_number(num), "")
        self.browser.execute_script(f"arguments[0].innerText = '{num_str}'",
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

class Side(Enum):
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"
