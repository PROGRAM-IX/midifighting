from __future__ import print_function

import time
import sys

import pyvjoy 
from rtmidi.midiconstants import NOTE_ON, NOTE_OFF
from rtmidi.midiutil import open_midiinput, open_midioutput


# You may need to set up a vJoy Device on your computer using the
# 'Configure vJoy' program included with vJoy. The default seems to be
# one joystick (analogue, X/Y axis) and 8 buttons. For this program,
# it needs to have one joystick (analogue, X/Y axis) and 10 
# or more buttons. If you need access to LT/RT/L3/R3 etc., add more
# buttons and mappings as needed.

# If you have multiple vJoy Devices, change this number
# to pick the one you need.
VJOY_DEVICE_ID = 1

# These tuples capture the args to move the 'left joystick' axes
LEFT = (pyvjoy.HID_USAGE_X, 0x1)
DOWN = (pyvjoy.HID_USAGE_Y, 0x8000)
RIGHT = (pyvjoy.HID_USAGE_X, 0x8000)
UP = (pyvjoy.HID_USAGE_Y, 0x1)
CENTRE_X = (pyvjoy.HID_USAGE_X, 0x4000)
CENTRE_Y = (pyvjoy.HID_USAGE_Y, 0x4000)

# Maps MIDI notes to joystick inputs.
# For directions: just hold the direction marker.
# For buttons: hold the button number and a name (the name isn't used at present).
MIDI_NOTE_MAP = {
    "48": ("l",), # Left
    "44": ("d",), # Down
    "40": ("r",), # Right
    "36": ("u",), # Up
    "50": (9, "back"), # Back button
    "51": (10, "start"), # Start button
    "45": (1, "x"), # X
    "46": (4, "y"), # Y
    "47": (6, "rb"), # RB
    "41": (2, "a"), # A
    "42": (3, "b"), # B
    "43": (8, "rt"), # RT
    # Uncomment these if you need them
    # "49": (11, "l3"), # Left stick click
    # "37": (12, "r3"), # Right stick click
    # "38": (5, "lb"), # LB
    # "39": (7, "lt"), # LT
}

# This keeps track of which directions are currently pressed,
# so that we can reason about what the joystick should do.
dirs = {
    "l": False,
    "r": False,
    "d": False,
    "u": False
}

# If the user presses more than one direction at a time
# we need to be able to reason about the 'actual' direction
# that the controller should use. In general, opposing
# directions should do nothing, but by convention UP and                   
# DOWN give UP.
SOCD_MAP = {
    "": [CENTRE_X, CENTRE_Y],
    "lrdu": [CENTRE_X, UP],
    "lrd": [CENTRE_X, DOWN],
    "du": [CENTRE_X, UP],
    "lr": [CENTRE_X],
    "lru": [CENTRE_X, UP],
    "ldu": [LEFT, UP],
    "rdu": [RIGHT, UP],
    "l": [LEFT, CENTRE_Y],
    "ld": [LEFT, DOWN],
    "lu": [LEFT, UP],
    "ldu": [LEFT, UP],
    "r": [RIGHT, CENTRE_Y],
    "rd": [RIGHT, DOWN],
    "ru": [RIGHT, UP],
    "rdu": [RIGHT, UP],
    "d": [CENTRE_X, DOWN],
    "u": [CENTRE_X, UP],
}

vjoy_device = pyvjoy.VJoyDevice(VJOY_DEVICE_ID)

class MidiNoteCallback(object):
    def __init__(self, port, midi_out=None):
        self.port = port
        self.midi_out = midi_out

    def __call__(self, event, data=None):
        message, _ = event
        m_type, val, vel = message
        if self.midi_out:
            midi_out.send_message(message)
        if m_type == NOTE_ON:
            mapping = MIDI_NOTE_MAP.get(str(val))
            if mapping:
                #print(mapping)
                if len(mapping) == 1: # direction
                    dirs[mapping[0]] = True
                    self.process_socd()
                else: # button
                    vjoy_device.set_button(mapping[0], 1)
        elif m_type == NOTE_OFF:
            mapping = MIDI_NOTE_MAP.get(str(val))
            if mapping:
                #print(mapping)
                if len(mapping) == 1: # direction
                    dirs[mapping[0]] = False
                    self.process_socd()
                else: # button
                    vjoy_device.set_button(mapping[0], 0)

        #print("[%s] @%0.6f %r" % (self.port, message))

    def process_socd(self):
        current = "".join([d for d in dirs if dirs[d]])
        #print(current)
        mapping = SOCD_MAP.get(current)
        for d in mapping:
            vjoy_device.set_axis(d[0], d[1])


try:
    midi_in, in_port_name = open_midiinput()
except (EOFError, KeyboardInterrupt) as e:
    print("Failed to open MIDI input device! {}".format(e))
    sys.exit()

out_message = ""
midi_out = None
if input("Do you want to forward the MIDI input on through another port? ").lower() in ("y", "yes"):
    try:
        midi_out, out_port_name = open_midioutput()
        out_message = ", output port {}".format(out_port_name)
    except (EOFError, KeyboardInterrupt) as e:
        print("Failed to open MIDI output device! {}".format(e))
        sys.exit()

print("Using input port {}, vJoy device {}{}".format(in_port_name, vjoy_device, out_message))
midi_in.set_callback(MidiNoteCallback(in_port_name, midi_out))


print("Running. Press Control-C to exit.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("")
finally:
    print("Done.")
    midi_in.close_port()
    del midi_in
