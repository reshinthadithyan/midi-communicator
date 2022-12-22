#!/usr/bin/env python
""" pygame.examples.midi

midi input, and a separate example of midi output.

By default it runs the output example.

python -m pygame.examples.midi --output
python -m pygame.examples.midi --input
python -m pygame.examples.midi --input
"""

import sys
import os

import pygame as pg
import pygame.midi
import pynput
import logging
import json
from pynput.keyboard import Key, Controller
kb = Controller()



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



#CONFIG
config = json.load(open(os.path.join("config","main_config.json")))
chrome_path  = config["chrome_path"]



def print_device_info():
    pygame.midi.init()
    _print_device_info()
    pygame.midi.quit()

def press(button):
    kb.press(button)
    kb.release(button)


def _print_device_info():
    for i in range(pygame.midi.get_count()):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print(
            "%2i: interface :%s:, name :%s:, opened :%s:  %s"
            % (i, interf, name, opened, in_out)
        )


def input_main(device_id=None):
    pg.init()

    pygame.midi.init()

    _print_device_info()

    if device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id

    print(f"using input_id :{input_id}:")
    i = pygame.midi.Input(input_id)

    pg.display.set_mode((1, 1))

    going = True
    print("Starting the loop...")
    while going:
        events = pygame.event.get()
        for e in events:
            if e.type in [pg.QUIT]:
                going = False
            if e.type in [pg.KEYDOWN]:
                going = False
            if e.type in [pygame.midi.MIDIIN]:
                print(e)
        import keyboard
        if i.poll():
            midi_events = i.read(10)
            # convert them into pygame events.
            midi_evs = pygame.midi.midis2events(midi_events, i.device_id)
            for m_e in midi_evs:
                if m_e.status != 248:
                    print(m_e)
                if m_e.status == 144:
                    key = m_e.data1
                    print(key)
                    if key == config["keys"]["UP"]:
                        logger.info("UP")
                        keyboard.press_and_release("up")
                        #press(Key.up)
                    elif key == config["keys"]["DOWN"]:
                        logger.info("DOWN")
                        #press(Key.down)
                        keyboard.press_and_release("down")
                    elif key == config["keys"]["LEFT"]:
                        logger.info("LEFT")
                        #press(Key.left)
                        keyboard.press_and_release("left")
                    elif key == config["keys"]["RIGHT"]:
                        logger.info("RIGHT")
                        #press(Key.right)
                        keyboard.press_and_release("right")
                    elif key == config["keys"]["PAGE_UP"]:
                        logger.info("PAGE_UP")
                        #press(Key.page_up)
                        keyboard.press_and_release("page up")
                    elif key == config["keys"]["PAGE_DOWN"]:
                        logger.info("PAGE_DOWN")
                        #press(Key.page_down)
                        keyboard.press_and_release("page down")
                    elif key == config["keys"]["TAB_CHANGE_RIGHT"]:
                        logger.info("TAB_CHANGE_RIGHT")
                        #press(Key.page_down)
                        #keyboard.press("control")
                        keyboard.press_and_release("right control+tab")
                        #keyboard.release("control")
                    # elif key == config["keys"]["TAB_CHANGE_LEFT"]:
                    #     logger.info("TAB_CHANGE_LEFT")
                    #     #press(Key.page_down)
                    #     keyboard.press_and_release("command+option+left")
                #COMMENT(reshinth) : pygame.event.post(m_e)
                

    del i
    pygame.midi.quit()

def usage():
    print("--input [device_id] : Midi message logger")
    print("--output [device_id] : Midi piano keyboard")
    print("--list : list available midi devices")


def main(mode="output", device_id=None):
    """Run a Midi example

    Arguments:
    mode - if 'output' run a midi keyboard output example
              'input' run a midi event logger input example
              'list' list available midi devices
           (default 'output')
    device_id - midi device number; if None then use the default midi input or
                output device for the system

    """

    if mode == "input":
        input_main(device_id)
    elif mode == "output":
        pass
        #output_main(device_id)
    elif mode == "list":
        print_device_info()
    else:
        raise ValueError(f"Unknown mode option '{mode}'")


if __name__ == "__main__":

    try:
        device_id = int(sys.argv[-1])
    except ValueError:
        device_id = None

    if "--input" in sys.argv or "-i" in sys.argv:
        input_main(device_id)
    elif "--list" in sys.argv or "-l" in sys.argv:
        print_device_info()
    else:
        usage()

    pg.quit()