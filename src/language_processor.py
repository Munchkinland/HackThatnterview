# language_processor.py
from deep_translator import GoogleTranslator
import functools

class LanguageProcessor:
  def __init__(self):
      self.translator = GoogleTranslator()

  @functools.lru_cache(maxsize=128)  # Cache translations
  def translate(self, text, target_language):
      try:
          return self.translator.translate(text, target_lang=target_language)
      except Exception as e:
          print(f"Error en la traducción: {e}")
          return text