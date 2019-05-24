# -*- coding: utf-8 -*-

"""
	Orion
    https://orionoid.com

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
"""

##############################################################################
# ORIONSETTINGS
##############################################################################
# Class for handling the Kodi addon settings.
##############################################################################

import re
import zipfile
import threading
import xbmcaddon
from orion.modules.oriontools import *
from orion.modules.orioninterface import *
from orion.modules.orionstream import *
from orion.modules.oriondatabase import *

OrionSettingsLock = threading.Lock()
OrionSettingsCache = None
OrionSettingsSilent = False
OrionSettingsBackup = False

class OrionSettings:

	##############################################################################
	# CONSTANTS
	##############################################################################

	DatabaseSettings = 'settings'
	DatabaseTemp = 'temp'

	ExtensionManual = 'zip'
	ExtensionAutomatic = 'bck'

	ParameterDefault = 'default'
	ParameterValue = 'value'
	ParameterVisible = 'visible'

	CategoryGeneral = 0
	CategoryAccount = 1
	CategoryFilters = 2

	NotificationsDisabled = 0
	NotificationsEssential = 1
	NotificationsAll = 2

	ScrapingExclusive = 0
	ScrapingSequential = 1
	ScrapingParallel = 2

	ExternalStart = '<!-- ORION FILTERS - %s START -->'
	ExternalEnd = '<!-- ORION FILTERS - %s END -->'

	##############################################################################
	# INTERNAL
	##############################################################################

	@classmethod
	def _filtersAttribute(self, attribute, type = None):
		if not type == None and not type == 'universal':
			attribute = attribute.replace('filters.', 'filters.' + type + '.')
		return attribute

	##############################################################################
	# LAUNCH
	##############################################################################

	@classmethod
	def launch(self, category = None, section = None):
		OrionTools.execute('Addon.OpenSettings(%s)' % OrionTools.addonId())
		if OrionTools.kodiVersionNew():
			if not category == None: OrionTools.execute('SetFocus(%i)' % (int(category) - 100))
		else:
			if not category == None: OrionTools.execute('SetFocus(%i)' % (int(category) + 100))
			if not section == None: OrionTools.execute('SetFocus(%i)' % (int(section) + 200))

	##############################################################################
	# PATH
	##############################################################################

	@classmethod
	def pathAddon(self):
		return OrionTools.pathJoin(OrionTools.addonPath(), 'resources', 'settings.xml')

	@classmethod
	def pathProfile(self):
		return OrionTools.pathJoin(OrionTools.addonProfile(), 'settings.xml')

	##############################################################################
	# HELP
	##############################################################################

	@classmethod
	def help(self, type = None):
		help = not self.getBoolean('help.enabled.general')
		data = OrionTools.fileRead(self.pathProfile())
		if OrionTools.kodiVersionNew(): data = re.sub('(id="help.enabled\..*")(.*)(<\/setting>)', '\\1>%s</setting>' % OrionTools.toBoolean(help, string = True), data, flags = re.IGNORECASE)
		else: data = re.sub('(id="help.enabled\..*?" )(.*)(\/>)', '\\1value="%s" />' % OrionTools.toBoolean(help, string = True), data, flags = re.IGNORECASE)
		OrionTools.fileWrite(self.pathProfile(), data)
		self.launch(category = type)

	##############################################################################
	# SILENT
	##############################################################################

	@classmethod
	def silent(self):
		from orion.modules.orionuser import OrionUser
		global OrionSettingsSilent
		return OrionSettingsSilent or not OrionUser.instance().enabled()

	@classmethod
	def silentSet(self, silent = True):
		global OrionSettingsSilent
		OrionSettingsSilent = silent

	@classmethod
	def silentAllow(self, type = None):
		if self.silent(): return False
		from orion.modules.orionapi import OrionApi
		if type in OrionApi.TypesBlock: return False
		notifications = self.getGeneralNotificationsApi()
		if notifications == OrionSettings.NotificationsDisabled: return False
		elif notifications == OrionSettings.NotificationsAll: return True
		return type == None or not type in OrionApi.TypesNonessential

	##############################################################################
	# DATA
	##############################################################################

	@classmethod
	def data(self):
		data = None
		path = OrionTools.pathJoin(self.pathAddon())
		with open(path, 'r') as file: data = file.read()
		return data

	@classmethod
	def _database(self):
		return OrionDatabase.instance(OrionSettings.DatabaseSettings, default = OrionTools.pathJoin(OrionTools.addonPath(), 'resources'))

	##############################################################################
	# LOCK
	##############################################################################

	@classmethod
	def _lock(self):
		global OrionSettingsLock
		OrionSettingsLock.acquire()

	@classmethod
	def _unlock(self):
		global OrionSettingsLock
		try: OrionSettingsLock.release()
		except: pass

	#############################################################################
	# CACHE
	##############################################################################

	@classmethod
	def cache(self):
		global OrionSettingsCache
		if OrionSettingsCache == None:
			OrionSettingsCache = {
				'enabled' : OrionTools.toBoolean(OrionTools.addon().getSetting('general.settings.cache')),
				'static' : {
					'data' : None,
					'values' : {},
				},
				'dynamic' : {
					'data' : None,
					'values' : {},
				},
			}
		return OrionSettingsCache

	@classmethod
	def cacheClear(self):
		global OrionSettingsCache
		OrionSettingsCache = None

	@classmethod
	def cacheEnabled(self):
		return self.cache()['enabled']

	@classmethod
	def cacheGet(self, id, raw, database = False, obfuscate = False):
		cache = self.cache()
		if raw:
			if cache['static']['data'] == None: cache['static']['data'] = OrionTools.fileRead(self.pathAddon())
			data = cache['static']['data']
			values = cache['static']['values']
			parameter = OrionSettings.ParameterDefault
		else:
			if cache['dynamic']['data'] == None: cache['dynamic']['data'] = OrionTools.fileRead(self.pathProfile())
			data = cache['dynamic']['data']
			values = cache['dynamic']['values']
			parameter = OrionSettings.ParameterValue

		if id in values:
			return values[id]
		elif database:
			result = self._getDatabase(id = id)
			if obfuscate: result = OrionTools.obfuscate(result)
			values[id] = result
			return result
		else:
			result = self.getRaw(id = id, parameter = parameter, data = data)
			if result == None: result = OrionTools.addon().getSetting(id)
			if obfuscate: result = OrionTools.obfuscate(result)
			values[id] = result
			return result

	@classmethod
	def cacheSet(self, id, value):
		self.cache()['dynamic']['values'][id] = value

	##############################################################################
	# SET
	##############################################################################

	@classmethod
	def set(self, id, value, commit = True, cached = False):
		if value is True or value is False:
			value = OrionTools.toBoolean(value, string = True)
		elif OrionTools.isStructure(value) or value is None:
			database = self._database()
			database.insert('INSERT OR IGNORE INTO %s (id) VALUES(?);' % OrionSettings.DatabaseSettings, parameters = (id,), commit = commit)
			database.update('UPDATE %s SET data = ? WHERE id = ?;' % OrionSettings.DatabaseSettings, parameters = (OrionTools.jsonTo(value), id), commit = commit)
			value = ''
		else:
			value = str(value)
		self._lock()
		OrionTools.addon().setSetting(id = id, value = value)
		if cached or self.cacheEnabled(): self.cacheSet(id = id, value = value)
		self._unlock()
		if commit: self._backupAutomatic(force = True)

	##############################################################################
	# GET
	##############################################################################

	@classmethod
	def _getDatabase(self, id):
		try: return OrionTools.jsonFrom(self._database().selectValue('SELECT data FROM %s WHERE id = "%s";' % (OrionSettings.DatabaseSettings, id)))
		except: return None

	@classmethod
	def get(self, id, raw = False, obfuscate = False, cached = True, database = False):
		if not raw and cached and self.cacheEnabled():
			return self.cacheGet(id = id, raw = raw, database = database, obfuscate = obfuscate)
		elif raw:
			return self.getRaw(id = id, obfuscate = obfuscate)
		else:
			self._backupAutomatic()
			data = OrionTools.addon().getSetting(id)
			if obfuscate: data = OrionTools.obfuscate(data)
			return data

	@classmethod
	def getRaw(self, id, parameter = ParameterDefault, data = None, obfuscate = False):
		try:
			if data == None: data = self.data()
			indexStart = data.find(id)
			if indexStart < 0: return None
			indexStart = data.find('"', indexStart)
			if indexStart < 0: return None
			indexEnd = data.find('/>', indexStart)
			if indexEnd < 0: return None
			data = data[indexStart : indexEnd]
			indexStart = data.find(parameter)
			if indexStart < 0: return None
			indexStart = data.find('"', indexStart) + 1
			indexEnd = data.find('"', indexStart)
			data = data[indexStart : indexEnd]
			if obfuscate: data = OrionTools.obfuscate(data)
			return data
		except:
			return None

	@classmethod
	def getString(self, id, raw = False, obfuscate = False):
		return self.get(id = id, raw = raw, obfuscate = obfuscate)

	@classmethod
	def getBoolean(self, id, raw = False, obfuscate = False):
		return OrionTools.toBoolean(self.get(id = id, raw = raw, obfuscate = obfuscate))

	@classmethod
	def getBool(self, id, raw = False, obfuscate = False):
		return self.getBoolean(id = id, raw = raw, obfuscate = obfuscate)

	@classmethod
	def getNumber(self, id, raw = False, obfuscate = False):
		return self.getDecimal(id = id, raw = raw, obfuscate = obfuscate)

	@classmethod
	def getDecimal(self, id, raw = False, obfuscate = False):
		value = self.get(id = id, raw = raw, obfuscate = obfuscate)
		try: return float(value)
		except: return 0

	@classmethod
	def getFloat(self, id, raw = False, obfuscate = False):
		return self.getDecimal(id = id, raw = raw, obfuscate = obfuscate)

	@classmethod
	def getInteger(self, id, raw = False, obfuscate = False):
		value = self.get(id = id, raw = raw, obfuscate = obfuscate)
		try: return int(value)
		except: return 0

	@classmethod
	def getInt(self, id, raw = False, obfuscate = False):
		return self.getInteger(id = id, raw = raw, obfuscate = obfuscate)

	@classmethod
	def getList(self, id):
		result = self._getDatabase(id)
		return [] if result == None or result == '' else result

	@classmethod
	def getObject(self, id):
		result = self._getDatabase(id)
		return None if result == None or result == '' else result

	##############################################################################
	# GET CUSTOM
	##############################################################################

	@classmethod
	def getApp(self, app):
		try: return self.getBoolean('filters.' + app + '.app', raw = True)
		except: return False

	@classmethod
	def getIntegration(self, app):
		try: return self.getString('filters.' + app + '.integration')
		except: return ''

	@classmethod
	def getGeneralNotificationsApi(self):
		return self.getInteger('general.notifications.api')

	@classmethod
	def getGeneralNotificationsNews(self):
		return self.getBoolean('general.notifications.news')

	@classmethod
	def getGeneralScrapingTimeout(self):
		return self.getInteger('general.scraping.timeout')

	@classmethod
	def getGeneralScrapingMode(self):
		return self.getInteger('general.scraping.mode')

	@classmethod
	def getGeneralScrapingCount(self):
		return self.getInteger('general.scraping.count')

	@classmethod
	def getGeneralScrapingQuality(self, index = False):
		quality = max(0, self.getInteger('general.scraping.quality') - 1)
		if not index: quality = OrionStream.QualityOrder[quality]
		return quality

	@classmethod
	def getFiltersBoolean(self, attribute, type = None):
		return self.getBoolean(self._filtersAttribute(attribute, type))

	@classmethod
	def getFiltersInteger(self, attribute, type = None):
		return self.getInteger(self._filtersAttribute(attribute, type))

	@classmethod
	def getFiltersString(self, attribute, type = None):
		return self.getString(self._filtersAttribute(attribute, type))

	@classmethod
	def getFiltersObject(self, attribute, type = None, include = False, exclude = False):
		values = self.getObject(self._filtersAttribute(attribute, type))
		try:
			if include: values = [key for key, value in values.iteritems() if value['enabled']]
		except: pass
		try:
			if exclude: values = [key for key, value in values.iteritems() if not value['enabled']]
		except: pass
		return values if values else [] if (include or exclude) else {}

	@classmethod
	def getFiltersEnabled(self, type = None):
		return self.getFiltersBoolean('filters.enabled', type = type)

	@classmethod
	def getFiltersStreamOrigin(self, type = None, include = False, exclude = False):
		return self.getFiltersObject('filters.stream.origin', type = type, include = include, exclude = exclude)

	@classmethod
	def getFiltersStreamSource(self, type = None, include = False, exclude = False):
		return self.getFiltersObject('filters.stream.source', type = type, include = include, exclude = exclude)

	@classmethod
	def getFiltersStreamHoster(self, type = None, include = False, exclude = False):
		return self.getFiltersObject('filters.stream.hoster', type = type, include = include, exclude = exclude)

	@classmethod
	def getFiltersMetaRelease(self, type = None, include = False, exclude = False):
		return self.getFiltersObject('filters.meta.release', type = type, include = include, exclude = exclude)

	@classmethod
	def getFiltersMetaUploader(self, type = None, include = False, exclude = False):
		return self.getFiltersObject('filters.meta.uploader', type = type, include = include, exclude = exclude)

	@classmethod
	def getFiltersMetaEdition(self, type = None, include = False, exclude = False):
		return self.getFiltersObject('filters.meta.edition', type = type, include = include, exclude = exclude)

	@classmethod
	def getFiltersVideoCodec(self, type = None, include = False, exclude = False):
		return self.getFiltersObject('filters.video.codec', type = type, include = include, exclude = exclude)

	@classmethod
	def getFiltersAudioType(self, type = None, include = False, exclude = False):
		return self.getFiltersObject('filters.audio.type', type = type, include = include, exclude = exclude)

	@classmethod
	def getFiltersAudioSystem(self, type = None, include = False, exclude = False):
		return self.getFiltersObject('filters.audio.system', type = type, include = include, exclude = exclude)

	@classmethod
	def getFiltersAudioCodec(self, type = None, include = False, exclude = False):
		return self.getFiltersObject('filters.audio.codec', type = type, include = include, exclude = exclude)

	@classmethod
	def getFiltersAudioLanguages(self, type = None, include = False, exclude = False):
		return self.getFiltersObject('filters.audio.languages', type = type, include = include, exclude = exclude)

	@classmethod
	def getFiltersSubtitleType(self, type = None, include = False, exclude = False):
		return self.getFiltersObject('filters.subtitle.type', type = type, include = include, exclude = exclude)

	@classmethod
	def getFiltersSubtitleLanguages(self, type = None, include = False, exclude = False):
		return self.getFiltersObject('filters.subtitle.languages', type = type, include = include, exclude = exclude)

	##############################################################################
	# SET CUSTOM
	##############################################################################

	@classmethod
	def setIntegration(self, app, value, commit = True):
		return self.set('filters.' + app + '.integration', value, commit = commit)

	@classmethod
	def setFilters(self, values, wait = False):
		# Do not use threads directly to update settings. Updating the settings in a threads can cause the settings file to become corrupt.
		# This was possibly fixed through the locking mechanism. Launching the thread directly (setFiltersUpdate) should hopefully work now.
		if wait:
			self.setFiltersUpdate(values)
		else:
			#thread = threading.Thread(target = self._setFiltersThread, args = (values,))
			thread = threading.Thread(target = self.setFiltersUpdate, args = (values,))
			thread.start()

	@classmethod
	def _setFiltersThread(self, values):
		# Do not pass the values as plugin parameters, since this immediately fills up the log, since Kodi prints the entire command.
		database = self._database()
		database.create('CREATE TABLE IF NOT EXISTS %s (data TEXT);' % OrionSettings.DatabaseTemp)
		database.insert('INSERT INTO %s (data) VALUES(?);' % OrionSettings.DatabaseTemp, parameters = (OrionTools.jsonTo([value.data() for value in values]),))
		OrionTools.executePlugin(execute = True, action = 'settingsFiltersUpdate')

		# There are thread limbo exceptions thrown here sometimes.
		# Wait for executePlugin() to finish.
		# Since this is a thread, simply sleeping and waiting isn't a problem.
		OrionTools.sleep(3)

	@classmethod
	def setFiltersUpdate(self, values = None):
		from orion.modules.orionapp import OrionApp
		try:
			if values == None:
				database = self._database()
				values = database.selectValue('SELECT data FROM  %s;' % OrionSettings.DatabaseTemp)
				database.drop(OrionSettings.DatabaseTemp)
			if OrionTools.isString(values):
				values = OrionTools.jsonFrom(values)
				values = [OrionStream(value) for value in values]
		except: pass
		apps = [None] + [i.id() for i in OrionApp.instances()]
		for app in apps:
			self.setFiltersStreamOrigin(values, type = app, commit = False)
			self.setFiltersStreamSource(values, type = app, commit = False)
			self.setFiltersStreamHoster(values, type = app, commit = False)
			self.setFiltersMetaRelease(values, type = app, commit = False)
			self.setFiltersMetaUploader(values, type = app, commit = False)
			self.setFiltersMetaEdition(values, type = app, commit = False)
			self.setFiltersVideoCodec(values, type = app, commit = False)
			self.setFiltersAudioType(values, type = app, commit = False)
			self.setFiltersAudioSystem(values, type = app, commit = False)
			self.setFiltersAudioCodec(values, type = app, commit = False)
		self._database()._commit()
		self._backupAutomatic(force = True)

	@classmethod
	def _setFilters(self, values, setting, functionStreams, functionGet, type = None, commit = True):
		if not values: return
		items = {}
		try:
			from orion.modules.orionstream import OrionStream
			for value in values:
				attribute = getattr(value, functionStreams)()
				if not attribute == None:
					items[attribute.lower()] = {'name' : attribute.upper(), 'enabled' : True}
			settings = getattr(self, functionGet)(type = type)
			if settings:
				for key, value in items.iteritems():
					if not key in settings:
						settings[key] = value
				items = settings
		except:
			items = values
		if items: count = len([1 for key, value in items.iteritems() if value['enabled']])
		else: count = 0
		self.set(self._filtersAttribute(setting, type), items, commit = commit)
		self.set(self._filtersAttribute(setting + '.label', type), str(count) + ' ' + OrionTools.translate(32096), commit = commit)

	@classmethod
	def _setFiltersLanguages(self, values, setting, functionStreams, functionGet, type = None, commit = True):
		if not values: return
		if values: count = len([1 for key, value in values.iteritems() if value['enabled']])
		else: count = 0
		self.set(self._filtersAttribute(setting, type), values, commit = commit)
		self.set(self._filtersAttribute(setting + '.label', type), str(count) + ' ' + OrionTools.translate(32096), commit = commit)

	@classmethod
	def setFiltersLimitCount(self, value, type = None, commit = True):
		self.set(self._filtersAttribute('filters.limit.count', type), value, commit = commit)

	@classmethod
	def setFiltersLimitRetry(self, value, type = None, commit = True):
		self.set(self._filtersAttribute('filters.limit.retry', type), value, commit = commit)

	@classmethod
	def setFiltersStreamOrigin(self, values, type = None, commit = True):
		if not values: return
		items = {}
		try:
			from orion.modules.orionstream import OrionStream
			for value in values:
				attribute = value.streamOrigin()
				if not attribute == None and not attribute == '':
					items[attribute.lower()] = {'name' : attribute.upper(), 'type' : value.streamType(), 'enabled' : True}
			settings = self.getFiltersStreamOrigin(type = type)
			if settings:
				for key, value in items.iteritems():
					if not key in settings:
						settings[key] = value
				items = settings
		except:
			items = values
		if items: count = len([1 for key, value in items.iteritems() if value['enabled']])
		else: count = 0
		self.set(self._filtersAttribute('filters.stream.origin', type), items, commit = commit)
		self.set(self._filtersAttribute('filters.stream.origin.label', type), str(count) + ' ' + OrionTools.translate(32096), commit = commit)

	@classmethod
	def setFiltersStreamSource(self, values, type = None, commit = True):
		if not values: return
		items = {}
		try:
			from orion.modules.orionstream import OrionStream
			for value in values:
				attribute = value.streamSource()
				if not attribute == None and not attribute == '':
					items[attribute.lower()] = {'name' : attribute.upper(), 'type' : value.streamType(), 'enabled' : True}
			settings = self.getFiltersStreamSource(type = type)
			if settings:
				for key, value in items.iteritems():
					if not key in settings:
						settings[key] = value
				items = settings
		except:
			items = values
		if items: count = len([1 for key, value in items.iteritems() if value['enabled']])
		else: count = 0
		self.set(self._filtersAttribute('filters.stream.source', type), items, commit = commit)
		self.set(self._filtersAttribute('filters.stream.source.label', type), str(count) + ' ' + OrionTools.translate(32096), commit = commit)

	@classmethod
	def setFiltersStreamHoster(self, values, type = None, commit = True):
		if not values: return
		items = {}
		try:
			from orion.modules.orionstream import OrionStream
			for value in values:
				attribute = value.streamHoster()
				if not attribute == None and not attribute == '':
					items[attribute.lower()] = {'name' : attribute.upper(), 'enabled' : True}
			settings = self.getFiltersStreamHoster(type = type)
			if settings:
				for key, value in items.iteritems():
					if not key in settings:
						settings[key] = value
				items = settings
		except:
			items = values
		if items: count = len([1 for key, value in items.iteritems() if value['enabled']])
		else: count = 0
		self.set(self._filtersAttribute('filters.stream.hoster', type), items, commit = commit)
		self.set(self._filtersAttribute('filters.stream.hoster.label', type), str(count) + ' ' + OrionTools.translate(32096), commit = commit)

	@classmethod
	def setFiltersMetaRelease(self, values, type = None, commit = True):
		self._setFilters(values, 'filters.meta.release', 'metaRelease', 'getFiltersMetaRelease', type, commit = commit)

	@classmethod
	def setFiltersMetaUploader(self, values, type = None, commit = True):
		self._setFilters(values, 'filters.meta.uploader', 'metaUploader', 'getFiltersMetaUploader', type, commit = commit)

	@classmethod
	def setFiltersMetaEdition(self, values, type = None, commit = True):
		self._setFilters(values, 'filters.meta.edition', 'metaEdition', 'getFiltersMetaEdition', type, commit = commit)

	@classmethod
	def setFiltersVideoCodec(self, values, type = None, commit = True):
		self._setFilters(values, 'filters.video.codec', 'videoCodec', 'getFiltersVideoCodec', type, commit = commit)

	@classmethod
	def setFiltersAudioType(self, values, type = None, commit = True):
		self._setFilters(values, 'filters.audio.type', 'audioType', 'getFiltersAudioType', type, commit = commit)

	@classmethod
	def setFiltersAudioSystem(self, values, type = None, commit = True):
		self._setFilters(values, 'filters.audio.system', 'audioSystem', 'getFiltersAudioSystem', type, commit = commit)

	@classmethod
	def setFiltersAudioCodec(self, values, type = None, commit = True):
		self._setFilters(values, 'filters.audio.codec', 'audioCodec', 'getFiltersAudioCodec', type, commit = commit)

	@classmethod
	def setFiltersAudioLanguages(self, values, type = None, commit = True):
		self._setFiltersLanguages(values, 'filters.audio.languages', 'audioLanguages', 'getFiltersAudioLanguages', type, commit = commit)

	@classmethod
	def setFiltersSubtitleType(self, values, type = None, commit = True):
		self._setFilters(values, 'filters.subtitle.type', 'subtitleType', 'getFiltersSubtitleType', type, commit = commit)

	@classmethod
	def setFiltersSubtitleLanguages(self, values, type = None, commit = True):
		self._setFiltersLanguages(values, 'filters.subtitle.languages', 'subtitleLanguages', 'getFiltersSubtitleLanguages', type, commit = commit)

	##############################################################################
	# BACKUP
	##############################################################################

	@classmethod
	def _backupPath(self, clear = False):
		path = OrionTools.pathResolve('special://temp/')
		path = OrionTools.pathJoin(path, OrionTools.addonName().lower(), 'backup')
		OrionTools.directoryDelete(path)
		OrionTools.directoryCreate(path)
		return path

	@classmethod
	def _backupName(self, extension = ExtensionManual):
		# Windows does not support colons in file names.
		return OrionTools.addonName() + ' ' + OrionTools.translate(32170) + ' ' + OrionTools.timeFormat(format = '%Y-%m-%d %H.%M.%S') + '%s.' + extension

	@classmethod
	def _backupAutomaticValid(self):
		return OrionTools.toBoolean(OrionTools.addon().getSetting(id = 'internal.backup'))

	@classmethod
	def _backupAutomatic(self, force = False):
		if not self._backupAutomaticValid() or OrionTools.toBoolean(OrionTools.addon().getSetting(id = 'general.settings.backup')):
			if not self._backupAutomaticImport(force = force):
				self._backupAutomaticExport(force = force)

	@classmethod
	def _backupAutomaticExport(self, force = False):
		global OrionSettingsBackup
		self._lock()
		OrionTools.addon().setSetting(id = 'internal.backup', value = OrionTools.toBoolean(True, string = True))
		self._unlock()
		if force or not OrionSettingsBackup:
			OrionSettingsBackup = True
			directory = OrionTools.addonProfile()
			fileFrom = OrionTools.pathJoin(directory, 'settings.xml')
			if 'internal.backup' in OrionTools.fileRead(fileFrom):
				fileTo = OrionTools.pathJoin(directory, 'settings.' + OrionSettings.ExtensionAutomatic)
				return OrionTools.fileCopy(fileFrom, fileTo, overwrite = True)
		return False

	@classmethod
	def _backupAutomaticImport(self, force = False):
		if self._backupAutomaticValid():
			# Why return force?
			# When returning force, the backup is never overwritten with new values.
			# If simply returning False causes problems, this has to be investigated again.

			#return force # Must return force
			return False
		else:
			directory = OrionTools.addonProfile()
			fileTo = OrionTools.pathJoin(directory, 'settings.xml')
			fileFrom = OrionTools.pathJoin(directory, 'settings.' + OrionSettings.ExtensionAutomatic)
			return OrionTools.fileCopy(fileFrom, fileTo, overwrite = True)

	@classmethod
	def backupImport(self, path = None, extension = ExtensionManual):
		try:
			from orion.modules.orionuser import OrionUser

			if path == None: path = OrionInterface.dialogBrowse(title = 32170, type = OrionInterface.BrowseFile, mask = extension)

			directory = self._backupPath(clear = True)
			directoryData = OrionTools.addonProfile()

			file = zipfile.ZipFile(path, 'r')
			file.extractall(directory)
			file.close()

			directories, files = OrionTools.directoryList(directory)
			counter = 0
			for file in files:
				fileFrom = OrionTools.pathJoin(directory, file)
				fileTo = OrionTools.pathJoin(directoryData, file)
				if OrionTools.fileMove(fileFrom, fileTo, overwrite = True):
					counter += 1

			OrionTools.directoryDelete(path = directory, force = True)

			# Get updated user status
			OrionInterface.loaderShow()
			OrionUser.instance().update()
			self.cacheClear()
			OrionInterface.loaderHide()

			if counter > 0:
				OrionInterface.dialogNotification(title = 32170, message = 33014, icon = OrionInterface.IconSuccess)
				return True
			else:
				OrionInterface.dialogNotification(title = 32170, message = 33016, icon = OrionInterface.IconError)
				return False
		except:
			OrionInterface.dialogNotification(title = 32170, message = 33016, icon = OrionInterface.IconError)
			OrionTools.error()
			return False

	@classmethod
	def backupExport(self, path = None, extension = ExtensionManual):
		try:
			if path == None: path = OrionInterface.dialogBrowse(title = 32170, type = OrionInterface.BrowseDirectoryWrite)

			OrionTools.directoryCreate(path)
			name = self._backupName(extension = extension)
			path = OrionTools.pathJoin(path, name)
			counter = 0
			suffix = ''
			while OrionTools.fileExists(path % suffix):
				counter += 1
				suffix = ' [%d]' % counter
			path = path % suffix

			file = zipfile.ZipFile(path, 'w')

			directory = self._backupPath(clear = True)
			directoryData = OrionTools.addonProfile()
			directories, files = OrionTools.directoryList(directoryData)

			content = []
			settings = ['settings.xml', (OrionSettings.DatabaseSettings + OrionDatabase.Extension).lower()]
			for i in range(len(files)):
				if files[i].lower() in settings:
					content.append(files[i])

			tos = [OrionTools.pathJoin(directory, i) for i in content]
			froms = [OrionTools.pathJoin(directoryData, i) for i in content]

			for i in range(len(content)):
				try:
					OrionTools.fileCopy(froms[i], tos[i], overwrite = True)
					file.write(tos[i], content[i])
				except: pass

			file.close()
			OrionTools.directoryDelete(path = directory, force = True)
			if OrionTools.fileExists(path):
				OrionInterface.dialogNotification(title = 32170, message = 33013, icon = OrionInterface.IconSuccess)
				return True
			else:
				OrionInterface.dialogNotification(title = 32170, message = 33015, icon = OrionInterface.IconError)
				return False
		except:
			OrionInterface.dialogNotification(title = 32170, message = 33015, icon = OrionInterface.IconError)
			OrionTools.error()
			return False

	##############################################################################
	# EXTERNAL
	##############################################################################

	@classmethod
	def _externalComment(self, app):
		return app.upper()

	@classmethod
	def _externalStart(self, app):
		return OrionSettings.ExternalStart % self._externalComment(app)

	@classmethod
	def _externalEnd(self, app):
		return OrionSettings.ExternalEnd % self._externalComment(app)

	@classmethod
	def _externalClean(self, data):
		while re.search('(\r?\n){3,}', data): data = re.sub('(\r?\n){3,}', '\n\n', data)
		return data

	@classmethod
	def externalCategory(self, app):
		if app == None: return self.launch(OrionSettings.CategoryFilters)
		elif not OrionTools.isString(app): app = app.id()
		if app == 'universal': return self.launch(OrionSettings.CategoryFilters)
		data = OrionTools.fileRead(self.pathAddon())
		data = data[:data.find('filters.' + app)]
		self.launch(data.count('<category') - 1)

	@classmethod
	def externalInsert(self, app, check = False):
		from orion.modules.orionapi import OrionApi
		if not app.key() == OrionApi._keyInternal() and not OrionTools.addonName().lower() == app.name().lower(): # Check name as well, in case the key changes.
			appId = app.id()
			if not check or not self.getApp(appId):
				self.externalRemove(app)
				data = OrionTools.fileRead(self.pathAddon())

				commentStart = self._externalStart('universal')
				commentEnd = self._externalEnd('universal')
				appComment = self._externalComment(appId)

				subset = data[data.find(commentStart) + len(commentStart) : data.find(commentEnd)].strip('\n').strip('\r')

				index = subset.find('filters.app')
				subset = subset[:index] + subset[index:].replace('default="false"', 'default="true"', 1)

				index = subset.find('filters.enabled')
				subset = subset[:index] + subset[index:].replace('default="true"', 'default="false"', 1)

				subset = subset.replace('&type=universal', '&type=' + appId)
				subset = subset.replace('id="filters.', 'id="filters.' + appId + '.')
				subset = subset.replace('id="help.filters.', 'id="help.filters.' + appId + '.')
				subset = subset.replace('id="help.enabled.filters', 'id="help.enabled.filters.' + appId)
				subset = subset.replace('id="help.enable.filters', 'id="help.enable.filters.' + appId)
				subset = subset.replace('id="help.disable.filters', 'id="help.disable.filters.' + appId)
				subset = subset.replace('action=settingsHelp&type=2', 'action=settingsHelp&type=' + str(data.count('<category')))

				appStart = '\n\n' + OrionSettings.ExternalStart % appComment + '\n<category label = "' + app.name() + '">'
				appEnd = '</category>\n' + OrionSettings.ExternalEnd % appComment + '\n'
				subset = appStart + subset + appEnd

				end = '</category>'
				end = data.rfind(end) + len(end)

				endComment = 'END -->'
				if data.find(endComment, end) > 0: end = data.find(endComment, end) + len(endComment)

				data = data[:end] + subset + data[end:]
				OrionTools.fileWrite(self.pathAddon(), self._externalClean(data))

				database = OrionDatabase(path = OrionTools.pathJoin(OrionTools.addonPath(), 'resources', OrionSettings.DatabaseSettings + OrionDatabase.Extension))
				settings = database.select('SELECT id, data FROM  %s;' % OrionSettings.DatabaseSettings)
				for setting in settings:
					if setting[0].startswith('filters.'):
						OrionSettings.set(self._filtersAttribute(setting[0], appId), OrionTools.jsonFrom(setting[1]))

	@classmethod
	def externalRemove(self, app):
		if not OrionTools.isString(app): app = app.id()
		data = OrionTools.fileRead(self.pathAddon())
		commentStart = self._externalStart(app)
		commentEnd = self._externalEnd(app)
		indexStart = data.find(commentStart)
		if indexStart >= 0:
			indexEnd = data.find(commentEnd)
			if indexStart > 0 and indexEnd > indexStart:
				data = data[:indexStart] + data[indexEnd + len(commentEnd):]
			OrionTools.fileWrite(self.pathAddon(), self._externalClean(data))

	@classmethod
	def externalClean(self):
		# orionremove
		# This is needed for old Orion versions that still used the addon name instead of the app ID.
		# Otherwise each addon might have a double entry in Orion's custom filters.
		# Can be removed in later versions, but leave in for now.
		from orion.modules.orionapp import OrionApp
		from orion.modules.orionintegration import OrionIntegration
		ids = [OrionIntegration.id(i) for i in OrionIntegration.Addons]
		self._database().delete('DELETE FROM %s WHERE %s;' % (OrionSettings.DatabaseSettings, ' OR '.join([('id LIKE "filters.%s.%%"' % i) for i in ids])))
		for i in ids:
			if self.getApp(i): self.externalRemove(i)

		# NB: This has to remain here permanently.
		# Re-insert the filters if the XML file is replaced during addon updates or if the default (universal) settings change in a new version.
		for i in OrionApp.instances():
			self.externalRemove(i)
			self.externalInsert(i, check = True)

	##############################################################################
	# ADAPT
	##############################################################################

	@classmethod
	def adapt(self):
		path = OrionTools.pathJoin(OrionTools.addonPath(), 'resources', 'settings.xml')
		if not OrionTools.fileExists(path):
			if OrionTools.kodiVersionNew(): pathOriginal = path + '.basic'
			else: pathOriginal = path + '.full'
			OrionTools.fileCopy(pathFrom = pathOriginal, pathTo = path, overwrite = True)
