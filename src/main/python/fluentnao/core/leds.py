"""Fluent API for controlling all LED groups on the NAO robot."""

class Leds():
    """Controls face, head, ear, chest, and foot LED colors and intensity.

    LED changes take effect immediately via fadeRGB/off calls (no go()
    needed), but go() is available for consistency with other modules.

    Args common to LED methods:
        hex: Color as a hex integer (e.g. 0xFF0000 for red). Default 0xCC0033.
        intensity: Fade duration in seconds; 0 means instant.

    Color reference: http://html-color-codes.com/

    Examples::

        nao.leds.eyes(0x00FF00)
        nao.leds.eyes(0x00FF00).chest(0x0000FF)
        nao.leds.off()
    """

    def __init__(self, nao):

        # jobs for threading
        self.nao = nao
        self.joints = nao.joints
        self.chains = nao.chains
        self.log = nao.log

        # http://html-color-codes.com/

    def go(self):
        """Execute any queued moves on the nao object and return it."""
        self.nao.go()
        return self.nao

    ###################################
    # LEDs
    ###################################
    def off(self):
        """Turn all LEDs off."""
        self.nao.env.leds.off(self.joints.LEDs.AllLeds);
        return self;

    def eyes(self, hex=0xCC0033, intensity=0):
        """Set face/eye LED color."""
        self.nao._eye_color = hex
        self.nao.env.leds.fadeRGB(self.joints.LEDs.FaceLeds, hex, intensity) # intensity & duration
        return self;

    def head(self, hex=0xCC0033, intensity=0):
        """Set brain/skull LED color (back, middle, and front)."""
        self.nao.env.leds.fadeRGB("BrainLedsBack", hex, intensity) # intensity & duration
        self.nao.env.leds.fadeRGB("BrainLedsMiddle", hex, intensity) # intensity & duration
        self.nao.env.leds.fadeRGB("BrainLedsFront", hex, intensity) # intensity & duration
        return self;

    def ears(self, hex=0xCC0033, intensity=0):
        """Set ear LED color."""
        self.nao.env.leds.fadeRGB(self.joints.LEDs.EarLeds, hex, intensity) # intensity & duration
        return self;

    def chest(self, hex=0xCC0033, intensity=0):
        """Set chest button LED color."""
        self.nao.env.leds.fadeRGB(self.joints.LEDs.ChestLeds, hex, intensity) # intensity & duration
        return self;

    def feet(self, hex=0xCC0033, intensity=0):
        """Set foot LED color."""
        self.nao.env.leds.fadeRGB(self.joints.LEDs.FeetLeds, hex, intensity) # intensity & duration
        return self;