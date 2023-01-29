import pyaudio	# working with a microphone
from playsound import playsound

class AudioInputOutput(object):
	def __init__(self, **kwargs): # accept all parameters and set them to variables
		"""
			kwargs:
			input_device_index (int): set up microphone
		"""				
		self.pa = pyaudio.PyAudio()

		if 'input_device_index' in kwargs.keys():
			self.__open_stream(kwargs['input_device_index'])
		else:
			self.__open_stream(self.pa.get_default_input_device_info()['index'])

	def get_data(self): # I give out data from the microphone
		data = self.stream.read(4000, exception_on_overflow=False)
		return data

	def start_stream(self):
		self.stream.start_stream()

	def stop_stream(self):
		self.stream.stop_stream()

	def __open_stream(self, input_device_index:int): # I open the stream with the microphone installed
		mic_info = self.pa.get_device_info_by_index(input_device_index)['defaultSampleRate']

		self.stream = self.pa.open(
			format=pyaudio.paInt16,
			channels=1,
			rate=int(mic_info),
			input=True,
			input_device_index=input_device_index
		)

	def get_microphones(self): # give out a list of microphones
		""" returns a dictionary of microphones available for connection.

		Returns:
			dictionary: id:name | id is the id of the microphone, which is specified in __init__ and selcect_device
		"""	
		info = self.pa.get_host_api_info_by_index(0)
		num_devices = info.get('deviceCount')

		devices = {}

		for i in range(0, num_devices):
			if (self.pa.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
				devices[i] = self.pa.get_device_info_by_host_api_device_index(0, i).get('name')

		return devices

	def selcect_device(self, id:int=None): # I close the stream, after which I set the microphone by id
		self.stream.stop_stream()
		self.stream.close()
		if id is None:
			self.__open_stream(self.pa.get_default_input_device_info()['index'])
		else:
			self.__open_stream(id)
	
	def stream_is_active(self):
		return self.stream.is_active()
	
	def play_sound(self, path:str):
		"""
		Args:
			path (str): file path
		"""
		playsound(path)