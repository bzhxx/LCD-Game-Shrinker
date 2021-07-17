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

DEBUG = True


def log(s):
    if DEBUG:
        print(s)


def get_dual_screen_view():

    # screen x,y offset
    # rom.bound_x
    # rom.bound_y

    # backgrounds
    # rom.background_topleft_xy
    # rom.background_bottomright_xy
    # rom.background_topleft_size
    # rom.background_bottomright_size

    # segments
    # rom.topleft_x
    # rom.topleft_y
    # rom.topleft_width
    # rom.topleft_height

    # rom.bottomright_x
    # rom.bottomright_y
    # rom.bottomright_width
    # rom.bottomright_height

    # Get Background and screen dimensions from MAME layout artwork file
    layout_file = os.path.join(rom.mame_rom_dir, 'default.lay')
    tree = lxml.etree.parse(layout_file)
    layout_root = tree.getroot()
    rom.layout_found = False

    # First tentative look for 'background' & 'only' in the name view
    for x in layout_root:
        if str(x.tag) == 'view':
            if (str(x.attrib).upper().find('BACK') > -1) \
                & (str(x.attrib).upper().find('ONLY') > -1) \
                    & (str(x.attrib).upper().find('SHADOW') > -1):

                # look for Screen dimension 'bounds'
                screen_bounds = x.find('bounds')
                rom.bound_x = int(screen_bounds.get('x'))
                rom.bound_y = int(screen_bounds.get('y'))
                rom.background_width = int(screen_bounds.get('width'))
                rom.background_height = int(screen_bounds.get('height'))

                # look for backgrounds dimension
                all_element = x.findall('element')
                for element in all_element:
                    element_bounds = element.find('bounds')

                    background_ref = element.get('ref')

                    if (str(element.attrib).upper().find('TOP') > -1) or \
                       (str(element.attrib).upper().find('LEFT') > -1):
                        rom.background_topleft_xy = (int(element_bounds.get('x')),
                                                     int(element_bounds.get('y')))
                        rom.background_topleft_size = (int(element_bounds.get('width')),
                                                       int(element_bounds.get('height')))
                        if (str(element.attrib).upper().find('PLAST') < 0) and \
                                (str(element.attrib).upper().find('FIX') < 0):
                            rom.background_topleft_file = str(
                                background_ref)+".png"

                    if (str(element.attrib).upper().find('BOTTOM') > -1) or \
                            (str(element.attrib).upper().find('RIGHT') > -1):
                        rom.background_bottomright_xy = (int(element_bounds.get('x')),
                                                         int(element_bounds.get('y')))
                        rom.background_bottomright_size = (int(element_bounds.get('width')),
                                                           int(element_bounds.get('height')))
                        if (str(element.attrib).upper().find('PLAST') < 0) and \
                                (str(element.attrib).upper().find('FIX') < 0):
                            rom.background_bottomright_file = str(
                                background_ref)+".png"

                # look for segments dimension
                all_element = x.findall('screen')
                for element in all_element:
                    element_bounds = element.find('bounds')

                    if (str(element.attrib).upper().find('0') > -1):
                        rom.topleft_x = int(element_bounds.get('x'))
                        rom.topleft_y = int(element_bounds.get('y'))
                        rom.topleft_width = int(element_bounds.get('width'))
                        rom.topleft_height = int(element_bounds.get('height'))

                    if (str(element.attrib).upper().find('1') > -1):
                        rom.bottomright_x = int(element_bounds.get('x'))
                        rom.bottomright_y = int(element_bounds.get('y'))
                        rom.bottomright_width = int(
                            element_bounds.get('width'))
                        rom.bottomright_height = int(
                            element_bounds.get('height'))

#  The follow code is generic for horizontal or vertical dual screen
#  It permits to stick backgrounds and segments according to MAME layout


def set_single_screen():

    get_dual_screen_view()

    # remove the bound x,y offset
    x, y = rom.background_topleft_xy
    rom.background_topleft_xy = (x-rom.bound_x, y-rom.bound_y)

    x, y = rom.background_bottomright_xy
    rom.background_bottomright_xy = (x-rom.bound_x, y-rom.bound_y)

    rom.topleft_x = rom.topleft_x-rom.bound_x
    rom.topleft_y = rom.topleft_y-rom.bound_y

    rom.bottomright_x = rom.bottomright_x-rom.bound_x
    rom.bottomright_y = rom.bottomright_y-rom.bound_y

    # Disable drop shadow rendering effect -TO FIX it failed during inkscape extraction
    rom.drop_shadow = False

    if rom.dual_screen_hor:
        segments_topleft_file = os.path.join(
            rom.mame_rom_dir, rom.segments_left_file)
        segments_bottomright_file = os.path.join(
            rom.mame_rom_dir, rom.segments_right_file)
    else:
        segments_topleft_file = os.path.join(
            rom.mame_rom_dir, rom.segments_top_file)
        segments_bottomright_file = os.path.join(
            rom.mame_rom_dir, rom.segments_bottom_file)

    # Stick bottom and top backgrounds
    #####################################
    background_topleft = PIL.Image.open(os.path.join(
        rom.mame_rom_dir, rom.background_topleft_file))
    background_bottomright = PIL.Image.open(os.path.join(
        rom.mame_rom_dir, rom.background_bottomright_file))

    background_topleft = background_topleft.resize(
        rom.background_topleft_size, PIL.Image.LANCZOS)
    background_bottomright = background_bottomright.resize(
        rom.background_bottomright_size, PIL.Image.LANCZOS)

    # create an empty image
    img_background = PIL.Image.new(
        "RGB", (rom.background_width, rom.background_height))

    img_background.paste(background_topleft, rom.background_topleft_xy)
    img_background.paste(background_bottomright, rom.background_bottomright_xy)

    # save it
    rom.background_file = "composite.png"
    img_background_file = os.path.join(rom.mame_rom_dir, rom.background_file)
    img_background.save(img_background_file)

    # Stick segments
    rom.segments_file = "segments_composite.svg"
    seg_file = os.path.join(rom.mame_rom_dir, rom.segments_file)

    # Get segments from original segments file
    originalSVG_TL = svgutils.compose.SVG(segments_topleft_file)
    originalSVG_BR = svgutils.compose.SVG(segments_bottomright_file)

    tree = lxml.etree.parse(segments_topleft_file,
                            parser=lxml.etree.XMLParser(huge_tree=True))
    svg_root = tree.getroot()
    viewbox = re.split('[ ,\t]+', svg_root.get('viewBox', '').strip())

    viewbox_TL_width = float(viewbox[2])
    viewbox_TL_height = float(viewbox[3])

    tree = lxml.etree.parse(segments_bottomright_file,
                            parser=lxml.etree.XMLParser(huge_tree=True))
    svg_root = tree.getroot()
    viewbox = re.split('[ ,\t]+', svg_root.get('viewBox', '').strip())

    viewbox_BR_width = float(viewbox[2])
    viewbox_BR_height = float(viewbox[3])

    TL_scale_x = rom.topleft_width / viewbox_TL_width
    TL_scale_y = rom.topleft_height / viewbox_TL_height

    BR_scale_x = rom.bottomright_width / viewbox_BR_width
    BR_scale_y = rom.bottomright_height / viewbox_BR_height

    svgutils.compose.Figure(rom.background_width, rom.background_height,
                            svgutils.compose.SVG(segments_topleft_file).scale(
                                TL_scale_x, TL_scale_y).move(rom.topleft_x, rom.topleft_y),
                            svgutils.compose.SVG(segments_bottomright_file).scale(BR_scale_x, BR_scale_y).move(
                                rom.bottomright_x, rom.bottomright_y)
                            ).save(seg_file)

    # Resize and add borders to background
    ############################################################################
    img_prev_background = PIL.Image.open(img_background_file)
    img_new_background = PIL.Image.new(
        "RGB", (rom.background_width, rom.background_height))

    w = rom.background_width
    h = rom.background_height

    w = int(w * (1-(2*rom.width_border_ratio)))
    h = int(h * (1-(2*rom.height_border_ratio)))
    x = int(rom.background_width*rom.width_border_ratio)
    y = int(rom.background_height*rom.height_border_ratio)

    img_prev_background = img_prev_background.resize((w, h), PIL.Image.LANCZOS)

    img_new_background.paste(img_prev_background, (x, y))

    img_new_background.save(img_background_file)

    # Resize and add borders to segments
    ############################################################################
    originalSVG = svgutils.compose.SVG(seg_file)

    tree = lxml.etree.parse(
        seg_file, parser=lxml.etree.XMLParser(huge_tree=True))
    svg_root = tree.getroot()
    viewbox = re.split('[ ,\t]+', svg_root.get('viewBox', '').strip())

    viewbox_width = float(viewbox[2])
    viewbox_height = float(viewbox[3])

    x = viewbox_width * rom.width_border_ratio
    y = viewbox_height * rom.height_border_ratio
    scalex = (1-(2 * rom.width_border_ratio))
    scaley = (1 - (2 * rom.height_border_ratio))

    rom.segments_file = "segments_composite_ratio_fix.svg"
    seg_ratio_fix_file = os.path.join(rom.mame_rom_dir, rom.segments_file)

    svgutils.compose.Figure(rom.background_width, rom.background_height,
                            svgutils.compose.SVG(seg_file).scale(
                                scalex, scaley).move(x, y)
                            ).save(seg_ratio_fix_file)

    # now it's a s single screen !
    rom.dual_screen_vert = False
    rom.dual_screen_hor = False
    rom.layout_found = True

    # set new coords
    rom.background_x = 0
    rom.background_y = 0

    rom.screen_x = 0
    rom.screen_y = 0
    rom.screen_width = rom.background_width
    rom.screen_height = rom.background_height


def dual2single_screen():
    set_single_screen()

