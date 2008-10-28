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

WIIMOTE_chord = 40
NUNCHUK_chord = 40

WIIMOTE_zeroY = 126
WIIMOTE_oneY = 151
NUNCHUK_zeroY = 124
NUNCHUK_oneY = 177

NUNCHUK_accY = 0
WIIMOTE_accY = 0

NUNCHUK_value = 0
WIIMOTE_value = 0

WIIMOTE_offsetY = -17
NUNCHUK_offsetY = -27
triggerA = 0
triggerB = 0
triggerC = 0
triggerZ = 1

MidiOut = None

def OpenDevice ():
    """ """
    for loop in range(pypm.CountDevices()):
        interf,name,inp,outp,opened = pypm.GetDeviceInfo(loop)
        print name
        if outp == 1 and name == "Hydrogen Midi-In":
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
    global MidiOut, WIIMOTE_chord, NUNCHUK_chord, NUNCHUK_value, WIIMOTE_value, NUNCHUK_accY, NUNCHUK_accY, WIIMOTE_accY, WIIMOTE_zeroY, triggerA, triggerB, triggerC, triggerZ
    if mesg[0] == cwiid.MESG_BTN:
        if mesg[1] == cwiid.BTN_A:
            WIIMOTE_chord = WIIMOTE_chord+1
        elif mesg[1] == cwiid.BTN_B:
            WIIMOTE_chord = WIIMOTE_chord-1 
        else:
	    pass

    elif mesg[0] == cwiid.MESG_ACC:
        WIIMOTE_accY = mesg[1][cwiid.Y]
        WIIMOTE_value = (WIIMOTE_accY + WIIMOTE_offsetY - WIIMOTE_zeroY)*2 #*0.717514
        if triggerB == 0 and WIIMOTE_accY > 130 and WIIMOTE_value > 10:
#            print "WIIMOTE: accY %s - value %s" % (WIIMOTE_accY, WIIMOTE_value)
            triggerB = 1
            MidiOut.WriteShort(0x90,WIIMOTE_chord,100) #int(WIIMOTE_value*3))
        elif triggerB and (WIIMOTE_value < 10 or WIIMOTE_accY < 120):
            triggerB = 0
                           
    elif mesg[0] == cwiid.MESG_NUNCHUK:
        NUNCHUK_accY = mesg[1]['acc'][2]
        NUNCHUK_value = (NUNCHUK_accY + NUNCHUK_offsetY - NUNCHUK_zeroY)*0.5  #*0.717514
	if mesg[1]['buttons'] == cwiid.NUNCHUK_BTN_C and not triggerC:
	   triggerC = 1
        elif mesg[1]['buttons'] != cwiid.NUNCHUK_BTN_C and triggerC:
           NUNCHUK_chord = NUNCHUK_chord+1
           triggerC = 0
	elif mesg[1]['buttons'] == cwiid.NUNCHUK_BTN_Z and not triggerZ:
	   triggerZ = 1
        elif mesg[1]['buttons'] != cwiid.NUNCHUK_BTN_Z and triggerZ:
	   NUNCHUK_chord = NUNCHUK_chord-1
           triggerZ = 0


        if triggerA == 0 and NUNCHUK_value > 40 and NUNCHUK_accY > 200:
            triggerA = 1
            MidiOut.WriteShort(0x90,NUNCHUK_chord,100) #int(NUNCHUK_value*3))
#            print "NUNCHUK: accY %s - value %s" % (NUNCHUK_accY, NUNCHUK_value)
        elif NUNCHUK_value < 40:
            triggerA = 0
