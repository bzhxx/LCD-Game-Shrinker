#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" ~LCD Game Shrinker~
  parser used to automatically recover required parameters to perform
  the shrinking process.

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
  This is the background ! BackgroundNS.png.

> segment_file
  This is the SVG file where the segments are defined (.svg)

> program_file
  the raw binary program file

> melody_file
  the raw binary melody file (if it exists)

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
> screen dimensions    (applied on .svg)

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
    by default the background is fromm the background file
    if a segment state is ON, the background and non_white segment pixels are 'RGB multiply".
  or
    If True ( case "tabletop" or "inverted lcd screen")
    by default the background is black
    if a segment state is ON, the background and the non_black segment pixels are 'RGB multiply".

 > flag_background_jpeg =True or False
  JPEG or all the rom is compressed wth LZ4

> jpeg_quality=90
typical values : 80 to 95
The following presets are available by default:
``web_low``, ``web_medium``, ``web_high``, ``web_very_high``, ``web_maximum``,
``low``, ``medium``, ``high``, ``maximum``.

https://github.com/python-pillow/Pillow/blob/master/src/PIL/JpegPresets.py#L71

> keys/buttons mapping
  keys/buttons mapping can be found in MAME source file (hh_sm510.cpp)
  CPU INPUTS S1..S8, BA, B
  GW 8 BUTTONS used for retro-go: 8 bits
  K4..K1 : 32 bits
  LEFT,RIGHT,UP,DOWN,GAME,SELECT,A,B

>sound configuration
  TODO define the appropritate functions to generate the sound piezo buzzer
"""
import os,sys,urllib.request,lxml

import rom_config as rom

DEBUG = False

def log(s):
  if DEBUG:
    print (s)

def warm(s):
    print (rom.mame_fullname+ " WARNING:"+s +' ['+str(rom_name) +']')

def error(s):
    print (rom.mame_fullname+ " ERROR:"+s +' [' +str(rom_name) +']')
    try :
      inkscape.close()
    except:
      pass
    exit()

#def set_parameters(rom_name,mame_rom_dir, mame_driver_file):
def set_parameters(rom_name,mame_rom_dir):

  rom.mame_rom_dir = mame_rom_dir
  rom.name = rom_name

## ROM Reset values
  rom.mame_year=0
  rom.mame_name=0
  rom.mame_parent=0
  rom.mame_comp=0
  rom.mame_machine=0
  rom.mame_input=0
  rom.mame_class  ="none"
  rom.mame_init  =0
  rom.mame_company  ="none"
  rom.mame_fullname="'unknown game'"
  rom.mame_flags  =0

  rom.background_file  = "BackgroundNS.png"
  rom.segments_file="none"
  rom.program_file="none"
  rom.melody_file="none"


  #dual screens
  rom.segments_top_file ="none"
  rom.segments_bottom_file = "none"

  rom.segments_left_file = "none"
  rom.segments_right_file = "none"
  
  rom.dual_screen_vert=False
  rom.dual_screen_hor=False

  rom.CPU_TYPE=0

  rom.background_x=0
  rom.background_y=0
  rom.background_width=0
  rom.background_height=0

  rom.screen_x=0
  rom.screen_y=0
  rom.screen_width=0
  rom.screen_height=0

  rom.border_left_right=0
  rom.border_top_down=0

  rom.flag_rendering_lcd_inverted=False

  #Buttons mapping according to the host machine
  rom.BTN_SIZE=10
  rom.BTN_DATA=[0]*rom.BTN_SIZE


  rom.flag_sound     = rom.FLAG_SOUND_R1_PIEZO
  
  rom.found = False
  ###################################################

  mame_driver_file = os.path.join("./build/","hh_sm510.cpp")
  url ="https://raw.githubusercontent.com/mamedev/mame/master/src/mame/drivers/hh_sm510.cpp"

  #print('Beginning file download from MAME github...')
  if not os.path.isfile(mame_driver_file) :
    urllib.request.urlretrieve(url, mame_driver_file)

  if not os.path.isfile(mame_driver_file) :
    error("Please copy hh_sm510.cpp in build directory")

  ### Get the full name
  with open(mame_driver_file, "r",encoding="utf8") as myfile:
    myline = myfile.readline()

    while myline:
      line_mame = myline.split(',')

      try:
        if (line_mame[0].find( 'CONS') > -1) & (line_mame[1].strip()==rom_name):

        # MAME constructor structure
          rom.mame_year=line_mame[0]
          rom.mame_name=line_mame[1]
          rom.mame_parent=line_mame[2]
          rom.mame_comp=line_mame[3]
          rom.mame_machine=line_mame[4]
          rom.mame_input=line_mame[5]
          rom.mame_class  =line_mame[6]
          rom.mame_init  =line_mame[7]
          rom.mame_company=line_mame[8]
          rom.mame_fullname=myline.split("\"")[3]
          rom.found = True

      except:
        pass
      myline = myfile.readline()
      
  if (rom.mame_fullname.find("Panorama Screen") > -1) :
    rom.flag_rendering_lcd_inverted = True

  if (rom.mame_fullname.find("Table Top") > -1) :
    rom.flag_rendering_lcd_inverted = True

  ## possible extensions are none, '.program' or '.bin'
  program_extension = ['.program','.bin']
  melody_extension = '.melody'
  seg_extension = '.svg'

  rom.dual_screen_hor = False
  rom.dual_screen_vert= False

  for root,dirs,files in os.walk(mame_rom_dir):

    for f in files:
      fileName, fileExtension = os.path.splitext(f)

  #maincpu
      if fileExtension in program_extension:
        rom.program_file=os.path.basename(f)


      if not fileExtension:
        rom.program_file=os.path.basename(f)

  #maincpu:melody
      if fileExtension == melody_extension:
        rom.melody_file=os.path.basename(f)

  #screen
      if fileExtension == seg_extension:

  #dual screens
        if f.find("_top.svg") >-1:
          rom.segments_top_file=os.path.basename(f)
          rom.dual_screen_vert = True

        if f.find("_bottom.svg")>-1:
          rom.segments_bottom_file=os.path.basename(f)
          rom.dual_screen_vert = True

        if f.find("_left.svg")>-1:
          rom.segments_left_file=os.path.basename(f)
          rom.dual_screen_hor = True

        if f.find("_right.svg")>-1:
          rom.segments_right_file=os.path.basename(f)
          rom.dual_screen_hor= True

  #single screens
        rom.segments_file=os.path.basename(f)

  # GET CPU SM5A SM510 SM511 SM512 or KB
  # Add sm510_tiger, sm511_tiger2bit supported
  mame_class_found= False
  if rom.found:

    with open(mame_driver_file, "r",encoding="utf8") as myfile:
  
      myline = myfile.readline()
  
      while myline:
  
        if (myline.find(rom.mame_class.strip()) > -1) & (myline.find(rom.mame_name.strip()) > -1) & (myline.find('machine_config') > -1):
          mame_class_found = True
  
        if mame_class_found :
          if (myline.find('sm510_common') > -1) :
            rom.CPU_TYPE = 'SM510__\0'
            rom.flag_lcd_deflicker_level = 1
            break
          if (myline.find('sm511_common') > -1) :
            rom.CPU_TYPE = 'SM511__\0'
            rom.flag_lcd_deflicker_level = 1
            break
          if (myline.find('sm512_common') > -1) :
            rom.CPU_TYPE = 'SM512__\0'
            rom.flag_lcd_deflicker_level = 1
            break
          if (myline.find('sm5a_common') > -1) :
            rom.flag_lcd_deflicker_level = 2
            rom.CPU_TYPE = 'SM5A___\0'
            break
          if (myline.find('kb1013vk12_common') > -1) :
            rom.flag_lcd_deflicker_level = 2
            rom.CPU_TYPE = 'SM5A___\0'
            break
          if (myline.find('sm510_tiger') > -1) :
            rom.CPU_TYPE = 'SM510__\0'
            rom.flag_lcd_deflicker_level = 1
            break
          if (myline.find('sm511_tiger2bit') > -1) :
            rom.CPU_TYPE = 'SM511__\0'
            rom.flag_lcd_deflicker_level = 1
            break
        myline = myfile.readline()
  
    log(rom.CPU_TYPE)
    log(rom.flag_lcd_deflicker_level)
    
     # Get Background and screen dimensions from MAME layout artwork file
    layout_file=os.path.join(mame_rom_dir,'default.lay')
    tree = lxml.etree.parse(layout_file)
    layout_root = tree.getroot()
    rom.layout_found = False
  
    # First tentative look for 'background' & 'only' in the name view 
    for x in layout_root:
  
      if str(x.tag) == 'view':
        if (str(x.attrib).upper().find('BACK' ) > -1) & (str(x.attrib).upper().find('ONLY' ) > -1):
          log('START ----------------------------------------------------')
          log(x.attrib)
          # log('-BOUND-')
  
          # bounds=x.find('bounds')
          # bound_x = int(bounds.get('x'))
          # bound_y = int(bounds.get('y'))
          # bound_width= int(bounds.get('width'))
          # bound_height= int(bounds.get('height'))
  
          log('-SCREEN-')
  
          rom.screen=x.find('screen')
          screen_bounds =rom.screen.find('bounds')
          rom.screen_x = int(screen_bounds.get('x'))
          rom.screen_y = int(screen_bounds.get('y'))
          rom.screen_width= int(screen_bounds.get('width'))
          rom.screen_height= int(screen_bounds.get('height'))
          log('-ELEMENTS/OVERLAY-')
  
          all_element=x.findall('element')
          for element in all_element:
  
            element_bounds =element.find('bounds')
            log(element.attrib)
            log(element_bounds.attrib)
            if (str(element.attrib).upper().find('GROUND' ) > -1) or \
              (str(element.attrib).upper().find('BG' ) > -1) or \
              (str(element.attrib).upper().find('OVERLAY' ) > -1) :
  
              background_ref = element.get('ref')
  
              log(element.attrib)
              log(element_bounds.attrib)
              rom.background_x = int(element_bounds.get('x'))
              rom.background_y = int(element_bounds.get('y'))
              rom.background_width= int(element_bounds.get('width'))
              rom.background_height= int(element_bounds.get('height'))
              rom.layout_found = True
  
  
          all_overlay =x.findall('overlay')
          for element in all_overlay:
  
            element_bounds =element.find('bounds')
            log(element.attrib)
            log(element_bounds.attrib)
            if (str(element.attrib).upper().find('GROUND' ) > -1) or \
              (str(element.attrib).upper().find('BG' ) > -1) or \
              (str(element.attrib).upper().find('OVERLAY' ) > -1) :
  
              background_ref = element.get('ref')
              log(element.attrib)
              log(element_bounds.attrib)
              rom.background_x = int(element_bounds.get('x'))
              rom.background_y = int(element_bounds.get('y'))
              rom.background_width= int(element_bounds.get('width'))
              rom.background_height= int(element_bounds.get('height')  )
              rom.layout_found = True
  
          log('END -------------------------------------------------------')
          
    # Second tentative look for 'background' in the name view 
    if not rom.layout_found:
        for x in layout_root:
        
          if str(x.tag) == 'view':
            if (str(x.attrib).upper().find('BACK' ) > -1) :
              log('START ----------------------------------------------------')
              log(x.attrib)
              # log('-BOUND-')
        
              # bounds=x.find('bounds')
              # bound_x = int(bounds.get('x'))
              # bound_y = int(bounds.get('y'))
              # bound_width= int(bounds.get('width'))
              # bound_height= int(bounds.get('height'))
        
              log('-SCREEN-')
        
              rom.screen=x.find('screen')
              screen_bounds =rom.screen.find('bounds')
              rom.screen_x = int(screen_bounds.get('x'))
              rom.screen_y = int(screen_bounds.get('y'))
              rom.screen_width= int(screen_bounds.get('width'))
              rom.screen_height= int(screen_bounds.get('height'))
              log('-ELEMENTS/OVERLAY-')
        
              all_element=x.findall('element')
              for element in all_element:
        
                element_bounds =element.find('bounds')
                log(element.attrib)
                log(element_bounds.attrib)
                if (str(element.attrib).upper().find('GROUND' ) > -1) or \
                  (str(element.attrib).upper().find('BG' ) > -1) or \
                  (str(element.attrib).upper().find('OVERLAY' ) > -1) :
        
                  background_ref = element.get('ref')
        
                  log(element.attrib)
                  log(element_bounds.attrib)
                  rom.background_x = int(element_bounds.get('x'))
                  rom.background_y = int(element_bounds.get('y'))
                  rom.background_width= int(element_bounds.get('width'))
                  rom.background_height= int(element_bounds.get('height'))
                  rom.layout_found = True
        
        
              all_overlay =x.findall('overlay')
              for element in all_overlay:
        
                element_bounds =element.find('bounds')
                log(element.attrib)
                log(element_bounds.attrib)
                if (str(element.attrib).upper().find('GROUND' ) > -1) or \
                  (str(element.attrib).upper().find('BG' ) > -1) or \
                  (str(element.attrib).upper().find('OVERLAY' ) > -1) :
        
                  background_ref = element.get('ref')
                  if background_ref == None:
                    background_ref = element.get('element')
                  log(element.attrib)
                  log(element_bounds.attrib)
                  rom.background_x = int(element_bounds.get('x'))
                  rom.background_y = int(element_bounds.get('y'))
                  rom.background_width= int(element_bounds.get('width'))
                  rom.background_height= int(element_bounds.get('height')  )
                  rom.layout_found = True
        
              log('END -------------------------------------------------------')
  
    if rom.layout_found:
      # look for the artwork file name
  
      log(background_ref)
      all_element=layout_root.findall('element')
      for element in all_element:
        log (element.get('name'))
        if str(element.get('name')) == background_ref :
  
          rom.background_file = str((element.find('image').get('file')))
          log (' background:'+rom.background_file)
  
    if not rom.layout_found:
       log ('Failed to find a layout...')
  
    log('background:'+rom.background_file)
  
    log('background_x:'+str(rom.background_x))
    log('background_y:'+str(rom.background_y))
    log('background_width:'+str(rom.background_width))
    log('background_height:'+str(rom.background_height))
  
    log('screen_x:'+str(rom.screen_x))
    log('screen_y:'+str(rom.screen_y))
    log('screen_width:'+str(rom.screen_width))
    log('screen_height:'+str(rom.screen_height))
  
    # Rules according to ROM file name used as a python module
    #check if there is a custom module to load
    
  custom_script=os.path.join("custom",rom_name+".py")
  if os.path.isfile(custom_script) :

    rom.custom_script_notfound = False

    import importlib
    module_name="custom."+rom_name
    if not (module_name in sys.modules):
      custom_mod = importlib.import_module(module_name)
    else:
      importlib.reload(sys.modules[module_name])

  else:
    rom.custom_script_notfound = True




