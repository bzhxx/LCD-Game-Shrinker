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
from custom.rotate_screen import rotate_screen
from custom.dual2single_screen import set_single_screen

#Enable the following line to rotate the screen rendering
rom.rotate = True

# Patch address to synchronize TIME with RTC host
rom.ADD_TIME_HOUR_MSB=20
rom.ADD_TIME_HOUR_LSB=21
rom.ADD_TIME_MIN_MSB=22
rom.ADD_TIME_MIN_LSB=23
rom.ADD_TIME_SEC_MSB=24
rom.ADD_TIME_SEC_LSB=25
rom.ADD_TIME_HOUR_MSB_PM_VALUE = 8

# In LCD-Game-Emulator,
# A specific custom keyboard is implemented for "Green House" when screen is rotated.
# It permits to play in rotate view with DPAD only.
# According to the character postion, the Button A is emulated over DPAD keys press.
#                 ~ ~   ~ ~
#                 A B C D E
#                 ~   F   ~
#                  ~  G  ~ 
#                   H I J
#
#In positions :
# A, H : LEFT or UP emulates Button A
# B, D : UP emulates Button A
# E, J : RIGHT or UP emulates Button A
# C,F,G,I :ignore
#
#SM51X series: output to x.y.z, where:
	# x = group a/b/bs/c (0/1/2/3)
	# y = segment 1-16 (0-15)
	# z = common H1-H4 (0-3)

#    CPU RAM display 
#	0X50.. 0X5F : c1..c16 (base=80)
#	0X60.. 0X6F : a1..a16 (base=96)
#	0X70.. 0X7F : b1..b16 (base=112)

# Position: segment      : RAM   MASk
#        A  h1b7  1.6.0    118   0x1
#        B  h1b12 1.11.0   123   0x1
#        C  h1a13 0.12.0   108   0x1
#        D  h1b13 1.12.0   124   0x1
#        E  h1a15 0.14.0   110   0x1
#        F  h3b3  1.2.2    114   0x4
#        G  h2b3  1.2.1    114   0x2
#        H  h1a4  0.3.0     99   0x1
#        I  h1b3  1.2.0    114   0x1
#        J  h1a3  0.2.0     98   0x1

if rom.rotate :

    # define width and height borders to keep an acceptable ratio
    rom.width_border_ratio = 0
    rom.height_border_ratio = 0

    # Input S1
    K1 = 0
    K2 = 0
    K3 = 0
    K4 = rom.BTN_A
    rom.BTN_DATA[rom.S1] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)

    # Input S2
    K1 = rom.BTN_DOWN #rom.BTN_RIGHT
    K2 = rom.BTN_RIGHT #rom.BTN_UP
    K3 = rom.BTN_UP #rom.BTN_LEFT
    K4 = rom.BTN_LEFT #rom.BTN_DOWN
    rom.BTN_DATA[rom.S2] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)

    # Input S3
    K1 = 0
    K2 = rom.BTN_TIME
    K3 = rom.BTN_GAME
    K4 = 0
    rom.BTN_DATA[rom.S3] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)

else :
    rom.width_border_ratio = 10/100
    rom.height_border_ratio = 0
    
    # Input S1
    K1 = 0
    K2 = 0
    K3 = 0
    K4 = rom.BTN_A + rom.BTN_B
    rom.BTN_DATA[rom.S1] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)

    # Input S2
    K1 = rom.BTN_RIGHT
    K2 = rom.BTN_UP
    K3 = rom.BTN_LEFT
    K4 = rom.BTN_DOWN
    rom.BTN_DATA[rom.S2] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)

    # Input S3
    K1 = 0
    K2 = rom.BTN_TIME
    K3 = rom.BTN_GAME
    K4 = 0
    rom.BTN_DATA[rom.S3] = K1 | (K2 << 8) | (K3 << 16) | (K4 << 24)

# convert it to a single screen
set_single_screen()

if rom.rotate:
    rotate_screen()