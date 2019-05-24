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



addon_id = 'plugin.video.youtube.monstercat'
addon = Addon(addon_id, sys.argv)
local = xbmcaddon.Addon(id=addon_id)
icon = local.getAddonInfo('icon')
fanart = local.getAddonInfo('fanart')


def go_youtube():
        addDir(title="Monstercat Uncaged", url="plugin://plugin.video.youtube/playlist/UUJ6td3C9QlPO9O_J5dF4ZzA/")
        addDir(title="Monstercat Instinct", url="plugin://plugin.video.youtube/playlist/UUp8OOssjSjGZRVYK6zWbNLg/")

def addDir(title, url):
    liz=xbmcgui.ListItem(title)
    liz.setProperty('IsPlayable', 'false')
    liz.setInfo(type="Video", infoLabels={"label":title,"title":title} )
    liz.setArt({'thumb':icon,'fanart':fanart})
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=True)
    
go_youtube()
    
xbmcplugin.endOfDirectory(int(sys.argv[1]))
