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

import compiz
import cwiid

def init():
    pass

def close ():
    """ """
    pass

def callback (mesg):
    """ """
    if mesg[0] == cwiid.MESG_BTN:
        if mesg[1] == 0x10:
            compiz.call("wall","prev_key")
        elif mesg[1] == 0x1000:
            compiz.call("wall","next_key")
        elif mesg[1] == 0x2:
            compiz.call("scale","initiate_key")
        elif mesg[1] == 0x1:
            compiz.call("scale","initiate_all_key")

    
