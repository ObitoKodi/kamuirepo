"""
    Plugin for Launching programs
"""

# -*- coding: UTF-8 -*-
# main imports
import sys
import os
import xbmc
import xbmcgui
import xbmcaddon

# plugin constants
__plugin__ = "retrosmc"
__author__ = "jcnventura/mcobit"
__url__ = "http://blog.petrockblock.com/retropie/"
__git_url__ = "https://github.com/mcobit/retrosmc/"
__credits__ = "mcobit"
__version__ = "0.0.1"

dialog = xbmcgui.Dialog()
addon = xbmcaddon.Addon(id='script.retrosmc')

output=os.popen("/home/osmc/RetroPie/scripts/retropie.sh").read()
#dialog.ok("Starting RetroPie",output)
#print output
