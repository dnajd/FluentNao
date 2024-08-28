import math

from fluentnao.core.recorder.translator import FluentNaoTranslator, joints_to_degrees

#
# Math
#

FLOAT_CMP_ACCURACY = 0.00000001

def feq(a, b, epsilon=FLOAT_CMP_ACCURACY):
    return abs(a - b) < epsilon

def is_zero(a, epsilon=FLOAT_CMP_ACCURACY):
    return abs(a) < epsilon

#
# Joints
#

JOINT_MOVE_AMOUNT = math.pi / 180.0

# joint names in same order as returned by ALMotion.getAngles('Body')
JOINT_NAMES = ['HeadYaw', 'HeadPitch',
               'LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll',
               'LWristYaw', 'LHand',
               'LHipYawPitch', 'LHipRoll', 'LHipPitch',
               'LKneePitch', 'LAnklePitch', 'LAnkleRoll',
               'RHipYawPitch', 'RHipRoll', 'RHipPitch',
               'RKneePitch', 'RAnklePitch', 'RAnkleRoll',
               'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll',
               'RWristYaw', 'RHand']

#
# Recorder
#

class Recorder():

    def __init__(self, nao):
        self.nao = nao
        self.log = nao.log
        self.last_keyframe_joints = None
        self.joints = {}
        self.keyframe_duration = 1.0
        for j in JOINT_NAMES:
            self.joints[j] = 0

    def joint_changes(self, oldangles, newangles, threshold=FLOAT_CMP_ACCURACY):
        """
        Return a set containing the names of joints that have changed.
        """
        changed_joints = set()
        if oldangles:
            for k in newangles.keys():
                j1 = oldangles[k]
                j2 = newangles[k]
                if not feq(j1, j2, threshold):
                    changed_joints.add(k)
        else:
            changed_joints.update(newangles.keys())
        return changed_joints

    def get_joint_angles(self, use_radians=True):
        angles = self.nao.env.motion.getAngles("Body", True)
        for n, v in zip(JOINT_NAMES, angles):
            self.joints[n] = v

        if use_radians:
            return self.joints
        else:
            return joints_to_degrees(self.joints, True)

    def keyframe(self):
        enabled_joints = set(JOINT_NAMES)
        angles = self.get_joint_angles()
        changed_joints = self.joint_changes(self.last_keyframe_joints, angles, JOINT_MOVE_AMOUNT)
        command_str = FluentNaoTranslator().generate(angles, changed_joints, enabled_joints,
                                                is_blocking=True, fluentnao="nao.",
                                                keyframe_duration=self.keyframe_duration,
                                                keyframe_comment="another move")
        self.last_keyframe_joints = angles.copy()
        return command_str
