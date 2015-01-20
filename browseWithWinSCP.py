import sublime_plugin, sublime, subprocess

from .dirConfig import getConfig

import os.path

sublime.load_settings('sublime-WinSCP.sublime-settings')

winscpPath = 'set PATH = %PATH%;%programfiles(x86)%\WinSCP;%programfiles%\WinSCP && '
configName = 'sftp-config.json'

def winscpCommand(conf):
	return 'WinSCP.exe {type}://{user}:{password}@{host}:{port}"{remote_path}"'.format(**conf)

class browse_with_winscpCommand(sublime_plugin.WindowCommand):
	def run(self, edit = None):
		conf = getConfig(configName)
		if conf is not None:
			subprocess.Popen(winscpPath+winscpCommand(conf), shell=True)
