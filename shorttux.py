import os
import json
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


path = os.path.expanduser("~") + "/Dropbox/"
current_settings = {}
# https://matsbauer.medium.com/how-to-run-ssh-terminal-commands-from-iphone-using-apple-shortcuts-ssh-29e868dccf22


class Event(PatternMatchingEventHandler):
	# Other event types of watchdog:
	# https://pythonhosted.org/watchdog/api.html

	def on_modified(self, event):
		changed_file = os.path.basename(event.src_path)
		mod_settings = load_json(changed_file)
		self.compare_dictionaries(mod_settings, changed_file)
		current_settings[changed_file] = mod_settings

	def set_ubuntu(self, key, mod_settings):
		# In case of running an external .sh script
		# don't forget to chmod +x ./*.sh
		#subprocess.call(['sh', path + '/test.sh']) 
		if key == 'appearance':
			if mod_settings[key] == 'dark':
				os.system('gsettings set org.gnome.desktop.interface gtk-theme "Yaru-dark"')
				os.system('gsettings set org.gnome.desktop.interface color-scheme "prefer-dark"')
			elif mod_settings[key] == 'light':
				os.system('gsettings set org.gnome.desktop.interface gtk-theme "Yaru"')
				os.system('gsettings set org.gnome.desktop.interface color-scheme "prefer-light"')
		elif key == 'focus':
			if mod_settings[key] == 'off':
				os.system('notify-send -u normal "iPhone focus turned off"')
			elif mod_settings[key] == 'dnd':
				# https://github.com/joshpetit/toggle_dnd/blob/master/toggle_dnd
				os.system('notify-send -u normal "iPhone Do Not Disturb focus turned on"')
			elif mod_settings[key] == 'work':
				os.system('notify-send -u normal "iPhone work focus turned on"')

	def compare_dictionaries(self, mod_settings, changed_file):
		changes = {}
		for key in mod_settings:
			# Check if key value did exist before
			if not key in current_settings[changed_file]:
				changes[key] = mod_settings[key]
				change_type = "added key"
				self.change_notification(mod_settings, changes, changed_file, change_type)
			# Check if key has changed
			elif (key in current_settings[changed_file] and
					mod_settings[key] != current_settings[changed_file][key]):
				changes[key] = mod_settings[key]
				change_type = "modified key"
				self.change_notification(mod_settings, changes, changed_file, change_type)
		
	def change_notification(self, mod_settings, changes, changed_file, change_type):
		for key in changes:
			now = datetime.now()
			current_time = now.strftime("%H:%M:%S")
			# ex.: 17:53:23 (ePhone) focus to off
			changes_string = (str(current_time) + " "
							  + change_type
							  + ' (' + changed_file[:-5] + ') '
							  + str(key) + ' to ' + str(mod_settings[key][0]))
			print(changes_string)
			os.system('notify-send -u normal "' + changed_file[:-5] + '" "' + changes_string + '"')
			
			# NOT GOOD
			self.set_ubuntu(key, mod_settings)


def load_json(device):
	with open(path + device) as f:
		currentdict = json.load(f)
	return currentdict

	
def first_notification(device_list):
	notification = ""
	for device in device_list:
		file_modified = os.path.getmtime(path + device)
		notification = (
			notification
			+ '<b>' + str(device[:-5]) + '</b>'
			+ ' (last modified: '
			+ datetime.utcfromtimestamp(file_modified).strftime('%Y-%m-%d %H:%M:%S')
			+ ')\r' # \r\t<i><b>'
		)
		
		for key in current_settings[device]:
			notification = (notification + '\t<i>'
							+ key.title() + '\t\t'
							+ current_settings[device][key][0]
							+ '</i>\r')
	# Icons for notifications in /usr/share/icons/Yaru/scalable
	os.system('notify-send -i phone "Currently saved settings:" "'
			  + notification
			  + '"')


def main():
	device_list = [json for json in os.listdir(path) if json.endswith('.json')]
	for device in device_list:
		current_settings[device] = load_json(device)

	first_notification(device_list)

	event_handler = Event(device_list)
	
	observer = Observer()
	observer.schedule(event_handler, path)
	observer.start()
	
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()


if __name__ == "__main__":
	main()
