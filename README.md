
# LCD-Game-Shrinker
This program permits to shrink MAME high resolution artwork and graphics for portable device running LCD-Game-Emulator : https://github.com/bzhxx/LCD-Game-Emulator


# Environment
Python (3.6) script tested under Linux Ubuntu and Windows 10.

# Requirements
The following application need to be installed
 - [x] Inkscape (v1.10 recommended) https://inkscape.org
 - [x] LZ4 compression command tool

The following Python modules are used
 - [x] import sys, os, subprocess, re, lxml, importlib, zipfile, numpy, urllib.request, svgutils 
 - [x] from struct import pack
 - [x] from PIL import Image,ImageChops


## Usage
### MAME Artworks and ROMs
This tool is used to shrink any MAME artwork and ROM **SM510** family.
You have to place Artwork file and ROM file in their respective directory **input/artwork** and **input/rom**.

### Execute
**Python shrink_it.py** to process all files or
**Python shrink_it.py input/rom/gnw_mygame_zip** to process a single file.

All intermediate files are created in **build/** directory.
At the end, resulting files are available under **output/** directory.
The resulting files can be executed by https://github.com/bzhxx/LCD-Game-Emulator ported on https://github.com/bzhxx/game-and-watch-retro-go

## Advanced usage : Custom rules
It's possible to customize the shrinking process by adding some image processing on artwork and graphics.
For this purpose, a python script is available or must be added in **custom/** directory. 
Sometimes, an example is better than any explanation. So, have a look on **https://github.com/bzhxx/LCD-Game-Shrinker/blob/main/custom/gnw_ball.py**;
This script customizes the rendering by adding gradient effect, anti-newton rings filter, artwork background shadow and experimental drop shadow effect on each LCD segments.
