#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" ~LCD Game Shrinker~

#  The follow code is generic for horizontal or vertical dual screen,
#  It permits to stick backgrounds and segments according to MAME layout.

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
import re
import lxml
import PIL
import svgutils

import rom_config as rom

def adjust_screen():
    # input files : rom.segments_file, rom_background_file inputs
    seg_file = os.path.join(rom.mame_rom_dir, rom.segments_file)
    back_file = os.path.join(rom.mame_rom_dir, rom.background_file)

    # Adjust background and segments
    #Background : Remove alpha layer
    png = PIL.Image.open(back_file).convert('RGBA')
    img_background = PIL.Image.new("RGBA", png.size, (255, 255, 255))

    alpha_composite = PIL.Image.alpha_composite(img_background, png).convert('RGB')

    #Background : resize to MAME layout
    MAME_composite = alpha_composite.resize((rom.background_width,rom.background_height),PIL.Image.LANCZOS)
    MAME_composite.save(back_file)

    #Segments : resize to MAME layout size
    originalSVG = svgutils.compose.SVG(seg_file)

    tree = lxml.etree.parse(seg_file,
                            parser=lxml.etree.XMLParser(huge_tree=True))
    svg_root = tree.getroot()

    viewbox = re.split('[ ,\t]+', svg_root.get('viewBox', '').strip())

    # Get segments size
    viewbox_width = float(viewbox[2])
    viewbox_height = float(viewbox[3])

    # Adjust segments to MAME layout
    # Rescale and Align segments (MAME scale)
    originalSVG.scale(rom.screen_width/viewbox_width,rom.screen_height/viewbox_height)
    originalSVG.moveto(rom.screen_x-rom.background_x,rom.screen_y-rom.background_y)

    # Save to SVG file as an intermediate result
    MAME_figure = svgutils.compose.Figure(rom.background_width,rom.background_height, originalSVG)
    MAME_figure.save(seg_file)

def rotate_screen():

    adjust_screen()

    # input files : rom.segments_file, rom_background_file inputs
    seg_file = os.path.join(rom.mame_rom_dir, rom.segments_file)
    back_file = os.path.join(rom.mame_rom_dir, rom.background_file)

    # Rotate background
    ###########################################
    png = PIL.Image.open(back_file).rotate(270, expand=True)
    png.save(back_file)

    # rotate segments
    ###########################################

    # Create a new figure with rotated segments and save it
    h = rom.background_width
    w = rom.background_height

    svgutils.compose.Figure(w, h, svgutils.compose.SVG(seg_file).rotate(90,0,0).move(w,0)
        ).save(seg_file)

    # Update layout according to rotate
    rom.screen_x = 0
    rom.screen_y = 0
    rom.screen_width = w
    rom.screen_height = h

    rom.background_x =0
    rom.background_y = 0
    rom.background_width = w
    rom.background_height = h

