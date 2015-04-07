import sublime_plugin, sublime, os, sys, re, json

configs = {}
nestingLimit = 30

def isString(var):
	var_type = type(var)
	if sys.version[0] == '3':
		return var_type is str or var_type is bytes
	else:
		return var_type is str or var_type is unicode

def getFolders(file_path):
	if file_path is None:
		return []
	folders = [file_path]
	limit = nestingLimit
	while True:
		split = os.path.split(file_path)
		if len(split) == 0:
			break
		file_path = split[0]
		limit -= 1
		if len(split[1]) == 0 or limit < 0:
			break
		folders.append(split[0])
	return folders

def hasActiveView():
	window = sublime.active_window()
	if window is None:
		return False
	view = window.active_view()
	if view is None or view.file_name() is None:
		return False
	return True

def guessConfigFile(folders, configName):
	for folder in folders:
		config = getConfigFile(folder, configName)
		if config is not None:
			return config
		for folder in os.walk(folder):
			config = getConfigFile(folder[0], configName)
			if config is not None:
				return config
	return None

def getConfigFile(file_path, configName):
	cacheKey = file_path
	if isString(cacheKey) is False:
		cacheKey = cacheKey.decode('utf-8')
	try:
		return configs[cacheKey]
	except KeyError:
		try:
			folders = getFolders(file_path)
			if folders is None or len(folders) == 0:
				return None
			configFolder = findConfigFile(folders, configName)
			if configFolder is None:
				return None
			config = os.path.join(configFolder, configName)
			configs[cacheKey] = config
			return config
		except AttributeError:
			return None

def findConfigFile(folders, configName):
	return findFile(folders, configName)

def findFile(folders, file_name):
	if folders is None:
		return None
	for folder in folders:
		if isString(folder) is False:
			folder = folder.decode('utf-8')
		if os.path.exists(os.path.join(folder, file_name)) is True:
			return folder
	return None

removeLineComment = re.compile('//.*', re.I)
removeComma = re.compile('\,(\s|\\n)+\}', re.I)


def parseJson(file_path):
	contents = ""
	try:
		file = open(file_path, 'r')
		for line in file:
			contents += removeLineComment.sub('', line)
	finally:
		file.close()
	contents = removeComma.sub('}', contents)
	decoder = json.JSONDecoder()
	return decoder.decode(contents)


def getConfig(name = 'sftp-config.json'):
	if hasActiveView() is False:
		file_path = os.path.dirname(guessConfigFile(sublime.active_window().folders(), name))
	else:
		file_path = os.path.dirname(sublime.active_window().active_view().file_name())
	_file = getConfigFile(file_path, name)
	try:
		if isString(_file):
			conf = parseJson(_file)
			conf['local_path'] = os.path.dirname(_file)
			return conf
	except:
		pass
	return None
