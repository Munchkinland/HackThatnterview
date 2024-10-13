import pytest
from resume_processor import ResumeProcessor

def test_process_txt_file():
  processor = ResumeProcessor()
  result = processor.process("test_resume.txt")
  assert isinstance(result, str)
  assert len(result) > 0

def test_process_docx_file():
  processor = ResumeProcessor()
  result = processor.process("test_resume.docx")
  assert isinstance(result, str)
  assert len(result) > 0

def test_process_pdf_file():
  processor = ResumeProcessor()
  result = processor.process("test_resume.pdf")
  assert isinstance(result, str)
  assert len(result) > 0

def test_process_ppt_file():
  processor = ResumeProcessor()
  result = processor.process("test_resume.ppt")
  assert isinstance(result, str)
  assert len(result) > 0

def test_process_pptx_file():
  processor = ResumeProcessor()
  result = processor.process("test_resume.pptx")
  assert isinstance(result, str)
  assert len(result) > 0

def test_unsupported_file_format():
  processor = ResumeProcessor()
  with pytest.raises(ValueError):
      processor.process("test_resume.jpg")

def test_nonexistent_file():
  processor = ResumeProcessor()
  with pytest.raises(FileNotFoundError):
      processor.process("nonexistent_file.txt")