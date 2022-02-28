#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" ~LCD Game Shrinker~
custom rules to apply to the same basename game.
The keys mapping need to be defined. The information can
found in 'hh_sm510.cpp' MAME driver.
More advanced image transformation can be created using this file.

This program permits to shrink MAME high resolution artwork and
 graphics for portable device running LCD game emulator.

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
rom.background_file = "bg.jpg"

K1 = 0
K2 = 0
K3 = rom.BTN_UP
K4 = 0
rom.BTN_DATA[rom.S1] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)

K1 = 0
K2 = rom.BTN_RIGHT
K3 = rom.BTN_LEFT
K4 = 0
rom.BTN_DATA[rom.S2] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)

K1 = 0
K2 = rom.BTN_DOWN
K3 = 0
K4 = 0
rom.BTN_DATA[rom.S3] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)

K1 = rom.BTN_A
K2 = rom.BTN_B
K3 = 0
K4 = 0
rom.BTN_DATA[rom.S4] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)

K1 = rom.BTN_TIME
K2 = 0
K3 = 0
K4 = 0
rom.BTN_DATA[rom.S5] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)

K1 = 0
K2 = 0
K3 = 0
K4 = rom.BTN_GAME
rom.BTN_DATA[rom.S6] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)

"""
static INPUT_PORTS_START( tgaiden )
	PORT_START("IN.0") // S1
	PORT_BIT( 0x04, IP_ACTIVE_HIGH, IPT_JOYSTICK_UP ) PORT_CHANGED_CB(input_changed)
	PORT_BIT( 0x0b, IP_ACTIVE_HIGH, IPT_UNUSED )

	PORT_START("IN.1") // S2
	PORT_BIT( 0x02, IP_ACTIVE_HIGH, IPT_JOYSTICK_RIGHT ) PORT_CHANGED_CB(input_changed)
	PORT_BIT( 0x04, IP_ACTIVE_HIGH, IPT_JOYSTICK_LEFT ) PORT_CHANGED_CB(input_changed)
	PORT_BIT( 0x09, IP_ACTIVE_HIGH, IPT_UNUSED )

	PORT_START("IN.2") // S3
	PORT_BIT( 0x02, IP_ACTIVE_HIGH, IPT_JOYSTICK_DOWN ) PORT_CHANGED_CB(input_changed)
	PORT_BIT( 0x0d, IP_ACTIVE_HIGH, IPT_UNUSED )

	PORT_START("IN.3") // S4
	PORT_BIT( 0x01, IP_ACTIVE_HIGH, IPT_BUTTON1 ) PORT_CHANGED_CB(input_changed) PORT_NAME("Jump")
	PORT_BIT( 0x02, IP_ACTIVE_HIGH, IPT_BUTTON2 ) PORT_CHANGED_CB(input_changed) PORT_NAME("Attack/Pick")
	PORT_BIT( 0x0c, IP_ACTIVE_HIGH, IPT_UNUSED )

	PORT_START("IN.4") // S5
	PORT_BIT( 0x01, IP_ACTIVE_HIGH, IPT_SELECT ) PORT_CHANGED_CB(input_changed) PORT_NAME("Pause")
	PORT_BIT( 0x0e, IP_ACTIVE_HIGH, IPT_UNUSED )

	PORT_START("IN.5") // GND!
	PORT_BIT( 0x07, IP_ACTIVE_HIGH, IPT_UNUSED )
	PORT_BIT( 0x08, IP_ACTIVE_HIGH, IPT_START ) PORT_CHANGED_CB(input_changed) PORT_NAME("Power On/Start")

	PORT_START("BA")
	PORT_BIT( 0x01, IP_ACTIVE_LOW, IPT_VOLUME_DOWN ) PORT_NAME("Sound")

	PORT_START("B")
	PORT_BIT( 0x01, IP_ACTIVE_LOW, IPT_POWER_OFF )

	PORT_START("ACL")
	PORT_BIT( 0x01, IP_ACTIVE_HIGH, IPT_SERVICE1 ) PORT_CHANGED_CB(acl_button) PORT_NAME("ACL")
INPUT_PORTS_END
"""