# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @tantrumdev wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

# Addon Name: AutoExec for Kamui
# Addon id: script.kamui.artwork
# Addon Provider: Obito

import xbmcvfs,xbmcgui
from kamuiartwork import theme_setter

def main():
    try:
        theme_setter.Apply_Theme('exuary')
        xbmcvfs.delete('special://userdata/autoexec.py')
    except Exception, e:
        xbmcvfs.delete('special://userdata/autoexec.py')

if __name__ == '__main__':
    main()