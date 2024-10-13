import os
import sys
import threading
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTextEdit, QFileDialog, QMessageBox, QComboBox, QSpinBox, QDoubleSpinBox,
    QGroupBox
)
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from resume_processor import ResumeProcessor
from speech_recognition_handler import SpeechRecognizer
from text_generation import TextGenerator
from language_processor import LanguageProcessor
from transcriber import Transcriber

ALLOWED_RESUME_EXTENSIONS = ('.txt', '.docx', '.pdf', '.ppt', '.pptx')
ALLOWED_JOB_DESCRIPTION_EXTENSIONS = ('.txt', '.docx', '.pdf')

class AnswerGenerator(QObject):
    answer_generated = pyqtSignal(str)

    def __init__(self, text_generator):
        super().__init__()
        self.text_generator = text_generator

    def generate_answer(self, question, context, resume, job_description, language, model, max_tokens, n, temperature):
        try:
            response = self.text_generator.generate_response(question, context, resume, job_description, language, model, max_tokens, n, temperature)
            self.answer_generated.emit(response)
        except Exception as e:
            self.answer_generated.emit(f"Error generating response: {str(e)}")

class InterviewAssistantGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.speech_recognizer = SpeechRecognizer()
        self.text_generator = TextGenerator()
        self.language_processor = LanguageProcessor()
        self.resume = ""
        self.job_description = ""
        self.is_listening = False
        self.transcriber = None
        self.answer_generator = AnswerGenerator(self.text_generator)
        self.answer_generator.answer_generated.connect(self.update_generated_answer)

    def init_ui(self):
        self.setWindowTitle('Interview Assistant')
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: Segoe UI, Arial;
            }
            QGroupBox {
                border: 2px solid #3a3a3a;
                border-radius: 5px;
                margin-top: 1ex;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QPushButton {
                background-color: #2a2a2a;
                border: 1px solid #3a3a3a;
                border-radius: 3px;
                padding: 5px;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
            QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                background-color: #2a2a2a;
                border: 1px solid #3a3a3a;
                border-radius: 3px;
                padding: 2px;
                color: #ffffff;
            }
            QComboBox::drop-down {
                border: 0px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
            QSpinBox::up-button, QDoubleSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 16px;
                border-left-width: 1px;
                border-left-color: #3a3a3a;
                border-top-right-radius: 3px;
                border-bottom: 0px;
            }
            QSpinBox::down-button, QDoubleSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 16px;
                border-left-width: 1px;
                border-left-color: #3a3a3a;
                border-bottom-right-radius: 3px;
                border-top: 0px;
            }
        """)

        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.create_language_group())
        top_layout.addWidget(self.create_model_group())
        main_layout.addLayout(top_layout)

        middle_layout = QHBoxLayout()
        middle_layout.addWidget(self.create_resume_group())
        middle_layout.addWidget(self.create_job_description_group())
        main_layout.addLayout(middle_layout)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.create_interviewer_question_group())
        bottom_layout.addWidget(self.create_generated_answer_group())
        main_layout.addLayout(bottom_layout)

        main_layout.addWidget(self.create_openai_parameters_group())

        self.setLayout(main_layout)

    def create_language_group(self):
        group = QGroupBox("Language")
        layout = QVBoxLayout()
        self.language_combo = QComboBox()
        self.language_combo.addItems(['Español', 'English'])
        self.language_combo.currentIndexChanged.connect(self.update_ui_language)
        layout.addWidget(self.language_combo)
        group.setLayout(layout)
        return group

    def create_model_group(self):
        group = QGroupBox("Model")
        layout = QVBoxLayout()
        self.model_combo = QComboBox()
        self.model_combo.addItems(['gpt-3.5-turbo', 'gpt-4'])
        layout.addWidget(self.model_combo)
        group.setLayout(layout)
        return group

    def create_resume_group(self):
        group = QGroupBox("Resume")
        layout = QVBoxLayout()
        self.resume_display = QTextEdit()
        self.resume_display.setPlaceholderText('Loaded resume will appear here...')
        self.resume_display.setReadOnly(True)
        layout.addWidget(self.resume_display)
        self.load_resume_button = QPushButton('Load Resume')
        self.load_resume_button.clicked.connect(self.show_load_resume_dialog)
        layout.addWidget(self.load_resume_button)
        group.setLayout(layout)
        return group

    def create_job_description_group(self):
        group = QGroupBox("Job Description")
        layout = QVBoxLayout()
        self.job_description_input = QTextEdit()
        self.job_description_input.setPlaceholderText('Enter job description here...')
        layout.addWidget(self.job_description_input)
        self.load_job_description_button = QPushButton('Upload Job Description')
        self.load_job_description_button.clicked.connect(self.show_load_job_description_dialog)
        layout.addWidget(self.load_job_description_button)
        group.setLayout(layout)
        return group

    def create_interviewer_question_group(self):
        group = QGroupBox("Interviewer Question")
        layout = QVBoxLayout()
        self.interviewer_question = QTextEdit()
        self.interviewer_question.setPlaceholderText('Enter interviewer\'s question here...')
        layout.addWidget(self.interviewer_question)
        self.listen_question_button = QPushButton('Listen to question')
        self.listen_question_button.clicked.connect(self.toggle_listening_question)
        layout.addWidget(self.listen_question_button)
        group.setLayout(layout)
        return group

    def create_generated_answer_group(self):
        group = QGroupBox("Generated Answer")
        layout = QVBoxLayout()
        self.generated_answer = QTextEdit()
        self.generated_answer.setPlaceholderText('Generated answer will appear here...')
        layout.addWidget(self.generated_answer)
        self.generate_button = QPushButton('Generate answer')
        self.generate_button.clicked.connect(self.generate_answer)
        layout.addWidget(self.generate_button)
        group.setLayout(layout)
        return group

    def create_openai_parameters_group(self):
        group = QGroupBox("OpenAI API Parameters")
        layout = QHBoxLayout()
        
        max_tokens_layout = QVBoxLayout()
        self.max_tokens_label = QLabel('Max words:')
        max_tokens_layout.addWidget(self.max_tokens_label)
        self.max_tokens_spinbox = QSpinBox()
        self.max_tokens_spinbox.setRange(1, 1000)
        self.max_tokens_spinbox.setValue(150)
        max_tokens_layout.addWidget(self.max_tokens_spinbox)
        layout.addLayout(max_tokens_layout)
        
        n_layout = QVBoxLayout()
        self.n_label = QLabel('Number of responses:')
        n_layout.addWidget(self.n_label)
        self.n_spinbox = QSpinBox()
        self.n_spinbox.setRange(1, 5)
        self.n_spinbox.setValue(1)
        n_layout.addWidget(self.n_spinbox)
        layout.addLayout(n_layout)
        
        temp_layout = QVBoxLayout()
        self.temperature_label = QLabel('Creativity (0.0 to 1.0):')
        temp_layout.addWidget(self.temperature_label)
        self.temperature_spinbox = QDoubleSpinBox()
        self.temperature_spinbox.setRange(0.0, 1.0)
        self.temperature_spinbox.setSingleStep(0.1)
        self.temperature_spinbox.setValue(0.7)
        temp_layout.addWidget(self.temperature_spinbox)
        layout.addLayout(temp_layout)
        
        group.setLayout(layout)
        return group

    def generate_answer(self):
        if not self.resume:
            self.show_error("Please load a resume first.")
            return

        question = self.interviewer_question.toPlainText()
        context = "Job interview"
        target_language, _ = self.get_language_codes()
        job_description = self.job_description_input.toPlainText()

        max_tokens = self.max_tokens_spinbox.value()
        n = self.n_spinbox.value()
        temperature = self.temperature_spinbox.value()
        model = self.model_combo.currentText()

        threading.Thread(target=self.answer_generator.generate_answer, 
                         args=(question, context, self.resume, job_description, target_language, model, max_tokens, n, temperature), 
                         daemon=True).start()

    def show_load_resume_dialog(self):
        self.show_load_file_dialog("Load Resume", ALLOWED_RESUME_EXTENSIONS, self.load_resume)

    def show_load_job_description_dialog(self):
        self.show_load_file_dialog("Load Job Description", ALLOWED_JOB_DESCRIPTION_EXTENSIONS, self.load_job_description)

    def show_load_file_dialog(self, title, allowed_extensions, callback):
        file_path, _ = QFileDialog.getOpenFileName(self, title, "", f"Allowed files (*{' *'.join(allowed_extensions)})")
        if file_path:
            callback(file_path)

    def load_resume(self, file_path):
        try:
            self.resume = ResumeProcessor.process_resume(file_path)
            self.resume_display.setPlainText(self.resume)
            self.show_message("Resume loaded successfully")
        except Exception as e:
            self.show_error(f"Error loading resume: {str(e)}")

    def load_job_description(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.job_description = file.read()
                self.job_description_input.setPlainText(self.job_description)
                self.show_message("Job description loaded successfully")
        except Exception as e:
            self.show_error(f"Error loading job description: {str(e)}")

    def toggle_listening_question(self):
        if not self.is_listening:
            self.start_listening(role="question")
            self.listen_question_button.setText('Stop listening' if self.language_combo.currentText() == 'English' else 'Dejar de escuchar')
            self.listen_question_button.setStyleSheet('background-color: #aa0000;')
        else:
            self.stop_listening(role="question")
            self.listen_question_button.setText('Listen to question' if self.language_combo.currentText() == 'English' else 'Escuchar pregunta')
            self.listen_question_button.setStyleSheet('')

    def start_listening(self, role):
        self.is_listening = True
        language_code, _ = self.get_language_codes()
        self.transcriber = Transcriber(language=language_code)

        thread = threading.Thread(target=self.transcriber.listen_continuously, args=(self.update_transcription, role))
        thread.daemon = True
        thread.start()

    def stop_listening(self, role):
        self.is_listening = False
        if self.transcriber:
            self.transcriber.stop()
            self.transcriber = None
        if role == "question":
            self.listen_question_button.setText('Listen to question' if self.language_combo.currentText() == 'English' else 'Escuchar pregunta')
            self.listen_question_button.setStyleSheet('')

    def update_transcription(self, text, role):
        if role == "question":
            self.interviewer_question.append(text + " ")

    def update_generated_answer(self, response):
        self.generated_answer.setPlainText(response)
        self.show_message("Answer generated successfully")

    def show_message(self, message):
        QMessageBox.information(self, "Success", message)

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

    def get_language_codes(self):
        return ("es", "es-ES") if self.language_combo.currentText() == "Español" else ("en", "en-US")
    
    def update_ui_language(self):
        language = self.language_combo.currentText()
        if language == "Español":
            self.load_resume_button.setText('Cargar currículum')
            self.load_job_description_button.setText('Cargar descripción del puesto')
            self.listen_question_button.setText('Escuchar pregunta' if not self.is_listening else 'Dejar de escuchar')
            self.generate_button.setText('Generar respuesta')
            self.resume_display.setPlaceholderText('El currículum cargado aparecerá aquí...')
            self.job_description_input.setPlaceholderText('Ingrese la descripción del puesto aquí...')
            self.interviewer_question.setPlaceholderText('Ingrese la pregunta del entrevistador aquí...')
            self.generated_answer.setPlaceholderText('La respuesta generada aparecerá aquí...')
            self.max_tokens_label.setText('Máximo de palabras:')
            self.n_label.setText('Número de respuestas:')
            self.temperature_label.setText('Creatividad (0.0 a 1.0):')
        else:
            self.load_resume_button.setText('Load Resume')
            self.load_job_description_button.setText('Upload Job Description')
            self.listen_question_button.setText('Listen to question' if not self.is_listening else 'Stop listening')
            self.generate_button.setText('Generate answer')
            self.resume_display.setPlaceholderText('Loaded resume will appear here...')
            self.job_description_input.setPlaceholderText('Enter job description here...')
            self.interviewer_question.setPlaceholderText('Enter interviewer\'s question here...')
            self.generated_answer.setPlaceholderText('Generated answer will appear here...')
            self.max_tokens_label.setText('Max words:')
            self.n_label.setText('Number of responses:')
            self.temperature_label.setText('Creativity (0.0 to 1.0):')

    def main():
        app = QApplication(sys.argv)
        assistant_gui = InterviewAssistantGUI()
        assistant_gui.show()
        sys.exit(app.exec())

        if __name__ == '__main__':
            main()
