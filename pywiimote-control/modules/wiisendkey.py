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
import Xlib
from Xlib.display import Display
from Xlib import X
from Xlib.protocol import event
import time

display = Display()

def init():
    pass

def close ():
    """ """
    pass

def pressKey(keycode):
        Xlib.ext.xtest.fake_input(display,Xlib.X.KeyPress, keycode)
        display.sync()

def releaseKey(keycode):
	Xlib.ext.xtest.fake_input(display,Xlib.X.KeyRelease, keycode)
        display.sync()

def sendKey(keycode):
        print("KEYCODE: %s" % keycode)
        Xlib.ext.xtest.fake_input(display,Xlib.X.KeyPress, keycode)
        #display.sync()
        Xlib.ext.xtest.fake_input(display,Xlib.X.KeyRelease, keycode)
        display.sync() 

def Fullscreen():
	sendKey(95)

def SlideMiniature():
	pressKey(50) #Shift
	sendKey(95) #F11
	releaseKey(50)

def CtrlPageDown():
        pressKey(37) #Shift
        sendKey(105) #F11
        releaseKey(37)

def CtrlPageDown():
        pressKey(37) #Shift
        sendKey(99) #F11
        releaseKey(37)

def ZoomIn():
        pressKey(37)
        sendKey(35)
        releaseKey(37)

def ZoomOut():
        pressKey(37)
        sendKey(61)
        releaseKey(37)

def Home():
	sendKey(110)

def End():
        sendKey(115)

def Enter():
	sendKey(36)

def Up():
        sendKey(111)

def Down():
        sendKey(104)

def Left():
        sendKey(113)

def Right(): 
        sendKey(114)

########################################

def callback(mesg):
    global NUNCHUK_accY, CHORD, BASE_NOTE
    if mesg[0] == cwiid.MESG_BTN:
        print 'Button Report: %.4X' % mesg[1]
        if mesg[1] == cwiid.BTN_UP:
            Up()
        if mesg[1] == cwiid.BTN_B ^ cwiid.BTN_UP: 
            ZoomIn()
        elif mesg[1] == cwiid.BTN_RIGHT:
            Right()
        elif mesg[1] == cwiid.BTN_DOWN:
	    Down()
        elif mesg[1] == cwiid.BTN_B ^ cwiid.BTN_DOWN:
            ZoomOut()
        elif mesg[1] == cwiid.BTN_LEFT:
            Left()
        elif mesg[1] == cwiid.BTN_B ^ cwiid.BTN_LEFT:
            Home()
        elif mesg[1] == cwiid.BTN_B ^ cwiid.BTN_RIGHT:
            End()
        elif mesg[1] == cwiid.BTN_B:
            SlideMiniature()
        elif mesg[1] == cwiid.BTN_A:
            Enter()


