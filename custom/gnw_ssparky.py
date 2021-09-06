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
from custom.rotate_screen import rotate_screen
import rom_config as rom

rom.keep_aspect_ratio = True

# Patch address to synchronize TIME with RTC host
rom.ADD_TIME_HOUR_MSB=10
rom.ADD_TIME_HOUR_LSB=11
rom.ADD_TIME_MIN_MSB=12
rom.ADD_TIME_MIN_LSB=13
rom.ADD_TIME_SEC_MSB=14
rom.ADD_TIME_SEC_LSB=15
rom.ADD_TIME_HOUR_MSB_PM_VALUE = 8

# Force to use Background with drop shadow
# rom.background_file="Background.png"

# Enable experimental drop shadow effect on LCD segments
#rom.drop_shadow = True

#Enable the following line to rotate the screen rendering
rom.rotate = True

if rom.rotate:

    K1 = rom.BTN_UP
    K2 = rom.BTN_DOWN
    K3 = rom.BTN_A+rom.BTN_RIGHT+rom.BTN_B
    K4 = 0
    rom.BTN_DATA[rom.S1] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)

    rotate_screen()

else:
    K1 = rom.BTN_LEFT
    K2 = rom.BTN_RIGHT
    K3 = rom.BTN_A+rom.BTN_UP+rom.BTN_B
    K4 = 0
    rom.BTN_DATA[rom.S1] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)

K1 = 0
K2 = rom.BTN_TIME
K3 = rom.BTN_GAME
K4 = 0
rom.BTN_DATA[rom.S2] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)
