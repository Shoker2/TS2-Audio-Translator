import configparser
import os

class Configure:
	def __init__(self, config_path):
		self.config_path = config_path
		self.config = configparser.ConfigParser()

		if not os.path.isfile(self.config_path):
			self.config['General'] = {
				'activate': '1',
				'device_id': '1',
				'recognition_model': 'ru',
			}

			self.config['Translate'] = {
				'translate': '1',
				'translate_from': 'Russian',
				'translate_to': 'English'
			}

			self.config['Output'] = {
				'x': '1',
				'y': '1',
				'width': '320',
				'height': '200',
				'font_size': '10',
				'font_family': 'MS Shell Dig 2',
			}

			self.write()
		
		self.reload()
		
	def read(self, section, key):
		return self.config[section][key]
	
	def	update(self, section, key, arg):
		self.config[section][key] = arg
		self.write()
	
	def reload(self):
		self.config.read(self.config_path, encoding='utf-8')

	def write(self):
		with open(self.config_path, 'w+', encoding='utf-8') as configfile:
			self.config.write(configfile)

if __name__ == '__main__':
	config = Configure('./config.ini')