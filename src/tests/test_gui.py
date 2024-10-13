import pytest
from unittest.mock import Mock, patch
from PyQt6.QtWidgets import QApplication
from gui import InterviewAssistantGUI

@pytest.fixture
def app():
  return QApplication([])

@pytest.fixture
def gui(app):
  return InterviewAssistantGUI()

def test_initialization(gui):
  assert isinstance(gui, InterviewAssistantGUI)

def test_ui_elements(gui):
  assert gui.resume_text_edit is not None
  assert gui.language_combo is not None
  assert gui.start_button is not None
  assert gui.stop_button is not None
  assert gui.answer_text_edit is not None

@patch('gui.QFileDialog.getOpenFileName')
def test_load_resume(mock_file_dialog, gui):
  mock_file_dialog.return_value = ("test_resume.txt", "")
  with patch('builtins.open', Mock()) as mock_open:
      mock_open.return_value.__enter__.return_value.read.return_value = "Test resume content"
      gui.load_resume()
  assert gui.resume_text_edit.toPlainText() == "Test resume content"

def test_change_language(gui):
  gui.language_combo.setCurrentText("Spanish")
  assert gui.current_language == "es"

@patch('gui.TextGenerator')
@patch('gui.SpeechRecognitionHandler')
def test_generate_answer(mock_speech_handler, mock_text_generator, gui):
  mock_speech_handler.return_value.recognize_speech.return_value = "Test question"
  mock_text_generator.return_value.generate_response.return_value = "Test answer"
  gui.generate_answer()
  assert gui.answer_text_edit.toPlainText() == "Test answer"