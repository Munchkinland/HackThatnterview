import pytest
from unittest.mock import Mock, patch
from transcriber import Transcriber

@pytest.fixture
def mock_vosk_model():
  with patch('transcriber.Model') as mock:
      yield mock

@pytest.fixture
def mock_recognizer():
  with patch('transcriber.KaldiRecognizer') as mock:
      yield mock

def test_initialization(mock_vosk_model, mock_recognizer):
  transcriber = Transcriber("en-US")
  assert isinstance(transcriber, Transcriber)
  mock_vosk_model.assert_called_once_with("model-en-US")
  mock_recognizer.assert_called_once()

@patch('transcriber.pyaudio.PyAudio')
def test_listen_continuously(mock_pyaudio, mock_vosk_model, mock_recognizer):
  transcriber = Transcriber("en-US")
  mock_stream = Mock()
  mock_pyaudio.return_value.open.return_value = mock_stream
  
  def side_effect():
      transcriber.stop()
      return b"audio_data"
  
  mock_stream.read.side_effect = side_effect
  mock_recognizer.return_value.Result.return_value = '{"text": "Test transcription"}'
  
  result = transcriber.listen_continuously()
  assert result == "Test transcription"

def test_stop(mock_vosk_model, mock_recognizer):
  transcriber = Transcriber("en-US")
  transcriber.stop()
  assert transcriber.should_stop == True