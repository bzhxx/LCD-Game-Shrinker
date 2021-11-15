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
from PIL import Image

import rom_config as rom

# Patch address to synchronize TIME with RTC host
rom.ADD_TIME_HOUR_MSB=64
rom.ADD_TIME_HOUR_LSB=65
rom.ADD_TIME_MIN_MSB=66
rom.ADD_TIME_MIN_LSB=67
rom.ADD_TIME_SEC_MSB=68
rom.ADD_TIME_SEC_LSB=69
rom.ADD_TIME_HOUR_MSB_PM_VALUE = 0

# gradient style
#Mix: background_file + 'bubbles.png' + 'background.png'
main_background_file = 'Background.png'
bubbles_file = 'Bubbles.png'

# experimental drop shadow effect on LCD segments
#rom.drop_shadow = True

score_board = Image.open(os.path.join(rom.mame_rom_dir, rom.background_file))
main_background = Image.open(os.path.join(
    rom.mame_rom_dir, main_background_file)).resize((score_board.size))
bubbles = Image.open(os.path.join(
    rom.mame_rom_dir, bubbles_file)).resize((score_board.size))

# create an empty image
img_background = Image.new("RGBA", score_board.size)

# add main background grey
img_background = Image.alpha_composite(img_background, main_background)

# vermin lines and score board
img_background = Image.alpha_composite(img_background, score_board)

# add bubbles
#img_background = Image.alpha_composite(img_background, bubbles)

# remove ALPHA channel
img_background = img_background.convert('RGB')

# save it
rom.background_file = "composite.png"
img_background_file = os.path.join(rom.mame_rom_dir, rom.background_file)
img_background.save(img_background_file)


# During vermin extermination, the animation is not visible with flag_lcd_deflicker_level = 2
rom.flag_lcd_deflicker_level = 1

# Input R(2)
K1 = 0
K2 = rom.BTN_TIME
K3 = rom.BTN_GAME
K4 = 0

rom.BTN_DATA[rom.R2] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)

rom.BTN_DATA[rom.BA] = rom.BTN_RIGHT + rom.BTN_A
rom.BTN_DATA[rom.B] = rom.BTN_LEFT
