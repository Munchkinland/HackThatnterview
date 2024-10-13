import sys
from PyQt6.QtWidgets import QApplication
from gui import InterviewAssistantGUI

def main():
    app = QApplication(sys.argv)
    assistant_gui = InterviewAssistantGUI()
    assistant_gui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()