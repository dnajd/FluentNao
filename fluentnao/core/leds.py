from joints import Joints

class Leds():

    # init method
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
        self.nao.ledsProxy.off(self.joints.LEDs.AllLeds);
        return self;

    def eyes(self, hex=0xCC0033, intensity=0):
        self.nao.ledsProxy.fadeRGB(self.joints.LEDs.FaceLeds, hex, intensity) # intensity & duration
        return self;

    def head(self, hex=0xCC0033, intensity=0):
        self.ledsProxy.fadeRGB(self.joints.LEDs.BrainLeds, hex, intensity) # intensity & duration
        return self;

    def ears(self, hex=0xCC0033, intensity=0):
        self.nao.ledsProxy.fadeRGB(self.joints.LEDs.EarLeds, hex, intensity) # intensity & duration
        return self;

    def chest(self, hex=0xCC0033, intensity=0):
        self.nao.ledsProxy.fadeRGB(self.joints.LEDs.ChestLeds, hex, intensity) # intensity & duration
        return self;

    def feet(self, hex=0xCC0033, intensity=0):
        self.nao.ledsProxy.fadeRGB(self.joints.LEDs.FeetLeds, hex, intensity) # intensity & duration
        return self;