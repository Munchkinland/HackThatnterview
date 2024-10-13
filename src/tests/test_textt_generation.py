import pytest
from unittest.mock import Mock, patch
from text_generation import TextGenerator

@pytest.fixture
def mock_openai():
  with patch('text_generation.openai') as mock:
      yield mock

def test_initialization():
  generator = TextGenerator()
  assert isinstance(generator, TextGenerator)

def test_process_resume():
  generator = TextGenerator()
  resume_text = "Software Engineer with 5 years of experience in Python"
  result = generator.process_resume(resume_text)
  assert isinstance(result, dict)
  assert "keywords" in result
  assert "skills" in result

def test_extract_keywords_and_skills():
  generator = TextGenerator()
  text = "Experienced Python developer with knowledge of Django and Flask"
  keywords, skills = generator.extract_keywords_and_skills(text)
  assert "Python" in skills
  assert "Django" in skills
  assert "Flask" in skills

def test_generate_response(mock_openai):
  generator = TextGenerator()
  mock_openai.Completion.create.return_value = Mock(choices=[Mock(text="Generated response")])
  response = generator.generate_response("Test prompt")
  assert response == "Generated response"