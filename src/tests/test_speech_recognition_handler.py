import pytest
from unittest.mock import Mock
from speech_recognition_handler import SpeechRecognitionHandler

@pytest.fixture
def mock_recognizer():
  return Mock()

def test_initialization(mock_recognizer):
  handler = SpeechRecognitionHandler(mock_recognizer)
  assert handler.recognizer == mock_recognizer

def test_recognize_speech(mock_recognizer):
  handler = SpeechRecognitionHandler(mock_recognizer)
  mock_recognizer.recognize_google.return_value = "Test speech"
  result = handler.recognize_speech()
  assert result == "Test speech"

def test_start_listening(mock_recognizer):
  handler = SpeechRecognitionHandler(mock_recognizer)
  handler.start_listening()
  assert handler.is_listening == True

def test_stop_listening(mock_recognizer):
  handler = SpeechRecognitionHandler(mock_recognizer)
  handler.start_listening()
  handler.stop_listening()
  assert handler.is_listening == False