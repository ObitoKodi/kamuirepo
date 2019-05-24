import sys, urllib, os
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

sysarg=str(sys.argv[1])
ADDON_ID='plugin.video.soggysandwich'
addon=xbmcaddon.Addon(id=ADDON_ID)
home=xbmc.translatePath(addon.getAddonInfo('path').decode('utf-8'))

# the main menu structure
mainMenu=[
    {
        "title":"Anime", 
        "url":"animeMenu",
        "mode":0, 
        "poster":os.path.join(home, 'resources/media', 'anime.jpg'),
        "icon":os.path.join(home, 'resources/media', 'anime.jpg'), 
        "fanart":os.path.join(home, 'resources/media', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Drama", 
        "url":"dramaMenu",
        "mode":0, 
        "poster":os.path.join(home, 'resources/media', 'drama_v2.jpg'),
        "icon":os.path.join(home, 'resources/media', 'drama_v2.jpg'), 
        "fanart":os.path.join(home, 'resources/media', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Search", 
        "url":"autocomplete",
        "extras":{"media_types": "anime<or>drama", "limit":10000},
        "mode":3, 
        "poster":os.path.join(home, 'resources/media', 'search.jpg'),
        "icon":os.path.join(home, 'resources/media', 'search.jpg'), 
        "fanart":os.path.join(home, 'resources/media', 'fanart.jpg'),
        "type":"", 
        "plot":""
    } 
]

animeMenu=[
    {
        "title":"Most Popular", 
        "url":"list_series",
        "extras":{"media_type":"anime", "filter":"popular", "limit":"20", "offset":"0"},
        "mode":1, 
        "poster":os.path.join(home, 'resources/media', 'mostpopular.jpg'),
        "icon":os.path.join(home, 'resources/media', 'mostpopular.jpg'), 
        "fanart":os.path.join(home, 'resources/media', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Featured", 
        "url":"list_series",
        "extras":{"media_type":"anime", "filter":"featured", "limit":"20", "offset":"0"},
        "mode":1, 
        "poster":os.path.join(home, 'resources/media', 'featured.jpg'),
        "icon":os.path.join(home, 'resources/media', 'featured.jpg'), 
        "fanart":os.path.join(home, 'resources/media', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Newest", 
        "url":"list_series",
        "extras":{"media_type":"anime", "filter":"newest", "limit":"20", "offset":"0"},
        "mode":1, 
        "poster":os.path.join(home, 'resources/media', 'newest.jpg'),
        "icon":os.path.join(home, 'resources/media', 'newest.jpg'), 
        "fanart":os.path.join(home, 'resources/media', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Genres", 
        "url":"categories",
        "extras":{"media_type":"anime"},
        "mode":4, 
        "poster":os.path.join(home, 'resources/media', 'genrest.jpg'),
        "icon":os.path.join(home, 'resources/media', 'genres.jpg'), 
        "fanart":os.path.join(home, 'resources/media', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Seasons", 
        "url":"categories",
        "extras":{"media_type":"anime"},
        "mode":4, 
        "poster":os.path.join(home, 'resources/media', 'seasons.jpg'),
        "icon":os.path.join(home, 'resources/media', 'seasons.jpg'), 
        "fanart":os.path.join(home, 'resources/media', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Search Alphabetically", 
        "url":"list_series",
        "extras":{"media_type":"anime"},
        "mode":5, 
        "poster":os.path.join(home, 'resources/media', 'alphabetical.jpg'),
        "icon":os.path.join(home, 'resources/media', 'alphabetical.jpg'), 
        "fanart":os.path.join(home, 'resources/media', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Search", 
        "url":"autocomplete",
        "extras":{"media_types": "anime", "limit":10000},
        "mode":3, 
        "poster":os.path.join(home, 'resources/media', 'search.jpg'),
        "icon":os.path.join(home, 'resources/media', 'search.jpg'), 
        "fanart":os.path.join(home, 'resources/media', 'fanart.jpg'),
        "type":"", 
        "plot":""
    } 
]

dramaMenu=[
    {
        "title":"Most Popular", 
        "url":"list_series",
        "extras":{"media_type":"drama", "filter":"popular", "limit":"20", "offset":"0"},
        "mode":1, 
        "poster":os.path.join(home, 'resources/media', 'mostpopular.jpg'),
        "icon":os.path.join(home, 'resources/media', 'mostpopular.jpg'), 
        "fanart":os.path.join(home, 'resources/media', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Featured", 
        "url":"list_series",
        "extras":{"media_type":"drama", "filter":"featured", "limit":"20", "offset":"0"},
        "mode":1, 
        "poster":os.path.join(home, 'resources/media', 'featured.jpg'),
        "icon":os.path.join(home, 'resources/media', 'featured.jpg'), 
        "fanart":os.path.join(home, 'resources/media', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Newest", 
        "url":"list_series",
        "extras":{"media_type":"drama", "filter":"newest", "limit":"20", "offset":"0"},
        "mode":1, 
        "poster":os.path.join(home, 'resources/media', 'newest.jpg'),
        "icon":os.path.join(home, 'resources/media', 'newest.jpg'), 
        "fanart":os.path.join(home, 'resources/media', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Genres", 
        "url":"categories",
        "extras":{"media_type":"drama"},
        "mode":4, 
        "poster":os.path.join(home, 'resources/media', 'genres.jpg'),
        "icon":os.path.join(home, 'resources/media', 'genres.jpg'), 
        "fanart":os.path.join(home, 'resources/media', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Seasons", 
        "url":"categories",
        "extras":{"media_type":"drama"},
        "mode":4, 
        "poster":os.path.join(home, 'resources/media', 'seasons.jpg'),
        "icon":os.path.join(home, 'resources/media', 'seasons.jpg'), 
        "fanart":os.path.join(home, 'resources/media', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Search Alphabetically", 
        "url":"list_series",
        "extras":{"media_type":"drama"},
        "mode":5, 
        "poster":os.path.join(home, 'resources/media', 'alphabetical.jpg'),
        "icon":os.path.join(home, 'resources/media', 'alphabetical.jpg'), 
        "fanart":os.path.join(home, 'resources/media', 'fanart.jpg'),
        "type":"", 
        "plot":""
    },
    {
        "title":"Search", 
        "url":"autocomplete",
        "extras":{"media_types": "drama", "limit":10000},
        "mode":3, 
        "poster":os.path.join(home, 'resources/media', 'search.jpg'),
        "icon":os.path.join(home, 'resources/media', 'search.jpg'), 
        "fanart":os.path.join(home, 'resources/media', 'fanart.jpg'),
        "type":"", 
        "plot":""
    } 
]