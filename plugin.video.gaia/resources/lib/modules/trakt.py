# -*- coding: utf-8 -*-

'''
	Gaia Add-on
	Copyright (C) 2016 Gaia

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os,re,imp,json,urlparse,time,base64,threading,xbmc

from resources.lib.modules import cache
from resources.lib.modules import control
from resources.lib.modules import cleandate
from resources.lib.modules import client
from resources.lib.modules import utils

from resources.lib.extensions import tools
from resources.lib.extensions import interface
from resources.lib.extensions import database
from resources.lib.extensions import clipboard

trakt1 = None
trakt2 = None

def getTrakt1():
	global trakt1
	if trakt1 == None: trakt1 = tools.System.obfuscate(tools.Settings.getString('internal.trakt.api.1', raw = True))
	return trakt1

def getTrakt2():
	global trakt2
	if trakt2 == None: trakt2 = tools.System.obfuscate(tools.Settings.getString('internal.trakt.api.2', raw = True))
	return trakt2

databaseName = control.cacheFile
databaseTable = 'trakt'

def getTrakt(url, post = None, cache = True, check = True, timestamp = None, extended = False, direct = False, authentication = None):
	try:
		if not url.startswith('http://api-v2launch.trakt.tv'):
			url = urlparse.urljoin('http://api-v2launch.trakt.tv', url)

		if authentication:
			valid = True
			token = authentication['token']
			refresh = authentication['refresh']
		else:
			valid = getTraktCredentialsInfo() == True
			token = tools.Settings.getString('accounts.informants.trakt.token')
			refresh = tools.Settings.getString('accounts.informants.trakt.refresh')

		headers = {'Content-Type': 'application/json', 'trakt-api-key': getTrakt1(), 'trakt-api-version': '2'}

		if not post == None: post = json.dumps(post)

		if direct or not valid:
			result = client.request(url, post = post, headers = headers)
			return result

		headers['Authorization'] = 'Bearer %s' % token
		result = client.request(url, post = post, headers = headers, output = 'extended', error = True)
		if result and not (result[1] == '401' or result[1] == '405'):
			if check: _cacheCheck()
			if extended: return result[0], result[2]
			else: return result[0]

		try: code = str(result[1])
		except: code = ''

		if code.startswith('5') or (result and isinstance(result, basestring) and '<html' in result) or not result:
			return _error(url = url, post = post, timestamp = timestamp, message = 33676)

		oauth = 'http://api-v2launch.trakt.tv/oauth/token'
		opost = {'client_id': getTrakt1(), 'client_secret': getTrakt2(), 'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob', 'grant_type': 'refresh_token', 'refresh_token': refresh}

		result = client.request(oauth, post = json.dumps(opost), headers = headers, error = True)

		try: code = str(result[1])
		except: code = ''

		if code.startswith('5') or not result or (result and isinstance(result, basestring) and '<html' in result):
			return _error(url = url, post = post, timestamp = timestamp, message = 33676)
		elif result and code in ['404']:
			return _error(url = url, post = post, timestamp = timestamp, message = 33786)
		elif result and code in ['401', '405']:
			return _error(url = url, post = post, timestamp = timestamp, message = 33677)

		result = json.loads(result)

		token, refresh = result['access_token'], result['refresh_token']
		tools.Settings.set('accounts.informants.trakt.token', token)
		tools.Settings.set('accounts.informants.trakt.refresh', refresh)

		headers['Authorization'] = 'Bearer %s' % token

		result = client.request(url, post = post, headers = headers, output = 'extended')
		if check: _cacheCheck()

		if extended: return result[0], result[2]
		else: return result[0]
	except:
		tools.Logger.error()

	return None


def _error(url, post, timestamp, message):
	_cache(url = url, post = post, timestamp = timestamp)
	if tools.Settings.getBoolean('accounts.informants.trakt.notifications'):
		interface.Dialog.notification(title = 32315, message = message, icon = interface.Dialog.IconError)
	interface.Loader.hide()
	return None

def _cache(url, post = None, timestamp = None):
	try:
		# Only cache the requests that change something on the Trakt account.
		# Trakt uses JSON post data to set things and only uses GET parameters to retrieve things.
		if post == None:
			return None

		data = database.Database(databaseName, connect = True)
		_cacheCreate(data)

		# post parameter already json.dumps from getTrakt.
		post = ('"%s"' % post.replace('"', '""').replace("'", "''")) if not post == None else data._null()
		if timestamp == None: timestamp = tools.Time.timestamp()
		data._insert('''
			INSERT INTO %s (time, link, data)
			VALUES (%d, "%s", %s);
			''' % (databaseTable, timestamp, url, post)
			, commit = True
		)

		data._close()
	except:
		tools.Logger.error()

def _cacheCreate(data):
	try:
		data._create('''
			CREATE TABLE IF NOT EXISTS %s
			(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				time INTEGER,
				link TEXT,
				data TEXT
			);
			''' % (databaseTable)
		)
	except: pass

def _cacheCheck():
	thread = threading.Thread(target = _cacheProcess)
	thread.start()

def _cacheProcess():
	data = database.Database(databaseName, connect = True)
	data._lock()
	_cacheCreate(data)
	data._unlock()
	try:
		while True:
			# Execute the select and delete as atomic operations.
			data._lock()
			result = data._selectSingle('SELECT id, time, link, data FROM %s ORDER BY time ASC LIMIT 1;' % (databaseTable))
			if not result: raise Exception()
			data._delete('DELETE FROM %s WHERE id IS %d;' % (databaseTable, result[0]), commit = True)
			data._unlock()
			result = getTrakt(url = result[2], post = json.loads(result[3]) if result[3] else None, cache = True, check = False, timestamp = result[1])
	except:
		data._unlock()
	data._close()

def _cacheClear():
	try:
		data = database.Database(databaseName, connect = True)
		data._drop(databaseTable, commit = True)
		data._close()
	except:
		tools.Logger.error()

def authTrakt(openSettings = True):
	# NB: Seems like there is a Kodi bug that you can't write the same setting twice in one execution.
	# After writing the second time, the settings still contains the first value.
	# Only write once.
	user = ''
	token = ''
	refresh = ''

	try:
		if getTraktCredentialsInfo() == True:
			if interface.Dialog.option(title = 32315, message = control.lang(32511).encode('utf-8') + ' ' + control.lang(32512).encode('utf-8')):
				pass
			else: # Gaia
				return False

		result = getTrakt('/oauth/device/code', {'client_id': getTrakt1()}, direct = True)
		result = json.loads(result)
		expires_in = int(result['expires_in'])
		device_code = result['device_code']
		interval = result['interval']

		# Link and token on top for skins that don't scroll text in a progress dialog.
		message = ''
		message += interface.Format.fontBold(interface.Translation.string(33381) + ': ' + result['verification_url'])
		message += interface.Format.newline()
		message += interface.Format.fontBold(interface.Translation.string(33495) + ': ' + result['user_code'])
		message += interface.Format.newline() + interface.Translation.string(33494) + ' ' + interface.Translation.string(33978)

		clipboard.Clipboard.copy(result['user_code'])
		progressDialog = interface.Dialog.progress(title = 32315, message = message, background = False)

		for i in range(0, expires_in):
			try:
				if progressDialog.iscanceled(): break
				time.sleep(1)
				if not float(i) % interval == 0: raise Exception()
				r = getTrakt('/oauth/device/token', {'client_id': getTrakt1(), 'client_secret': getTrakt2(), 'code': device_code}, direct = True)
				r = json.loads(r)
				if 'access_token' in r: break
			except:
				pass

		try: progressDialog.close()
		except: pass

		token, refresh = r['access_token'], r['refresh_token']

		headers = {'Content-Type': 'application/json', 'trakt-api-key': getTrakt1(), 'trakt-api-version': '2', 'Authorization': 'Bearer %s' % token}

		result = client.request('http://api-v2launch.trakt.tv/users/me', headers=headers)
		result = json.loads(result)

		user = result['username']
	except:
		tools.Logger.error()

	tools.Settings.set('accounts.informants.trakt.user', user)
	tools.Settings.set('accounts.informants.trakt.token', token)
	tools.Settings.set('accounts.informants.trakt.refresh', refresh)

	if openSettings:
		tools.Settings.launch(category = tools.Settings.CategoryAccounts)

	return {'user' : user, 'token' : token, 'refresh' : refresh}


def getTraktCredentialsInfo():
	enabled = tools.Settings.getString('accounts.informants.trakt.enabled') == 'true'
	user = tools.Settings.getString('accounts.informants.trakt.user').strip()
	token = tools.Settings.getString('accounts.informants.trakt.token')
	refresh = tools.Settings.getString('accounts.informants.trakt.refresh')
	if (not enabled or user == '' or token == '' or refresh == ''): return False
	return True


def getTraktIndicatorsInfo():
	indicators = tools.Settings.getString('general.playback.status') if getTraktCredentialsInfo() == False else tools.Settings.getString('general.playback.status.alternative')
	indicators = True if indicators == '1' else False
	return indicators


def getTraktAddonMovieInfo():
	try: scrobble = control.addon('script.trakt').getSetting('scrobble_movie')
	except: scrobble = ''
	try: ExcludeHTTP = control.addon('script.trakt').getSetting('ExcludeHTTP')
	except: ExcludeHTTP = ''
	try: authorization = control.addon('script.trakt').getSetting('authorization')
	except: authorization = ''
	if scrobble == 'true' and ExcludeHTTP == 'false' and not authorization == '': return True
	else: return False


def getTraktAddonEpisodeInfo():
	try: scrobble = control.addon('script.trakt').getSetting('scrobble_episode')
	except: scrobble = ''
	try: ExcludeHTTP = control.addon('script.trakt').getSetting('ExcludeHTTP')
	except: ExcludeHTTP = ''
	try: authorization = control.addon('script.trakt').getSetting('authorization')
	except: authorization = ''
	if scrobble == 'true' and ExcludeHTTP == 'false' and not authorization == '': return True
	else: return False

def watch(imdb = None, tvdb = None, season = None, episode = None, refresh = True, notification = False):
	if tvdb == None:
		markMovieAsWatched(imdb)
		cachesyncMovies()
	elif not episode == None:
		markEpisodeAsWatched(imdb, tvdb, season, episode)
		cachesyncTV(imdb)
	elif not season == None:
		markSeasonAsWatched(imdb, tvdb, season)
		cachesyncTV(imdb)
	elif not tvdb == None:
		markTVShowAsWatched(imdb, tvdb)
		cachesyncTV(imdb)
	else:
		markMovieAsWatched(imdb)
		cachesyncMovies()
	if refresh: control.refresh()
	if notification: interface.Dialog.notification(title = 32315, message = 35502, icon = interface.Dialog.IconSuccess)

def unwatch(imdb = None, tvdb = None, season = None, episode = None, refresh = True, notification = False):
	if tvdb == None:
		markMovieAsNotWatched(imdb)
		cachesyncMovies()
	elif not episode == None:
		markEpisodeAsNotWatched(imdb, tvdb, season, episode)
		cachesyncTV(imdb)
	elif not season == None:
		markSeasonAsNotWatched(imdb, tvdb, season)
		cachesyncTV(imdb)
	elif not tvdb == None:
		markTVShowAsNotWatched(imdb, tvdb)
		cachesyncTV(imdb)
	else:
		markMovieAsNotWatched(imdb)
		cachesyncMovies()
	if refresh: control.refresh()
	if notification: interface.Dialog.notification(title = 32315, message = 35503, icon = interface.Dialog.IconSuccess)

def rate(imdb = None, tvdb = None, season = None, episode = None):
	return _rating(action = 'rate', imdb = imdb, tvdb = tvdb, season = season, episode = episode)

def unrate(imdb = None, tvdb = None, season = None, episode = None):
	return _rating(action = 'unrate', imdb = imdb, tvdb = tvdb, season = season, episode = episode)

def rateShow(imdb = None, tvdb = None, season = None, episode = None):
	if tools.Settings.getInteger('accounts.informants.trakt.rating') == 1:
		rate(imdb = imdb, tvdb = tvdb, season = season, episode = episode)

def _rating(action, imdb = None, tvdb = None, season = None, episode = None):
	try:
		addon = 'script.trakt'
		if tools.System.installed(addon):
			data = {}
			data['action'] = action
			if not tvdb == None:
				data['video_id'] = tvdb
				if not episode == None:
					data['media_type'] = 'episode'
					data['dbid'] = 1
					data['season'] = int(season)
					data['episode'] = int(episode)
				elif not season == None:
					data['media_type'] = 'season'
					data['dbid'] = 5
					data['season'] = int(season)
				else:
					data['media_type'] = 'show'
					data['dbid'] = 2
			else:
				data['video_id'] = imdb
				data['media_type'] = 'movie'
				data['dbid'] = 4

			script = os.path.join(tools.System.path(addon), 'resources', 'lib', 'sqlitequeue.py')
			sqlitequeue = imp.load_source('sqlitequeue', script)
			data = {'action' : 'manualRating', 'ratingData' : data}
			sqlitequeue.SqliteQueue().append(data)
		else:
			interface.Dialog.notification(title = 32315, message = 33659)
	except:
		pass

def manager(imdb = None, tvdb = None, season = None, episode = None, refresh = True):
	try:
		interface.Loader.show()
		if not season == None: season = int(season)
		if not episode == None: episode = int(episode)

		lists = []
		try:
			result = getTrakt('/users/me/lists')
			result = tools.Converter.jsonFrom(result)
			result = [(i['name'], i['ids']['slug']) for i in result]
			result = [result[i//2] for i in range(len(result)*2)]
			for i in range(0, len(result), 2):
				lists.append({
					'title' : result[i][1],
					'items' : [
						{'title' : interface.Translation.string(32521) % result[i][0], 'value' : interface.Translation.string(33580) % result[i][0], 'return' : '/users/me/lists/%s/items' % result[i][1]},
						{'title' : interface.Translation.string(32522) % result[i+1][0], 'value' : interface.Translation.string(33581) % result[i+1][0], 'return' : '/users/me/lists/%s/items/remove' % lists[i+1][1]},
					],
				})
		except:
			tools.Logger.error()

		items = [
			{'title' : interface.Dialog.prefixBack(33486), 'close' : True},
			{
				'title' : 35500,
				'items' : [
					{'title' : 33651, 'value' : 33655, 'return' : 'watch'},
					{'title' : 33652, 'value' : 33656, 'return' : 'unwatch'},
				],
			},
			{
				'title' : 35501,
				'items' : [
					{'title' : 33653, 'value' : 33657, 'return' : 'rate'},
					{'title' : 33654, 'value' : 33658, 'return' : 'unrate'},
				],
			},
			{
				'title' : 32032,
				'items' : [
					{'title' : 32516, 'value' : 33575, 'return' : '/sync/collection'},
					{'title' : 32517, 'value' : 33576, 'return' : '/sync/collection/remove'},
				],
			},
			{
				'title' : 32033,
				'items' : [
					{'title' : 32518, 'value' : 33577, 'return' : '/sync/watchlist'},
					{'title' : 32519, 'value' : 33578, 'return' : '/sync/watchlist/remove'},
				],
			},
		]
		items += lists
		items += [{
			'title' : 33002,
			'items' : [
				{'title' : 32520, 'value' : 33579, 'return' : '/users/me/lists/%s/items'},
			],
		}]

		interface.Loader.hide()
		select = interface.Dialog.information(title = 32070, items = items)

		if select:
			if select in ['watch', 'unwatch']:
				interface.Loader.show()
				globals()[select](imdb = imdb, tvdb = tvdb, season = season, episode = episode, refresh = refresh, notification = True)
				interface.Loader.hide()
			elif select in ['rate', 'unrate']:
				interface.Loader.show()
				globals()[select](imdb = imdb, tvdb = tvdb, season = season, episode = episode)
				interface.Loader.hide()
			else:
				interface.Loader.show()
				if tvdb == None:
					post = {"movies": [{"ids": {"imdb": imdb}}]}
				else:
					if not episode == None:
						post = {"shows": [{"ids": {"tvdb": tvdb}, "seasons": [{"number": season, "episodes": [{"number": episode}]}]}]}
					elif not season == None:
						post = {"shows": [{"ids": {"tvdb": tvdb}, "seasons": [{"number": season}]}]}
					else:
						post = {"shows": [{"ids": {"tvdb": tvdb}}]}

				if select == '/users/me/lists/%s/items':
					slug = listAdd(successNotification = False)
					if not slug == None: getTrakt(select % slug, post = post)
				else:
					getTrakt(select, post = post)

				interface.Loader.hide()
				interface.Dialog.notification(title = 32315, message = 33583 if '/remove' in select else 33582, icon = interface.Dialog.IconSuccess)
	except:
		tools.Logger.error()
		interface.Loader.hide()


def listAdd(successNotification = True):
	t = control.lang(32520).encode('utf-8')
	k = control.keyboard('', t) ; k.doModal()
	new = k.getText() if k.isConfirmed() else None
	if (new == None or new == ''): return
	result = getTrakt('/users/me/lists', post = {"name" : new, "privacy" : "private"})

	try:
		slug = json.loads(result)['ids']['slug']
		if successNotification:
			interface.Dialog.notification(title = 32070, message = 33661, icon = interface.Dialog.IconSuccess)
		return slug
	except:
		interface.Dialog.notification(title = 32070, message = 33584, icon = interface.Dialog.IconError)
		return None


def lists(id = None):
	return cache.get(getTraktAsJson, 48, 'https://api.trakt.tv/users/me/lists' + ('' if id == None else ('/' + str(id))))


def list(id):
	return lists(id = id)


def slug(name):
	name = name.strip()
	name = name.lower()
	name = re.sub('[^a-z0-9_]', '-', name)
	name = re.sub('--+', '-', name)
	return name


def verify(authentication = None):
	try:
		if getTraktAsJson('/sync/last_activities', authentication = authentication):
			return True
	except: pass
	return False


def getActivity():
	try:
		i = getTraktAsJson('/sync/last_activities')

		activity = []
		activity.append(i['movies']['collected_at'])
		activity.append(i['episodes']['collected_at'])
		activity.append(i['movies']['watchlisted_at'])
		activity.append(i['shows']['watchlisted_at'])
		activity.append(i['seasons']['watchlisted_at'])
		activity.append(i['episodes']['watchlisted_at'])
		activity.append(i['lists']['updated_at'])
		activity.append(i['lists']['liked_at'])
		activity = [int(cleandate.iso_2_utc(i)) for i in activity]
		activity = sorted(activity, key=int)[-1]

		return activity
	except:
		pass


def getWatchedActivity():
	try:
		i = getTraktAsJson('/sync/last_activities')

		activity = []
		activity.append(i['movies']['watched_at'])
		activity.append(i['episodes']['watched_at'])
		activity = [int(cleandate.iso_2_utc(i)) for i in activity]
		activity = sorted(activity, key=int)[-1]

		return activity
	except:
		pass


def cachesyncMovies(timeout=0):
	indicators = cache.get(syncMovies, timeout)
	return indicators


def timeoutsyncMovies():
	timeout = cache.timeout(syncMovies)
	return timeout


def syncMovies():
	try:
		if getTraktCredentialsInfo() == False: return
		indicators = getTraktAsJson('/users/me/watched/movies')
		indicators = [i['movie']['ids'] for i in indicators]
		indicators = [str(i['imdb']) for i in indicators if 'imdb' in i]
		return indicators
	except:
		pass


# Gaia
def watchedMovies():
	try:
		if getTraktCredentialsInfo() == False: return
		return getTraktAsJson('/users/me/watched/movies?extended=full')
	except:
		pass


# Gaia
def watchedMoviesTime(imdb):
	try:
		imdb = str(imdb)
		items = watchedMovies()
		for item in items:
			if str(item['movie']['ids']['imdb']) == imdb:
				return item['last_watched_at']
	except:
		pass


def cachesyncTV(imdb):
	threads = [threading.Thread(target = cachesyncTVShows), threading.Thread(target = cachesyncSeason, args = (imdb,))]
	[i.start() for i in threads]
	[i.join() for i in threads]


def cachesyncTVShows(timeout=0):
	indicators = cache.get(syncTVShows, timeout)
	return indicators


def timeoutsyncTVShows():
	timeout = cache.timeout(syncTVShows)
	return timeout


def syncTVShows():
	try:
		if getTraktCredentialsInfo() == False: return
		indicators = getTraktAsJson('/users/me/watched/shows?extended=full')
		indicators = [(i['show']['ids']['tvdb'], i['show']['aired_episodes'], sum([[(s['number'], e['number']) for e in s['episodes']] for s in i['seasons']], [])) for i in indicators]
		indicators = [(str(i[0]), int(i[1]), i[2]) for i in indicators]
		return indicators
	except:
		pass


# Gaia
def watchedShows():
	try:
		if getTraktCredentialsInfo() == False: return
		return getTraktAsJson('/users/me/watched/shows?extended=full')
	except:
		pass


# Gaia
def watchedShowsTime(tvdb, season, episode):
	try:
		tvdb = str(tvdb)
		season = int(season)
		episode = int(episode)
		items = watchedShows()
		for item in items:
			if str(item['show']['ids']['tvdb']) == tvdb:
				seasons = item['seasons']
				for s in seasons:
					if s['number'] == season:
						episodes = s['episodes']
						for e in episodes:
							if e['number'] == episode:
								return e['last_watched_at']
	except:
		pass


def cachesyncSeason(imdb, timeout=0):
	indicators = cache.get(syncSeason, timeout, imdb)
	return indicators


def timeoutsyncSeason(imdb):
	timeout = cache.timeout(syncSeason, imdb)
	return timeout


def syncSeason(imdb):
	try:
		if getTraktCredentialsInfo() == False: return
		indicators = getTraktAsJson('/shows/%s/progress/watched?specials=false&hidden=false' % imdb)
		indicators = indicators['seasons']
		indicators = [(i['number'], [x['completed'] for x in i['episodes']]) for i in indicators]
		indicators = ['%01d' % int(i[0]) for i in indicators if not False in i[1]]
		return indicators
	except:
		pass


# Gaia
def showCount(imdb, refresh = True, wait = False):
	try:
		if not imdb: return None
		result = {'total' : 0, 'watched' : 0, 'unwatched' : 0}
		indicators = seasonCount(imdb = imdb, refresh = refresh, wait = wait)
		for indicator in indicators:
			result['total'] += indicator['total']
			result['watched'] += indicator['watched']
			result['unwatched'] += indicator['unwatched']
		return result
	except:
		return None

def seasonCount(imdb, refresh = True, wait = False):
	try:
		if not imdb: return None
		if not imdb.startswith('tt'): imdb = 'tt' + imdb
		indicators = cache.cache_existing(_seasonCountRetrieve, imdb)
		if refresh:
			# NB: Do not retrieve a fresh count, otherwise loading show/season menus are slow.
			thread = threading.Thread(target = _seasonCountCache, args = (imdb,))
			thread.start()
			if wait:
				thread.join()
				indicators = cache.cache_existing(_seasonCountRetrieve, imdb)
		return indicators
	except:
		return None

def _seasonCountCache(imdb):
	return cache.get(_seasonCountRetrieve, 0, imdb)

def _seasonCountRetrieve(imdb):
	try:
		if getTraktCredentialsInfo() == False: return
		indicators = getTraktAsJson('/shows/%s/progress/watched?specials=false&hidden=false' % imdb)
		seasons = indicators['seasons']
		return [{'total' : season['aired'], 'watched' : season['completed'], 'unwatched' : season['aired'] - season['completed']} for season in seasons]
	except:
		return None


def markMovieAsWatched(imdb):
	if not imdb.startswith('tt'): imdb = 'tt' + imdb
	return getTrakt('/sync/history', {"movies": [{"ids": {"imdb": imdb}}]})


def markMovieAsNotWatched(imdb):
	if not imdb.startswith('tt'): imdb = 'tt' + imdb
	return getTrakt('/sync/history/remove', {"movies": [{"ids": {"imdb": imdb}}]})


def markTVShowAsWatched(imdb, tvdb):
	if imdb and not imdb.startswith('tt'): imdb = 'tt' + imdb
	result = getTrakt('/sync/history', {"shows": [{"ids": {"tvdb": tvdb}}]})
	seasonCount(imdb)
	return result


def markTVShowAsNotWatched(imdb, tvdb):
	if imdb and not imdb.startswith('tt'): imdb = 'tt' + imdb
	result = getTrakt('/sync/history/remove', {"shows": [{"ids": {"tvdb": tvdb}}]})
	seasonCount(imdb)
	return result


def markSeasonAsWatched(imdb, tvdb, season):
	if imdb and not imdb.startswith('tt'): imdb = 'tt' + imdb
	season = int('%01d' % int(season))
	result = getTrakt('/sync/history', {"shows": [{"seasons": [{"number": season}], "ids": {"tvdb": tvdb}}]})
	seasonCount(imdb)
	return result


def markSeasonAsNotWatched(imdb, tvdb, season):
	if imdb and not imdb.startswith('tt'): imdb = 'tt' + imdb
	season = int('%01d' % int(season))
	result = getTrakt('/sync/history/remove', {"shows": [{"seasons": [{"number": season}], "ids": {"tvdb": tvdb}}]})
	seasonCount(imdb)
	return result


def markEpisodeAsWatched(imdb, tvdb, season, episode):
	if imdb and not imdb.startswith('tt'): imdb = 'tt' + imdb
	season, episode = int('%01d' % int(season)), int('%01d' % int(episode))
	result = getTrakt('/sync/history', {"shows": [{"seasons": [{"episodes": [{"number": episode}], "number": season}], "ids": {"tvdb": tvdb}}]})
	seasonCount(imdb)
	return result


def markEpisodeAsNotWatched(imdb, tvdb, season, episode):
	if imdb and not imdb.startswith('tt'): imdb = 'tt' + imdb
	season, episode = int('%01d' % int(season)), int('%01d' % int(episode))
	result = getTrakt('/sync/history/remove', {"shows": [{"seasons": [{"episodes": [{"number": episode}], "number": season}], "ids": {"tvdb": tvdb}}]})
	seasonCount(imdb)
	return result


def getMovieTranslation(id, lang, full=False):
	url = '/movies/%s/translations/%s' % (id, lang)
	try:
		item = cache.get(getTraktAsJson, 48, url)[0]
		result = item if full else item.get('title')
		return None if result == 'none' else result
	except:
		pass


def getTVShowTranslation(id, lang, season=None, episode=None, full=False):
	if season and episode:
		url = '/shows/%s/seasons/%s/episodes/%s/translations/%s' % (id, season, episode, lang)
	else:
		url = '/shows/%s/translations/%s' % (id, lang)
	try:
		item = cache.get(getTraktAsJson, 48, url)[0]
		result = item if full else item.get('title')
		return None if result == 'none' else result
	except:
		pass


def getMovieSummary(id):
	return cache.get(getTraktAsJson, 48, '/movies/%s' % id)


def getTVShowSummary(id):
	return cache.get(getTraktAsJson, 48, '/shows/%s' % id)


def sort_list(sort_key, sort_direction, list_data):
	reverse = False if sort_direction == 'asc' else True
	if sort_key == 'rank':
		return sorted(list_data, key=lambda x: x['rank'], reverse=reverse)
	elif sort_key == 'added':
		return sorted(list_data, key=lambda x: x['listed_at'], reverse=reverse)
	elif sort_key == 'title':
		return sorted(list_data, key=lambda x: utils.title_key(x[x['type']].get('title')), reverse=reverse)
	elif sort_key == 'released':
		return sorted(list_data, key=lambda x: x[x['type']].get('first_aired', ''), reverse=reverse)
	elif sort_key == 'runtime':
		return sorted(list_data, key=lambda x: x[x['type']].get('runtime', 0), reverse=reverse)
	elif sort_key == 'popularity':
		return sorted(list_data, key=lambda x: x[x['type']].get('votes', 0), reverse=reverse)
	elif sort_key == 'percentage':
		return sorted(list_data, key=lambda x: x[x['type']].get('rating', 0), reverse=reverse)
	elif sort_key == 'votes':
		return sorted(list_data, key=lambda x: x[x['type']].get('votes', 0), reverse=reverse)
	else:
		return list_data


def getTraktAsJson(url, post = None, authentication = None):
	try:
		res_headers = {}
		r = getTrakt(url = url, post = post, extended = True, authentication = authentication)
		if isinstance(r, tuple) and len(r) == 2:
			res_headers = r[1]
			r = r[0]
		r = utils.json_loads_as_str(r)
		res_headers = dict((k.lower(), v) for k, v in res_headers.iteritems())
		if 'x-sort-by' in res_headers and 'x-sort-how' in res_headers:
			r = sort_list(res_headers['x-sort-by'], res_headers['x-sort-how'], r)
		return r
	except:
		pass


def getMovieAliases(id):
	try: return cache.get(getTraktAsJson, 48, '/movies/%s/aliases' % id)
	except: return []


def getTVShowAliases(id):
	try: return cache.get(getTraktAsJson, 48, '/shows/%s/aliases' % id)
	except: return []

def getTVShowSummary(id, full=True):
	try:
		url = '/shows/%s' % id
		if full: url += '?extended=full'
		return cache.get(getTraktAsJson, 48, url)
	except:
		return


def getPeople(id, content_type, full=True):
	try:
		url = '/%s/%s/people' % (content_type, id)
		if full: url += '?extended=full'
		return cache.get(getTraktAsJson, 48, url)
	except:
		return

def SearchAll(title, year, full=True):
	try:
		return SearchMovie(title, year, full) + SearchTVShow(title, year, full)
	except:
		return

def SearchMovie(title, year, full=True):
	try:
		url = '/search/movie?query=%s' % title

		if year: url += '&year=%s' % year
		if full: url += '&extended=full'
		return getTraktAsJson(url)
	except:
		return

def SearchTVShow(title, year, full=True):
	try:
		url = '/search/show?query=%s' % title

		if year: url += '&year=%s' % year
		if full: url += '&extended=full'
		return getTraktAsJson(url)
	except:
		return


def getGenre(content, type, type_id):
	try:
		r = '/search/%s/%s?type=%s&extended=full' % (type, type_id, content)
		r = cache.get(getTraktAsJson, 48, r)
		r = r[0].get(content, {}).get('genres', [])
		return r
	except:
		return []

# GAIA

def _scrobbleType(type):
	if tools.Media.typeTelevision(type):
		return 'episode'
	else:
		return 'movie'

def scrobbleProgress(type, imdb = None, tvdb = None, season = None, episode = None):
	try:
		type = _scrobbleType(type)
		if not imdb == None: imdb = str(imdb)
		if not tvdb == None: tvdb = int(tvdb)
		if not episode == None: episode = int(episode)
		if not episode == None: episode = int(episode)
		link = '/sync/playback/type'
		items = getTraktAsJson(link)

		if type == 'episode':
			if imdb and items:
				for item in items:
					if 'show' in item and 'imdb' in item['show']['ids'] and item['show']['ids']['imdb'] == imdb:
						if item['episode']['season'] == season and item['episode']['number'] == episode:
							return item['progress']
			if tvdb:
				for item in items:
					if 'show' in item and 'tvdb' in item['show']['ids'] and item['show']['ids']['tvdb'] == tvdb:
						if item['episode']['season'] == season and item['episode']['number'] == episode:
		 					return item['progress']
		else:
			if imdb and items:
				for item in items:
					if 'movie' in item and 'imdb' in item['movie']['ids'] and item['movie']['ids']['imdb'] == imdb:
						return item['progress']
	except:
		tools.Logger.error()
	return 0

# action = start, pause, stop
# type = tools.Media.Type
# progress = float in [0, 100]
def scrobbleUpdate(action, type, imdb = None, tvdb = None, season = None, episode = None, progress = 0):
	try:
		if action:
			type = _scrobbleType(type)
			if not imdb == None: imdb = str(imdb)
			if not tvdb == None: tvdb = int(tvdb)
			if not season == None: season = int(season)
			if not episode == None: episode = int(episode)

			if imdb: link = '/search/imdb/' + str(imdb)
			elif tvdb: link = '/search/tvdb/' + str(tvdb)
			if type == 'episode': link += '?type=show'
			else: link += '?type=movie'
			items = tools.Cache.cache(getTraktAsJson, 760, link)

			if len(items) > 0:
				item = items[0]
				if type == 'episode':
					slug = item['show']['ids']['slug']
					link = '/shows/%s/seasons/%d/episodes/%d' % (slug, season, episode)
					item = tools.Cache.cache(getTraktAsJson, 760, link)
				else:
					item = item['movie']

				if item:
					link = '/scrobble/' + action
					data = {
						type : item,
						'progress' : progress,
						'app_version' : tools.System.version(),
					}
					result = getTrakt(url = link, post = data)
					return 'progress' in result
	except:
		pass
	return False
