import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import shutil
import urllib2,urllib
import re

import time
import plugintools
from addon.common.addon import Addon
from addon.common.net import Net




USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
addon_id = 'plugin.program.kamuiwidgets'
ADDON = xbmcaddon.Addon(id=addon_id)
AddonID='plugin.program.kamuiwidgets'
AddonTitle="Kamui Widgets"
dialog       =  xbmcgui.Dialog()
net = Net()
U = ADDON.getSetting('User')
FANART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
ART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
VERSION = "1.2.0"
DBPATH = xbmc.translatePath('special://database')
TNPATH = xbmc.translatePath('special://thumbnails');
PATH = "Kamui Widgets"
BASEURL = "http://kamui.ga"
H = 'http://'
EXCLUDES     = ['']

def INDEX():
    #addDir('MOVIES1',BASEURL,150,ART+'icon.png',FANART,'')
    #addDir('MOVIES2',BASEURL,151,ART+'icon.png',FANART,'')
    #addDir('TV SHOWS1',BASEURL,152,ART+'icon.png',FANART,'')
    #addDir('TV SHOWS2',BASEURL,153,ART+'icon.png',FANART,'')
    #addDir('KIDS1',BASEURL,154,ART+'icon.png',FANART,'')
    #addDir('KIDS2',BASEURL,155,ART+'icon.png',FANART,'')
    #addDir('LIVE TV',BASEURL,156,ART+'icon.png',FANART,'')
    #addDir('MUSIC',BASEURL,157,ART+'icon.png',FANART,'')
    #addDir('SPORTS1',BASEURL,158,ART+'icon.png',FANART,'')
    #addDir('SPORTS2',BASEURL,159,ART+'icon.png',FANART,'')
    #addDir('ONLINE1',BASEURL,160,ART+'icon.png',FANART,'')
    #addDir('ONLINE2',BASEURL,161,ART+'icon.png',FANART,'')
    #addDir('ANIME',BASEURL,162,ART+'icon.png',FANART,'')
    #addDir('UPDATE1',BASEURL,163,ART+'icon.png',FANART,'')
    #addDir('UPDATE2',BASEURL,164,ART+'icon.png',FANART,'')
    setView('movies', 'MAIN')

def MOVIESBUTTON1():
    addDir('Kamui Streams','url',20,ART+'kamuistreams.png',FANART,'')
    addDir('AtTheFlix','url',22,ART+'attheflix.png',FANART,'')
    addDir('Seren','url',21,ART+'seren.png',FANART,'')
    addDir('Yoda','url',23,ART+'yoda.png',FANART,'')
    setView('movies', 'MAIN')

def MOVIESBUTTON2():
    addDir('Gaia','url',24,ART+'gaia.png',FANART,'')
    setView('movies', 'MAIN')

def TVSHOWSBUTTON1():
    addDir('Kamui Streams','url',30,ART+'kamuistreams.png',FANART,'')
    addDir('AtTheFlix','url',32,ART+'attheflix.png',FANART,'')
    addDir('Seren','url',31,ART+'seren.png',FANART,'')
    addDir('Yoda','url',33,ART+'yoda.png',FANART,'')
    setView('movies', 'MAIN')

def TVSHOWSBUTTON2():
    addDir('Gaia','url',34,ART+'gaia.png',FANART,'')
    addDir('Documented.HD','url',35,ART+'documented.png',FANART,'')
    setView('movies', 'MAIN')

def KIDSBUTTON1():
    addDir('Kamui Kids','url',40,ART+'kamuikids.png',FANART,'')
    addDir('AtTheFlix','url',41,ART+'attheflix.png',FANART,'')
    addDir('Cartoon HD','url',42,ART+'cartoonhd.png',FANART,'')
    addDir('Little Baby Bum','url',43,ART+'lbb.png',FANART,'')
    setView('movies', 'MAIN')

def KIDSBUTTON2():
    addDir('Kids Movies','url',44,ART+'kidsmovies.png',FANART,'')
    addDir('BinkyTV','url',45,ART+'binkytv.png',FANART,'')
    setView('movies', 'MAIN')

def LIVETVBUTTON1():
    addDir('TV Player','url',50,ART+'tvplayer.png',FANART,'')
    addDir('BBC IPlayer','url',51,ART+'bbciplayer.png',FANART,'')
    addDir('ITV Player','url',52,ART+'itvplayer.png',FANART,'')
    addDir('UKTV Play','url',53,ART+'uktvplay.png',FANART,'')
    setView('movies', 'MAIN')

def LIVETVBUTTON2():
    addDir('Live TV','url',54,ART+'kamuiwizard.png',FANART,'')
    setView('movies', 'MAIN')

def MUSICBUTTON():
    addDir('MTV Music','url',60,ART+'mtv.png',FANART,'')
    addDir('Youtube Music','url',61,ART+'youtubemusic.png',FANART,'')
    addDir('Monstercat','url',62,ART+'monstercat.png',FANART,'')
    addDir('XFactor','url',63,ART+'xfactor.png',FANART,'')
    setView('movies', 'MAIN')

def SPORTSBUTTON1():
    addDir('PlanetMMA','url',70,ART+'planetmma.png',FANART,'')
    addDir('WrestleManiac','url',71,ART+'wrestlemaniac.png',FANART,'')
    addDir('Sparkle','url',72,ART+'sparkle.png',FANART,'')
    addDir('Joker Sports','url',73,ART+'jokersports.png',FANART,'')
    setView('movies', 'MAIN')
    
def SPORTSBUTTON2():
    addDir('Skynet Sports','url',74,ART+'skynetsports.png',FANART,'')
    addDir('Sports Devil','url',75,ART+'sportsdevil.png',FANART,'')
    addDir('World of Wrestling','url',76,ART+'worldofwrestling.png',FANART,'')
    setView('movies', 'MAIN')

def ONLINEBUTTON1():
    addDir('Twitch','url',80,ART+'twitch.png',FANART,'')
    addDir('Youtube','url',81,ART+'youtube.png',FANART,'')
    addDir('UFC on Youtube','url',82,ART+'mmayoutube.png',FANART,'')
    addDir('WWE On Youtube','url',83,ART+'wweyoutube.png',FANART,'')
    setView('movies', 'MAIN')

def ONLINEBUTTON2():
    addDir('JRE','url',84,ART+'jre.png',FANART,'')
    addDir('Live Tube','url',85,ART+'livetube.png',FANART,'')
    setView('movies', 'MAIN')

def ANIMEBUTTON():
    addDir('WonderfulSubs','url',92,ART+'wonsub.png',FANART,'')
    addDir('9Anime','url',90,ART+'9anime.png',FANART,'')
    addDir('MasterAni Redux','url',91,ART+'masterani.png',FANART,'')
    addDir('Watch Nixtoons','url',93,ART+'watchnixtoons.png',FANART,'')
    setView('movies', 'MAIN')

def UPDATEBUTTON1():
    addDir('Kamui Wizard','url',100,ART+'kamuiwizard.png',FANART,'')
    addDir('Fix Buffering','url',101,ART+'fixbuffer.png',FANART,'')
    addDir('Refresh Repos','url',102,ART+'fixskin.png',FANART,'')
    addDir('Fresh Start','url',103,ART+'freshstart.png',FANART,'')
    setView('movies', 'MAIN')

def UPDATEBUTTON2():
    addDir('Real Debrid','url',104,ART+'rdlogo.png',FANART,'')
    addDir('Trakt','url',105,ART+'traktlogo.png',FANART,'')
    addDir('Logins','url',106,ART+'loginlogo.png',FANART,'')
    setView('movies', 'MAIN')


#################################
##### HOMESCREEN SHORTCUTS ######
#################################

def MOVIES1():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.kamui,return)')

def MOVIES2():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.seren,return)')

def MOVIES3():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.AtTheFlix,return)')

def MOVIES4():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.yoda,return)')
    
def MOVIES5():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.gaia,return)')
   
def TVSHOWS1():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.kamui,return)')

def TVSHOWS2():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.seren,return)')

def TVSHOWS3():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.AtTheFlix,return)')

def TVSHOWS4():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.yoda,return)')
    
def TVSHOWS5():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.gaia,return)')
    
def TVSHOWS6():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.documented.hd,return)')
    
def KIDS1():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.kamui/?action=kidscorner,return)')

def KIDS2():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.AtTheFlix/?description=No%20information%20available&amp;mode=get_list&amp;name=%5bCOLOR%20red%5d%5bB%5dKids%20Movie%20Boxsets%5b%2fB%5d%5b%2fCOLOR%5d&amp;url=https%3a%2f%2fpastebin.com%2fraw%2ffmUTKku0,return)')

def KIDS3():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.cartoonhd,return)')

def KIDS4():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.youtube.lbb,return)')

def KIDS5():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.kmERlink,return)')

def KIDS6():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.binkytv,return)')

def LIVETV1():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.tvplayer,return)')

def LIVETV2():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.iplayerwww,return)')

def LIVETV3():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.itv,return)')

def LIVETV4():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.uktvplay,return)')

def LIVETV5():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(TVChannels,return)')

def MUSIC1():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.mdmtvuk,return)')

def MUSIC2():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.spotitube,return)')

def MUSIC3():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.youtube.monstercat,return)')

def MUSIC4():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.XFactorInternational,return)')

def SPORTS1():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.ufc-finest,return)')

def SPORTS2():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.wrestlemaniac,return)')

def SPORTS3():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.sparkle,return)')

def SPORTS4():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.JokerSports,return)')

def SPORTS5():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.SkyNet/?mode=1&amp;name=%5bCOLOR%20white%5dSkynet%20Sports%5b%2fCOLOR%5d&amp;url=https%3a%2f%2fpastebin.com%2fraw%2f8LwbCQkv,return)')

def SPORTS6():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.sportsdevil,return)')

def SPORTS7():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.WorldOfWrestling,return)')

def ONLINE1():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.twitch,return)')

def ONLINE2():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.youtube,return)')

def ONLINE3():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.ytMMA,return)')

def ONLINE4():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.wwe-on-youtube,return)')

def ONLINE5():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.jre.tva,return)')

def ONLINE6():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.LiveTube,return)')

def ANIME1():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.9anime,return)')

def ANIME2():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.masteraniredux,return)')

def ANIME3():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.wonderfulsubs,return)')

def ANIME4():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.watchnixtoons,return)')

def UPDATE1():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10001,plugin://plugin.program.kamuiwizard,return)')

def UPDATE2():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10001,plugin://plugin.program.kamuiwizard/?mode=autoadvanced,return)')

def UPDATE3():
    import xbmc
    xbmc.executebuiltin('UpdateAddonRepos')
    xbmc.executebuiltin('UpdateLocalAddons')
    xbmc.executebuiltin('xbmc.activatewindow(home)')
    dialog = xbmcgui.Dialog()
    dialog.ok("Repos Refreshed", "Please allow a few minutes for addons to update.")

def UPDATE4():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10001,plugin://plugin.program.kamuiwizard/?mode=freshstart,return)')

def UPDATE5():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10001,plugin://plugin.program.kamuiwizard/?mode=realdebrid,return)')

def UPDATE6():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10001,plugin://plugin.program.kamuiwizard/?mode=trakt,return)')
    
def UPDATE7():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10001,plugin://plugin.program.kamuiwizard/?mode=login,return)')


#################################
############## CODE ##############
#################################

    
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

N = base64.decodestring('')
T = base64.decodestring('')
B = base64.decodestring('')
F = base64.decodestring('')
def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        if mode==5 :
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

        
                      
params=get_params()                     

url=None
name=None
mode=None
iconimage=None
fanart=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
        
        
print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)


def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
        
        
if mode==None or url==None or len(url)<1:
        INDEX()

elif mode==2:
        BUILDMENU()

elif mode==3:
        MAINTENANCE()
		
elif mode==4:
        deletecachefiles(url)
		
elif mode==5:
        WIZARD(name,url,description)

elif mode==6:        
	FRESHSTART(params)
	
elif mode==7:
       DeletePackages(url)
		
elif mode==150:
        MOVIESBUTTON1()

elif mode==151:
        MOVIESBUTTON2()

elif mode==152:        
	TVSHOWSBUTTON1()

elif mode==153:        
	TVSHOWSBUTTON2()
	
elif mode==154:
       KIDSBUTTON1()

elif mode==155:
       KIDSBUTTON2()

elif mode==156:
       LIVETVBUTTON1()

elif mode==165:
       LIVETVBUTTON2()
       
elif mode==157:
       MUSICBUTTON()

elif mode==158:
       SPORTSBUTTON1()

elif mode==159:
       SPORTSBUTTON2()

elif mode==160:
       ONLINEBUTTON1()

elif mode==161:
       ONLINEBUTTON2()

elif mode==162:
       ANIMEBUTTON()

elif mode==163:
       UPDATEBUTTON1()

elif mode==164:
       UPDATEBUTTON2()

elif mode==20:
       MOVIES1()

elif mode==21:
       MOVIES2()

elif mode==22:
       MOVIES3()

elif mode==23:
       MOVIES4()

elif mode==24:
       MOVIES5()

elif mode==30:
       TVSHOWS1()

elif mode==31:
       TVSHOWS2()

elif mode==32:
       TVSHOWS3()

elif mode==33:
       TVSHOWS4()

elif mode==34:
       TVSHOWS5()

elif mode==35:
       TVSHOWS6()

elif mode==40:
       KIDS1()

elif mode==41:
       KIDS2()

elif mode==42:
       KIDS3()

elif mode==43:
       KIDS4()

elif mode==44:
       KIDS5()

elif mode==45:
       KIDS6()

elif mode==50:
       LIVETV1()

elif mode==51:
       LIVETV2()

elif mode==52:
       LIVETV3()

elif mode==53:
       LIVETV4()

elif mode==54:
       LIVETV5()

elif mode==60:
       MUSIC1()

elif mode==61:
       MUSIC2()

elif mode==62:
       MUSIC3()

elif mode==63:
       MUSIC4()

elif mode==70:
       SPORTS1()

elif mode==71:
       SPORTS2()

elif mode==72:
       SPORTS3()

elif mode==73:
       SPORTS4()

elif mode==74:
       SPORTS5()
	   
elif mode==75:
       SPORTS6()

elif mode==76:
       SPORTS7()

elif mode==80:
       ONLINE1()

elif mode==81:
       ONLINE2()

elif mode==82:
       ONLINE3()

elif mode==83:
       ONLINE4()

elif mode==84:
       ONLINE5()

elif mode==85:
       ONLINE6()

elif mode==90:
       ANIME1()

elif mode==91:
       ANIME2()

elif mode==92:
       ANIME3()

elif mode==93:
       ANIME4()

elif mode==100:
       UPDATE1()
       
elif mode==101:
       UPDATE2()
       
elif mode==102:
       UPDATE3()
       
elif mode==103:
       UPDATE4()

elif mode==104:
       UPDATE5()

elif mode==105:
       UPDATE6()

elif mode==106:
       UPDATE7()

elif mode==206:
       DELETEIVUEDB()
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
