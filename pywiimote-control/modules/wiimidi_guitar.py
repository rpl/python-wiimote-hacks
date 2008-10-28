# pywiimote-control: a tiny modular wiimote remote control application
# Copyright (C) 2008 Luca Greco <rpl@salug.it>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import cwiid
import sys
import pypm

OUTPUT = 1
INPUT = 0

CHORD = 40
BASE_NOTE = 40

WIIMOTE_zeroY = 126
WIIMOTE_oneY = 151
NUNCHUK_zeroY = 124
NUNCHUK_oneY = 177

NUNCHUK_accY = 0
offsetY = -37

MidiOut = None

def OpenDevice ():
    """ """
    for loop in range(pypm.CountDevices()):
        interf,name,inp,outp,opened = pypm.GetDeviceInfo(loop)
        print name
        if outp == 1 and name == "ZynAddSubFX":
           print "OK %s" % name
           return pypm.Output(loop,0.0)

def init():
    global MidiOut
    MidiOut = OpenDevice()
    pass

def close ():
    """ """
    global MidiOut
    if MidiOut:        
        del MidiOut
        MidiOut = None
    pass


def PrintDevices(InOrOut):
    for loop in range(pypm.CountDevices()):
        interf,name,inp,outp,opened = pypm.GetDeviceInfo(loop)
        if ((InOrOut == INPUT) & (inp == 1) |
            (InOrOut == OUTPUT) & (outp ==1)):
            print loop, name," ",
            if (inp == 1): print "(input) ",
            else: print "(output) ",
            if (opened == 1): print "(opened)"
            else: print "(unopened)"
    print

def callback(mesg):
    global NUNCHUK_accY, CHORD, BASE_NOTE, MidiOut
    if mesg[0] == cwiid.MESG_BTN:
        if mesg[1] == 4:
            MidiOut.WriteShort(0x80,CHORD,50)
            CHORD = BASE_NOTE
        elif mesg[1] == 8:
            MidiOut.WriteShort(0x80,CHORD,50)
            CHORD = BASE_NOTE+3
        elif mesg[1] == 0x800:
            BASE_NOTE+=1
        elif mesg[1] == 0x400:
            BASE_NOTE-=1
        else:
            MidiOut.WriteShort(0x80,CHORD,50)
            CHORD = BASE_NOTE-3
    elif mesg[0] == cwiid.MESG_NUNCHUK:
        NUNCHUK_accY = mesg[1]['acc'][2]
        value = (NUNCHUK_accY + offsetY - NUNCHUK_zeroY)*0.717514
        if value > 30:
            trigger = 1
            MidiOut.WriteShort(0x80,CHORD,50)
            MidiOut.WriteShort(0x90,CHORD,int(value))
        else:
            MidiOut.WriteShort(0x80,CHORD,50)
