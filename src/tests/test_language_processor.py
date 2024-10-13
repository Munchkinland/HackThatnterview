import pytest
from language_processor import LanguageProcessor

@pytest.fixture
def processor():
  return LanguageProcessor()

def test_initialization(processor):
  assert isinstance(processor, LanguageProcessor)

def test_translate(processor):
  text = "Hello, world!"
  translated = processor.translate(text, "es")
  assert translated == "¡Hola, mundo!"

def test_translate_cache(processor):
  text = "Hello, world!"
  processor.translate(text, "es")
  cached_translation = processor.translate(text, "es")
  assert cached_translation == "¡Hola, mundo!"

def test_translate_unsupported_language(processor):
  with pytest.raises(ValueError):
      processor.translate("Hello", "unsupported_lang")