import math
from math import radians
import random
from random import randint
import ast

import bmesh
import mathutils
from mathutils import Vector, Euler

"""
lifted from: http://www.4dsolutions.net/ocn/lsystems.html
"""



class Lturtle:

    import mathutils
    from mathutils import Vector, Euler
    Xvec = Vector((1, 0, 0))
    Yvec = Vector((0, 1, 0))
    Zvec = Vector((0, 0, 1))

    # looking down on YX axis. Z is vertical.

    stackstate = []    # remembers saved state
    delta = 0.2     # angle of rotation
    length = 0.5   # full length of turtle move
    thickness = 0.02  # default thickness of cylinder
    instrudict = {
        '+': 'turnleft',
        '-': 'turnright',
        '&': 'pitchdown',
        '^': 'pitchup',
        '<': 'leftroll',
        '>': 'rightroll',
        '[': 'storeloc_rot',
        ']': 'restoreloc_rot',
        '%': 'roll180',
        '$': 'rollhoriz',
        'x': 'randturn',
        't': 'gravity',
        'F': 'fdraw',
        'f': 'fnodraw',
        'Z': 'halfdraw',
        'z': 'halfnodraw',
        'g': 'Fnorecord',
        '.': 'Nomove'
    }

    stored_states = []
    verts = []
    edges = []

    def __init__(self, vPos=Vector((0, 0, 0))):
        self.vHeading = Vector((0, 0, 1))
        self.vPos = vPos
        self.delta = 0.2

    def chomp(self, instructions):

        getparam = 0
        checkparam = 0
        param = ""

        for item in instructions:

            if getparam:
                if item == ")":
                    getparam = 0  # done getting
                    command = command + "(" + param + ")"
                    eval(command)
                    continue
                else:
                    param = param + item  # building parameter
                    continue

            if checkparam:        # checking for parameter?
                checkparam = 0
                if item == "(":
                    param = ""
                    getparam = 1  # parameter exists
                    continue
                else:
                    command = command + "()"  # no parameter
                    eval(command)

            # initializing command string
            command = "self." + self.instrudict.get(item, 'notHandled')
            checkparam = 1    # set flag

        else:  # dealing with last item
            if checkparam:
                command = command + "()"  # no parameter
                eval(command)

    def add_edge(self):
        i = len(self.verts)
        self.edges.append([i - 2, i - 1])

    def add_verts(self, amp=1):
        self.verts.append(self.vPos[:])
        self.vPos = self.vPos + (self.vHeading * self.length * amp)
        self.verts.append(self.vPos[:])

    def fnodraw(self, n=""):
        self.vPos = self.vPos + self.vHeading * self.length
        print("Forward %s (no draw)" % n)

    def halfnodraw(self, n=""):
        self.vPos = self.vPos + (self.vHeading * self.length * 0.5)
        print("half no draw %s" % n)

    def fdraw(self, n=""):
        self.add_verts()
        self.add_edge()
        print("fdraw %s" % n)

    def halfdraw(self, n=""):
        self.add_verts(amp=0.5)
        self.add_edge()
        print("half draw %s" % n)

    # Turning, Pitch, Roll
    def storeloc_rot(self, n=""):
        self.stored_states.append([self.vPos, self.vHeading])
        print("Store rotation and location %s" % n)

    def restoreloc_rot(self, n=""):
        if len(self.stored_states) > 0:
            self.vPos, self.vHeading = self.stored_states.pop()
            print("Restore rotation and location %s" % n)
        else:
            print('tried restore loc/rot but stored states was empty. you suck :)')

    def do_rotation(self, axis, sign, n=""):
        """ axis 0=x, 1=y, z=2 """
        if n:
            self.delta = float(n)
        components = [0, 0, 0]
        components[axis] = sign * radians(self.delta)
        myEul = Euler(components, 'XYZ')
        self.vHeading.rotate(myEul)

    def turnleft(self, n=""):
        self.do_rotation(1, 2, n)
        print("Turn Left around Z axis %s" % n)

    def turnright(self, n=""):
        self.do_rotation(-1, 2, n)
        print("Turn Right around Z axis %s" % n)

    def pitchdown(self, n=""):
        self.do_rotation(1, 1, n)
        print("Pitch down %s" % n)

    def pitchup(self, n=""):
        self.do_rotation(-1, 1, n)
        print("Pitch up %s" % n)

    def leftroll(self, n=""):
        self.do_rotation(1, 0, n)
        print("left roll %s" % n)

    def rightroll(self, n=""):
        self.do_rotation(-1, 0, n)
        print("right roll %s" % n)

    def turn180(self, n=""):
        self.do_rotation(-1, 2, 180)
        print("turn180 %s" % n)

    def roll180(self, n=""):
        self.do_rotation(1, 0, 180)
        print("roll180 %s" % n)

    def rollhoriz(self, n=""):
        # not exactly sure what this command was intended to do but how
        # about resetting to vertical.
        self.vHeading = Vector((0, 0, 1))
        print("roll horiz %s" % n)

    def randturn(self, n=""):
        ax_x = radians(randint(0, 360))
        ax_y = radians(randint(0, 360))
        ax_z = radians(randint(0, 360))
        myEul = Euler((ax_x, ax_y, ax_z), 'XYZ')
        self.vHeading.rotate(myEul)
        print("randturn %s" % n)

    def gravity(self, n=""):
        print("not handled yet")
        print("gravity %s" % n)

    def Fnorecord(self, n=""):
        print("Fnorecord %s" % n)

    def Nomove(self, n=""):
        print("No move %s" % n)

    def notHandled(self, n=""):
        print("Not handled %s" % n)


def sv_main(t_angle=0.2):
    verts_out = []
    edges_out = []

    in_sockets = [
        ['s', 't_angle', t_angle]
    ]

    def produce(axiom, rules):
        output = ""
        for i in axiom:
            output = output + rules.get(i, i)
        return output


    def iterate(n, axiom, rules):
        if n > 0:
            axiom = produce(axiom, rules)
            return iterate(n - 1, axiom, rules)
        return axiom

    texts = bpy.data.texts
    f = texts['RULES'].as_string()
    rules = {}
    rules = ast.literal_eval(f)
    axiom = 'I'

    m = iterate(5, axiom, rules)
    
    ffff = 'poonjab' in globals()
    
    poonjab = Lturtle()
    poonjab.verts = []
    poonjab.edges = []
    poonjab.chomp(m)
    
    verts_out.extend(poonjab.verts)
    edges_out.extend(poonjab.edges)

    out_sockets = [
        ['v', 'verts', [verts_out]],
        ['s', 'edges', [edges_out]]
    ]

    return in_sockets, out_sockets
