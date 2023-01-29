from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMenu
from PyQt5.QtGui import QIcon
import pyaudio

import sys
import multiprocessing
import os
import threading
import traceback

from modules.audio_io import AudioInputOutput
from modules.recognizer import Recognizer
from modules.Translator import Translator
from modules.Configure import Configure
from modules.Logger import Logger
from ui.Settings import Ui_SettingsWindow
from ui.ScreenOutput import Ui_Output_Ui
from ui.Tray import SystemTray

logger = Logger('log_records.csv')

class StoppableThread(threading.Thread):
	"""Thread class with a stop() method. The thread itself has to check
	regularly for the stopped() condition."""

	def __init__(self,  *args, **kwargs):
		super(StoppableThread, self).__init__(*args, **kwargs)
		self._stop_event = threading.Event()

	def stop(self):
		self._stop_event.set()

	def stopped(self):
		return self._stop_event.is_set()

class Ui_Output(Ui_Output_Ui):
	def closeEvent(self, event):
		try:
			config.update('Output', 'x', str(self.pos().x()))
			config.update('Output', 'y', str(self.pos().y()))
			config.update('Output', 'width', str(self.size().width()))
			config.update('Output', 'height', str(self.size().height()))

		except Exception:
			logger.logging.error(traceback.format_exc().replace('"', '\''))

class Ui_Settings(Ui_SettingsWindow):		
	def fill_data(self):
		try:
			pa = pyaudio.PyAudio()

			info = pa.get_host_api_info_by_index(0)
			num_devices = info.get('deviceCount')

			self.devices = {}

			for i in range(0, num_devices): # Получаю все устройства, что подключены для ввода аудио
				if (pa.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
					self.devices[i] = pa.get_device_info_by_host_api_device_index(0, i).get('name')
			
			for device in self.devices.keys(): # добавляю все аудио устройства
				self.deviceComboBox.addItem(self.devices[device])
			
			for i in os.listdir('./resources/models'): # Прохожусь по названиям всех файлов в папке 
				if i.find('.') == -1:	# Если в названии нет ".", то добавляю в список
					self.modelComboBox.addItem(i)
			
			for lang in self.langs.keys(): # Добавляю все языки
				self.translateFromComboBox.addItem(lang)
				self.translateToComboBox.addItem(lang)
			
			config.reload()

			if config.read('General', 'activate') == '1':
				self.activeCheckBox.setChecked(True)
			else:
				self.activeCheckBox.setChecked(False)
			
			if config.read('Translate', 'translate') == '1':
				self.translateCheckBox.setChecked(True)
			else:
				self.translateCheckBox.setChecked(False)
			
			self.deviceComboBox.setCurrentText(self.devices[int(config.read('General', 'device_id'))])
			self.modelComboBox.setCurrentText(config.read('General', 'recognition_model'))
			
			self.translateFromComboBox.setCurrentText(config.read('Translate', 'translate_from'))
			self.translateToComboBox.setCurrentText(config.read('Translate', 'translate_to'))

			self.fontComboBox.setCurrentText(config.read('Output', 'font_family'))
			self.fontSpinBox.setValue(int(config.read('Output', 'font_size')))

		except Exception:
			logger.logging.error(traceback.format_exc().replace('"', '\''))
		
	def save_data(self):
		try:
			global general
			global translate

			config.reload()
			if self.activeCheckBox.isChecked():
				config.update('General', 'activate', '1')
				general.value['activate'] = '1'
			else:
				config.update('General', 'activate', '0')
				general.value['activate'] = '0'
			
			if self.translateCheckBox.isChecked():
				config.update('Translate', 'translate', '1')
				translate.value['translate'] = '1'
			else:
				config.update('Translate', 'translate', '0')
				translate.value['translate'] = '0'

			device_id = list(self.devices.keys())[list(self.devices.values()).index(self.deviceComboBox.currentText())]
			config.update('General', 'device_id', str(device_id))

			recognition_model = self.modelComboBox.currentText()
			config.update('General', 'recognition_model', recognition_model)

			translate_from = self.translateFromComboBox.currentText()
			config.update('Translate', 'translate_from', translate_from)

			translate_to = self.translateToComboBox.currentText()
			config.update('Translate', 'translate_to', translate_to)

			config.update('Output', 'font_family', self.fontComboBox.currentText())
			config.update('Output', 'font_size', str(self.fontSpinBox.value()))

			
			general.value =  {
			'activate': config.read('General', 'activate'),
			'device_id': str(device_id),
			'recognition_model': recognition_model
			}

			translate.value = {
			'translate': config.read('Translate', 'translate'),
			'translate_from': Ui_Settings.langs[translate_from],
			'translate_to': Ui_Settings.langs[translate_to]
			}
		
		except Exception:
			logger.logging.error(traceback.format_exc().replace('"', '\''))
	
	def customizePshButton_pressed(self):
		try:
			global output
			output = Ui_Output(False, './resources/icon.png')

			output.setText('text', int(config.read('Output', 'font_size')), config.read('Output', 'font_family'))
			output.resize(int(config.read('Output', 'width')), int(config.read('Output', 'height')))
			output.move(int(config.read('Output', 'x')), int(config.read('Output', 'y')))

			output.show()
		
		except Exception:
			logger.logging.error(traceback.format_exc().replace('"', '\''))

class Tray(SystemTray):
	def set_menu(self):
		try:
			menu = QMenu()

			exitAction = menu.addAction('Settings')
			exitAction.triggered.connect(open_settings)

			exitAction = menu.addAction('Exit')
			exitAction.triggered.connect(self.exit)

			self.setContextMenu(menu)

		except Exception:
			logger.logging.error(traceback.format_exc().replace('"', '\''))

def open_settings():
	try:
		global settings
		settings = Ui_Settings('./resources/icon.png')
		settings.show()
	
	except Exception:
			logger.logging.error(traceback.format_exc().replace('"', '\''))

def	tray_main():
	try:
		global config

		global app
		app = QtWidgets.QApplication(sys.argv)
		app.setQuitOnLastWindowClosed(False)

		tray = Tray(QIcon('./resources/icon.png'), app)
		tray.show()

		sys.exit(app.exec_())

	except Exception:
			logger.logging.error(traceback.format_exc().replace('"', '\''))

def output_main(text, x, y, width, height, font_size, font_family):
	global output
	app = QtWidgets.QApplication(sys.argv)

	output = Ui_Output(True, './resources/icon.png')

	output.setText(text, font_size, font_family)
	output.resize(width, height)
	output.move(x, y)

	output.show()
	sys.exit(app.exec_())

def recognition_main(general, translate):
	logger = Logger('log_records.csv')

	try:
		old_general = {'device_id': -123, 'recognition_model': 101}

		global config
		config = Configure('./config.ini')
		
		while True:
			if old_general == general.value and general.value['activate'] == '1':
				try:
					data = appIO.get_data() # получаю массив байт с микрофона
				except OSError:
					pass
				
				text = appRecognizer.speech2text(data) # превращяю этот массив в текст
				if text != None:
					if translate.value['translate'] == '1':
						text = Translator.translate(text, translate.value['translate_to'], translate.value['translate_from'], 'Google')

					try:
						output_thread.stop()
					except UnboundLocalError:
						pass
					
					config.reload()
					output_thread = StoppableThread(target=output_main, daemon=True, args=(
						text,
						int(config.read('Output', 'x')),
						int(config.read('Output', 'y')),
						int(config.read('Output', 'width')),
						int(config.read('Output', 'height')),
						int(config.read('Output', 'font_size')),
						config.read('Output', 'font_family')
						))	# Передаю данные для окна
					output_thread.start()
					
			else:
				if general.value['activate'] == '1':
					if old_general['device_id'] != general.value['device_id']:
						appIO = AudioInputOutput(input_device_index=int(general.value['device_id'])) # инициализирую нужные классы
						appIO.start_stream() # Начинаю работу с микрофона
					
					if old_general['recognition_model'] != general.value['recognition_model']:
						appRecognizer = Recognizer(f"./resources/models/{general.value['recognition_model']}")	# Переинициализирую модель для распознования
						appIO.play_sound('./resources/notification.wav')

					old_general = general.value
	
	except Exception:
			logger.logging.error(traceback.format_exc().replace('"', '\''))

if __name__ == '__main__':
	try:
		global config
		config = Configure('./config.ini')

		manager = multiprocessing.Manager()

		global general
		general = manager.Value('dic', {
			'activate': config.read('General', 'activate'),
			'device_id': config.read('General', 'device_id'),
			'recognition_model': config.read('General', 'recognition_model')
		})

		global translate
		translate = manager.Value('dic', {
			'translate': config.read('Translate', 'translate'),
			'translate_from': Ui_Settings.langs[config.read('Translate', 'translate_from')],
			'translate_to': Ui_Settings.langs[config.read('Translate', 'translate_to')]
			})
			
		tray_process = multiprocessing.Process(target=recognition_main, args=(general, translate), daemon=True).start()
		tray_main()

	except Exception:
			logger.logging.error(traceback.format_exc().replace('"', '\''))