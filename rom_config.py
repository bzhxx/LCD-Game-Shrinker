#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" ~LCD Game Shrinker~
default configuration

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

"""
Various parameters for different ROM files
the repository of the original ROM files is composed of:
<rom_name> directory /
		- BackgroundNS.png 	 (mandatory)
		- <rom name>.svg		 (mandatory)
		- binary program 		 (mandatory)
		- melody 			 			 (optional)

> background_file
 This is the background ! BackgroundNS.png.or fanart .png

> segment_file
 This is the SVG file where the segments are defined (.svg)

> program_file
 the raw binary program file

> melody_file
 the raw binary melody file (if it exists)

> border_trim (not used)
 used during the rescaling of artwork to keep or remove the borders
 border_trim=True : remove the border otherwise keep it

> full name
 The name of the generated file at the end

> CPU to emulate
 indicates which CPU need to be emulated
 from MAME source code or .ini files, hh_sm510.cpp
 The follwing values are supported
 CPU_TYPE="SM512__\0"
 CPU_TYPE="SM511__\0"
 CPU_TYPE="SM510__\0"
 CPU_TYPE="SM500__\0"
 CPU_TYPE="SM5A___\0"

> background dimensions (applied on backgroundNS.png)
> screen dimensions (applied on .svg)
> border dimensions (applied on .svg)

 ### Parameters from MAME layout file default.lay
 # <view name="Background Only (No Shadow)">
 background_x=0
 background_y=0
 background_width=1290
 background_height=854

 screen_x=35
 screen_y=17
 screen_width=1221
 screen_height=802

> flag_rendering_lcd_inverted = True or False
graphic rendering (multiply)
 If false (default case)
 by default the background is from the background artwork file
 the background and non_white segment pixels are 'RGB multiply".
 or
 If True ( case "tabletop" or "inverted lcd screen")
 by default the background is black
 if a segment state is ON, the artwork file and the non_black segment pixels are 'RGB multiply".

 > flag_background_jpeg =True or False
 JPEG is used to compress the artwork file.

> jpeg_quality=90
typical values : 80 to 95
The following presets are available by default:
``web_low``, ``web_medium``, ``web_high``, ``web_very_high``, ``web_maximum``,
``low``, ``medium``, ``high``, ``maximum``.

> background_resolution = RGB565
The background image resolution can reduced using this feature.

https://github.com/python-pillow/Pillow/blob/master/src/PIL/JpegPresets.py#L71

> keys/buttons mapping
 keys/buttons mapping can be found in MAME source file (hh_sm510.cpp)
 CPU INPUTS S1..S8, BA, B
 GW 8 BUTTONS used for retro-go: 8 bits
 K4..K1 : 32 bits
 LEFT,RIGHT,UP,DOWN,GAME,SELECT,A,B

> flag_sound
 define how to drive the external sound piezo buzzer
#R1 to piezo FLAG_SOUND_R1_PIEZO
#R2 to piezo FLAG_SOUND_R2_PIEZO
#R1&R2 to piezo FLAG_SOUND_R1R2_PIEZO
#R1(+S1) to piezo FLAG_SOUND_R1S1_PIEZO
#S1(+R1) to piezo FLAG_SOUND_S1R1_PIEZO

"""

# WARNING : this file is used to share the ROM parameters along the building processs
# if you want to customize some of parameters for a specific ROM, it's better to create
# or to modify the corresponding script in the custom directory
#######################################################################################

### You can reduce the ROM size by changing the following parameters:
## flag_segments_resolution_bits
## flag_background_jpeg
## jpeg_quality

## To get the highest resolution
'''
flag_segments_resolution_bits = 4
flag_background_jpeg = False
'''

## To get the lowest ROM file size
'''
flag_segments_resolution_bits = 2
flag_background_jpeg = True
jpeg_quality = 75
'''

## To reduce ROM file size (medium configuration)
'''
flag_segments_resolution_bits = 4
flag_background_jpeg = True
jpeg_quality = 90
'''

# Enable shortcut B+TIME and B+GAME to get TIME and ALARM
shortcut_time_alarm = False

# Customized segments resolution is 8bits(8), 4bits(4) or 2bits(2)
flag_segments_resolution_bits = 4

## Set the 2 following seeting to True to get smaller rom files
# select if the background is JPEG compressed (lossly) or compressed within ROM data as RGB565
flag_background_jpeg = False

# For JPEG compressed
jpeg_quality = 90

# Enable to keep aspect ratio, otherwise the display is full screen
keep_aspect_ratio = False

# Enable to rotate display by 90° clock wise
rotate = False

# you can reduce the background resolution
# 1 no reduction RGB565
# 2 (-1 bit) resolution RGB454
# 4 (-2 bit) resolution RGB343
# 8 (-3 bit) resolution RGB232
RGB565 = 1
RGB454 = 2
RGB343 = 4
RGB232 = 8

background_resolution = RGB565

# Defined the LCD deflicker level
# 0 : filter is disabled
# 1 : medium filtering
# 2 : high fltering
flag_lcd_deflicker_level = 2

# ROM files
background_file = "none"
segments_file = "none"
program_file = "none"
melody_file = "none"

# dual screen
segments_top_file = "none"
segments_bottom_file = "none"
segments_left_file = "none"
segments_right_file = "none"

background_top_file = "none"
background_bottom_file = "none"
background_left_file = "none"
background_right_file = "none"

# dual screen ?
dual_screen_vert = False
dual_screen_hor = False

# error indication
found = False
layout_found = False

# Warum user no custom script
# at least keys are undefined
custom_script_notfound = False

mame_rom_dir = "_"
build_dir = "_"
rom_name = "_"

# MAME constructor structure
mame_year = 0
mame_name = 0
mame_parent = 0
mame_comp = 0
mame_machine = 0
mame_input = 0
mame_class = 0
mame_init = 0
mame_company = 0
mame_fullname = "'unknown game'"
mame_flags = 0

CPU_TYPE = "NOCPU__\0"

# background coords from MAME layout
background_x = 0
background_y = 0
background_width = 0
background_height = 0

# screen coords from MAME layout
screen_x = 0
screen_y = 0
screen_width = 0
screen_height = 0

# use to define the right way to proceed the LCD segments blending
# False : LCD segments are black, by default the background is the artwork.
# True : LCD segments are white, by default the background is black.
flag_rendering_lcd_inverted = False

# Enable drop shadow rendering effect
drop_shadow = False

# Crop the black border of jpeg background to reduce a little bit the jpeg file size
crop_jpeg_background_border = True

# Buttons mapping
# up to 8 columns outputs to address 4 inputs (K1..K4)
# S1..S8 or R1..R4
# 2 independants inputs
# BA,B

BTN_SIZE = 10
BTN_DATA = [0]*BTN_SIZE

# RAM address of the time count
# used to get consistent time emulation
ADD_TIME_HOUR_MSB=0
ADD_TIME_HOUR_LSB=0
ADD_TIME_MIN_MSB=0
ADD_TIME_MIN_LSB=0
ADD_TIME_SEC_MSB=0
ADD_TIME_SEC_LSB=0
ADD_TIME_HOUR_MSB_PM_VALUE=0


###################################################
# Buttons mapping according to the host machine (retro-go)

# left | (up << 1) | (right << 2) | (down << 3) |
# (a << 4) | (b << 5) | (time << 6) | (game << 7) |
BTN_LEFT = 0x1
BTN_UP = 0x2
BTN_RIGHT = 0x4
BTN_DOWN = 0x8
BTN_A = 0x10
BTN_B = 0x20
BTN_TIME = 0x40
BTN_GAME = 0x80

BTN_SHORTCUT_B_TIME = 0x0
BTN_SHORTCUT_B_GAME = 0x0

if shortcut_time_alarm:
  BTN_SHORTCUT_B_TIME = BTN_B + BTN_TIME
  BTN_SHORTCUT_B_GAME = BTN_B + BTN_GAME

# SM5A buttons according to R1..R4
R1 = 0
R2 = 1
R3 = 2
R4 = 3

# SM510 buttons S1..S9
S1 = 0
S2 = 1
S3 = 2
S4 = 3
S5 = 4
S6 = 5
S7 = 6
S8 = 7

# Direct input BA & B
BA = 8
B = 9

# Piezo buzzer output configuration
FLAG_SOUND_R1_PIEZO = 1
FLAG_SOUND_R2_PIEZO = 2
FLAG_SOUND_R1R2_PIEZO = 3
FLAG_SOUND_R1S1_PIEZO = 4
FLAG_SOUND_S1R1_PIEZO = 5

flag_sound = FLAG_SOUND_R1_PIEZO
