# MIDIfighting
A means for Windows users to control a vJoy virtual joystick device using any MIDI device (virtual or otherwise).

Developed for me to use a [DJ Tech Tools MIDI Fighter](https://store.djtechtools.com/products/midi-fighter-3d) as an actual fighting game controller, but not in any way restricted to fighting games!

### Requirements

For pip-accessible requirements, you should be able to do:
```bash
pip install -r requirements.txt
```

#### *Python*
I've been using Python 3.8 for this because that's what I have locally, but I think it would work fine with 2.7 or maybe some earlier versions if they are supported by the libraries. The Py3 `print()` function is imported from `__future__` so there should be no code changes required for 2.7.

#### *[vJoy](http://vjoystick.sourceforge.net/site/index.php/download-a-install/download)*
This is the tool that allows you to create and 'feed' inputs to a virtual game controller. From their own site: "vJoy is a device driver that bridges the gap between any device that is not a joystick and an application that requires a joystick. If you develop an application for windows that requires user physical input you should consider incorporating vJoy into your product." 

*Note: You may need to set up a vJoy Device on your computer using the 'Configure vJoy' program included with vJoy. The default seems to be one joystick (analogue, X/Y axis) and 8 buttons. For this program, it needs to have one joystick (analogue, X/Y axis) and 10 or more buttons. If you need access to LT/RT/L3/R3 etc., add more buttons and mappings as needed.*

#### *[pyvjoy](https://github.com/tidzo/pyvjoy)*
This is the tool that exposes a Python interface to the vJoy devices. It uses the DLLs installed by the vJoy installer linked above. I haven't had any performance issues with it that might be attributed to Python, gaming feels fairly spot on.
```bash
pip install pyvjoy
```

#### *[python-rtmidi](https://github.com/SpotlightKid/python-rtmidi)*
This is the tool that pulls in real-time MIDI events so that we can turn them into vJoy events.
```bash
pip install python-rtmidi
```

#### *Microsoft Windows* 
vJoy, as far as I know, is Windows-exclusive, so until I do some bigtime investigating into a more portable way to make a virtual controller magically appear, we are stuck with that. Luckily, most PC gaming happens on Windows.

### Running

If you're using a MIDI Fighter as well, in theory it will be as simple as running
```bash
python midifighting.py
```
from the source directory, once you have installed the requirements. The program will prompt you to pick a MIDI input device to use - they are usually helpfully named. Here's what it looks like for me:
```bash
$ py -u midifighting.py
Available MIDI ports:

[0] Midi Fighter 3D 0
[1] loopMIDI Port 1

Select MIDI input port (Control-C to exit): 0
```

If all is well the MIDI input will be opened, the vJoy device will be initialised, and you'll be able to start sending notes/game inputs!

```bash
Using port Midi Fighter 3D 0, vJoy device <pyvjoy.vjoydevice.VJoyDevice object at 0x000001A1CF354C40>
Running. Press Control-C to exit.
```

I used [this tool](http://www.planetpointy.co.uk/joystick-test-application/) to confirm that my device was sending joystick inputs through vJoy, then started up my game and was able to play as normal. 

*Note: It is very helpful if the game you're going to play allows multiple controllers to be connected, and whichever one is active to work! If the game strongly depends on only a single joystick being plugged in, it may fail to see the vJoy one when you have other joystick devices configured on your PC.*

### Layouts
For now the layout is hardcoded but can be changed easily enough by users. I'd like to add a JSON or similar method for loading in different layouts, but it may require more thought in how the directions and buttons are separated. In any case:

#### MIDI Fighter for Xbox-compatible fighting games

This is the first 'page' of the MIDI Fighter, which by default starts on C0/C1 (MIDI note 36). On the MIDI Fighter, the lowest note is on the bottom right, and notes increase in value across the rows and up the columns.
```
[48][49][50][51]
[44][45][46][47]
[40][41][42][43]
[36][37][38][40]
```
We don't have much room here, but what room we have is probably best used for making action buttons easy to access and differentiate.
So to give a somewhat HitBox-like layout, I set it up like this (`NA` = not used):
```
[L ][NA][Bk][St]
[D ][X ][Y ][RB]
[R ][A ][B ][RT]
[U ][NA][NA][NA]
```
For playing I hold it rotated about 45deg to the left, like a diamond with the Up button (36/low C) at the bottom. This is just my first layout, but it works fine so far. There is room to do the same arrangement of directions on the bottom row instead, if you want to have your wrists very close together, but I prefer to have them apart.

### Other notes/improvements
Most importantly: *feedback or PRs welcome!*

#### SOCD
This tool implements pretty basic SOCD management (Simultaneous Opposite Cardinal Directions) to prevent weird inputs that might upset a game. It probably isn't ideal or perfect.

#### Analogue stick versus hat/directional-pad
Analogue stick inputs were the ones I could find and make work easily, but I think if I could get the d-pad working that would be my preferred way to work, especially for fighting games.

#### More layouts/layout swapping
As discussed above, it's fairly easy to change the hardcoded layout to match whatever controller you have, but I'd like to lift that out of the code and make it swappable easily with a CLI argument or similar.

#### Doing weird _other stuff_ with the MIDI inputs
We are already getting in these cool MIDI inputs, what else could we do with them? Perhaps play sounds, as they were designed to do?
