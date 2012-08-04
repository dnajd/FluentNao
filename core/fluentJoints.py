class FluentJoints():

    # init method
    def __init__(self):

        # enums for all chains and joints
        self.Chains = Enum(["Body","Head","LArm","RArm","LLeg","RLeg"])
        self.Head =   Enum(["HeadYaw", "HeadPitch"])
        self.LArm =   Enum(["LShoulderPitch","LShoulderRoll","LElbowYaw","LElbowRoll","LWristYaw","LHand"])
        self.RArm =   Enum(["RShoulderPitch","RShoulderRoll","RElbowYaw","RElbowRoll","RWristYaw","RHand"])
        self.LLeg =   Enum(["LHipYawPitch1","LHipRoll","LHipPitch","LKneePitch","LAnklePitch","RAnkleRoll"])
        self.RLeg =   Enum(["RHipYawPitch1","RHipRoll","RHipPitch","RKneePitch","RAnklePitch","LAnkleRoll"])        


class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError 