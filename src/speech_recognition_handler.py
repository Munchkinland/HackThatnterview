import speech_recognition as sr

class SpeechRecognizer:
  def __init__(self):
      self.recognizer = sr.Recognizer()
      self.microphone = sr.Microphone()
      self.stop_listening_callback = None

  def recognize_speech(self, language_code):
      with self.microphone as source:
          self.recognizer.adjust_for_ambient_noise(source)
          audio = self.recognizer.listen(source)

      try:
          return self.recognizer.recognize_google(audio, language=language_code)
      except sr.UnknownValueError:
          return ""
      except sr.RequestError as e:
          print(f"Could not request results from Google Speech Recognition service; {e}")
          return ""

  def start_listening(self, callback, language_code):
      self.stop_listening_callback = self.recognizer.listen_in_background(
          self.microphone, 
          lambda recognizer, audio: self.background_callback(recognizer, audio, callback, language_code)
      )

  def background_callback(self, recognizer, audio, callback, language_code):
      try:
          text = recognizer.recognize_google(audio, language=language_code)
          callback(text)
      except sr.UnknownValueError:
          pass
      except sr.RequestError as e:
          print(f"Could not request results from Google Speech Recognition service; {e}")

  def stop_listening(self):
      if self.stop_listening_callback:
          self.stop_listening_callback(wait_for_stop=False)
          self.stop_listening_callback = None