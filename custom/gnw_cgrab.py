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
from PIL import ImageOps
from PIL import ImageChops
from custom.rotate_screen import rotate_screen
import rom_config as rom

rom.keep_aspect_ratio = True
rom.crop_jpeg_background_border = True
background_file = 'Background2.png'

subtract_file = 'Subtract.png'
overlay_file = 'Overlay.png'
lines_file = 'Lines.png'
lines2_file = 'Lines2.png'
frame_file = 'Frame2.png'

rom.overlay_file = 'Overlay.png'

# experimental drop shadow effect on LCD segment
rom.drop_shadow = False
background_file_path = os.path.join(rom.mame_rom_dir, background_file)
if os.path.isfile(background_file_path):

    background = Image.open(background_file_path)
    frame = Image.open(os.path.join(rom.mame_rom_dir, frame_file))
    subtract = Image.open(os.path.join(rom.mame_rom_dir, subtract_file))
    overlay = Image.open(os.path.join(rom.mame_rom_dir, overlay_file))
    lines = Image.open(os.path.join(rom.mame_rom_dir, lines_file))
    lines2 = Image.open(os.path.join(rom.mame_rom_dir, lines2_file))

    #subtract = subtract.resize((background.size))
    #frame = ImageOps.fit(frame,background.size,bleed=0.0,centering=(0.5,0.5))
    #frame = frame.resize((background.size))
#    lines = lines.resize((background.size))

    # create an empty layer to mix images with ALPHA channel
    img_layer = Image.new("RGBA", (background.size))

    # add main background
    img_layer = Image.alpha_composite(img_layer, background)

    # add subtract
    img_layer = ImageChops.multiply(img_layer, subtract)

   # add overlay
    img_layer = ImageChops.add(img_layer, overlay)

    # create an empty image as background with ALPHA channel
    img_background = Image.new("RGBA", (background.size))

    img_background = Image.alpha_composite(img_background, background)
    img_background.paste(img_layer,(0,0), overlay)

    #add lines
    #lines_tmp = Image.new("RGBA", (lines.size))

    img_background.paste(lines,(0,100),lines)
    #img_background = Image.blend(img_background,lines_tmp,0.1)

    #add lines2
    #lines2_tmp = Image.new("RGBA", (background.size))
    img_background.paste(lines2,(0,100),lines2)
    #img_background = Image.blend(img_background,lines2_tmp,0.1)

    #add frames
    img_background.paste(frame,(0,0),frame)

    # remove ALPHA channel
    img_background = img_background.convert('RGB')

    # save it
    rom.background_file = "composite.png"
    img_background_file = os.path.join(rom.mame_rom_dir, rom.background_file)
    img_background.save(img_background_file)


# Patch address to synchronize TIME with RTC host
rom.ADD_TIME_HOUR_MSB=20
rom.ADD_TIME_HOUR_LSB=21
rom.ADD_TIME_MIN_MSB=22
rom.ADD_TIME_MIN_LSB=23
rom.ADD_TIME_SEC_MSB=24
rom.ADD_TIME_SEC_LSB=25
rom.ADD_TIME_HOUR_MSB_PM_VALUE = 8

#Enable the following line to rotate the screen rendering
rom.rotate = True

# Force to use Background with drop shadow
#rom.background_file="Background.png"

# Enable experimental drop shadow effect on LCD segments
#rom.drop_shadow = True

if rom.rotate:
    K1 = rom.BTN_DOWN  # BTN_RIGHT
    K2 = rom.BTN_RIGHT  # BTN_UP
    K3 = rom.BTN_UP  # BTN_LEFT
    K4 = rom.BTN_LEFT  # BTN_DOWN
    rom.BTN_DATA[rom.S1] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)

    rotate_screen()

else:
    K1 = rom.BTN_RIGHT
    K2 = rom.BTN_UP
    K3 = rom.BTN_LEFT
    K4 = rom.BTN_DOWN
    rom.BTN_DATA[rom.S1] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)

K1 = 0
K2 = rom.BTN_TIME
K3 = rom.BTN_GAME
K4 = 0
rom.BTN_DATA[rom.S2] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)
