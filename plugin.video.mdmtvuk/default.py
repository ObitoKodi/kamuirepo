import sys,urllib,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os
import requests
from addon.common.addon import Addon
from addon.common.net import Net

#MTV UK Add-on Created By Mucky Duck (3/2016)

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
addon_id='plugin.video.mdmtvuk'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
autoplay = selfAddon.getSetting('auto-play')
baseurl = 'http://www.mtv.co.uk'
s = requests.session()
net = Net()




def CAT():
        addDir('[B][COLOR white]Trending Artists[/COLOR][/B]',baseurl+'/music/artists',13,icon,fanart,'')
        addDir('[B][COLOR white]Latest Playlists[/COLOR][/B]',baseurl+'/music/playlists/mtv-music-playlist',10,icon,fanart,'')
        addDir('[B][COLOR white]Music Videos[/COLOR][/B]','url',6,icon,fanart,'')
        addDir('[B][COLOR white]Live Music[/COLOR][/B]','url',8,icon,fanart,'')
        addDir('[B][COLOR white]MTV Push[/COLOR][/B]',baseurl+'/mtv-push',1,icon,fanart,'')
        addDir('[B][COLOR white]Playlists[/COLOR][/B]','url',9,icon,fanart,'')
        addDir('[B][COLOR white]Charts[/COLOR][/B]','url',4,icon,fanart,'')
        addDir('[B][COLOR white]Search[/COLOR][/B]','url',12,icon,fanart,'')
        xbmc.executebuiltin("Container.SetViewMode(50)")




def CHARTS():
        addDir('[B][COLOR white]The Official UK Top 40 Singles Chart[/COLOR][/B]',baseurl+'/music/charts/the-official-uk-top-40-singles-chart',5,icon,fanart,'')
        addDir('[B][COLOR white]The Official Uk Urban Chart[/COLOR][/B]',baseurl+'/music/charts/the-official-uk-urban-chart',5,icon,fanart,'')
        addDir('[B][COLOR white]The Official Uk Dance Chart[/COLOR][/B]',baseurl+'/music/charts/the-official-uk-dance-chart',5,icon,fanart,'')
        addDir('[B][COLOR white]The Official UK Top 20 Download Chart[/COLOR][/B]',baseurl+'/music/charts/the-official-uk-top-20-download-chart',5,icon,fanart,'')
        addDir('[B][COLOR white]This Week\'s Top 20[/COLOR][/B]',baseurl+'/music/charts/this-weeks-top-20',5,icon,fanart,'')
        #addDir('[B][COLOR red]The Official Chart Update[/COLOR][/B]',baseurl+'music/charts/the-official-chart-update',1,icon,fanart,'')
        addDir('[B][COLOR white]The Official Uk Audio Streaming Chart[/COLOR][/B]',baseurl+'/music/charts/the-official-uk-audio-streaming-chart-top-20',5,icon,fanart,'')
        xbmc.executebuiltin("Container.SetViewMode(50)")




def MUSIC_VIDS():
        addDir('[B][COLOR white]latest music videos[/COLOR][/B]',baseurl+'/charts/videos/latest-music-videos-collection',5,icon,fanart,'')
        addDir('[B][COLOR white]the brit awards 2016 winners![/COLOR][/B]',baseurl+'/the-brit-awards/videos/playlist-the-brit-awards-2016-winners',5,icon,fanart,'')
        addDir('[B][COLOR white]1d: a whole lotta history...[/COLOR][/B]',baseurl+'/one-direction/videos/the-best-of-one-direction',5,icon,fanart,'')
        addDir('[B][COLOR white]the official no.1 singles of 2015[/COLOR][/B]',baseurl+'/music-0/videos/the-official-no1-singles-of-2015',5,icon,fanart,'')
        addDir('[B][COLOR white]#rockstrending[/COLOR][/B]',baseurl+'/mtv-rocks-channel/videos/rockstrending',5,icon,fanart,'')
        addDir('[B][COLOR white]hottest music videos[/COLOR][/B]',baseurl+'/music/videos',1,icon,fanart,'')
        addDir('[B][COLOR white]justin bieber\'s hottest music video moments[/COLOR][/B]',baseurl+'/justin-bieber/videos/justin-biebers-hottest-music-video-moments',5,icon,fanart,'')
        xbmc.executebuiltin("Container.SetViewMode(50)")




def LIVE():
        addDir('[B][COLOR white]mtv world stage[/COLOR][/B]',baseurl+'/mtv-world-stage',1,icon,fanart,'')
        addDir('[B][COLOR white]mtv unplugged[/COLOR][/B]',baseurl+'/mtv-unplugged',1,icon,fanart,'')
        addDir('[B][COLOR white]mtv live sessions[/COLOR][/B]',baseurl+'/mtv-live-sessions',1,icon,fanart,'')
        addDir('[B][COLOR white]mtv brand new for 2015[/COLOR][/B]',baseurl+'/brand-new-for-2015',1,icon,fanart,'')
        xbmc.executebuiltin("Container.SetViewMode(50)")




def PLAYLISTS():
        addDir('[B][COLOR white]mtv music playlist[/COLOR][/B]',baseurl+'/music/playlists/mtv-music-playlist',5,icon,fanart,'')
        addDir('[B][COLOR white]mtv dance playlist[/COLOR][/B]',baseurl+'/music/playlists/mtv-dance-playlist',5,icon,fanart,'')
        addDir('[B][COLOR white]mtv hits playlist[/COLOR][/B]',baseurl+'/music/playlists/mtv-hits-playlist',5,icon,fanart,'')
        addDir('[B][COLOR white]mtv base playlist[/COLOR][/B]',baseurl+'/music/playlists/mtv-base-playlist',5,icon,fanart,'')
        addDir('[B][COLOR white]mtv rocks playlist[/COLOR][/B]',baseurl+'/music/playlists/mtv-rocks-playlist',5,icon,fanart,'')
        addDir('[B][COLOR white]MTV Brand New Top 10 Presented By Emporio Armani Diamonds[/COLOR][/B]',baseurl+'/music/playlists/brand-new-playlist-presented-by-emporio-armani-diamonds',5,icon,fanart,'')
        xbmc.executebuiltin("Container.SetViewMode(50)")




def INDEX(name,url):
        link = OPEN_URL(url).text
        link = link.encode('ascii', 'ignore').decode('ascii')
        link = link.replace('\n','').replace('\r','')
        name = name.replace('[B][COLOR white]','').replace('[/COLOR][/B]','').lower()
        all_links = regex_get_all(link, '<h2 class="', '</div>.*?</div></div>  </div>')
        all_videos = regex_get_all(str(all_links), 'vimn_video', '</article')

        for a in all_videos:
                name = regex_from_to(a, '<h2>', '</').replace('\\','')
                url = regex_from_to(a, 'href="', '"')
                thumb = regex_from_to(a, 'original="', '"')
                if 'http://' not in url:
                        url = baseurl+url
                if 'default_image_frontend' in thumb:
                        thumb = fanart
                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,5,thumb,thumb,'')
        try:
                np = re.findall("plugin-params='(.*?)'", str(link), re.I|re.DOTALL)[0]
                addDir('[B][COLOR orangered]Next Page >>>[/COLOR][/B]',np,11,art+'MTV_Orange.png',fanart,'')
        except: pass
        xbmc.executebuiltin("Container.SetViewMode(500)")




def INDEX2(url):
        link = OPEN_URL(url).text
        link = link.encode('ascii', 'ignore').decode('ascii')
        try:
                plist = re.compile('"video_id":"(.*?)"').findall(link)[-1]
        except:
                plist = re.compile('"video_id":"(.*?)"').findall(link)[0]
        plist = plist.replace(':','%3A')
        plist = 'http://www.mtv.co.uk/mrss/'+plist
        if '.xml' not in plist:
                plist = plist + '.xml'
        link = OPEN_URL(plist).text
        link = link.encode('ascii', 'ignore').decode('ascii')
        all_videos = regex_get_all(link, '<item>', '</item>')
        for a in all_videos:
                name = regex_from_to(a, '<title><\!\[CDATA\[', '\]').replace('\\','')
                name = addon.unescape(name)
                name = name.encode('ascii', 'ignore').decode('ascii')
                url = regex_from_to(a, 'isDefault="true" url="', '"').replace('{device}','none')
                thumb = regex_from_to(a, 'image url="', '"')
                if 'default_image_frontend' in thumb:
                        thumb = fanart
                if autoplay == 'true':
                        link = OPEN_URL(url).text
                        link = link.encode('ascii', 'ignore').decode('ascii')
                        try:
                                try:
                                        url = re.findall("<src>(.*?)</", str(link), re.I|re.DOTALL)[-1]
                                        if 'http://static.mtv.co.uk/player/mtv.png' in url:
                                                url = re.findall("<src>(.*?)</", str(link), re.I|re.DOTALL)[-2]
                                except:
                                        url = re.findall("<src>(.*?)</", str(link), re.I|re.DOTALL)[0]
                        except:pass
                        if 'http' not in url:
                                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,3,thumb,thumb,'')
                else:
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,2,thumb,thumb,'')
        xbmc.executebuiltin("Container.SetViewMode(500)")




def INDEX3(name,url):
        link = OPEN_URL(url).text
        link = link.encode('ascii', 'ignore').decode('ascii')
        link = link.replace('\n','').replace('\r','')
        name = name.replace('[B][COLOR white]','').replace('[/COLOR][/B]','').lower()
        all_links = regex_get_all(link, '<h2 class="pane-title">%s'%name, '</div>.*?</div></div>  </div>')
        all_videos = regex_get_all(str(all_links), '<article', '</article')
        for a in all_videos:
                name = regex_from_to(a, '<h2>', '</').replace('\\','')
                url = regex_from_to(a, 'href="', '"')
                thumb = regex_from_to(a, 'original="', '"')
                if 'default_image_frontend' in thumb:
                        thumb = fanart
                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,5,thumb,thumb,'')
        try:
                np = re.findall("plugin-params='(.*?)'", str(link), re.I|re.DOTALL)[-1]
                addDir('[B][COLOR orangered]Next Page >>>[/COLOR][/B]',np,11,art+'MTV_Orange.png',fanart,'')
        except: pass
        xbmc.executebuiltin("Container.SetViewMode(500)")




def INDEX4(url):
        try:
                link = OPEN_URL('http://www.mtv.co.uk/loadmore?plugin=VimnContentListing&params='+url).json()
        except:
                link = OPEN_URL('http://www.mtv.co.uk/loadmore?plugin=VimnSubjectListing&params='+url).json()
        all_videos = regex_get_all(str(link), '<article', '</article')
        for a in all_videos:
                name = regex_from_to(a, '<h2>', '</').replace('\\','')
                url = regex_from_to(a, 'href="', '"')
                thumb = regex_from_to(a, 'original="', '"')
                if 'default_image_frontend' in thumb:
                        thumb = fanart
                if 'http://' not in url:
                        url = baseurl+url
                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,5,thumb,thumb,'')
        try:
                np = re.findall("params': u'(.*?)'", str(link), re.I|re.DOTALL)[0]
                addDir('[B][COLOR orangered]Next Page >>>[/COLOR][/B]',np,11,art+'MTV_Orange.png',fanart,'')
        except: pass
        xbmc.executebuiltin("Container.SetViewMode(500)")




def ARTISTS(name,url):
        link = OPEN_URL(url).text
        link = link.encode('ascii', 'ignore').decode('ascii')
        all_videos = regex_get_all(link, 'article class=".*?music.*?"', '</article')
        for a in all_videos:
                name = regex_from_to(a, '<h2>', '</').replace('\\','')
                url = regex_from_to(a, 'href="', '"')
                thumb = regex_from_to(a, 'original="', '"')
                if 'http://' not in url:
                        url = baseurl+url
                if 'default_image_frontend' in thumb:
                        thumb = fanart
                r = OPEN_URL(url).text
                r = r.encode('ascii', 'ignore').decode('ascii')
                video_id = re.findall('content="http://media.mtvnservices.com/fb/(.*?)\.swf',str(r))[0]
                url = 'http://intl.mtvnservices.com/mediagen/'+video_id+'/?device=none'
                if autoplay == 'true':
                        r = OPEN_URL(url).text
                        r = r.encode('ascii', 'ignore').decode('ascii')
                        try:
                                try:
                                        url = re.findall("<src>(.*?)</", str(r), re.I|re.DOTALL)[-1]
                                        if 'http://static.mtv.co.uk/player/mtv.png' in url:
                                                url = re.findall("<src>(.*?)</", str(link), re.I|re.DOTALL)[-2]
                                except:
                                        url = re.findall("<src>(.*?)</", str(r), re.I|re.DOTALL)[0]
                        except:pass
                        if 'http' not in url:
                                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,3,thumb,thumb,'')
                else:
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,2,thumb,thumb,'')
                
        try:
                np = re.findall("plugin-params='(.*?)'", str(link), re.I|re.DOTALL)[0]
                addDir('[B][COLOR orangered]Next Page >>>[/COLOR][/B]',np,14,art+'MTV_Orange.png',fanart,'')
        except: pass
        xbmc.executebuiltin("Container.SetViewMode(500)")




def ARTISTS2(name,url):
        link = OPEN_URL(url).text
        link = link.encode('ascii', 'ignore').decode('ascii')
        all_videos = regex_get_all(link, 'promo-type-.*?music.*?', '</article')
        for a in all_videos:
                name = regex_from_to(a, '<h2>', '</').replace('\\','')
                url = regex_from_to(a, 'href="', '"')
                thumb = regex_from_to(a, 'original="', '"')
                if 'http://' not in url:
                        url = baseurl+url
                if 'default_image_frontend' in thumb:
                        thumb = fanart
                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,7,thumb,thumb,'')
        try:
                np = re.findall("plugin-params='(.*?)'", str(link), re.I|re.DOTALL)[0]
                addDir('[B][COLOR orangered]Next Page >>>[/COLOR][/B]',np,14,art+'MTV_Orange.png',fanart,'')
        except: pass
        xbmc.executebuiltin("Container.SetViewMode(500)")




def ARTISTS3(url):
        try:
                link = OPEN_URL('http://www.mtv.co.uk/loadmore?plugin=VimnContentListing&params='+url).json()
        except:
                link = OPEN_URL('http://www.mtv.co.uk/loadmore?plugin=VimnSubjectListing&params='+url).json()
        all_videos = regex_get_all(str(link), '<article', '</article')
        for a in all_videos:
                name = regex_from_to(a, '<h2>', '</').replace('\\','')
                url = regex_from_to(a, 'href="', '"')
                thumb = regex_from_to(a, 'original="', '"')
                if 'default_image_frontend' in thumb:
                        thumb = fanart
                if 'http://' not in url:
                        url = baseurl+url
                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,7,thumb,thumb,'')
        try:
                np = re.findall("params': u'(.*?)'", str(link), re.I|re.DOTALL)[0]
                addDir('[B][COLOR orangered]Next Page >>>[/COLOR][/B]',np,14,art+'MTV_Orange.png',fanart,'')
        except: pass
        xbmc.executebuiltin("Container.SetViewMode(500)")



def SEARCH():
        keyb = xbmc.Keyboard('', '[B][COLOR orangered]SEARCH MTV UK[/COLOR][/B]')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace('%20','+')
                url = baseurl+'/search/liveresults?keywords='+search
                link = OPEN_URL(url).text
                link = link.encode('ascii', 'ignore').decode('ascii')
                link = link.replace('\n','').replace('\r','')
                try:
                        all_links = regex_get_all(link, '>Artists<', '</div>  </div>')
                        all_videos = regex_get_all(str(all_links), '<article', '</article')
                        addLink('[COLOR orangered]Artists[/COLOR]','url','',icon,fanart,'')
                        for a in all_videos:
                                name = regex_from_to(a, '<h2><a href=.*?>', '</').replace('\\','')
                                name = addon.unescape(name)
                                name = name.encode('ascii', 'ignore').decode('ascii')
                                thumb = regex_from_to(a, 'original="', '"')
                                if 'default_image_frontend' in thumb:
                                        thumb = fanart
                                url = regex_from_to(a, 'href="', '"')
                                if 'http' not in url:
                                        url = baseurl+url
                                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,7,thumb,thumb,'')
                except: pass
                addLink('','url','',icon,fanart,'')
                try:
                        all_links = regex_get_all(link, '>Music videos<', '</div>  </div>')
                        all_videos = regex_get_all(str(all_links), '<article', '</article')
                        addLink('[COLOR orangered]Music Videos[/COLOR]','url','',icon,fanart,'')
                        for a in all_videos:
                                name = regex_from_to(a, 'content-subject">', '</').replace('\\','')
                                name = addon.unescape(name)
                                name = name.encode('ascii', 'ignore').decode('ascii')
                                name2 = regex_from_to(a, '<h2><a href=.*?>', '</').replace('\\','')
                                name2 = addon.unescape(name2)
                                name2 = name2.encode('ascii', 'ignore').decode('ascii')
                                thumb = regex_from_to(a, 'original="', '"')
                                url = regex_from_to(a, 'href="', '"')
                                if 'http' not in url:
                                        url = baseurl+url
                                if 'default_image_frontend' in thumb:
                                        thumb = fanart
                                r = OPEN_URL(url).text
                                r = r.encode('ascii', 'ignore').decode('ascii')
                                video_id = re.findall('content="http://media.mtvnservices.com/fb/(.*?)\.swf',r)[0]
                                url = 'http://intl.mtvnservices.com/mediagen/'+video_id+'/?device=none'
                                if autoplay == 'true':
                                        r = OPEN_URL(url).text
                                        r = r.encode('ascii', 'ignore').decode('ascii')
                                        try:
                                                try:
                                                        url = re.findall("<src>(.*?)</", str(r), re.I|re.DOTALL)[-1]
                                                        if 'http://static.mtv.co.uk/player/mtv.png' in url:
                                                                url = re.findall("<src>(.*?)</", str(link), re.I|re.DOTALL)[-2]
                                                except:
                                                        url = re.findall("<src>(.*?)</", str(r), re.I|re.DOTALL)[0]
                                        except:pass
                                        if 'http' not in url:
                                                addDir('[B][COLOR white]%s[/COLOR][/B][B][COLOR orangered] | [/COLOR][/B][B][COLOR white]%s[/COLOR][/B]' %(name,name2),url,3,thumb,thumb,'')
                                else:
                                        addDir('[B][COLOR white]%s[/COLOR][/B][B][COLOR orangered] | [/COLOR][/B][B][COLOR white]%s[/COLOR][/B]' %(name,name2),url,2,thumb,thumb,'')
                except: pass
                xbmc.executebuiltin("Container.SetViewMode(50)")




def LINKS(name,url,iconimage):
        link = OPEN_URL(url).text
        link = link.encode('ascii', 'ignore').decode('ascii')
        all_videos = regex_get_all(link, '<rendition', '</rendition')
        for a in all_videos:
                name2 = regex_from_to(a, 'bitrate="', '"')
                url = regex_from_to(a, '<src>', '<')
                addDir('[B][COLOR white]Bitrate[/COLOR][/B] [B][COLOR red]%s[/COLOR][/B]' %name2,url,3,iconimage,iconimage,'')




def RESOLVE(url):
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(str(url))
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)




def regex_from_to(text, from_string, to_string, excluding=True):
        if excluding:
                try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
                except: r = ''
        else:
                try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
                except: r = ''
        return r




def regex_get_all(text, start_with, end_with):
        r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
        return r




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




def addDir(name,url,mode,iconimage,fanart,description):
        name = name.replace('()','')
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
        liz.setProperty('fanart_image', fanart)
        if mode==3:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok



def addLink(name,url,mode,iconimage,fanart,description=''):
        #u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        #ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok




def OPEN_URL(url):
    headers = {}
    headers['User-Agent'] = User_Agent
    link = s.get(url, headers=headers, allow_redirects=False)
    return link




params=get_params()
url=None
name=None
mode=None
iconimage=None
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
        description=urllib.unquote_plus(params["description"])
except:
        pass




if mode==None or url==None or len(url)<1:
        CAT()

elif mode==1:
        INDEX(name,url)

elif mode==2:
        LINKS(name,url,iconimage)

elif mode==3:
        RESOLVE(url)

elif mode==4:
        CHARTS()

elif mode==5:
        INDEX2(url)

elif mode==6:
        MUSIC_VIDS()

elif mode==7:
        ARTISTS(name,url)

elif mode==8:
        LIVE()

elif mode==9:
        PLAYLISTS()

elif mode==10:
        INDEX3(name,url)

elif mode==11:
        INDEX4(url)

elif mode==12:
        SEARCH()

elif mode==13:
        ARTISTS2(name,url)

elif mode==14:
        ARTISTS3(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
































































































