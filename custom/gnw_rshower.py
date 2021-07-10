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
import custom.dual2single_screen as d2s

# define width and height borders to keep an acceptable ratio
rom.width_border_ratio = 0
rom.height_border_ratio = 10/100

# Input S1
K1 = 0
K2 = 0
K3 = rom.BTN_A
K4 = 0
rom.BTN_DATA[rom.S1] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)

# Input S2
K1 = 0
K2 = rom.BTN_TIME
K3 = rom.BTN_GAME
K4 = 0
rom.BTN_DATA[rom.S2] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)

# Input S3
K1 = rom.BTN_RIGHT
K2 = rom.BTN_UP
K3 = rom.BTN_LEFT
K4 = rom.BTN_DOWN
rom.BTN_DATA[rom.S3] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)

# Backgrounds Only (No Shadow) layout

# x,y offset of Bound
rom.bound_x = 0
rom.bound_y = 0

# information of the 2 different backgrounds
rom.background_width = 2463
rom.background_height = 776

rom.background_topleft_xy = (0, 0)
rom.background_topleft_size = (1214, 776)

rom.background_bottomright_xy = (1249, 0)
rom.background_bottomright_size = (1214, 776)

rom.background_topleft_file = "Screen-LeftNS.png"
rom.background_bottomright_file = "Screen-RightNS.png"

# Segments .svg file position and size
rom.topleft_x = -19
rom.topleft_y = -47
rom.topleft_width = 1280
rom.topleft_height = 855

rom.bottomright_x = 1201
rom.bottomright_y = -65
rom.bottomright_width = 1300
rom.bottomright_height = 853

# convert it to a single screen
d2s.set_single_screen()
