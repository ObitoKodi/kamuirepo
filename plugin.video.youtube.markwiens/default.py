# -*- coding: utf-8 -*-
#------------------------------------------------------------
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#------------------------------------------------------------
# -*- coding: utf-8 -*-

import os
import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
from addon.common.addon import Addon



addon_id = 'plugin.video.youtube.markwiens'
addon = Addon(addon_id, sys.argv)
local = xbmcaddon.Addon(id=addon_id)
icon = local.getAddonInfo('icon')
fanart = local.getAddonInfo('fanart')



def go_youtube():
        addDir(title="Latest Videos", url="plugin://plugin.video.youtube/playlist/UUyEd6QBSgat5kkC6svyjudA/")
        addDir(title="Best Food Videos",url="plugin://plugin.video.youtube/playlist/PL96D2A64E5B680F9C/")
        addDir(title="Street Food Tours",url="plugin://plugin.video.youtube/playlist/PLeoy0zUu6bqlV_IYKPec6F6lLrDIJdmsn/")
        addDir(title="Village Food",url="plugin://plugin.video.youtube/playlist/PLeoy0zUu6bqnnb-zOdXKSvydabszYN1dc/")
        addDir(title="High End Food",url="plugin://plugin.video.youtube/playlist/PLeoy0zUu6bql-JwyfV9yweySAJOxcwgvN/")
        addDir(title="Unseen Food",url="plugin://plugin.video.youtube/playlist/PLeoy0zUu6bqlymSe1JfXaJJGITGYfI5to/")     


def addDir(title, url):
    liz=xbmcgui.ListItem(title)
    liz.setProperty('IsPlayable', 'false')
    liz.setInfo(type="Video", infoLabels={"label":title,"title":title} )
    liz.setArt({'thumb':icon,'fanart':fanart})
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=True)
    
go_youtube()
    
xbmcplugin.endOfDirectory(int(sys.argv[1]))
