#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" ~LCD Game Shrinker~
custom rules to apply to the same basename game.
The keys mapping need to be defined. The information can
found in 'hh_sm510.cpp' MAME driver.
More advanced image transformation can be created using this file.

This program permits to shrink MAME high resolution artwork and
 graphics for protable device running LCD game emulator.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""
__author__ = "bzhxx"
__contact__ = "https://github.com/bzhxx"
__license__ = "GPLv3"

import rom_config as rom

#This section describes how to map the keys

"""
The keys function on LCD Games based on Sharp Microcomputer are composed of :
- a keyboard 8x4 keys for SM51X or 4x4 for SM5A
- 2 inputs : B and BA

The keyboard is composed of :
outputs : S1..S8 for SM51X or R1..R4 for SM5A
input   : K1..K4
A keyboard button is implemented as a shorcut function between one S pin and one K pin

The 2 inputs B and BA can also be directly connected to button.
B and BA are pull-up shortcut to ground when the connected key is pressed.

PORT_START() & PORT_BIT():
PORT_START() is used to select the output port (S or R) of the keyboard matrix
PORT_BIT(K_MASK,) is used to select the input port (K) of the keyboard matrix
K_MASK value is a mask indicating which inputs are concerned (K1=0x1, K2=0x2,K3=0x4,K4=0x8)
"""

# Example : Extract from MAME hh_sm510.cpp driver Micro vs System.

""" static INPUT_PORTS_START( microvs_shared )
S1 is selected 	        PORT_START("IN.0") // S1 
K1,K2,K4 unused 	    PORT_BIT( 0x0b, IP_ACTIVE_HIGH, IPT_UNUSED )        
K3=BUTTON1 of PLAYER2	PORT_BIT( 0x04, IP_ACTIVE_HIGH, IPT_BUTTON1 ) PORT_CHANGED_CB(input_changed) PORT_PLAYER(2)
"""

# we don't have player2, so nothing is connected
K1 = 0
K2 = 0
K3 = 0
K4 = 0
rom.BTN_DATA[rom.S1] = K1 + (K2 << 8) + (K3 << 16) + (K4 << 24)

"""
S2 is selected 	        PORT_START("IN.1") // S2
K1=BUTTON1 of PLAYER1	PORT_BIT( 0x01, IP_ACTIVE_HIGH, IPT_BUTTON1 ) PORT_CHANGED_CB(input_changed)
K2,K3,K4 unused     	PORT_BIT( 0x0e, IP_ACTIVE_HIGH, IPT_UNUSED )
"""

# connect A Button to S2.K1
K1 = rom.BTN_A
K2 = 0
K3 = 0
K4 = 0
rom.BTN_DATA[rom.S2] = K1 + (K2 << 8) + (K3 << 16) + (K4 << 24)

"""
	PORT_START("IN.2") // S3
	PORT_BIT( 0x03, IP_ACTIVE_HIGH, IPT_UNUSED )
	PORT_BIT( 0x04, IP_ACTIVE_HIGH, IPT_JOYSTICK_DOWN ) PORT_CHANGED_CB(input_changed) PORT_PLAYER(2)
	PORT_BIT( 0x08, IP_ACTIVE_HIGH, IPT_JOYSTICK_UP ) PORT_CHANGED_CB(input_changed) PORT_PLAYER(2)
"""
# player 2 is not supported
K1 = 0
K2 = 0
K3 = 0
K4 = 0
rom.BTN_DATA[rom.S3] = K1 + (K2 << 8) + (K3 << 16) + (K4 << 24)

"""
	PORT_START("IN.3") // S4
	PORT_BIT( 0x01, IP_ACTIVE_HIGH, IPT_JOYSTICK_DOWN ) PORT_CHANGED_CB(input_changed)
	PORT_BIT( 0x02, IP_ACTIVE_HIGH, IPT_JOYSTICK_UP ) PORT_CHANGED_CB(input_changed)
	PORT_BIT( 0x0c, IP_ACTIVE_HIGH, IPT_UNUSED )
"""
# connect DOWN & UP (player 1)
K1 = rom.BTN_DOWN
K2 = rom.BTN_UP
K3 = 0
K4 = 0
rom.BTN_DATA[rom.S4] = K1 + (K2 << 8) + (K3 << 16) + (K4 << 24)

"""
	PORT_START("IN.4") // S5
	PORT_BIT( 0x03, IP_ACTIVE_HIGH, IPT_UNUSED )
	PORT_BIT( 0x04, IP_ACTIVE_HIGH, IPT_JOYSTICK_RIGHT ) PORT_CHANGED_CB(input_changed) PORT_PLAYER(2)
	PORT_BIT( 0x08, IP_ACTIVE_HIGH, IPT_JOYSTICK_LEFT ) PORT_CHANGED_CB(input_changed) PORT_PLAYER(2)
"""
#  player 2 is not supported
K1 = 0
K2 = 0
K3 = 0
K4 = 0
rom.BTN_DATA[rom.S5] = K1 + (K2 << 8) + (K3 << 16) + (K4 << 24)

"""
	PORT_START("IN.5") // S6
	PORT_BIT( 0x01, IP_ACTIVE_HIGH, IPT_JOYSTICK_RIGHT ) PORT_CHANGED_CB(input_changed)
	PORT_BIT( 0x02, IP_ACTIVE_HIGH, IPT_JOYSTICK_LEFT ) PORT_CHANGED_CB(input_changed)
	PORT_BIT( 0x0c, IP_ACTIVE_HIGH, IPT_UNUSED )
"""
# connect RIGHT & LEFT (player 1)
K1 = rom.BTN_RIGHT
K2 = rom.BTN_LEFT
K3 = 0
K4 = 0
rom.BTN_DATA[rom.S6] = K1 + (K2 << 8) + (K3 << 16) + (K4 << 24)

"""
	PORT_START("IN.6") // S7
	PORT_BIT( 0x01, IP_ACTIVE_HIGH, IPT_SELECT ) PORT_CHANGED_CB(input_changed) PORT_NAME("Time")
	PORT_BIT( 0x02, IP_ACTIVE_HIGH, IPT_START2 ) PORT_CHANGED_CB(input_changed) PORT_NAME("Game B")
	PORT_BIT( 0x04, IP_ACTIVE_HIGH, IPT_START1 ) PORT_CHANGED_CB(input_changed) PORT_NAME("Game A")
	PORT_BIT( 0x08, IP_ACTIVE_HIGH, IPT_SERVICE2 ) PORT_CHANGED_CB(input_changed) PORT_NAME("Alarm")
 """

# Connect only "Game A" as a single player game to "GAME" button
K1 = 0
K2 = 0
K3 = rom.BTN_GAME
K4 = 0
rom.BTN_DATA[rom.S7] = K1 + (K2 << 8) + (K3 << 16) + (K4 << 24)
