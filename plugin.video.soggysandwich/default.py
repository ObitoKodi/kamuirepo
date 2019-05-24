import util, menu, time
import ast, json, re, os, urllib
import xbmcaddon, xbmcgui, xbmcvfs, xbmc
#import xbmcplugin, xbmcaddon, xbmcgui

sysarg=str(sys.argv[1])

if xbmcaddon.Addon().getSetting('debug')=="true":
    util.logError("Session ID = "+xbmcaddon.Addon().getSetting('session_id'))

parameters=util.parseParameters()

try:
    mode=int(parameters["mode"])
except:
    mode=None

if mode==0:
    # load in menus
    util.addMenuItems(getattr(menu, parameters['url']))
elif mode==1:
    # get series folders
    extras=ast.literal_eval(parameters['extras'])
    series=util.crunchyroll_api(parameters['url'], extras)
    results=json.loads(series)
    if not results['data']:
        util.notify("No results found.")
    else:
        util.buildSeriesMenu(results['data'], extras['filter'], extras['media_type'], extras['limit'], extras['offset'])
elif mode==2:
    # get episode list
    extras = ast.literal_eval(parameters['extras'])
    episodes=util.crunchyroll_api(parameters['url'], extras)
    results=json.loads(episodes)
    if not results['data']:
        util.notify("No results found.")
    else:
        util.buildCollectionMenu(results['data'], extras['series_name'])
elif mode==6:
    # get episode list
    extras=ast.literal_eval(parameters['extras'])
    episodes=util.crunchyroll_api(parameters['url'], extras)
    
    results=json.loads(episodes)
    if not results['data']:
        util.notify("No results found.")
    else:
        util.buildEpisodesMenu(results['data'], extras['collection_id'])
elif mode==3:
    # run a search
    search=util.search(ast.literal_eval(parameters['extras'].replace("<or>", "|")))
    results=util.crunchyroll_api(parameters['url'], search)
    results=json.loads(results)
    if not results['data']:
        util.notify("No results found.")
    else:
        util.buildSeriesMenu(results['data'], '', 'anime|drama', 20, 0)
elif mode==4:
    # get category list
    extras=ast.literal_eval(parameters['extras'])
    categories=util.crunchyroll_api(parameters['url'], extras)
    results=json.loads(categories)
    if not results['data']:
        util.notify("No results found.")
    else:
        util.buildCategoryMenu(results['data'][parameters['name'][:-1].lower()], extras['media_type'])
elif mode==5:
    # show an alphabetical list
    extras=ast.literal_eval(parameters['extras'])
    util.buildAlphabetMenu(extras['media_type'])     
elif mode==9:
    libraryPath = xbmcaddon.Addon().getSetting('download')

    if libraryPath:
        sData = json.loads(util.crunchyroll_api("info", {"series_id" : parameters['series_id']}))

        folder_name = re.sub(r'[\\/*?:"<>|]', "", sData['data']['name'])
        toAdd=os.path.join(libraryPath, folder_name)

        if not os.path.isdir(toAdd):
            pDialog = xbmcgui.DialogProgressBG()
            pDialog.create("Adding " + sData['data']['name'] + " to library", 'Creating folder...')
            xbmcvfs.mkdir(toAdd)

            pDialog.update(1, message='Gathering information...')

            # get fanart and poster image
            fanart = util.getImage(sData['data']['landscape_image']['full_url'])
            if fanart:
                f =xbmcvfs.File (os.path.join(toAdd, "fanart.jpg"), 'w')
                f.write(fanart.read())

            pDialog.update(2, message='Gathering information...')

            poster = util.getImage(sData['data']['portrait_image']['large_url'])
            if poster:
                f =xbmcvfs.File (os.path.join(toAdd, "poster.jpg"), 'w')
                f.write(poster.read())

            pDialog.update(3, message='Getting episode data...')
            
            eData = json.loads(util.crunchyroll_api("list_media", {"series_id" : parameters['series_id'], "limit": 10000}))
            #util.logError(eData)

            updateBy = 96.0 / len(eData['data'])

            season = 1
            temp_season = 0
            episode_num = 1
            counter = 1



            for item in eData['data']:
                """util.logError(str(item))
                try:
                    if temp_season != item['collection_id']:
                        temp_season = item['collection_id']
                        season = season + 1
                        episode_num = 1
                except:
                    season = 1"""
                #episodeXML = "<?xml version='1.0' encoding='UTF-8'?>\n<episodedetails>\n<title></title>\n<showtitle>" + str(sData['data']['name'].encode("ascii", errors="ignore")) + "</showtitle>\n<season>" + str(season) + "</season>\n<episode>" + str(episode_num) + "</episode>\n<uniqueid>" + str(item['media_id']) + "</uniqueid>\n<plot>" + str(item['description'].encode("ascii", errors="ignore")) + "</plot>\n<thumb>" + str(item['screenshot_image']['full_url']) + "</thumb>\n<path>" + xbmc.translatePath(toAdd) + "</path>\n<filenameandpath>" + xbmc.translatePath(toAdd) + "\episode"+str(item['episode_number'])+".strm" + "</filenameandpath>\n<basepath>" + xbmc.translatePath(toAdd) + "\episode"+str(item['episode_number'])+".strm" + "</basepath>\n<art>\n<fanart></fanart>\n<poster></poster>\n</art>\n</episodedetails>"
                episodeXML = "<episodedetails>\n\t<title>" + str(item['name'].encode("ascii", errors="ignore")) + "</title>\n\t<season>" + str(episode_num) + "</season>\n\t<episode>" + str(episode_num) + "</episode>\n\t<plot>" + str(item['description'].encode("ascii", errors="ignore")) + "</plot>\n\t<thumb>" + str(item['screenshot_image']['full_url']) + "</thumb>\n\t<file></file>\n\t<path>" + xbmc.translatePath(toAdd) + "</path>\n\t<filenameandpath>" + xbmc.translatePath(toAdd) + "\episode"+str(item['episode_number'])+".strm" + "</filenameandpath>\n\t<basepath>" + xbmc.translatePath(toAdd) + "\episode"+str(item['episode_number'])+".strm" + "</basepath>\n\t<uniqueid type=\"unknown\" default=\"true\">" + str(parameters['series_id']) + "</uniqueid><art>\n\t\t<thumb>" + str(item['screenshot_image']['full_url']) + "</thumb>\n\t</art>\n</episodedetails>"
                nfo = os.path.join(toAdd.encode('utf-8'), "episode"+str(item['episode_number'])+".nfo")
                f = xbmcvfs.File (nfo, 'w')
                f.write(episodeXML)
                f.close()

                strm = os.path.join(toAdd.encode('utf-8'), "episode"+str(item['episode_number'])+".strm")
                f = xbmcvfs.File (strm, 'w')
                f.write("plugin://plugin.video.soggysandwich/?url=info&mode=10&name=" + urllib.quote_plus(item['name'].encode("utf-8")) + "&icon=" + str(item['screenshot_image']['full_url'])  + "&fanart=" + str(item['screenshot_image']['full_url']) + "&extras={'fields': 'media.stream_data', 'media_id': '" + str(item['media_id']) + "'}")
                f.close()

                pDialog.update(int(3 + (updateBy * counter)), message='Getting episode data...')
                counter = counter + 1

            pDialog.update(100, message='Getting episode data...')

            # create nfo file
            tvshowXML = "<tvshow>\n\t<title>" + sData['data']['name'] + "</title>\n\t<plot>" + sData['data']['description'] + "</plot>\n\t<file></file>\n\t<path>" + xbmc.translatePath(toAdd) + "</path>\n\t<filenameandpath></filenameandpath>\n\t<basepath>" + xbmc.translatePath(toAdd) + "</basepath>\n\t<uniqueid type=\"unknown\" default=\"true\">" + str(parameters['series_id']) + "</uniqueid>\n\t<genre>Animation</genre>\n</tvshow>"
            nfo = os.path.join(toAdd.encode('utf-8'), "tvshow.nfo")
            f = xbmcvfs.File (nfo, 'w')
            f.write(tvshowXML.encode("ascii", errors="ignore"))
            f.close()
        try:
            pDialog.close()
        except:
            pass
    else:
        util.notify("You must specify your library folder")
elif mode==10:
    # play episode
    episode=util.crunchyroll_api(parameters['url'], ast.literal_eval(parameters['extras']))
    if episode!=False:
        results=json.loads(episode)
        util.playMedia(parameters['name'], parameters['fanart'], results['data']['stream_data']['streams'])
else:
    util.addMenuItems(menu.mainMenu)