import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import shutil
import urllib2,urllib
import re
import extract
import downloader
import time
import plugintools
from addon.common.addon import Addon
from addon.common.net import Net




USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
addon_id = 'plugin.video.kamuiunblock'
ADDON = xbmcaddon.Addon(id=addon_id)
AddonID='plugin.video.kamuiunblock'
AddonTitle="Kamui Unblocker"
dialog       =  xbmcgui.Dialog()
net = Net()
U = ADDON.getSetting('User')
FANART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
ART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
VERSION = "1.1.0"
DBPATH = xbmc.translatePath('special://database')
TNPATH = xbmc.translatePath('special://thumbnails');
PATH = "Kamui Unblocker"            
BASEURL = "http://kamui.online"
H = 'http://'
EXCLUDES     = ['']

def INDEX():
    addDir('PRIMEWIRE UNBLOCK','https://www.dropbox.com/s/lhigmh02elo4yi6/unblock.zip?dl=1',5,ART+'icon.png',FANART,'')
    setView('list', 'MAIN')

def CHANNELS():
    addDir('SPORTS','url',13,ART+'icon.png',FANART,'')
    addDir('TV CATCHUP','url',14,ART+'icon.png',FANART,'')
    addDir('KIDS','url',15,ART+'icon.png',FANART,'')
    setView('list', 'MAIN')

def SPORTS():
    addDir('SPORTS ZONE','url',73,ART+'sportszone.png',FANART,'')
    addDir('ZEM TV','url',19,ART+'zemtv.png',FANART,'')
    addDir('CASTAWAY','url',20,ART+'castaway.png',FANART,'')
    addDir('SPORTS DEVIL','url',24,ART+'sportsdevil.png',FANART,'')
    addDir('AK47','url',74,ART+'ak47.png',FANART,'')
    addDir('PHOENIX SPORTS','url',17,ART+'phoenix.png',FANART,'')
    addDir('CCLOUD','url',75,ART+'ccloud.png',FANART,'')
    addDir('ADRIAN SPORTS','url',76,ART+'adriansports.png',FANART,'')
    addDir('UKTVNOW','url',77,ART+'uktvnow.png',FANART,'')
    addDir('ULTIMATEMANIA','url',78,ART+'ultimatemania.png',FANART,'')
    addDir('SPORTSNATIONHD','url',79,ART+'sportsnation.png',FANART,'')
    addDir('SPORTSMANIA','url',80,ART+'sportsmania.png',FANART,'')
    addDir('NJMSOCCER SPORTS','url',81,ART+'njmsoccer.png',FANART,'')    
    addDir('SPORTS MIX','url',82,ART+'sportsmix.png',FANART,'')
    addDir('DC SPORTS','url',83,ART+'dcsports.png',FANART,'')
    addDir('BULLDOG STREAMS','url',84,ART+'bulldog.png',FANART,'')
    addDir('MONEY SPORTS','url',85,ART+'moneysports.png',FANART,'')
    addDir('DAHENCHMAN SPORTS','url',86,ART+'dahenchmansports.png',FANART,'')
    addDir('EVOLVE SPORTS','url',87,ART+'evolvesports.png',FANART,'')
    addDir('SKY SPORTS VIDEO','url',88,ART+'ssv.png',FANART,'')
    addDir('CELTIC FC','url',89,ART+'celtic.png',FANART,'')
    addDir('PRO SPORT','url',90,ART+'prosport.png',FANART,'')
    addDir('MUCKY DUCK LIVE SPORTS','url',91,ART+'muckyducklivesports.png',FANART,'')
    addDir('MD SPORTS EXTRA','url',92,ART+'mdsports.png',FANART,'')
    addDir('ISRAELIVE SPORTS','url',25,ART+'israel.png',FANART,'')
    addDir('UK TURK','url',26,ART+'ukturk.png',FANART,'')
    setView('list', 'MAIN')

def LIVESPORTS():
    addDir('ADRIAN SPORTS - LIVE BPL','url',51,ART+'adriansports.png',FANART,'')
    addDir('CASTAWAY - LIVE SPORTS','url',52,ART+'castaway.png',FANART,'')
    addDir('NJM - MAGIC SPONGE','url',53,ART+'njm1.jpg',FANART,'')
    addDir('NJM - EXTRA TIME','url',54,ART+'njm2.jpg',FANART,'')
    addDir('COSMIX - LIVE EVENTS','url',55,ART+'cosmixevents.png',FANART,'')
    addDir('PHOENIX - VC EVENTS','url',56,ART+'vcevents.jpg',FANART,'')
    addDir('NJMLIVE - SPORTS EDITION','url',57,ART+'njmsoccer.png',FANART,'')
    addDir('BULLDOG STREAMS - ALL SECTIONS','url',58,ART+'bulldog.png',FANART,'')
    addDir('MONEY SPORTS - LIVE LINKS','url',59,ART+'moneysports1.jpg',FANART,'')
    addDir('DC SPORTS - LIVE UK SPORTS','url',60,ART+'dcsports1.png',FANART,'')
    addDir('SPORTS DEVIL - LIVE SPORTS','url',61,ART+'sportsdevil.png',FANART,'')
    addDir('HALOW - LIVE SPORT','url',62,ART+'halowsports1.jpg',FANART,'')
    addDir('HALOW - MATCHDAY 2016','url',63,ART+'halowsports2.jpg',FANART,'')
    addDir('DAHENCHMEN - LIVE EVENTS','url',64,ART+'dahenchmenevents.jpg',FANART,'')
    addDir('EVOLVE - SPORTS DAY','url',65,ART+'evolve1.png',FANART,'')
    addDir('EVOLVE - CORNERFLAG','url',66,ART+'evolve2.png',FANART,'')
    addDir('MONEY SPORTS  - SKY SPORTS NEWS','url',67,ART+'moneysports2.jpg',FANART,'')
    addDir('DC SPORTS - REQUESTS/EVENTS','url',68,ART+'dcsports2.jpg',FANART,'')
    addDir('ZEM STREAMHD - FOOTBALL','url',69,ART+'zemtv.png',FANART,'')
    addDir('ZEM STREAMHD - ALL SPORTS','url',70,ART+'zemtv.png',FANART,'')
    addDir('MD SPORTS EXTRA - LIVE','url',71,ART+'mdsports2.png',FANART,'')
    addDir('NJM - FLASH SPORTS','url',72,ART+'njm3.jpg',FANART,'')
    setView('list', 'MAIN')
    
def DOCUMENTARIES():
    addDir('RTN NEWS','url',103,ART+'rtnnews.png',FANART,'')
    addDir('BIOGRAPHY','url',104,ART+'biog.jpg',FANART,'')
    addDir('DOCUMENTARIES','url',105,ART+'documentaries',FANART,'')
    addDir('SPORTS DOCUMENTARIES','url',106,ART+'sportsdoc.jpg',FANART,'')
    addDir('ROCK DOCUMENTARIES','url',107,ART+'rockdoc.jpg',FANART,'')
    addDir('HORROR DOCUMENTARIES','url',108,ART+'horrordoc.jpg',FANART,'')
    addDir('DOC-FILM','url',109,ART+'docfilm.png',FANART,'')
    addDir('DOC-SERIES','url',110,ART+'docseries.png',FANART,'')
    addDir('DOC-MUSIC','url',111,ART+'docmusic.png',FANART,'')
    addDir('DOC-FOOD','url',112,ART+'docfood.png',FANART,'')
    addDir('GOLIATH','url',113,ART+'golliathdoc.png',FANART,'')
    addDir('FILMON DOCS','url',114,ART+'filmondoc.png',FANART,'')
    addDir('CCLOUD','url',115,ART+'cclouddoc.png',FANART,'')
    setView('list', 'MAIN')

def TVCATCHUP():
    addDir('BBC IPLAYER','url',27,ART+'bbciplayer.png',FANART,'')
    addDir('ITV PLAYER','url',28,ART+'itvplayer.png',FANART,'')
    addDir('SOAP CATCHUP','url',29,ART+'soapcatchup.png',FANART,'')
    addDir('UKTV PLAY','url',47,ART+'uktvplay.png',FANART,'')
    addDir('WE LOVE SOAPS','url',48,ART+'welovesoaps.png',FANART,'')
    addDir('X FACTOR UK','url',49,ART+'xfactor.png',FANART,'')
    setView('list', 'MAIN')

def KIDS():
    addDir('CARTOONHD','url',30,ART+'cartoonhd.png',FANART,'')
    addDir('KIDDIECARTOONS','url',31,ART+'kiddiecartoons.png',FANART,'')
    addDir('SUPERCARTOONS','url',32,ART+'supercartoons.png',FANART,'')
    addDir('CARTOON CRAZY','url',33,ART+'cartooncrazy.png',FANART,'')
    addDir('PHOENIX KIDS','url',34,ART+'phoenixkids.png',FANART,'')
    addDir('KIDS TUBE','url',35,ART+'kidstube.png',FANART,'')
    setView('list', 'MAIN')

def UFC():
    addDir('UFC LIVE','url',46,ART+'ufc5.png',FANART,'')
    addDir('UFC/BOXING REPLAYS','url',36,ART+'ufc1.png',FANART,'')
    addDir('UFC FIGHT NIGHT','url',37,ART+'ufc2.png',FANART,'')
    addDir('UFC MOVIES','url',38,ART+'ufc3.png',FANART,'')
    addDir('UFC DOCUMENTARIES','url',39,ART+'ufc4.png',FANART,'')
    addDir('UFC YOUTUBE','url',41,ART+'ufc6.png',FANART,'')
    addDir('ULTIMATE FIGHTER','url',42,ART+'ufc7.png',FANART,'')
    addDir('UFC RETRO','url',40,ART+'ufc1.png',FANART,'')
    addDir('UFC SELECT','url',43,ART+'ufc8.png',FANART,'')
    addDir('UFC ZONE','url',44,ART+'ufc9.jpg',FANART,'')
    setView('list', 'MAIN')

def REPLAY():
    addDir('ARES FOOTBALL','url',94,ART+'aresfootball.png',FANART,'')
    addDir('HALOW SPORTS REPLAYS','url',95,ART+'halowsports3.jpg',FANART,'')
    addDir('EFL - THE CHAMPIONSHIP','url',96,ART+'efl1.jpg',FANART,'')
    addDir('PREMIER LEAGUE','url',97,ART+'pl1.jpg',FANART,'')
    addDir('CUP COMPETITION HIGHLIGHTS','url',98,ART+'cch1.jpg',FANART,'')
    addDir('SKY SPORTS VIDEO','url',99,ART+'skysportsvideo2.png',FANART,'')
    addDir('PRO SPORT','url',100,ART+'prosport2.png',FANART,'')
    addDir('MUCKY DUCK HIGHLIGHTS','url',101,ART+'mdhighlights1.png',FANART,'')
    setView('list', 'MAIN')

def FISHING():
    addDir('FISHERMANS COVE','url',117,ART+'fishcove.png',FANART,'')
    addDir('FISHING TUBE','url',118,ART+'fishtube.png',FANART,'')
    addDir('VID TIME','url',119,ART+'fishvid.jpg',FANART,'')
    setView('list', 'MAIN')

def PHOENIXSPORTS():
    addDir('CHANNELS','url',17,ART+'phoenixchannels.png',FANART,'')
    addDir('EVENTS','url',18,ART+'phoenixevents.png',FANART,'')
    setView('list', 'MAIN')
	
def MAINTENANCE():
    addDir('DELETE CACHE','url',4,ART+'deletecache.png',FANART,'')
    addDir('FRESH START','url',6,ART+'freshstart.png',FANART,'')
    addDir('DELETE PACKAGES','url',7,ART+'deletepackages.png',FANART,'')
    setView('list', 'MAIN')


#################################
####### CHANNELS ########
#################################

def SPORTS1():
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10025,plugin://plugin.video.phstreams/?action=directory&url=http%3a%2f%2fphoenixtv.offshorepastebin.com%2ftv%2fevents.xml,return)")

def SPORTS2():
    import xbmc
    xbmc.executebuiltin("ActivateWindow(10025,plugin://plugin.video.phstreams/?action=directory&amp;url=http%3a%2f%2fphoenixtv.offshorepastebin.com%2ftv%2fevents.xml,return)")

def SPORTS3():
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10025,plugin://plugin.video.ZemTV-shani/?mode=13&amp;name=Sports&amp;url=Live,return)")

def SPORTS4():
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10025,plugin://plugin.video.castaway/?mode=live_sport,return)")

def SPORTS5():
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10025,plugin://plugin.video.NJMSoccer/?fanart&amp;mode=1&amp;url=http%3a%2f%2fnjmsoccer.kodistream.info%2fSiv7for21_NJMSoccer.xml,return)")

def SPORTS6():
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10025,plugin://plugin.video.LwSLive/?action=ndmode&amp;audio=0&amp;content=0&amp;name=LwS%20Sport%20Lists&amp;tvshow=0&amp;url=https%3a%2f%2farchive.org%2fdownload%2fLwSTesting%2fLwSLiveLinks.xml;iconimage=special://home/addons/plugin.video.LwSLive/icon.png,return)")

def SPORTS7():
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10025,plugin://plugin.video.MoneySports,return)")

def SPORTS8():
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10025,plugin://plugin.video.SportsDevil,return)")

def SPORTS9():
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10025,plugin://plugin.video.israelive/?categoryid=9999&amp;mode=2&amp;url,return))")

def SPORTS10():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.ukturk,return)')

def SPORTS11():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.communityallsorts/?fanart=http%3a%2f%2fwallpapercave.com%2fwp%2fzoU7uGD.jpg&mode=1&name=%5bB%5d%5bCOLOR%20blue%5d%2a%2a%2a%2a%2a%2a%2a%2a%5bB%5d%5bCOLOR%20white%5dSPORTS-ZONE%5bB%5d%5bCOLOR%20blue%5d%2a%2a%2a%2a%2a%2a%2a%2a%5b%2fB%5d%5b%2fCOLOR%5d&url=http%3a%2f%2fallsorts.kodi-pirates.tv%2fALLSORTS-FILES%2fSPORTS-MAIN.XML,return)')

def SPORTS12():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.AK-47/?mode=17&regexs=%7bu%27makelist%27%3a%20%7b%27listrepeat%27%3a%20u%27%5cr%5cn%3ctitle%3e%5bCOLOR%20red%5dAK%5b%2fCOLOR%5d%20%5bCOLOR%20yellow%5d-%5b%2fCOLOR%5d%20%5bCOLOR%20turquoise%5d47%5b%2fCOLOR%5d%20%5bCOLOR%20yellow%5d%5cxbb%5b%2fCOLOR%5d%20%5bCOLOR%20lime%5d%5bmakelist.param2%5d%5b%2fCOLOR%5d%3c%2ftitle%3e%5cr%5cn%3clink%3e%24doregex%5bselect_Url%5d%3c%2flink%3e%5cr%5cn%3cthumbnail%3ehttp%3a%2f%2frepo.run%2fzip%2frepository.Agent-47%2ficon.png%3c%2fthumbnail%3e%5cr%5cn%20%5cr%5cn%3cregex%3e%5cr%5cn%3cname%3eselect_Url%3c%2fname%3e%5cr%5cn%3cexpres%3e%24pyFunction%3a%20%5c%27%24doregex%5bget_sxstream%5d%7cUser-Agent%3dMozilla%2f5.0%20(Windows%20NT%2010.0%3b%20WOW64)%20AppleWebKit%2f537.36%20(KHTML%2c%20like%20Gecko)%20Chrome%2f48.0.2564.116%20Safari%2f537.36%5c%27%20if%20not%20%5c%27%24doregex%5bget_sxstream%5d%7cUser-Agent%3dMozilla%2f5.0%20(Windows%20NT%2010.0%3b%20WOW64)%20AppleWebKit%2f537.36%20(KHTML%2c%20like%20Gecko)%20Chrome%2f48.0.2564.116%20Safari%2f537.36%5c%27%3d%3d%5c%27%5c%27%20else%20%5c%27%24doregex%5bget_sxstream1%5d%7cUser-Agent%3diPhone%5c%27%3c%2fexpres%3e%5cr%5cn%3cpage%3e%3c%2fpage%3e%5cr%5cn%3c%2fregex%3e%5cr%5cn%20%5cr%5cn%3cregex%3e%5cr%5cn%3cname%3eget_sxstream%3c%2fname%3e%5cr%5cn%3cexpres%3esrc%3d.%2a%3f%5b%22%2c%5c%27%5d(.%2am3u8.%2a%3f)%5b%22%2c%5c%27%5d%3c%2fexpres%3e%5cr%5cn%3cpage%3ehttp%3a%2f%2fwww.liveonlinetv247.info%2fembed%2f%5bmakelist.param1%5d.php%3fwidth%3d650%26height%3d480%3c%2fpage%3e%5cr%5cn%3creferer%3ehttp%3a%2f%2fwww.liveonlinetv247.info%2f%3c%2freferer%3e%5cr%5cn%3cagent%3e%3c%2fagent%3e%5cr%5cn%3c%2fregex%3e%5cr%5cn%20%5cr%5cn%3cregex%3e%5cr%5cn%3cname%3eget_sxstream1%3c%2fname%3e%5cr%5cn%3cexpres%3esrc%3d.%2a%3f%5b%22%2c%5c%27%5d(.%2am3u8.%2a%3f)%5b%22%2c%5c%27%5d%3c%2fexpres%3e%5cr%5cn%3cpage%3ehttp%3a%2f%2fwww.liveonlinetv247.info%2fembed%2f%5bmakelist.param1%5d.php%3fwidth%3d650%26height%3d480%3c%2fpage%3e%5cr%5cn%3creferer%3ehttp%3a%2f%2fwww.liveonlinetv247.info%2f%3c%2freferer%3e%5cr%5cn%3cagent%3e%3c%2fagent%3e%5cr%5cn%3c%2fregex%3e%5cr%5cn%27%2c%20%27expres%27%3a%20u%27channel%3d(.%2a%3f)%22%3e(%5b%5e%5c%5c%3c%5d%2b)%27%2c%20%27name%27%3a%20u%27makelist%27%2c%20%27page%27%3a%20u%27http%3a%2f%2fwww.liveonlinetv247.info%2ftvchannels.php%27%7d%7d&url=%24doregex%5bmakelist%5d,return)')

def SPORTS13():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.ccloudtv/?iconimage=%2fUsers%2fgarethlovell%2fLibrary%2fApplication%20Support%2fKodi%2faddons%2fplugin.video.ccloudtv%2fresources%2ficons%2f%2fsports.png&mode=52&name=%5bCOLOR%20white%5dSports%5b%2fCOLOR%5d&url=sports,return)')

def SPORTS14():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.adriansports,return)')

def SPORTS15():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.ZemTV-shani/?mode=57&name=UKTVNow&url=sss,return)')

def SPORTS16():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.ultimatemania,return)')

def SPORTS17():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.sportsnationhdtv,return)')

def SPORTS18():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.sportsmania,return)')

def SPORTS19():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.NJMSoccer,return)')

def SPORTS20():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.sportsmix,return)')

def SPORTS21():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.DCSports,return)')

def SPORTS22():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.bulldogstreams,return)')

def SPORTS23():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.MoneySports,return)')

def SPORTS24():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.dahenchmen/?description&fanart=http%3a%2f%2fdahenchmen.xyz%2f01%2f1m4g3z%2fD4h3nchm3n%2ffanart.jpg&mode=1&name=%5bCOLOR%20lime%5d%5b%2fCOLOR%5d%5bCOLOR%20white%5d%20Sports%20%5b%2fCOLOR%5d%20%5bCOLOR%20red%5d%20%5b%2fCOLOR%5d&url=http%3a%2f%2fdahenchmen.xyz%2f01%2fD4Henchm3n%2fsp0rtz%2fsportz.xml,return)')

def SPORTS25():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.Evolve/?description&fanart=http%3a%2f%2fwww.matsbuilds.uk%2fpics%2fevolve%2ffanart.jpg&mode=1&name=%5bB%5d%5bCOLOR%20red%5dE%5b%2fCOLOR%5d%5bCOLOR%20white%5dvolve%5b%2fCOLOR%5d%20%20%5bCOLOR%20red%5dS%5b%2fCOLOR%5d%5bCOLOR%20white%5dports%5b%2fCOLOR%5d%5b%2fB%5d&url=http%3a%2f%2fwww.matsbuilds.uk%2fabe%2fevolve_main.xml,return)')

def SPORTS26():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.skysports,return)')

def SPORTS27():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.DCSports/?fanart=http%3a%2f%2fgoo.gl%2fvw6qo5&mode=1&name=Celtic%20FC&url=https%3a%2f%2fgoo.gl%2fnO9AHD,return)')

def SPORTS28():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.prosport,return)')

def SPORTS29():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.mdsportsextra/?description&mode=10&name=%5bCOLOR%20white%5dLive%20Scores%5b%2fCOLOR%5d&url=http%3a%2f%2fwww.scorespro.com%2frss%2flive-soccer.xml,return)')

def SPORTS30():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.mdsportsextra,return)')

def LIVESPORTS1():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.adriansports/?fanart=https%3a%2f%2fgoo.gl%2fkw8Rmg&mode=1&name=LIVE%20BPL&url=https%3a%2f%2fgitlab.com%2fadrian1730%2fAdrian_Sports%2fraw%2fmaster%2fList%2fLIVE-BPL%3fprivate_token%3dMGo-s_Q1qNTQwVJc8RQT,return)')

def LIVESPORTS2():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.castaway/?mode=live_sport,return)')

def LIVESPORTS3():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.NJMSoccer/?fanart&mode=1&name=%5bB%5d---%3d%3d%3d%5bCOLOR%20red%5dMAGIC%5b%2fCOLOR%5d%5bCOLOR%20blue%5d%20SPONGE%5b%2fCOLOR%5d%3d%3d%3d---%5b%2fB%5d&url=http%3a%2f%2fnjmsoccer.ares-project.com%2frh_matchday.xml,return)')

def LIVESPORTS4():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.NJMSoccer/?fanart&mode=1&name=%5bB%5d---%3d%3d%3d%5bCOLOR%20red%5dEXTRA%5b%2fCOLOR%5d%5bCOLOR%20blue%5d%20TIME%5b%2fCOLOR%5d%3d%3d%3d---%5b%2fB%5d&url=http%3a%2f%2fnjmsoccer.ares-project.com%2fSiv7for21_NJMSoccer.xml,return)')

def LIVESPORTS5():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.phstreams/?action=directory&url=http%3a%2f%2fbit.ly%2fCosmix-New-Events,return)')

def LIVESPORTS6():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.phstreams/?action=directory&url=http%3a%2f%2fvalhalla.offshorepastebin.com%2fVCc%2fVC%2520events.xml,return)')

def LIVESPORTS7():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.NJMLive,return)')

def LIVESPORTS8():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.bulldogstreams,return)')

def LIVESPORTS9():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.MoneySports/?fanart=http%3a%2f%2fi65.tinypic.com%2fbbtld.jpg&mode=1&name=LIVE%20SPORTS%20LINKS&url=https%3a%2f%2fraw.githubusercontent.com%2fWALKINGDEAD987456%2frick%2fmaster%2flive,return)')

def LIVESPORTS10():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.DCSports/?fanart=http%3a%2f%2fgoo.gl%2fXdF28T&mode=1&name=Live%20UK%20Sports&url=https%3a%2f%2fgoo.gl%2f8wGGXm,return)')

def LIVESPORTS11():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.SportsDevil/?item=title%3dLive%2bSports%26url%3dlivesports.cfg%26definedIn%3dmainMenu.cfg%26director%3dSportsDevil%26genre%3dLive%2bSports%26type%3drss%26&mode=1,return)')

def LIVESPORTS12():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.Test/?fanart&mode=1&name=%5bCOLOR%20royalblue%5d%5bB%5dLIVE%20SPORT%5b%2fB%5d%5b%2fCOLOR%5d&url=http%3a%2f%2fhalowtv.org%2fHALOWXML%2fkurd1.xml,return)')

def LIVESPORTS13():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.Test/?fanart&mode=1&name=%5bCOLOR%20royalblue%5d%5bB%5dMATCH%20DAY%202016%20%5b%2fB%5d%5b%2fCOLOR%5d&url=http%3a%2f%2fhalowtv.org%2fHALOWXML%2fmatcday.xml,return)')

def LIVESPORTS14():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.dahenchmen/?description&fanart=http%3a%2f%2fdahenchmen.xyz%2f01%2fD4Henchm3n%2f1m4g3z%2fD4h3nchm3n%2ffanart.jpg&mode=1&name=%5bCOLOR%20white%5d%20Live%20Events%5b%2fCOLOR%5d&url=http%3a%2f%2fdahenchmen.xyz%2f01%2fD4Henchm3n%2fl1v3%2fl1v3.xml,return)')

def LIVESPORTS15():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.Evolve/?description&fanart=http%3a%2f%2fi.imgur.com%2f0pxYoFB.png&mode=1&name=%5bB%5d%5bCOLOR%20red%5dSports%20%5b%2fCOLOR%5d%5bCOLOR%20white%5dDay%5b%2fCOLOR%5d%5b%2fB%5d&url=http%3a%2f%2fwww.matsbuilds.uk%2fabe%2fevolve_day.xml,return)')

def LIVESPORTS16():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.Evolve/?description&fanart=http%3a%2f%2fi.imgur.com%2fNPwQVGl.png&mode=1&name=%5bB%5d%5bCOLOR%20red%5dCorner%5b%2fCOLOR%5d%5bCOLOR%20white%5d%20Flag%5b%2fCOLOR%5d%5b%2fB%5d&url=http%3a%2f%2fwww.matsbuilds.uk%2fabe%2fevolve_corner.xml,return)')

def LIVESPORTS17():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.MoneySports/?fanart=http%3a%2f%2fi65.tinypic.com%2fbbtld.jpg&mode=1&name=SPORTS%20NEWS&url=https%3a%2f%2fraw.githubusercontent.com%2fWALKINGDEAD987456%2frick%2fmaster%2fnewshq,return)')

def LIVESPORTS18():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.DCSports/?fanart=http%3a%2f%2fgoo.gl%2fBB2HHf&mode=1&name=Requests%2fEvents&url=https%3a%2f%2fgoo.gl%2fp4ssDK,return)')

def LIVESPORTS19():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.ZemTV-shani/?mode=76&name=Footbal&url=http%3a%2f%2fwww.streamhd.eu%2ffootball%2f,return)')

def LIVESPORTS20():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.ZemTV-shani/?mode=76&name=All%20sports&url=http%3a%2f%2fwww.streamhd.eu%2f,return)')

def LIVESPORTS21():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.mdsportsextra/?description&mode=91&name=%5bCOLOR%20white%5dLive%5b%2fCOLOR%5d&url=http%3a%2f%2fwww.liveonlinetv247.info%2ftvchannels.php,return)')

def LIVESPORTS22():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.NJMSoccer/?fanart&mode=1&name=%5bB%5d---%3d%3d%3d%5bCOLOR%20red%5dFLASH%5b%2fCOLOR%5d%5bCOLOR%20blue%5d%20SPORTS%5b%2fCOLOR%5d%3d%3d%3d---%5b%2fB%5d&url=http%3a%2f%2fnjmsoccer.ares-project.com%2frh_matchday.xml,return)')

def REPLAY1():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.AresFootBall,return)')

def REPLAY2():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.Test/?fanart&mode=53&name=%5bCOLOR%20royalblue%5d%5bB%5dSports%20Replays%20%5b%2fB%5d%5b%2fCOLOR%5d&url=plugin%3a%2f%2fplugin.video.footballreplays,return)')

def REPLAY3():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.MoneySports/?fanart=http%3a%2f%2fi65.tinypic.com%2fbbtld.jpg&mode=1&name=EFL%20GOALS%20AND%20HIGHLIGHTS&url=https%3a%2f%2fraw.githubusercontent.com%2fWALKINGDEAD987456%2frick%2fmaster%2fprem,return)')

def REPLAY4():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.MoneySports/?fanart=http%3a%2f%2fi65.tinypic.com%2fbbtld.jpg&mode=1&name=PREMIER%20LEAGUE%20GOALS%20AND%20HIGHLIGHTS&url=https%3a%2f%2fraw.githubusercontent.com%2fWALKINGDEAD987456%2frick%2fmaster%2fchamp,return)')

def REPLAY5():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.MoneySports/?fanart=http%3a%2f%2fi65.tinypic.com%2fbbtld.jpg&mode=1&name=%5bCOLOR%20yellow%5d2016%2f17%5b%2fCOLOR%5d%20CUP%20COMPETITION%20HIGHLIGHTS&url=https%3a%2f%2fraw.githubusercontent.com%2fWALKINGDEAD987456%2frick%2fmaster%2fCUPS,return)')

def REPLAY6():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.skysports,return)')

def REPLAY7():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.prosport,return)')

def REPLAY8():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.mdsportsextra/?description&mode=23&name=%5bCOLOR%20white%5dHighlights%5b%2fCOLOR%5d&url=http%3a%2f%2fwww.okgoals.com%2f,return)')

def DOCUMENTARIES1():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.rt,return)')

def DOCUMENTARIES2():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.phstreams/?action=directory&url=http%3a%2f%2fone242415.offshorepastebin.com%2fCollections%2fbiography.xml,return)')

def DOCUMENTARIES3():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.phstreams/?action=directory&url=http%3a%2f%2fone242415.offshorepastebin.com%2fMisc%2fdocs.xml,return)')

def DOCUMENTARIES4():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.phstreams/?action=directory&url=http%3a%2f%2fone242415.offshorepastebin.com%2fMisc%2fsportdocs.xml,return)')

def DOCUMENTARIES5():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.phstreams/?action=directory&url=http%3a%2f%2fone242415.offshorepastebin.com%2fCollections%2frockdoc.xml,return)')

def DOCUMENTARIES6():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.phstreams/?action=directory&url=http%3a%2f%2fone242415.offshorepastebin.com%2fCollections%2fparanormal.xml,return)')

def DOCUMENTARIES7():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.phstreams/?action=directory&url=http%3a%2f%2ftnpb.offshorepastebin.com%2fDocs%2fFilm.xml,return)')

def DOCUMENTARIES8():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.phstreams/?action=directory&url=http%3a%2f%2ftnpb.offshorepastebin.com%2fDirectories%2fDocs%2520Directories%2fDocu%2520Series%2520Directory.xml,return)')

def DOCUMENTARIES9():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.phstreams/?action=directory&url=http%3a%2f%2ftnpb.offshorepastebin.com%2fDirectories%2fDocs%2520Directories%2fDocu%2520Music%2520Directory.xml,return)')

def DOCUMENTARIES10():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.phstreams/?action=directory&url=http%3a%2f%2ftnpb.offshorepastebin.com%2fDirectories%2fDocs%2520Directories%2fDocu%2520Food%2520Directory.xml,return)')

def DOCUMENTARIES11():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.Evolve/?description&fanart=http%3a%2f%2fwww.matsbuilds.co.uk%2fpics%2fevolve%2ffanart.jpg&mode=1&name=%5bB%5d%5bCOLOR%20red%5dD%5b%2fCOLOR%5d%5bCOLOR%20white%5documentaries%5b%2fCOLOR%5d%5b%2fB%5d&url=http%3a%2f%2fpastebin.com%2fraw%2fbAd5cCRm,return)')

def DOCUMENTARIES12():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.F.T.V/?ch_fanart=documentary&description=2786%2c4304%2c2954%2c3608%2c4166%2c4172%2c4184%2c4283%2c2710%2c381%2c3548%2c3554%2c3569&mode=123&name=DOCUMENTARY&url=32,return)')

def DOCUMENTARIES13():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.ccloudtv/?mode=54&name=%5bCOLOR%20royalblue%5d%5bB%5dDocumentary%5b%2fB%5d%5b%2fCOLOR%5d&url=documentary,return)')

def FISHING1():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.fishermanscove,return)')

def FISHING2():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.fishingtube,return)')

def FISHING3():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.VidTime,return)')

def TVCATCHUP1():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.iplayerwww,return)')

def TVCATCHUP2():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.itv,return)')

def TVCATCHUP3():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.SoapCatchup,return)')

def TVCATCHUP4():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.uktvplay,return)')

def TVCATCHUP5():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.welovesoaps,return)')

def TVCATCHUP6():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.xfactoruk,return)')

def KIDS1():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.cartoonhd,return)')

def KIDS2():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.kiddiecartoons,return)')

def KIDS3():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.supercartoons,return)')

def KIDS4():
    import xbmc
    xbmc.executebuiltin('ActivateWindow(10025,plugin://plugin.video.phstreams/?action=cartoon,return)')

def KIDS5():
    import xbmc
    xbmc.executebuiltin('ActivateWindow(10025,plugin://plugin.video.phstreams/?action=directory&amp;url=http%3a%2f%2ftnpb.offshorepastebin.com%2fDirectories%2fMain%2520Directory%2fKids%2520Main.xml,return)')

def KIDS6():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.kids-tube,return)')

def UFC1():
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10025,plugin://plugin.video.communityallsorts/?fanart=http%3a%2f%2fwww.lumbre.tv%2fimages%2fuploads%2fmodule-images%2fo_19iuu1nc51f3q1e981coa1n9r1a88t___UFC_PICS_05.jpg&mode=1&name=%5bB%5d%5bCOLOR%20blue%5d%2a%2a%2a%2a%2a%2a%2a%2a%20%5bB%5d%5bCOLOR%20white%5d%20UFC%20%26%20BOXING%7eRING%20%5bB%5d%5bCOLOR%20blue%5d%20%2a%2a%2a%2a%2a%2a%2a%2a%5b%2fB%5d%5b%2fCOLOR%5d&url=http%3a%2f%2fallsorts.kodi-pirates.tv%2fALLSORTS-FILES%2fUFC-BOXING.XML,return)")

def UFC2():
    import xbmc
    xbmc.executebuiltin("ReplaceWindow(10025,plugin://plugin.video.ufc-finest/?description&fanart=http%3a%2f%2fdkrepo.netai.net%2fUltimateUfc%2fUFC%2520Art%2fOther%2fUfcFightnight.jpg&mode=1&name=%5bCOLOR%20white%5d%5bB%5dUFC%5b%2fB%5d%5b%2fCOLOR%5d%20%5bCOLOR%20red%5d%5bB%5dFight%5b%2fB%5d%5b%2fCOLOR%5d%20%5bCOLOR%20white%5d%5bB%5dNight%5b%2fB%5d%5b%2fCOLOR%5d&url=http%3a%2f%2fdkrepo.netai.net%2fUltimateUfc%2fufcfights.xml,return)")

def UFC3():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.ufc-finest/?description&fanart=http%3a%2f%2fdkrepo.netai.net%2fUltimateUfc%2fUFC%2520Art%2fUFCMovies%2fMoviesfanart.jpg&mode=1&name=%5bCOLOR%20white%5d%5bB%5dUFC%5b%2fB%5d%5b%2fCOLOR%5d%20%5bCOLOR%20red%5d%5bB%5dMovies%5b%2fB%5d%5b%2fCOLOR%5d&url=http%3a%2f%2fdkrepo.netai.net%2fUltimateUfc%2fMovies.xml,return)')

def UFC4():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.ufc-finest/?description&fanart=http%3a%2f%2fdkrepo.netai.net%2fUltimateUfc%2fUFC%2520Art%2fOther%2fdocs.jpg&mode=1&name=%5bCOLOR%20white%5d%5bB%5dUFC%5b%2fB%5d%5b%2fCOLOR%5d%20%5bCOLOR%20red%5d%5bB%5dDocumentaries%5b%2fB%5d%5b%2fCOLOR%5d&url=http%3a%2f%2fdkrepo.netai.net%2fUltimateUfc%2fDocumentry.xml,return)')

def UFC5():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.ufc-finest/?description&fanart=http%3a%2f%2fdkrepo.netai.net%2fUltimateUfc%2fUFC%2520Art%2fOther%2fRetro.jpg&mode=1&name=%5bCOLOR%20white%5d%5bB%5dUFC%5b%2fB%5d%5b%2fCOLOR%5d%20%5bCOLOR%20red%5d%5bB%5dRetro%5b%2fB%5d%5b%2fCOLOR%5d&url=http%3a%2f%2fdkrepo.netai.net%2fUltimateUfc%2fretro.xml,return)')

def UFC6():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.ufc-finest/?description&fanart=http%3a%2f%2fdkrepo.netai.net%2fUltimateUfc%2fUFC%2520Art%2fOther%2fufcyoutube.jpg&mode=1&name=%5bCOLOR%20white%5d%5bB%5dUFC%5b%2fB%5d%5b%2fCOLOR%5d%20%5bCOLOR%20red%5d%5bB%5dYoutube%5b%2fB%5d%5b%2fCOLOR%5d&url=http%3a%2f%2fdkrepo.netai.net%2fUltimateUfc%2fYou%2520Tube.xml,return)')

def UFC7():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.ufc-finest/?description&fanart=http%3a%2f%2fdkrepo.netai.net%2fUltimateUfc%2fUFC%2520Art%2fOther%2fUltimate.jpg&mode=1&name=%5bCOLOR%20white%5d%5bB%5dUltimate%5b%2fB%5d%5b%2fCOLOR%5d%20%5bCOLOR%20red%5d%5bB%5dFighter%5b%2fB%5d%5b%2fCOLOR%5d&url=http%3a%2f%2fdkrepo.netai.net%2fUltimateUfc%2fUltimate.xml,return)')

def UFC8():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.ufc-finest/?description&fanart=http%3a%2f%2fdkrepo.netai.net%2fUltimateUfc%2fUFC%2520Art%2fOther%2fUFC%2520Select.jpg&mode=1&name=%5bCOLOR%20white%5d%5bB%5dUFC%5b%2fB%5d%5b%2fCOLOR%5d%20%5bCOLOR%20red%5d%5bB%5dSelect%5b%2fB%5d%5b%2fCOLOR%5d&url=http%3a%2f%2fdkrepo.netai.net%2fUltimateUfc%2fRandoms.xml,return)')

def UFC9():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.Evolve/?description&fanart=http%3a%2f%2fi.imgur.com%2f0pxYoFB.png&mode=1&name=%5bB%5d%5bCOLOR%20red%5dUFC%20%5b%2fCOLOR%5d%5bCOLOR%20white%5dZone%5b%2fCOLOR%5d%5b%2fB%5d&url=http%3a%2f%2fwww.matsbuilds.uk%2fabe%2fevolve_ufc.xml,return)')

def UFC10():
    import xbmc
    xbmc.executebuiltin('ReplaceWindow(10025,plugin://plugin.video.ufc-finest/?description&fanart=http%3a%2f%2fdkrepo.netai.net%2fUltimateUfc%2fUFC%2520Art%2fUFCtv%2fUFCtv.jpg&mode=1&name=%5bCOLOR%20white%5d%5bB%5dUFC%5b%2fB%5d%5b%2fCOLOR%5d%20%5bCOLOR%20red%5d%5bB%5dLive%5b%2fB%5d%5b%2fCOLOR%5d&url=http%3a%2f%2fdkrepo.netai.net%2fUltimateUfc%2fUFCTv.xml,return)')


#################################
####### POPUP TEXT BOXES ########
#################################

def TextBoxes(heading,announce):
  class TextBox():
    WINDOW=10147
    CONTROL_LABEL=1
    CONTROL_TEXTBOX=5
    def __init__(self,*args,**kwargs):
      xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
      self.win=xbmcgui.Window(self.WINDOW) # get window
      xbmc.sleep(500) # give window time to initialize
      self.setControls()
    def setControls(self):
      self.win.getControl(self.CONTROL_LABEL).setLabel(heading) # set heading
      try: f=open(announce); text=f.read()
      except: text=announce
      self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
      return
  TextBox()

def facebook():
    TextBoxes('Kamui Unblocker', 'Welcome to Kamui')
        
    

#################################
####BUILD INSTALL################
#################################

def WIZARD(name,url,description):
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("Kamui Unblocker","Downloading ",'', 'Please Wait')
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"", "Extracting,")
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    dialog = xbmcgui.Dialog()
    dialog.ok("Kamui Unblocker", "To save changes you now need to force close Kodi, Press OK to force close Kodi")
    killxbmc()



################################
###DELETE PACKAGES##############
####THANKS GUYS @ XUNITY########

def DeletePackages(url):
    print '############################################################       DELETING PACKAGES             ###############################################################'
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
    try:    
        for root, dirs, files in os.walk(packages_cache_path):
            file_count = 0
            file_count += len(files)
            
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Package Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                            
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                    dialog = xbmcgui.Dialog()
                    dialog.ok("Kamui Unblocker", "Packages Successfuly Removed", "[COLOR yellow]Brought To You By Kamui[/COLOR]")
    except: 
        dialog = xbmcgui.Dialog()
        dialog.ok("Kamui Unblocker", "Sorry we were not able to remove Package Files", "[COLOR yellow]Brought To You By Kamui[/COLOR]")
    


#################################
###DELETE CACHE##################
####THANKS GUYS @ XUNITY########
	
def deletecachefiles(url):
    print '############################################################       DELETING STANDARD CACHE             ###############################################################'
    xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'), 'cache')
    if os.path.exists(xbmc_cache_path)==True:    
        for root, dirs, files in os.walk(xbmc_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        try:
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'Other'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'LocalAndRental'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
              # Set path to Cydia Archives cache files
                             

    # Set path to What th Furk cache files
    wtf_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk/cache'), '')
    if os.path.exists(wtf_cache_path)==True:    
        for root, dirs, files in os.walk(wtf_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete WTF Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
                
                # Set path to 4oD cache files
    channel4_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.4od/cache'), '')
    if os.path.exists(channel4_cache_path)==True:    
        for root, dirs, files in os.walk(channel4_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete 4oD Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
                
                # Set path to BBC iPlayer cache files
    iplayer_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache'), '')
    if os.path.exists(iplayer_cache_path)==True:    
        for root, dirs, files in os.walk(iplayer_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete BBC iPlayer Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
                
                
                # Set path to Simple Downloader cache files
    downloader_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/script.module.simple.downloader'), '')
    if os.path.exists(downloader_cache_path)==True:    
        for root, dirs, files in os.walk(downloader_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Simple Downloader Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
                
                # Set path to ITV cache files
    itv_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.itv/Images'), '')
    if os.path.exists(itv_cache_path)==True:    
        for root, dirs, files in os.walk(itv_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ITV Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
				
                # Set path to temp cache files
    temp_cache_path = os.path.join(xbmc.translatePath('special://home/temp'), '')
    if os.path.exists(temp_cache_path)==True:    
        for root, dirs, files in os.walk(temp_cache_path):
            file_count = 0
            file_count += len(files)
        
        # Count files and give option to delete
            if file_count > 0:
    
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete TEMP dir Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
				

    dialog = xbmcgui.Dialog()
    dialog.ok("Kamui Unblocker", " All Cache Files Removed", "[COLOR yellow]Brought To You By Kamui[/COLOR]")
 
        
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

###############################################################
###FORCE CLOSE KODI - ANDROID ONLY WORKS IF ROOTED#############
#######LEE @ COMMUNITY BUILDS##################################

def killxbmc():
	choice = plugintools.message_yes_no('Force Close Kodi', 'You are about to close Kodi','Would you like to continue?')
	if choice == 0:
		return
	elif choice == 1:
		pass
	myplatform = platform()
	print "Platform: " + str(myplatform)

	try:
		os._exit(1)
	except:
		pass

	if myplatform == 'osx':  # OSX
		print "############   try osx force close  #################"
		try:
			os.system('killall -9 XBMC')
		except:
			pass
		try:
			os.system('killall -9 Kodi')
		except:
			pass
		plugintools.message(AddonTitle, "If you\'re seeing this message it means the force close","was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.", '')
	elif myplatform == 'linux':  # Linux
		print "############   try linux force close  #################"
		try:
			os.system('killall XBMC')
		except:
			pass
		try:
			os.system('killall Kodi')
		except:
			pass
		try:
			os.system('killall -9 xbmc.bin')
		except:
			pass
		try:
			os.system('killall -9 kodi.bin')
		except:
			pass
		plugintools.message(AddonTitle, "If you\'re seeing this message it means the force close","was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.", '')
	elif myplatform == 'android':  # Android

		print "############   try android force close  #################"

		try:
			os._exit(1)
		except:
			pass
		try:
			os.system('adb shell am force-stop org.xbmc.kodi')
		except:
			pass
		try:
			os.system('adb shell am force-stop org.kodi')
		except:
			pass
		try:
			os.system('adb shell am force-stop org.xbmc.xbmc')
		except:
			pass
		try:
			os.system('adb shell am force-stop org.xbmc')
		except:
			pass
		try:
			os.system('adb shell am force-stop com.semperpax.spmc16')
		except:
			pass
		try:
			os.system('adb shell am force-stop com.spmc16')
		except:
			pass
		time.sleep(5)
		plugintools.message(AddonTitle,"Press the HOME button on your remote and [COLOR=red][b]FORCE STOP[/b][/COLOR] KODI via the Manage Installed Applications menu in settings on your Amazon home page then re-launch KODI")
	elif myplatform == 'windows':  # Windows
		print "############   try windows force close  #################"
		try:
			os.system('@ECHO off')
			os.system('tskill XBMC.exe')
		except:
			pass
		try:
			os.system('@ECHO off')
			os.system('tskill Kodi.exe')
		except:
			pass
		try:
			os.system('@ECHO off')
			os.system('TASKKILL /im Kodi.exe /f')
		except:
			pass
		try:
			os.system('@ECHO off')
			os.system('TASKKILL /im XBMC.exe /f')
		except:
			pass
		plugintools.message(AddonTitle, "If you\'re seeing this message it means the force close","was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.", "Use task manager and NOT ALT F4")
	else:  # ATV
		print "############   try atv force close  #################"
		try:
			os.system('killall AppleTV')
		except:
			pass
		print "############   try raspbmc force close  #################"  # OSMC / Raspbmc
		try:
			os.system('sudo initctl stop kodi')
		except:
			pass
		try:
			os.system('sudo initctl stop xbmc')
		except:
			pass
		plugintools.message(AddonTitle, "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.","iOS detected.  Press and hold both the Sleep/Wake and Home button for at least 10 seconds, until you see the Apple logo.")


# Get Current platform
def platform():
	if xbmc.getCondVisibility('system.platform.android'):
		return 'android'
	elif xbmc.getCondVisibility('system.platform.linux'):
		return 'linux'
	elif xbmc.getCondVisibility('system.platform.windows'):
		return 'windows'
	elif xbmc.getCondVisibility('system.platform.osx'):
		return 'osx'
	elif xbmc.getCondVisibility('system.platform.atv2'):
		return 'atv2'
	elif xbmc.getCondVisibility('system.platform.ios'):
		return 'ios'   

##########################
###DETERMINE PLATFORM#####
##########################
        
def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'
    
############################
###FRESH START##############
####THANKS TO TVADDONS######

def FRESHSTART(params):
    plugintools.log("freshstart.main_list "+repr(params)); yes_pressed=plugintools.message_yes_no(AddonTitle,"Do you wish to restore your","Kodi configuration to default settings?")
    if yes_pressed:
        addonPath=xbmcaddon.Addon(id=AddonID).getAddonInfo('path'); addonPath=xbmc.translatePath(addonPath); 
        xbmcPath=os.path.join(addonPath,"..",".."); xbmcPath=os.path.abspath(xbmcPath); plugintools.log("freshstart.main_list xbmcPath="+xbmcPath); failed=False
        try:
            for root, dirs, files in os.walk(xbmcPath,topdown=True):
                dirs[:] = [d for d in dirs if d not in EXCLUDES]
                for name in files:
                    try: os.remove(os.path.join(root,name))
                    except:
                        if name not in ["Addons15.db","MyVideos75.db","Textures13.db","xbmc.log"]: failed=True
                        plugintools.log("Error removing "+root+" "+name)
                for name in dirs:
                    try: os.rmdir(os.path.join(root,name))
                    except:
                        if name not in ["Database","userdata"]: failed=True
                        plugintools.log("Error removing "+root+" "+name)
            if not failed: plugintools.log("freshstart.main_list All user files removed, you now have a clean install"); plugintools.message(AddonTitle,"The process is complete, you're now back to a fresh Kodi configuration with Kamui","Please reboot your system or restart Kodi in order for the changes to be applied.")
            else: plugintools.log("freshstart.main_list User files partially removed"); plugintools.message(AddonTitle,"The process is complete, you're now back to a fresh Kodi configuration with Kamui","Please reboot your system or restart Kodi in order for the changes to be applied.")
        except: plugintools.message(AddonTitle,"Problem found","Your settings has not been changed"); import traceback; plugintools.log(traceback.format_exc()); plugintools.log("freshstart.main_list NOT removed")
        plugintools.add_item(action="",title="Now Exit Kodi",folder=False)
    else: plugintools.message(AddonTitle,"Your settings","has not been changed"); plugintools.add_item(action="",title="Done",folder=False)

          
        
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
T = base64.decodestring('L2FkZG9ucy50eHQ=')
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

elif mode==8:
       NORMAL()
       
elif mode==9:
       ANIME()

elif mode==10:
       FIXES()

elif mode==12:
       CHANNELS()

elif mode==13:
       SPORTS()

elif mode==14:
       TVCATCHUP()

elif mode==15:
       KIDS()

elif mode==16:
       PHOENIXSPORTS()

elif mode==17:
       SPORTS1()

elif mode==18:
       SPORTS2()

elif mode==19:
       SPORTS3()

elif mode==20:
       SPORTS4()

elif mode==21:
       SPORTS5()

elif mode==22:
       SPORTS6()

elif mode==23:
       SPORTS7()

elif mode==24:
       SPORTS8()

elif mode==25:
       SPORTS9()

elif mode==26:
       SPORTS10()

elif mode==73:
       SPORTS11()

elif mode==74:
       SPORTS12()

elif mode==75:
       SPORTS13()

elif mode==76:
       SPORTS14()

elif mode==77:
       SPORTS15()

elif mode==78:
       SPORTS16()

elif mode==79:
       SPORTS17()

elif mode==80:
       SPORTS18()

elif mode==81:
       SPORTS19()

elif mode==82:
       SPORTS20()

elif mode==83:
       SPORTS21()

elif mode==84:
       SPORTS22()

elif mode==85:
       SPORTS23()

elif mode==86:
       SPORTS24()

elif mode==87:
       SPORTS25()

elif mode==88:
       SPORTS26()

elif mode==89:
       SPORTS27()

elif mode==90:
       SPORTS28()

elif mode==91:
       SPORTS29()
	   
elif mode==92:
       SPORTS30()

elif mode==27:
       TVCATCHUP1()

elif mode==28:
       TVCATCHUP2()

elif mode==29:
       TVCATCHUP3()

elif mode==30:
       KIDS1()

elif mode==31:
       KIDS2()

elif mode==32:
       KIDS3()

elif mode==33:
       KIDS4()

elif mode==34:
       KIDS5()

elif mode==35:
       KIDS6()

elif mode==36:
       UFC1()

elif mode==37:
       UFC2()
       
elif mode==38:
       UFC3()
       
elif mode==39:
       UFC4()
       
elif mode==40:
       UFC5()

elif mode==41:
       UFC6()

elif mode==42:
       UFC7()

elif mode==43:
       UFC8()

elif mode==44:
       UFC9()

elif mode==45:
        UFC()

elif mode==46:
       UFC10()

elif mode==47:
       TVCATCHUP4()

elif mode==48:
       TVCATCHUP5()

elif mode==49:
       TVCATCHUP6()

elif mode==50:
       LIVESPORTS()

elif mode==51:
       LIVESPORTS1()

elif mode==52:
       LIVESPORTS2()
       
elif mode==53:
       LIVESPORTS3()
       
elif mode==54:
       LIVESPORTS4()
       
elif mode==55:
       LIVESPORTS5()

elif mode==56:
       LIVESPORTS6()

elif mode==57:
       LIVESPORTS7()

elif mode==58:
       LIVESPORTS8()

elif mode==59:
       LIVESPORTS9()

elif mode==60:
       LIVESPORTS10()

elif mode==61:
       LIVESPORTS11()

elif mode==62:
       LIVESPORTS12()

elif mode==63:
       LIVESPORTS13()

elif mode==64:
       LIVESPORTS14()

elif mode==65:
       LIVESPORTS15()

elif mode==66:
       LIVESPORTS16()

elif mode==67:
       LIVESPORTS17()

elif mode==68:
       LIVESPORTS18()

elif mode==69:
       LIVESPORTS19()

elif mode==70:
       LIVESPORTS20()

elif mode==71:
       LIVESPORTS21()

elif mode==72:
       LIVESPORTS22()

elif mode==93:
       REPLAY()

elif mode==94:
       REPLAY1()

elif mode==95:
       REPLAY2()

elif mode==96:
       REPLAY3()

elif mode==97:
       REPLAY4()

elif mode==98:
       REPLAY5()

elif mode==99:
       REPLAY6()

elif mode==100:
       REPLAY7()

elif mode==101:
       REPLAY8()

elif mode==102:
       DOCUMENTARIES()

elif mode==103:
       DOCUMENTARIES1()

elif mode==104:
       DOCUMENTARIES2()

elif mode==105:
       DOCUMENTARIES3()

elif mode==106:
       DOCUMENTARIES4()

elif mode==107:
       DOCUMENTARIES5()

elif mode==108:
       DOCUMENTARIES6()

elif mode==109:
       DOCUMENTARIES7()

elif mode==110:
       DOCUMENTARIES8()

elif mode==111:
       DOCUMENTARIES9()

elif mode==112:
       DOCUMENTARIES10()

elif mode==113:
       DOCUMENTARIES11()

elif mode==114:
       DOCUMENTARIES12()

elif mode==115:
       DOCUMENTARIES13()

elif mode==116:
       FISHING()

elif mode==117:
       FISHING1()

elif mode==118:
       FISHING2()

elif mode==119:
       FISHING3()
       
elif mode==11:
       DELETEIVUEDB()

        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
