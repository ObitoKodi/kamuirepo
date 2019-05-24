# -*- coding: utf-8 -*-


import os
import sys
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.ytMMA'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID = "UFC YOUTUBE"


def run():
    plugintools.log("ytMMA.run")
    params = plugintools.get_params()
    if params.get("action") is None:
        main_list(params)
    else:
        pass
    
    plugintools.close_item_list()


def main_list(params):
    plugintools.log("ytMMA.main_list "+repr(params))

    plugintools.add_item( 
        #action="", 
        title = "UFC",
        url = 'plugin://plugin.video.youtube/user/UFC/',
        thumbnail = icon,
        folder=True )

run()
