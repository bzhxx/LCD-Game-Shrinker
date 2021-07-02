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


import  os
from PIL import Image

import rom_config as rom

rom.layout_found = True
rom.found = True

background_file = 'background.png'
bezel_background_file = 'bezel.png'

background         = Image.open(os.path.join(rom.mame_rom_dir,background_file))
bezel_background = Image.open(os.path.join(rom.mame_rom_dir,bezel_background_file)).resize((background.size))

# create an empty image with ALPHA channel
img_background = Image.new("RGBA", (background.size))
        
# add main background 
img_background = Image.alpha_composite(img_background,background)
        
# add bezel background
img_background = Image.alpha_composite(img_background,bezel_background)

# remove ALPHA channel
img_background=img_background.convert('RGB')
        
# save it
rom.background_file = "composite.png"
img_background_file = os.path.join(rom.mame_rom_dir , rom.background_file)
img_background.save(img_background_file)

rom.mame_fullname='Bride'
rom.mame_parent=""

rom.CPU_TYPE="SM510__\0"

# background coords from MAME layout
rom.background_x=0
rom.background_y=0
rom.background_width=1647
rom.background_height=1080

# screen coords from MAME layout
rom.screen_x=0
rom.screen_y=0
rom.screen_width=1647
rom.screen_height=1080

#use to define the right way to proceed the LCD segments blending
# False : LCD segments are black, by default the background is the artwork.
#True : LCD segments are white, by default the background is black.
rom.flag_rendering_lcd_inverted = False
rom.flag_lcd_deflicker_level = 0

#Enable drop shadow rendering effect
rom.drop_shadow = False

K1=0
K2=0
K3=0
K4=rom.BTN_A
rom.BTN_DATA[rom.S1]=K1 + (K2 << 8) + (K3 << 16) + (K4 << 24)

K1=rom.BTN_RIGHT
K2=0
K3=rom.BTN_LEFT
K4=0
rom.BTN_DATA[rom.S2]=K1 + (K2 << 8) + (K3 << 16) + (K4 << 24)

K2=rom.BTN_B
K4=rom.BTN_TIME
K1=rom.BTN_GAME
K3=rom.BTN_A
rom.BTN_DATA[rom.S3]=K1 + (K2 << 8) + (K3 << 16) + (K4 << 24)
