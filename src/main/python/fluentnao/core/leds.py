'''
FluentNao Leds Module -- controls all LED groups on the NAO robot.

This module provides the Leds class, which sets LED colors and intensity
using a fluent chaining API. LED changes take effect immediately (no go()
needed), but go() is available for consistency with other body part modules.

Key Methods
-----------
    eyes(hex=0xCC0033, intensity=0)   -- set face/eye LED color
    head(hex=0xCC0033, intensity=0)   -- set brain/skull LED color
    ears(hex=0xCC0033, intensity=0)   -- set ear LED color
    chest(hex=0xCC0033, intensity=0)  -- set chest button LED color
    feet(hex=0xCC0033, intensity=0)   -- set foot LED color
    off()                             -- turn all LEDs off

Parameters:
    hex       -- color as a hex integer, e.g. 0xFF0000 for red,
                 0x00FF00 for green, 0x0000FF for blue.
                 Default is 0xCC0033 (pinkish red).
    intensity -- fade duration in seconds (0 = instant).

Execution:
    go() -- execute any queued moves on the nao object and return it.
            Note: LED methods apply immediately via fadeRGB/off calls,
            so go() is only needed if you have queued moves on other
            body parts.

Usage Examples
--------------
    # Set eyes to green
    nao.leds.eyes(0x00FF00)

    # Set eyes green and chest blue in one chain
    nao.leds.eyes(0x00FF00).chest(0x0000FF)

    # Turn all LEDs off
    nao.leds.off()

    # Set eyes to red with a 1-second fade
    nao.leds.eyes(0xFF0000, 1)

Notes
-----
- This is Python 2.7 code.
- LED methods return self (the Leds instance) for chaining.
- The head() method controls three LED groups: BrainLedsBack,
  BrainLedsMiddle, and BrainLedsFront.
- Color reference: http://html-color-codes.com/
'''

class Leds():

    def __init__(self, nao):
        
        # jobs for threading
        self.nao = nao
        self.joints = nao.joints
        self.chains = nao.chains
        self.log = nao.log

        # http://html-color-codes.com/

    def go(self):
        self.nao.go()
        return self.nao

    ###################################
    # LEDs
    ###################################
    def off(self):
        self.nao.env.leds.off(self.joints.LEDs.AllLeds);
        return self;

    def eyes(self, hex=0xCC0033, intensity=0):
        self.nao.env.leds.fadeRGB(self.joints.LEDs.FaceLeds, hex, intensity) # intensity & duration
        return self;

    def head(self, hex=0xCC0033, intensity=0):
        self.nao.env.leds.fadeRGB("BrainLedsBack", hex, intensity) # intensity & duration
        self.nao.env.leds.fadeRGB("BrainLedsMiddle", hex, intensity) # intensity & duration
        self.nao.env.leds.fadeRGB("BrainLedsFront", hex, intensity) # intensity & duration
        return self;

    def ears(self, hex=0xCC0033, intensity=0):
        self.nao.env.leds.fadeRGB(self.joints.LEDs.EarLeds, hex, intensity) # intensity & duration
        return self;

    def chest(self, hex=0xCC0033, intensity=0):
        self.nao.env.leds.fadeRGB(self.joints.LEDs.ChestLeds, hex, intensity) # intensity & duration
        return self;

    def feet(self, hex=0xCC0033, intensity=0):
        self.nao.env.leds.fadeRGB(self.joints.LEDs.FeetLeds, hex, intensity) # intensity & duration
        return self;