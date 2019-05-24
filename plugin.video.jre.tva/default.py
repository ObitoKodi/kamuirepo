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



addon_id = 'plugin.video.jre.tva'
addon = Addon(addon_id, sys.argv)
local = xbmcaddon.Addon(id=addon_id)
icon = local.getAddonInfo('icon')
fanart = local.getAddonInfo('fanart')



def go_youtube():
        addDir(title="The Joe Rogan Experience", url="plugin://plugin.video.youtube/playlist/PLk1Sqn_f33KuS7ZSVMJqzFaqOyyl-esmG/")
        addDir(title="Best of the Week videos",url="plugin://plugin.video.youtube/playlist/PLk1Sqn_f33KtA0OOlTxl7CHizKmKeD70T/")
        addDir(title="JRE Toons",url="plugin://plugin.video.youtube/playlist/PLk1Sqn_f33Kub1gS-MQuw4slwAv1R2tcy/")
        addDir(title="JRE MMA Show", url="plugin://plugin.video.youtube/playlist/PLk1Sqn_f33KuQyLE4RjEOdJ_-0epbcBb4/")
        addDir(title="JRE Archive - Episodes #1-199", url="plugin://plugin.video.youtube/playlist/PLk1Sqn_f33KvtMA4mCQSnzGsZe8qsTdzV/")
        addDir(title="JRE Archive - Episodes #200-349",url="plugin://plugin.video.youtube/playlist/PLk1Sqn_f33KtUuWHwNl3ndvbPKlQ6LJZB/")
        addDir(title="JRE Archive - JRE #350-499",url="plugin://plugin.video.youtube/playlist/PLk1Sqn_f33Kvv8T6ZESpJ2nvEHT9xBhlb/")
        addDir(title="JRE Archive - Episodes #500-700",url="plugin://plugin.video.youtube/playlist/PLk1Sqn_f33KtVQWWnE_V6-sypm5zUMkU6/")
        addDir(title="JRE Archive - Episodes #701-1000",url="plugin://plugin.video.youtube/playlist/PLk1Sqn_f33KuU_aJDvMPPAy_SoxXTt_ub/")
        addDir(title="JRE Archive - Episodes #1001-Now",url="plugin://plugin.video.youtube/playlist/PLk1Sqn_f33Ku0Oa3t8MQjV7D_G_PBi8g1/")



def addDir(title, url):
    liz=xbmcgui.ListItem(title)
    liz.setProperty('IsPlayable', 'false')
    liz.setInfo(type="Video", infoLabels={"label":title,"title":title} )
    liz.setArt({'thumb':icon,'fanart':fanart})
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=True)
    
go_youtube()
    
xbmcplugin.endOfDirectory(int(sys.argv[1]))
