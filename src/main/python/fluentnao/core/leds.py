class Leds():

    def __init__(self, nao):
        
        # jobs for threading
        self.nao = nao
        self.joints = nao.joints
        self.chains = nao.chains
        self.log = nao.log

        # http://html-color-codes.com/

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