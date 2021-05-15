import curses
import logging
import threading

from inqbus.rpi.widgets.base.input import Input
from inqbus.rpi.widgets.base.signals import InputChar
from inqbus.rpi.widgets.errors import SignalNotCatched
from inqbus.rpi.widgets.input.signals import KEYBOARD_SIGNALS
from inqbus.rpi.widgets.interfaces.input import IInput
from inqbus.rpi.widgets.interfaces.interfaces import IGUI
from zope.component import getUtility
from zope.interface import implementer



@implementer(IInput)
class InputCurses(Input):
    """
    Input from a curses frame_buffer. CURRENTLY NOT WORKING!
    """

    def __init__(self, curses_display=None, keyboard_signals=None):

        if not curses_display:
            self.curses_window = curses.newwin(1, 1, 0, 0)
        else:
            self.curses_window = curses_display

        if keyboard_signals:
            self.keyboard_signals = keyboard_signals
        else:
            self.keyboard_signals = KEYBOARD_SIGNALS

        curses.noecho()

    def init(self):
        gui = getUtility(IGUI)
        self.gui = gui

    def key2signal(self, key):
        # if the key is registered for a signal ..
        if key in self.keyboard_signals:
            # .. obtain the signal
            signal = self.keyboard_signals[key]
        else:
            # if not generate a character input signal containing the character
            signal = InputChar(key)
        return signal


    def run(self):
        thread = threading.Thread(target=self.run_curses)
        thread.start()

    def run_curses(self):
        while True:
            key = self.curses_window.getkey()
            signal = self.key2signal(key)
            try:
                self.gui.dispatch(signal)
            except SignalNotCatched:
                logging.error('Signal {} not catched'.format(signal))
