import logging

from pocketsphinx import LiveSpeech

class Assistant:
    def __init__(self):
        self.callbacks = {
            "I like apples": self.eat_apple
        }
        self.callbacks = {k.lower(): v for k, v in self.callbacks.items()}

    def run(self):
        logging.info("Running")
        for phrase in LiveSpeech():
            callback = self.callbacks.get(phrase.hypothesis(), False)
            if callback is not False:
                callback()
            else:
                print(phrase.hypothesis())

    def eat_apple(self):
        print("Eating an apple now")
