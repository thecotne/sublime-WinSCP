import sublime_plugin, sublime, subprocess, os, sys
from .dirConfig import getConfig

configName = 'sftp-config.json'
winscpExe = 'WinSCP'

if sys.platform.startswith('win'):
	for programFilesVar in ['ProgramFiles', 'ProgramFiles(x86)']:
		try:
			_winscpExe = os.environ[programFilesVar] + '\WinSCP\WinSCP.exe'
			if os.path.exists(_winscpExe):
				winscpExe = _winscpExe
				break
		except KeyError:
			pass

startWinscpCommand = '"'+ winscpExe + '"' + ' {type}://"{user}":"{password}"@{host}:{port}"{remote_path}" /rawsettings LocalDirectory="{local_path}"'

class browse_with_winscpCommand(sublime_plugin.WindowCommand):
	def run(self, edit = None):
		conf = getConfig(configName)
		if conf is not None:
			subprocess.Popen(startWinscpCommand.format(**conf), shell=True)

