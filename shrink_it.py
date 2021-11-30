#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" ~LCD Game Shrinker~
main script.

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

import sys, os, subprocess
from pathlib import Path
import re, lxml
from struct import pack
from PIL import Image,ImageChops

import importlib

import svgutils
import zipfile
import zlib
import lz4.frame as lz4
from pyunpack import Archive
import numpy as np

#ROM default defintion & parser
import rom_config as rom
import rom_parser

artwork_rpath="../artwork/"
output_dir   ="./output/"

DEBUG = False


# select if the ROM data are compressed with ZLIB, LZ4 or LZMA
LZ4_COMPRESSOR =1
ZLIB_COMPRESSOR=2
LZMA_COMPRESSOR=3

COMPRESS_WITH = LZ4_COMPRESSOR
#COMPRESS_WITH = LZMA_COMPRESSOR

#G&W LCD resolution
gw_width=320
gw_height=240

def log(s):
  if DEBUG:
    print (s)

def warm(s):
    print ( " WARNING:"+s +' ['+str(rom_name) +']')

def error(s):
    print (" ERROR:"+s +' [' +str(rom_name) +']')
    exit()

#try to locate tools
inkscape_path = os.environ["INKSCAPE_PATH"] if "INKSCAPE_PATH" in os.environ else "inkscape"

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', length = 20, fill = "▆"):
  """
  Call in a loop to create terminal progress bar
  @params:
    iteration  - Required : current iteration (Int)
    total    - Required : total iterations (Int)
    prefix   - Optional : prefix string (Str)
    suffix   - Optional : suffix string (Str)
    length   - Optional : character length of bar (Int)
    fill    - Optional : bar fill character (Str)
  """
  filledLength = int(length * iteration // total)
  bar = fill * filledLength + '-' * (length - filledLength)

  if not DEBUG:
    sys.stdout.write('\r'+prefix+'|'+bar+'| '+str(iteration)+"/"+str(total)+' '+suffix)
    sys.stdout.flush()

def osmkdir (path):
  if not os.path.isdir(path):
    os.mkdir(path)

if len(sys.argv) < 2:
 rom_file  = "./input/rom/"
else:
  rom_file  = sys.argv[1]

rom_path = os.path.dirname(rom_file)
rom_name = os.path.splitext(os.path.basename(rom_file))[0]

#checks args :if path is a directory process all files
if os.path.isdir(rom_file) :
  ## get all files with .zip extension
  ## call this script for each file
  for x in os.listdir(rom_file) :
    if x.endswith(".zip") or x.endswith(".7z"):
      os.system(sys.executable +" "+ sys.argv[0] + ' ' + os.path.join(rom_path, str(x)))
  exit()

printProgressBar(0, 1, prefix = rom_name.ljust(25), suffix = 'Unzip')

artwork_path=os.path.join(rom_path,artwork_rpath)
artwork_file=os.path.join(artwork_path,rom_name+".zip")

# Create directories to build things
built_root = os.path.join('.',"build")
preview_root = os.path.join('.',"preview")
title_image_root = os.path.join('.',"title")
rom.build_dir =os.path.join(built_root,rom_name)
rom.mame_rom_dir = os.path.join(rom.build_dir ,"original")

osmkdir(built_root)
osmkdir(preview_root)
osmkdir(title_image_root)
osmkdir(rom.build_dir)
osmkdir(rom.mame_rom_dir)

# Output dir : create it for generated ROM file(s)
osmkdir(output_dir)

#unzip original rom
if rom_file.endswith(".zip"):
    with zipfile.ZipFile(rom_file, 'r') as zip_ref:
        zip_ref.extractall(rom.mame_rom_dir)
elif rom_file.endswith(".7z"):
    Archive(rom_file).extractall(rom.mame_rom_dir)
else:
    raise ValueError(f"Unknown extension for rom {rom_file}")

#unzip Artwork
if os.path.isfile(artwork_file) :
  with zipfile.ZipFile(artwork_file, 'r') as zip_ref:
    zip_ref.extractall(rom.mame_rom_dir)
else:
  error('No Artwork ? '+str(artwork_file))

rom_parser.set_parameters(rom_name, rom.mame_rom_dir)

if not rom.found :
    printProgressBar(1, 1, prefix = rom_name.ljust(25), suffix = 'Failed ( unknown )')
    print("")
    exit()

#need some files from a rom parent ?
parent_file=rom_path+'/'+rom.mame_parent.strip()+'.zip'
if os.path.isfile(parent_file) :
  log('parent found:'+parent_file)

  with zipfile.ZipFile(parent_file, 'r') as zip_ref:
    zip_ref.extractall(rom.mame_rom_dir)

  rom_parser.set_parameters(rom_name, rom.mame_rom_dir)

parent_file=rom_path+'/'+rom.mame_parent.strip()+'.7z'
if os.path.isfile(parent_file) :
  log('parent found:'+parent_file)

  Archive(parent_file).extractall(rom.mame_rom_dir)

  rom_parser.set_parameters(rom_name, rom.mame_rom_dir)

if rom.mame_fullname == "'unknown game'":
  error("There is no entry for this game")

log(str(rom.mame_fullname))

if rom.dual_screen_vert or rom.dual_screen_hor:
  error('Dual screen not supported')

background_file = os.path.join(rom.mame_rom_dir,rom.background_file)
segments_file = os.path.join(rom.mame_rom_dir,rom.segments_file)
program_file = os.path.join(rom.mame_rom_dir,rom.program_file)
melody_file = os.path.join(rom.mame_rom_dir,rom.melody_file)

### output files

#svg files
seg_file = os.path.join(rom.build_dir,"segments.svg")
seg_shadow_file = os.path.join(rom.build_dir,"segments_shadow.svg")
MAME_seg_file = os.path.join(rom.build_dir,"MAME_segments.svg")

#background png files
back_file = os.path.join(rom.build_dir,"background.png")
MAME_back_file = os.path.join(rom.build_dir,"MAME_background.png")

jpeg_background = os.path.join(rom.build_dir,"gnw_background.jpg")
# intermediate ROM file (raw / uncompressed)
# without JPEG background
# with or without 565 16bits background

rom_filename = os.path.join(rom.build_dir, rom_name+".gw")

# Final ROM file (compressed)
final_rom_filename = os.path.join(output_dir,str(rom.mame_fullname+".gw"))

### Files to build
BGD_FILE = os.path.join(rom.build_dir,"gnw_background")
SGD_FILE = os.path.join(rom.build_dir,"gnw_segments")
SGD_FILE_4BITS = os.path.join(rom.build_dir, "gnw_segments_4bits")
SGD_FILE_2BITS = os.path.join(rom.build_dir, "gnw_segments_2bits")
SGO_FILE = os.path.join(rom.build_dir,"gnw_segments_offset")
SGX_FILE = os.path.join(rom.build_dir,"gnw_segments_x")
SGY_FILE = os.path.join(rom.build_dir,"gnw_segments_y")
SGH_FILE = os.path.join(rom.build_dir,"gnw_segments_height")
SGW_FILE= os.path.join(rom.build_dir,"gnw_segments_width")
MLD_FILE = melody_file
PGM_FILE= program_file
BTN_FILE = os.path.join(rom.build_dir,"gnw_buttons")

### Adapt Artwork background to target
######################################################################################

bar_prefix=(rom.mame_fullname).split(": ",1)[-1].split(" (",1)[0]

if rom.custom_script_notfound :
    bar_prefix=bar_prefix+'*'

bar_prefix=bar_prefix.ljust(25)
printProgressBar(1, 3, prefix = bar_prefix, suffix = 'Shrink artwork  ')

# check if it exists
background_file =os.path.join(rom.mame_rom_dir, rom.background_file)

if os.path.isfile(background_file) :

  #Remove alpha layer
  png = Image.open(background_file).convert('RGBA')
  img_background = Image.new("RGBA", png.size, (255, 255, 255))

  alpha_composite = Image.alpha_composite(img_background, png).convert('RGB')

  #resize to MAME
  MAME_composite = alpha_composite.resize((rom.background_width,rom.background_height),Image.LANCZOS)
  MAME_composite.save(MAME_back_file)

  # resize to target keeping aspect ratio or full screen

  if rom.keep_aspect_ratio:
    scale_x = float(gw_width) / float(rom.background_width)
    scale_y = float(gw_height) / float(rom.background_height)

    # select the factor and position x,y
    if scale_x < scale_y:
      bgnd_width = gw_width
      bgnd_height= int(scale_x * float(rom.background_height))
      mov_x = 0
      mov_y = int((gw_height - bgnd_height)/2)

    else:
      bgnd_width = int(scale_y * float(rom.background_width))
      bgnd_height= gw_height

      mov_y = 0
      mov_x = int((gw_width - bgnd_width)/2)

    alpha_composite = alpha_composite.resize((bgnd_width,bgnd_height),Image.LANCZOS)

    img_jpeg_background=alpha_composite.copy()

    # Create background data section in RGB565
    tmp_new_background = Image.new(mode="RGB", size=(gw_width, gw_height),color=(0,0,0))

    tmp_new_background.paste(alpha_composite, (mov_x, mov_y))

    tmp_new_background.save(back_file)
    alpha_composite = Image.open(back_file).convert('RGB')

  else:
    alpha_composite = alpha_composite.resize((gw_width,gw_height),Image.LANCZOS)

    alpha_composite.save(back_file)

    img_jpeg_background=alpha_composite.copy()

## Create JPEG background ###
######################################################################################
## remove black borders to reduce the file size ##
  #get black pixels boolean

  if rom.crop_jpeg_background_border :
    image_mask = np.array(img_jpeg_background) != (0.,0.,0.)
    image_mask=image_mask[:,:,1]
    width, height = img_jpeg_background.size
    mask0,mask1=image_mask.any(0),image_mask.any(1)
    x0,x1=mask0.argmax(),width-mask0[::-1].argmax()
    y0,y1=mask1.argmax(),height-mask1[::-1].argmax()

    # crop right and bottom borders
    bbox=(x0,y0,x1,y1)

    img_jpeg_background = img_jpeg_background.crop(bbox)

    # Create background data section in JPEG
  img_jpeg_background.save(jpeg_background, optimize=True, quality=rom.jpeg_quality )


  # Create background data section in 16bits reduced space color
  pixels = list(alpha_composite.getdata())

## Create RGB background ###
######################################################################################

  with open(BGD_FILE, 'wb') as f:
    for pix in pixels:

      # round MSB according to LSB value
      r_pix = rom.background_resolution*8*int(round(float(pix[0]) / (rom.background_resolution*8.0)))
      g_pix = rom.background_resolution*4*int(round(float(pix[1]) / (rom.background_resolution*4.0)))
      b_pix = rom.background_resolution*8*int(round(float(pix[2]) / (rom.background_resolution*8.0)))

      # check saturation
      if r_pix > 255 : r_pix=255
      if g_pix > 255 : g_pix=255
      if b_pix > 255 : b_pix=255

      # RGB888 to RGB565 : drop LSB
      r = (r_pix >> 3) & 0x1F
      g = (g_pix >> 2) & 0x3F
      b = (b_pix >> 3) & 0x1F

      f.write(pack('H', (r << 11) + (g << 5) + b))

else:
  # warm user
  warm('No background found')

if not os.path.isfile(segments_file):
  #Error there is no .svg file
    error('No segment file ('+segments_file+')')

if not os.path.isfile(program_file):
  #Error, there is no program file
  error('No program_file ('+program_file+')')

### Adapt segments file to target
printProgressBar(1, 3, prefix = bar_prefix, suffix = 'Load segments  ')

#Get segments from original segments file
svg        = svgutils.transform.fromfile(segments_file)
originalSVG = svgutils.compose.SVG(segments_file)
tree       = lxml.etree.parse(segments_file, parser=lxml.etree.XMLParser(huge_tree=True))

svg_root = tree.getroot()
viewbox = re.split('[ ,\t]+', svg_root.get('viewBox', '').strip())

viewbox_width=float(viewbox[2])
viewbox_height=float(viewbox[3])

log("View box width:"+str(float(viewbox_width)))

log("View box height:"+str(float(viewbox_height)))


### Adapt Original graphic files to target screen size

# Rescale and Align segments (MAME scale)
originalSVG.scale(rom.screen_width/viewbox_width,rom.screen_height/viewbox_height)
originalSVG.moveto(rom.screen_x-rom.background_x,rom.screen_y-rom.background_y)

# Save to SVG file as an intermediate result
MAME_figure = svgutils.compose.Figure(rom.background_width,rom.background_height, originalSVG)
MAME_figure.save(MAME_seg_file)

## Rescale the Segments file to LCD Game&Watch scale
#Get segments from original segments file
### Adapt segments file to target
printProgressBar(2, 3, prefix = bar_prefix, suffix = 'Shrink segments', length = 20)
svg = svgutils.transform.fromfile(MAME_seg_file)
tree = lxml.etree.parse(MAME_seg_file, parser=lxml.etree.XMLParser(huge_tree=True))

svg_root = tree.getroot()
viewbox = re.split('[ ,\t]+', svg_root.get('viewBox', '').strip())

viewbox_width = float(viewbox[2])
viewbox_height = float(viewbox[3])

# keep aspect ratio or full screen
originalSVG = svgutils.compose.SVG(MAME_seg_file)

if rom.keep_aspect_ratio:
  scale_x = float(gw_width) / viewbox_width
  scale_y = float(gw_height) / viewbox_height

  # select the factor and postion x,y
  if scale_x < scale_y:
    scale = scale_x
    mov_x = 0
    mov_y = (gw_height - (scale * viewbox_height))/2

  else:
    scale = scale_y
    mov_x = (gw_width - (scale * viewbox_width))/2
    mov_y = 0

  # reshape the figure
  originalSVG.scale(scale, scale).move(mov_x, mov_y)

else:
  originalSVG.scale(gw_width/viewbox_width,gw_height/viewbox_height)

figure = svgutils.compose.Figure(gw_width,gw_height, originalSVG)
figure.save(seg_file)

### Generate drop shadow LCD segments file (experimental)
# need to improve this and to add user paremeters for dx,dy,stDeviation and flood-opacity.

# filter definition for drop shadow effect
filter_def = """
  <defs id="bzhxx_drop_shadow_fx">
  <filter id="filter_drop_shadow" x="0" y="0" width="200%" height="200%">
   <feFlood flood-opacity="0.4" flood-color="rgb(0,0,0)" result="flood" id="feFlood1" />
   <feComposite in="SourceGraphic" in2="flood" operator="in" result="composite1" id="feComposite1" />
   <feGaussianBlur in="composite1" stdDeviation="6" result="blur" id="feGaussianBlur1" />
   <feOffset dx="30" dy="30" result="offset" id="feOffset1" />
   <feComposite in="SourceGraphic" in2="offset" operator="over" result="composite2" id="feComposite2" />
  </filter>
 </defs>
"""
filter2_def = """
  <defs id="bzhxx_drop_shadow_fx2">
    <filter id="filter2_drop_shadow" x="0" y="0" width="200%" height="200%">
      <feFlood id="feFlood12" flood-opacity="0.4" result="result1" />
      <feComposite in2="result1" id="feComposite12" in="SourceGraphic" result="composite11" operator="in" />
      <feGaussianBlur in="composite11" stdDeviation="6" result="blur12" id="feGaussianBlur12" />
      <feOffset dx="30" dy="30" id="feOffset12" result="result3" preserveAlpha="false" />
      <feComposite in2="SourceGraphic" id="feComposite13" in="result3" operator="out" result="result4" />
      <feComposite in2="SourceGraphic" id="feComposite14" in="result4" />
  </filter>
 </defs>
"""

# TODO: need to improve this to cover more cases
search_string ="fill:#000000;fill-opacity:0.8"
nofilter_string ="fill:#000000;fill-opacity:0.84705883"
nofilter_string2="fill:#000000;fill-opacity:0.84705882"
filter_string = "fill:#000000;fill-opacity:0.84705883;filter:url(#filter_drop_shadow)"

svg_found = False
filter_notinjected = True

with open(seg_file,"r") as input_file :
  with open(seg_shadow_file,"w") as output_file:
    while True:
      content=input_file.readline()

      if not content:
        break
      if '<g' in content:
        svg_found = True
      if '>' in content and svg_found and filter_notinjected:
        output_file.write(filter_def)
        filter_notinjected = False

      if search_string in content:
        content=content.replace(nofilter_string,filter_string)
        content=content.replace(nofilter_string2,filter_string)

        output_file.write(content)
      else:
        output_file.write(content)

###################################################################################################
### Create a preview of the final rendering
###################################################################################################
#Change the svg source file if drop_shadow filter feature is enabled
if (rom.drop_shadow ) and (not rom.flag_rendering_lcd_inverted):
  seg_preview_file = seg_shadow_file
else:
  seg_preview_file = seg_file

preview_file = os.path.join(preview_root,rom.mame_fullname.replace(":","")+".png")
title_image_file = os.path.join(title_image_root,rom.mame_fullname.replace(":","")+".png")
seg_png_file = os.path.join(rom.build_dir,rom.name+".png")

if rom.flag_rendering_lcd_inverted:
  cmd =  " "+seg_preview_file+" --export-type=png --export-overwrite"+ " --export-background=#000000 --export-background-opacity=1"+" --export-type=png"+" -o "+seg_png_file
else:
  cmd =  " "+seg_preview_file+" --export-type=png --export-overwrite"+ " --export-background=#FFFFFF --export-background-opacity=1"+" --export-type=png"+" -o "+seg_png_file

cmd = inkscape_path+cmd
inkscape_output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL,shell=True)
log(inkscape_output)


#mix background and segment to get a preview
background_preview = Image.open(back_file).convert('RGB')
segment_preview = Image.open(seg_png_file).convert('RGB').resize((background_preview.size))
preview = Image.new("RGB", (background_preview.size))
preview  = ImageChops.multiply(background_preview, segment_preview)
# copy the generated preview to make just the title image
title_image = preview.copy().resize((128,96))

unit= Image.open("./custom/unit_x206y99.png").convert('RGB')
unit.paste(preview,(206,99))

# save it
unit.save(preview_file)

if rom.rotate:
    unit = Image.open(preview_file).rotate(90, expand=True)
    unit.save(preview_file)

# save title image
title_image.save(title_image_file)

###################################################################################################
### open/save svg file using Inkscape (workaround to fix modification applied on path name by Inkscape)
###################################################################################################
seg_file_fix =os.path.join(rom.build_dir,"segments_fix.svg")
cmd = " "+ seg_file + " --query-all"+" --export-overwrite --export-type=svg" + " -o " + seg_file_fix
cmd = inkscape_path + cmd

log(cmd)

inkscape_output=subprocess.check_output(cmd,stderr=subprocess.DEVNULL,shell=True)
log(inkscape_output)

seg_file = seg_file_fix

#####
if (rom.drop_shadow ) and (not rom.flag_rendering_lcd_inverted):
    seg_shadow_file_fix =os.path.join(rom.build_dir,"segments_shadow_fix.svg")
    cmd = " "+ seg_shadow_file + " --query-all"+" --export-overwrite --export-type=svg" + " -o " + seg_shadow_file_fix
    cmd = inkscape_path + cmd

    log(cmd)

    inkscape_output=subprocess.check_output(cmd,stderr=subprocess.DEVNULL,shell=True)
    log(inkscape_output)

    seg_shadow_file = seg_shadow_file_fix

###################################################################################################
## parse all the objects in the svg file and keep only relevant ones
###################################################################################################

# object dimensions index : returned by Inkscape query
ID=0
X=1
Y=2
WIDTH=3
HEIGHT=4

# defines the maximum number of segments
NB_SEGMENTS=256

# depending on the CPU,
# the segment position is determined like this:

# for SM510 series: output to x.y.z, where:
			# x = group a/b/bs/c (0/1/2/3)
			# y = segment 1-16 (0-15)
			# z = common H1-H4 (0-3)
  #segment position  = 64*x + 4*y + z

# For SM500 series: output to x.y.z, where:
			# x = O group (0-*)
			# y = O segment 1-4 (0-3)
			# z = common H1/H2 (0/1)
  #segment position = 8*x + 2*y + z

# Init all tables
tab_x = [0]*NB_SEGMENTS
tab_y = [0]*NB_SEGMENTS
tab_offset = [0]*NB_SEGMENTS
tab_width = [0]*NB_SEGMENTS
tab_height = [0]*NB_SEGMENTS
tab_id = [0]*NB_SEGMENTS

#clean up the segments data file(s)
wr = open(SGD_FILE, 'w')
wr.close()

wr = open(SGD_FILE_4BITS, 'w')
wr.close()

wr = open(SGD_FILE_2BITS, 'w')
wr.close()

#Get all objects from svg file using Inkscape
#it's important to extract x,y coordinates from 'no shadow' segment file
#because injecting drop shadow effect change original coordinates
objects_all = subprocess.check_output([inkscape_path, "--query-all",seg_file],stderr=subprocess.DEVNULL)
log(objects_all)

# get XML from .svg file
svg = svgutils.transform.fromfile(seg_file)

#Init progress bar
bar_total=len(objects_all.splitlines())
bar_progress=0

## parse all the objects in the svg file and keep only relevant ones
for obj in objects_all.splitlines():

  # Index of the object in svg file
  obj_id = obj.split(b',')[0].decode('utf-8') #keep only ID:
  obj_pos_start = 0
  obj_title_found = False

  bar_progress=bar_progress+1
  printProgressBar(bar_progress, bar_total, prefix = bar_prefix, suffix = 'Parse segments  ')

  try:
    obj_xml = svg.find_id(obj_id)
  except:
    pass
    log("object not found:"+obj_id)
  else:
    obj_xmlstr = obj_xml.tostr()

    search_title = obj_xmlstr.find(b"id=\"title")
    nb_title = obj_xmlstr.count(b"id=\"title")

    # title found and only one object id
    if (search_title > -1) and (nb_title == 1) :
      obj_title_found = True
      log("OBJ>" + obj_id)

      #get the title x.y.z
      segment_xyz=re.findall(br">([^]]*)</title",obj_xmlstr[search_title:])[0]

      #get the description field (segment name)
      search_desc = obj_xmlstr.find(b'<desc id=')
      segment = "seg"
      if search_desc > -1:
        segment = re.findall(br'>([^]]*)</desc',obj_xmlstr[search_desc:])[0]
        segment = segment.split(b'<')[0]

      seg_xyz_txt = segment_xyz.split(b'<')[0]

      seg_xyz = seg_xyz_txt.split(b'.')

      x= int(seg_xyz[0] )
      y= int(seg_xyz[1] )
      z= int(seg_xyz[2] )

      # SM510 64*x + 4*y + z
      # SM500 8*x + 2*y + z

      # format is SM510 family (default)
      seg_pos = 64*x + 4*y + z

      # format is SM500 family
      if rom.CPU_TYPE == "SM5A___\0":
        seg_pos = 8*x + 2*y + z
      # format is SM510 family (default)
      else:
        seg_pos = 64*x + 4*y + z

      log("Segment:"+str(segment)+"|"+str(seg_xyz_txt)+",x="+str(x)+",y="+str(y)+",z="+str(z)+"@"+str(seg_pos))

    if obj_title_found :

      #Object position x,y
      obj_x = obj.split(b',')[X]
      obj_y = obj.split(b',')[Y]

      x = int((float(obj_x.replace(b',',b'.'))))
      y = int((float(obj_y.replace(b',',b'.'))))

      tab_x[seg_pos] = x
      tab_y[seg_pos] = y

     #  tab_width[seg_pos] = width
     #  tab_height[seg_pos] = height

      tab_id[seg_pos] = obj_id

###################################################################################################
### Extract all segments
###################################################################################################
#Change the svg source file if drop_shadow filter feature is enabled
if (rom.drop_shadow ) and (not rom.flag_rendering_lcd_inverted):
  seg_file = seg_shadow_file

# if it's 'table top' or 'LCD reverse', the background shall be black and segments are white
# otherwise, the background is white and the segments are black

list_obj = [i for i in tab_id if i != 0]
obj_to_extract = ';'.join(list_obj)

if os.name == 'posix':
    obj_to_extract ="\'" + obj_to_extract + "\'"

if rom.flag_rendering_lcd_inverted:
  cmd = " "+seg_file+" -i "+obj_to_extract+" -j" + " --export-overwrite --export-area-snap" + " --export-background=#000000"+" --export-type=png"
else:
  cmd = " "+seg_file+" -i "+obj_to_extract+" -j" + " --export-overwrite --export-area-snap" + " --export-background=#FFFFFF"+" --export-type=png"

cmd= inkscape_path + cmd

log(cmd)

inkscape_output=subprocess.check_output(cmd,stderr=subprocess.DEVNULL,shell=True)
log(inkscape_output)

bar_total=NB_SEGMENTS
bar_progress=0

#fix all segments and get dimensions
for seg_pos in range(NB_SEGMENTS):

  bar_progress=bar_progress+1
  printProgressBar(bar_progress, bar_total, prefix = bar_prefix, suffix = 'Extract segments')

  if tab_id[seg_pos] == 0:
    continue

  PNG_FILE_PREFIX= os.path.splitext(os.path.basename(seg_file))[0]
  PNG_FILE = os.path.join(rom.build_dir,PNG_FILE_PREFIX +"_"+ tab_id[seg_pos]+".png")

  png = Image.open(PNG_FILE).convert('RGBA')
  img_seg = Image.new("RGBA", png.size, (255, 255, 255))
  image = Image.alpha_composite(img_seg, png).convert('RGB')

  #crop left and bottom borders due drop shadow region extension
  if rom.drop_shadow and not(rom.flag_rendering_lcd_inverted) :

    #get white pixels boolean
    image_mask = np.array(image) != (255.,255.,255.)
    image_mask=image_mask[:,:,1]

    width, height = image.size
    mask0,mask1=image_mask.any(0),image_mask.any(1)
    x0,x1=mask0.argmax(),width-mask0[::-1].argmax()
    y0,y1=mask1.argmax(),height-mask1[::-1].argmax()

    # crop right and bottom borders
    bbox=(x0,y0,x1,y1)
    image = image.crop(bbox)

  #get the image size and coords
  width, height = image.size
  x = tab_x[seg_pos]
  y = tab_y[seg_pos]

  ## oversize check & fix

  # check if we need to crop (error in Artwork or Bug in this rom builder)
  # format of .crop() is image = image.crop((left, top, right, bottom))

  if x+width > gw_width:
    #crop right side by x+width - gw_width
    image = image.crop((0, 0, gw_width -x ,height))
    width, height = image.size

  if y+height > gw_height:
    #crop upper side by y+height - gw_height
    image = image.crop((0, 0, width, gw_height -y))
    width, height = image.size

  ## negative x,y check
  if x < 0:
    # crop right side by x
    image = image.crop((-x, 0, width, height))
    width, height = image.size
    x=0

  if y < 0:
    # crop right side by y
    image = image.crop((0, -y, width, height))
    width, height = image.size
    y=0

  image.save(PNG_FILE,"PNG")
  image.close()

  #restore dims and coords
  tab_x[seg_pos]=x
  tab_y[seg_pos]=y

  tab_width[seg_pos]=width
  tab_height[seg_pos]=height

  tab_offset[seg_pos]=os.path.getsize(SGD_FILE)

  ###### Use PIL to get segments in 8bits
  #open and merge ARGB
  #keep 1 colour

  png = Image.open(PNG_FILE).convert('RGBA')
  img_seg = Image.new("RGBA", png.size, (255, 255, 255))
  img_composite = Image.alpha_composite(img_seg, png).convert('RGB')

  with open(SGD_FILE, 'rb+') as file:
    #Go to the end of file
    file.seek(0,2)
    seg_value_8bits = bytearray((img_composite.getdata(band=1)))

    file.write(seg_value_8bits)

## Padding to 16 bits aligned in case of we need to consider 4 bits resolution
rd_modulo     = os.path.getsize(SGD_FILE) % 2

if rd_modulo != 0:
  with open(SGD_FILE, 'rb+') as file:
    file.seek(0,2)
    file.write(pack("c", b'P'))

##### Create 4 bits segments value resolution file
#remove LSB and pack 2 pixels as 1 byte

with open(SGD_FILE, 'rb') as in_file:
  segment_data_in = in_file.read()

with open(SGD_FILE_4BITS, 'wb') as out_file:
  for msb,lsb in zip(segment_data_in[0::2],segment_data_in[1::2]):

    lsb = lsb >> 4
    msb = msb >> 4

    segment_data_out = lsb | (msb <<4)
    out_file.write(pack("=B",segment_data_out))
##### Create 2 bits segments value resolution file
#remove LSB and pack 4 pixels as 1 byte
with open(SGD_FILE_2BITS, 'wb') as out_file:
  for lsb2,lsb,msb,msb2 in zip(segment_data_in[0::4],segment_data_in[1::4],segment_data_in[2::4],segment_data_in[3::4]):

    lsbr = lsb >> 6
    msbr = msb >> 6
    lsbr2 = lsb2 >> 6
    msbr2 = msb2 >> 6

    segment_data_out = msbr2 << 6 | msbr << 4 | lsbr << 2 | lsbr2
    out_file.write(pack("=B",segment_data_out))

#### Create Segment Coordinates files
out_filename = SGX_FILE
with open(out_filename, "wb") as out_file:
  for c in tab_x:
    out_file.write(pack("<H", int(c)))

out_filename = SGY_FILE
with open(out_filename, "wb") as out_file:
  for c in tab_y:
    out_file.write(pack("<H", int(c)))

out_filename = SGW_FILE
with open(out_filename, "wb") as out_file:
  for c in tab_width:
    out_file.write(pack("<H", int(c)))

out_filename = SGH_FILE
with open(out_filename, "wb") as out_file:
  for c in tab_height:
    out_file.write(pack("<H", int(c)))

out_filename = SGO_FILE
with open(out_filename, "wb") as out_file:
  for c in tab_offset:
    out_file.write(pack("<I", int(c)))

#### Create Buttons configuration file
with open(BTN_FILE, "wb") as out_file:
  for c in rom.BTN_DATA:
    out_file.write(pack("<I", int(c)))

###################################################################################################
### This section elaborates the rom file
###################################################################################################
### Build ROM file
rom_offset=0

##ROM file Header : flags #######

#Various flags (4 bytes)
GW_FLAGS=0

# flag_rendering_lcd_inverted @0
if rom.flag_rendering_lcd_inverted :
  GW_FLAGS|=1

# flag_sound @1..3
GW_FLAGS|=(rom.flag_sound << 1) & 0xE

# flag_segments_resolution_bits @4
# replace the segment file with 4 bits resolution file
if rom.flag_segments_resolution_bits == 4 :
  GW_FLAGS|= 0x10
  SGD_FILE=SGD_FILE_4BITS

# replace the segment file with 2 bits resolution file
if rom.flag_segments_resolution_bits == 2 :
  GW_FLAGS|= 0x100
  SGD_FILE=SGD_FILE_2BITS

# flag_background_jpeg @5
# If the background is compressed, remove it from the payload
# The jpeg background is added right after the LZ4 payload

if rom.flag_background_jpeg :
  GW_FLAGS|=0x20
  BGD_FILE="xxx-xxx-x.empty"

 # flag_lcd_deflicker_level @6..7
GW_FLAGS|=(rom.flag_lcd_deflicker_level << 6) & 0xC0

 ## Write header sections
 ####################################################################

# 10 types of 2 elements (x 4 bytes)    	(80 bytes)
element_file=[BGD_FILE, SGD_FILE,SGO_FILE, SGX_FILE, SGY_FILE, SGH_FILE, SGW_FILE, MLD_FILE, PGM_FILE, BTN_FILE]

with open(rom_filename, "wb") as out_file:

  ### CPU TYPE     	    (8 bytes)
  out_file.write(rom.CPU_TYPE.encode("utf-8"))
  rom_offset+=8

  ## ROM SIGNATURE   (8 bytes)
  out_file.write(rom_name.rjust(8)[-8:].encode("utf-8"))
  rom_offset+=8

  ### Address counter time used by the program to manage it RTC (6 bytes)
  out_file.write(pack("B",rom.ADD_TIME_HOUR_MSB))
  out_file.write(pack("B",rom.ADD_TIME_HOUR_LSB))
  out_file.write(pack("B",rom.ADD_TIME_MIN_MSB))
  out_file.write(pack("B",rom.ADD_TIME_MIN_LSB))
  out_file.write(pack("B",rom.ADD_TIME_SEC_MSB))
  out_file.write(pack("B",rom.ADD_TIME_SEC_LSB))
  out_file.write(pack("B",rom.ADD_TIME_HOUR_MSB_PM_VALUE))

  rom_offset+=7

  ### byte_spare1     	    (1 byte)
  out_file.write(pack("B", 0))
  rom_offset+=1

  ### ROM Flags         (4bytes)
  out_file.write(pack("<l", GW_FLAGS))
  rom_offset+=4

  ## Data section offset  (80bytes)
  rom_offset += 10*2*4

  for elt_file in element_file:
    out_file.write(pack("<l", rom_offset))

    if os.path.exists(elt_file):
      elt_size=os.path.getsize(elt_file)
    else:
      elt_size=0

    out_file.write(pack("<l", elt_size))

    log(elt_file+"> offset="+str(rom_offset)+" size="+str(elt_size))

    #determine next offset (aligned 32bits)
    rom_offset+=elt_size
    if (rom_offset % 4) != 0:
      log("Padding:" + str(4-(rom_offset % 4)))
      rom_offset+=4 - (rom_offset % 4)

## Write Data sections
####################################################################

  for elt_file in element_file:
    if os.path.exists(elt_file):
      rd_modulo= os.path.getsize(elt_file) % 4
      log("Add data section:"+ str(elt_file) +",size="+str(os.path.getsize(elt_file))+"at:"+str( os.path.getsize(rom_filename) ))

      with open(elt_file,"rb") as input_file:
        out_file.write( input_file.read())

      if rd_modulo != 0:
        while (rd_modulo != 4):
          out_file.write(pack("c", b'P'))
          rd_modulo=rd_modulo+1
          log("Write Padding")


if COMPRESS_WITH == ZLIB_COMPRESSOR:
  ## Compress ROM file using zlib

  c = zlib.compressobj(level=9, method=zlib.DEFLATED, wbits=-15, memLevel=9)
  compressed_rom = c.compress(Path(rom_filename).read_bytes()) + c.flush()

  ## Compress ROM file using zopfli
  #import zopfli
  #c = zopfli.ZopfliCompressor(zopfli.ZOPFLI_FORMAT_DEFLATE)
  #compressed_rom = c.compress(Path(rom_filename).read_bytes()) + c.flush()

elif COMPRESS_WITH == LZ4_COMPRESSOR:
  ## Compress ROM using LZ4
  compressed_rom = lz4.compress(
                Path(rom_filename).read_bytes(),
                compression_level=9,
                block_size=lz4.BLOCKSIZE_MAX1MB,
                block_linked=False,)

elif COMPRESS_WITH == LZMA_COMPRESSOR:
  ## Compress ROM using LZMA
  import lzma

  compressed_rom = lzma.compress(
        Path(rom_filename).read_bytes(),
        format=lzma.FORMAT_ALONE,
        filters=[
            {
                "id": lzma.FILTER_LZMA1,
                "preset": 6,
                "dict_size": 16 * 1024,
            }
        ])
  compressed_rom = compressed_rom[13:]

# fix windows issue due to ':' in file name
final_rom_filename = final_rom_filename.replace(':','')

with open(final_rom_filename, "wb") as out_file:

  if COMPRESS_WITH == ZLIB_COMPRESSOR:
    out_file.write( b'ZLIB')
    out_file.write(pack("<l",len(compressed_rom)))

  if COMPRESS_WITH == LZMA_COMPRESSOR:
    out_file.write( b'LZMA')
    out_file.write(pack("<l",len(compressed_rom)))
  out_file.write(compressed_rom)

  #Append JPEG background (if it exists and flag_background_jpeg is set)
  if os.path.exists(jpeg_background) & (rom.flag_background_jpeg == True):
    log('\tAdd JPEG background')
    with open(jpeg_background,"rb") as input_file:
      out_file.write( input_file.read())

final_rom_size = os.path.getsize(final_rom_filename)
log('-> BUILD SUCCESS '+ final_rom_filename+' size:'+str(final_rom_size))
printProgressBar(bar_progress, bar_total, prefix = bar_prefix, suffix = 'COMPLETE        ')
if not DEBUG:
  print("")
