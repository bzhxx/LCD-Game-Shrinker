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

import os
import rom_config as rom
if not os.path.isfile(os.path.join(rom.mame_rom_dir, rom.background_file)):
  rom.background_file = "bg.jpg"
  rom.background_x = -130
  rom.background_y = -111
  rom.background_width = 1770
  rom.background_height = 1349

  rom.screen_x = 0
  rom.screen_y = 0
  rom.screen_width = 1505
  rom.screen_height = 1080

K1 = rom.BTN_LEFT
K2 = rom.BTN_UP
K3 = rom.BTN_DOWN
K4 = rom.BTN_RIGHT
rom.BTN_DATA[rom.S1] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)

K1 = rom.BTN_TIME
K2 = 0
K3 = 0
K4 = rom.BTN_GAME
rom.BTN_DATA[rom.S2] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)

K1 = rom.BTN_B
K2 = rom.BTN_A
K3 = 0
K4 = 0
rom.BTN_DATA[rom.S3] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)
