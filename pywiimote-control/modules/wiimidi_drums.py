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

WIIMOTE_zeroZ = 126
WIIMOTE_oneZ = 151
NUNCHUK_zeroZ = 124
NUNCHUK_oneZ = 177

NUNCHUK_accZ = 0
WIIMOTE_accZ = 0

NUNCHUK_value = 0
WIIMOTE_value = 0

WIIMOTE_offsetZ = -27
NUNCHUK_offsetZ = -27
triggerAccNC = 0
triggerAccWM = 0
triggerC = 0
triggerZ = 0

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
    global MidiOut, WIIMOTE_chord, NUNCHUK_chord,\
           NUNCHUK_value, WIIMOTE_value, NUNCHUK_accZ, NUNCHUK_accZ, \
           WIIMOTE_accZ, WIIMOTE_zeroZ, triggerAccNC, triggerAccWM, triggerC, triggerZ
    
    if MidiOut == None:
       return

    if mesg[0] == cwiid.MESG_BTN:
        if mesg[1] == cwiid.BTN_A:
            WIIMOTE_chord = WIIMOTE_chord+1
        elif mesg[1] == cwiid.BTN_B:
            WIIMOTE_chord = WIIMOTE_chord-1 
        else:
	    pass

    elif mesg[0] == cwiid.MESG_ACC:
        WIIMOTE_accZ = mesg[1][cwiid.Z]
        WIIMOTE_value = (WIIMOTE_accZ + WIIMOTE_offsetZ - WIIMOTE_zeroZ)*0.5
        if triggerAccWM == 0 and WIIMOTE_accZ > 200 and WIIMOTE_value > 40:
            #print "WIIMOTE: accZ %s - value %s" % (WIIMOTE_accZ, WIIMOTE_value)
            triggerAccWM = 1
            MidiOut.WriteShort(0x90,WIIMOTE_chord,100) #int(WIIMOTE_value*3))
        elif triggerAccWM and (WIIMOTE_value < 10 or WIIMOTE_accZ < 120):
            triggerAccWM = 0
                           
    elif mesg[0] == cwiid.MESG_NUNCHUK:
        NUNCHUK_accZ = mesg[1]['acc'][cwiid.Z]
        NUNCHUK_value = (NUNCHUK_accZ + NUNCHUK_offsetZ - NUNCHUK_zeroZ)*0.5
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


        if triggerAccNC == 0 and NUNCHUK_value > 40 and NUNCHUK_accZ > 200:
            triggerAccNC = 1
            MidiOut.WriteShort(0x90,NUNCHUK_chord,100) #int(NUNCHUK_value*3))
            #print "NUNCHUK: accZ %s - value %s" % (NUNCHUK_accZ, NUNCHUK_value)
        elif NUNCHUK_value < 40:
            triggerAccNC = 0
