from vosk import Model, KaldiRecognizer	# translate audio to json with text
import json								# to get text from json

class Recognizer(object):
	def __init__(self, path:str="."):
		"""

		Args:
			path (str): path to vosk model. Defaults to ".".
		"""		
		self.set_settings(path)

	def set_settings(self, path:str):
		""" setup settings

		Args:
			path (str): path to the folder with Vosk voice recognition model
		"""		
		model = Model(path)
		self.rec = KaldiRecognizer(model, 44100) # Regular 8000 | Small 44100

	def speech2text(self, data:bytes):
		""" Converts an array of bytes to text

		Args:
			data (bytes): byte array (I personally used it with pyaudio)

		Returns:
			(str): returns the text spoken by the person after the START word, which is specified when the class is initialized. If there is no word START, it returns the entire text without slices.
		"""		
		if self.rec.AcceptWaveform(data): # Accumulate data until ready to process it
			voice_input=json.loads(self.rec.Result()) # we remake the received processed data from a string (of the json type) to json
			if voice_input["text"] != "":
				text = voice_input["text"]
				return text