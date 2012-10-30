class Joints():

    # init method
    def __init__(self):

        # enums for all chains and joints
        self.Chains = Enum(["Body","Head","LArm","RArm","LLeg","RLeg"])
        self.Head =   Enum(["HeadYaw", "HeadPitch"])
        self.LArm =   Enum(["LShoulderPitch","LShoulderRoll","LElbowYaw","LElbowRoll","LWristYaw","LHand"])
        self.RArm =   Enum(["RShoulderPitch","RShoulderRoll","RElbowYaw","RElbowRoll","RWristYaw","RHand"])
        self.LLeg =   Enum(["LHipYawPitch","LHipRoll","LHipPitch","LKneePitch","LAnklePitch","LAnkleRoll"])
        self.RLeg =   Enum(["RHipYawPitch","RHipRoll","RHipPitch","RKneePitch","RAnklePitch","RAnkleRoll"])        

        # foot state
        self.SupportLeg = Enum(["Legs","LLeg","RLeg"])        
        self.StateName = Enum(["Fixed","Plane","Free"])        

        # http://www.aldebaran-robotics.com/documentation/naoqi/sensors/alleds.html
        self.LEDs = Enum(["AllLeds","BrainLeds","EarLeds","FaceLeds","ChestLeds","FeetLeds"])       


class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError 