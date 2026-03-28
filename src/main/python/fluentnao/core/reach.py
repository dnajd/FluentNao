"""Cartesian (3D position) control of NAO robot end effectors.

Accessed via nao.reach. Python 2.7 compatible.
"""
import math


class Reach():
    """Cartesian end-effector control using NaoQi inverse kinematics.

    Instead of specifying joint angles, you specify X/Y/Z positions
    relative to a reference frame, and NaoQi solves the joint angles.
    All coordinates are in meters. Rotations are in radians.

    Frame Constants:
        TORSO = 0 -- coordinates relative to the torso (default)
        WORLD = 1 -- coordinates in the world frame
        ROBOT = 2 -- coordinates in the robot base frame

    Axis Mask Constants:
        POSITION = 7  -- control X, Y, Z only (bits 0-2)
        ROTATION = 56 -- control WX, WY, WZ only (bits 3-5)
        ALL = 63      -- control all 6 degrees of freedom

    Chain names: 'Head', 'LArm', 'RArm', 'LLeg', 'RLeg'.
    All movement methods return self for fluent chaining.
    Speed parameter is a fraction from 0.0 to 1.0.
    """

    # frames
    TORSO = 0
    WORLD = 1
    ROBOT = 2

    # axis masks
    POSITION = 7      # x, y, z only
    ROTATION = 56     # wx, wy, wz only
    ALL = 63          # position + rotation

    def __init__(self, nao):
        self.nao = nao
        self.log = nao.log

    ###################################
    # query
    ###################################

    def position(self, chain='RArm', frame=None):
        """Return [x, y, z, wx, wy, wz] for the given chain, rounded to 4 decimals."""
        if frame is None:
            frame = self.TORSO
        pos = self.nao.env.motion.getPosition(chain, frame, True)
        return [round(p, 4) for p in pos]

    def positions(self):
        """Return dict mapping all chain names to their positions."""
        result = {}
        for chain in ['Head', 'LArm', 'RArm', 'LLeg', 'RLeg']:
            result[chain] = self.position(chain)
        return result

    ###################################
    # absolute movement
    ###################################

    def to(self, chain, x, y, z, speed=0.3, frame=None):
        """Move end effector to absolute position, preserving current rotation."""
        if frame is None:
            frame = self.TORSO
        current = self.nao.env.motion.getPosition(chain, frame, True)
        target = [x, y, z, current[3], current[4], current[5]]
        self.nao.env.motion.setPosition(chain, frame, target, speed, self.POSITION)
        self.log('reach.to: {} -> ({}, {}, {})'.format(chain, x, y, z))
        return self

    def to_with_rotation(self, chain, x, y, z, wx, wy, wz, speed=0.3, frame=None):
        """Move end effector to absolute position and rotation."""
        if frame is None:
            frame = self.TORSO
        target = [x, y, z, wx, wy, wz]
        self.nao.env.motion.setPosition(chain, frame, target, speed, self.ALL)
        self.log('reach.to_with_rotation: {} -> ({}, {}, {}, {}, {}, {})'.format(chain, x, y, z, wx, wy, wz))
        return self

    ###################################
    # relative movement
    ###################################

    def forward(self, chain='RArm', distance=0.1, speed=0.3, frame=None):
        """Move end effector forward along the +X axis."""
        if frame is None:
            frame = self.TORSO
        self.nao.env.motion.changePosition(chain, frame, [distance, 0, 0, 0, 0, 0], speed, self.POSITION)
        self.log('reach.forward: {} {}m'.format(chain, distance))
        return self

    def back(self, chain='RArm', distance=0.1, speed=0.3, frame=None):
        """Move end effector backward along the -X axis."""
        return self.forward(chain, -distance, speed, frame)

    def left(self, chain='RArm', distance=0.05, speed=0.3, frame=None):
        """Move end effector left along the +Y axis."""
        if frame is None:
            frame = self.TORSO
        self.nao.env.motion.changePosition(chain, frame, [0, distance, 0, 0, 0, 0], speed, self.POSITION)
        self.log('reach.left: {} {}m'.format(chain, distance))
        return self

    def right(self, chain='RArm', distance=0.05, speed=0.3, frame=None):
        """Move end effector right along the -Y axis."""
        return self.left(chain, -distance, speed, frame)

    def up(self, chain='RArm', distance=0.05, speed=0.3, frame=None):
        """Move end effector up along the +Z axis."""
        if frame is None:
            frame = self.TORSO
        self.nao.env.motion.changePosition(chain, frame, [0, 0, distance, 0, 0, 0], speed, self.POSITION)
        self.log('reach.up: {} {}m'.format(chain, distance))
        return self

    def down(self, chain='RArm', distance=0.05, speed=0.3, frame=None):
        """Move end effector down along the -Z axis."""
        return self.up(chain, -distance, speed, frame)

    ###################################
    # trajectory
    ###################################

    def trace(self, chain, waypoints, duration=4.0, frame=None):
        """Move smoothly through a list of waypoints over the given duration.

        Args:
            chain: Chain name (e.g. 'RArm').
            waypoints: List of [x, y, z] or [x, y, z, wx, wy, wz] positions.
            duration: Total time in seconds for the trajectory.
            frame: Reference frame (default TORSO).
        """
        if frame is None:
            frame = self.TORSO
        current = self.nao.env.motion.getPosition(chain, frame, True)

        path = []
        for wp in waypoints:
            if len(wp) == 3:
                path.append([wp[0], wp[1], wp[2], current[3], current[4], current[5]])
            else:
                path.append(list(wp))

        n = len(path)
        times = [duration * (i + 1) / n for i in range(n)]

        self.nao.env.motion.positionInterpolation(chain, frame, path, self.POSITION, times, True)
        self.log('reach.trace: {} through {} waypoints in {}s'.format(chain, n, duration))
        return self

    def trace_relative(self, chain, deltas, duration=4.0, frame=None):
        """Like trace, but each entry is a delta [dx, dy, dz] from the previous position."""
        if frame is None:
            frame = self.TORSO
        current = self.nao.env.motion.getPosition(chain, frame, True)

        path = []
        cx, cy, cz = current[0], current[1], current[2]
        for d in deltas:
            cx += d[0]
            cy += d[1]
            cz += d[2]
            path.append([cx, cy, cz, current[3], current[4], current[5]])

        n = len(path)
        times = [duration * (i + 1) / n for i in range(n)]

        self.nao.env.motion.positionInterpolation(chain, frame, path, self.POSITION, times, True)
        self.log('reach.trace_relative: {} through {} deltas in {}s'.format(chain, n, duration))
        return self

    ###################################
    # gestures
    ###################################

    def point_at(self, x, y, z, chain='RArm', speed=0.3, frame=None):
        """Extend arm toward a target point, scaled to arm length (~0.22m)."""
        if frame is None:
            frame = self.TORSO
        current = self.nao.env.motion.getPosition(chain, frame, True)

        # direction from shoulder toward target, extend arm
        dx = x - current[0]
        dy = y - current[1]
        dz = z - current[2]
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        if dist < 0.01:
            return self

        # normalize and scale to arm length (~0.22m)
        arm_len = 0.22
        scale = arm_len / dist
        target = [current[0] + dx * scale, current[1] + dy * scale, current[2] + dz * scale,
                  current[3], current[4], current[5]]

        self.nao.env.motion.setPosition(chain, frame, target, speed, self.POSITION)
        self.log('reach.point_at: {} -> ({}, {}, {})'.format(chain, x, y, z))
        return self

    def wave(self, chain='RArm', cycles=2, duration=3.0):
        """Raise hand and wave side to side for the given number of cycles."""
        current = self.position(chain)
        x, y, z = current[0], current[1], current[2]

        # raise hand up first
        up_pos = [x, y, z + 0.15]
        path = [up_pos]
        for i in range(cycles):
            path.append([x, y - 0.08, z + 0.15])
            path.append([x, y + 0.08, z + 0.15])
        path.append(up_pos)

        self.trace(chain, path, duration)
        self.log('reach.wave: {} {} cycles'.format(chain, cycles))
        return self
