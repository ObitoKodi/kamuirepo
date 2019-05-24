import sys, urllib, urllib2, cookielib, json, os, re, urlparse, time, ast
from string import digits
import xbmcaddon, xbmc, xbmcgui, xbmcplugin
import requests
from tvdb_api import Tvdb

sysarg=str(sys.argv[1])
ADDON_ID='plugin.video.soggysandwich'
addon=xbmcaddon.Addon(id=ADDON_ID)
home=xbmc.translatePath(addon.getAddonInfo('path').decode('utf-8'))

libraryDir=xbmc.translatePath(xbmcaddon.Addon().getSetting('download'))
if not os.path.exists(libraryDir):
    os.makedirs(libraryDir)

def parseParameters(inputString=sys.argv[2]):
    parameters = {}
    p1 = inputString.find('?')
    if p1 >= 0:
        splitParameters = inputString[p1 + 1:].split('&')
        for nameValuePair in splitParameters:
            try:
                if (len(nameValuePair) > 0):
                    pair = nameValuePair.split('=')
                    key = pair[0]
                    value = urllib.unquote(urllib.unquote_plus(pair[1])).decode('utf-8')
                    parameters[key] = value
                    #logError(value)
            except:
                pass
    return parameters

def logError(error):
    try:
        xbmc.log(ADDON_ID+" - "+str(error.encode("utf-8")), xbmc.LOGERROR)
    except:
        xbmc.log(ADDON_ID+" - "+str(error), xbmc.LOGERROR)

def addMenuItems(details, isFolder=True, addLibrary=False):
    changed=False
    for detail in details:
        try:
            u=sys.argv[0]+"?url="+detail['url']+"&mode="+str(detail['mode'])+"&name="+urllib.quote_plus(detail['title'].encode("utf-8"))+"&icon="+detail['icon']
            liz=xbmcgui.ListItem(detail['title'].encode("utf-8"), iconImage=detail['icon'], thumbnailImage=detail['icon'])
            liz.setInfo(type=detail['type'], infoLabels={ "Title": detail['title'].encode("utf-8"),"Plot": detail['plot']} )
        except:
            u=sys.argv[0]+"?url="+detail['url']+"&mode="+str(detail['mode'])+"&name="+urllib.quote_plus(detail['title']).decode("utf-8")+"&icon="+detail['icon']
            liz=xbmcgui.ListItem(detail['title'].encode("utf-8"), iconImage=detail['icon'], thumbnailImage=detail['icon'])
            liz.setInfo(type=detail['type'], infoLabels={ "Title": detail['title'].decode("utf-8"),"Plot": detail['plot']} )
            
        try:
            liz.setProperty("Fanart_Image", detail['fanart'])
            u=u+"&fanart="+detail['fanart']
        except:
            pass
        try:
            liz.setProperty("Landscape_Image", detail['landscape'])
            u=u+"&landscape="+detail['landscape']
        except:
            pass
        try:
            liz.setProperty("Poster_Image", detail['poster'])
            u=u+"&poster="+detail['poster']
        except:
            pass
        try:
            u=u+"&extras="+str(detail["extras"])
        except:
            pass
        """if addLibrary:
            try:
                extras = ast.literal_eval(str(detail['extras']))
                dwnld = (sys.argv[0] + "?mode=9&series_id="+str(extras['series_id']))
                liz.addContextMenuItems([('Add series to library', 'xbmc.RunPlugin('+dwnld+')')])
            except:
                pass"""
        if isFolder:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        else:
            liz.setProperty('IsPlayable', 'true')
            #logError(u)
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    xbmcplugin.endOfDirectory(int(sysarg))

def notify(message, reportError=False, timeShown=5000):
    """Displays a notification to the user
    
    Parameters:
    addonId: the current addon id
    message: the message to be shown
    timeShown: the length of time for which the notification will be shown, in milliseconds, 5 seconds by default
    """
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (addon.getAddonInfo('name'), message, timeShown, addon.getAddonInfo('icon')))
    if reportError:
        logError(message)
    
def buildSeriesMenu(items, filter, media_type, limit=20, offset=0):
    menu=[]

    for item in items:
        logError(item['name'])
        menu.append({
            "title": item['name'],
            "url": "list_media",
            "extras": {"series_id": item['series_id'], "limit": 10000, "series_name": urllib.quote_plus(item['name'].replace("'", "\\'"))},
            "mode":2, 
            "poster":item['portrait_image']['large_url'],
            "icon":item['portrait_image']['large_url'], 
            "fanart":item['landscape_image']['full_url'],
            "type":"video", 
            "plot":item['description']
        })
    if len(menu)==20:
        menu.append({
            "title": "Next >",
            "url": "list_series",
            "extras": {"media_type": media_type, "filter": filter, "limit": str(limit), "offset": int(offset)+int(limit)},
            "mode":1, 
            "poster":"none",
            "icon":"none", 
            "fanart":"none",
            "type":"video", 
            "plot":""
        })
    addMenuItems(menu, isFolder=True, addLibrary=True)

def buildEpisodesMenu(items, collection=0):
    menu=[]
    for item in items:
        if collection == 0:
            if item['free_available']==False and int(item['free_available_time'][:4])<9000:
                title="[COLOR lightcoral]Episode "+item['episode_number']+" - "+item['name']+" (Available "+item['free_available_time'][8:][:2]+"/"+item['free_available_time'][5:][:2]+"/"+item['free_available_time'][:4]+")[/COLOR]"
            else:
                title="Episode "+item['episode_number']+" - "+item['name']
            menu.append({
                "title": title,
                "url": "info",
                "extras": {"media_id": item['media_id'], "fields": "media.stream_data"},
                "mode":10, 
                "poster":item['screenshot_image']['large_url'],
                "icon":item['screenshot_image']['large_url'], 
                "fanart":item['screenshot_image']['full_url'],
                "type":"video", 
                "plot":item['description']
            })
        elif item['collection_id'] == collection:   
            if item['free_available']==False and int(item['free_available_time'][:4])<9000:
                title="[COLOR lightcoral]Episode "+item['episode_number']+" - "+item['name']+" (Available "+item['free_available_time'][8:][:2]+"/"+item['free_available_time'][5:][:2]+"/"+item['free_available_time'][:4]+")[/COLOR]"
            else:
                title="Episode "+item['episode_number']+" - "+item['name']
            menu.append({
                "title": title,
                "url": "info",
                "extras": {"media_id": item['media_id'], "fields": "media.stream_data"},
                "mode":10, 
                "poster":item['screenshot_image']['large_url'],
                "icon":item['screenshot_image']['large_url'], 
                "fanart":item['screenshot_image']['full_url'],
                "type":"video", 
                "plot":item['description']
            })
    addMenuItems(menu, isFolder=False)

def buildCollectionMenu(items, name):
    menu=[]
    collection = 0
    try:
        artwork = Tvdb(banners=True)[name]['_banners']['season']['raw']
    except:
        pass
    details = json.loads(crunchyroll_api("info", {"collection_id":items[0]['collection_id']}))
    if int(details['data']['season']) > 0:
        for item in items:
            if item['free_available'] is True:
                if collection != item['collection_id']:
                    collection = item['collection_id']
                    details = json.loads(crunchyroll_api("info", {"collection_id":item['collection_id']}))
                    if  " Dub)" not in details['data']['name']:
                        poster = ""
                        try:
                            t = Tvdb()
                            for s in artwork:
                                logError(str(s['subKey']) + " = " + (details['data']['season']))
                                if str(s['subKey']) == str(details['data']['season']):
                                    poster = "https://www.thetvdb.com/banners/" + s['fileName']
                        except:
                            pass

                        menu.append({
                            "title": "Season " + str(details['data']['season']) + " - " + details['data']['name'],
                            "url": "list_media",
                            "extras": {"series_id": item['series_id'], "limit": "10000", "collection_id": collection},
                            "mode":6, 
                            "poster":poster,
                            "icon":poster, 
                            "fanart":item['screenshot_image']['full_url'],
                            "type":"video", 
                            "plot":details['data']['description']
                        })
    else:
        buildEpisodesMenu(items)
    addMenuItems(menu, isFolder=True)
        
    
def buildCategoryMenu(items, media_type):
    menu=[]
    for item in items:
        path=filter(lambda x: x.isalpha(), item['label'])
        menu.append({
            "title": item['label'],
            "url": "list_series",
            "extras": {"media_type" : media_type, "filter" : "tag:"+item['tag'], "limit": 20, "offset": 0},
            "mode":1, 
            "poster":os.path.join(home, 'resources/media/genre', path.lower()+'.jpg'),
            "icon":os.path.join(home, 'resources/media/genre', path.lower()+'.jpg'), 
            "fanart":os.path.join(home, 'resources/media', 'fanart.jpg'),
            "type":"video", 
            "plot":""
        })
    addMenuItems(menu, isFolder=True)

def buildAlphabetMenu(media_type):
    menu=[]
    letters=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for letter in letters:
        menu.append({
            "title": letter.upper(),
            "url": "list_series",
            "extras": {"media_type" : media_type, "filter" : "prefix:"+letter, "limit": 20, "offset": 0},
            "mode":1, 
            "poster":os.path.join(home, 'resources/media/letters', letter+'.jpg'),
            "icon":os.path.join(home, 'resources/media/letters', letter+'.jpg'), 
            "fanart":os.path.join(home, 'resources/media', 'fanart.jpg'),
            "type":"video", 
            "plot":""
        })
    addMenuItems(menu, isFolder=True)
    
def search(items):
    find=searchDialog()
    if find!=False:
        #items['media_types']="anime|drama"
        items['q']=find
        return items
    else:
        return False

def searchDialog(searchText="Please enter search text") :    
    keyb=xbmc.Keyboard('', searchText)
    keyb.doModal()
    searchText=''
    
    if (keyb.isConfirmed()) :
        searchText = keyb.getText()
    if searchText!='':
        return searchText
    return False
        
def playMedia(title, thumbnail, items) :
    
    for item in items:

        if item['quality']=='adaptive':
            logError(str(item['url']))
            li = xbmcgui.ListItem(label=title, iconImage=thumbnail, thumbnailImage=thumbnail, path=item['url'])
            li.setInfo( "video", { "Title" : title } )
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
            break
            
def crunchyroll_login():
    s=requests.Session()

    s = requests.Session()

    r = s.get("https://www.crunchyroll.com/en-gb/login")

    p=re.compile('login_form\[_token\]\" value=\"(.*?)\"')
    token = re.search(p, r.text).group(1)

    data ={"login_form[_token]": token, "login_form[name]": xbmcaddon.Addon().getSetting('username'), "login_form[password]": xbmcaddon.Addon().getSetting('password'), "login_form[redirect_url]": "/"}
    r = s.post("https://www.crunchyroll.com/en-gb/login", data = data)

    r = s.get("https://www.crunchyroll.com/editprofile")
    
    xbmcaddon.Addon().setSetting('session_id', s.cookies['session_id'])
    
def crunchyroll_api(func, args):
    run=0
    while True:
        args['session_id'] = xbmcaddon.Addon().getSetting('session_id')
       
        if not args['session_id']:
            crunchyroll_login()
            args['session_id'] = xbmcaddon.Addon().getSetting('session_id')
            
        api_url = 'http://api.crunchyroll.com/'+func+'.0.json'
        
        logError(api_url)

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        
        data = urllib.urlencode(args)

        logError(str(data))
        
        if xbmcaddon.Addon().getSetting('debug')=="true":
            logError("API Call = "+api_url+"?"+data)
        
        resp=opener.open(api_url, data)

        content = resp.read()
        logError(str(content))
        results=json.loads(content)
        
        if results['error']==True:
            # try refreshing the login and try again
            crunchyroll_login()
        else:
            break
        run+=1
        if run==2:
            notify(results['message'])
            logError("API Error = "+results['message'])
            return False
    #logError(func+str(results))
    return content
    
def parseJSString(s):
    try:
        offset=1 if s[0]=='+' else 0
        val = int(eval(s.replace('!+[]','1').replace('!![]','1').replace('[]','0').replace('(','str(')[offset:]))
        return val
    except:
        pass

def getImage(url):
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    try:
        req = urllib2.Request(url, headers=header)
        response = urllib2.urlopen(req)
        if response and response.getcode() == 200:
            return response
    except:
        return False
    
    return False