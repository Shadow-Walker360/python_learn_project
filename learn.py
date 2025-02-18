import sys
import openai
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QListWidget, QTabWidget, QLineEdit, QCheckBox
)
from PyQt5.QtGui import QColor, QPalette, QFont
from PyQt5.QtCore import Qt

# OpenAI API Key (DO NOT SHARE PUBLICLY - Store securely)
OPENAI_API_KEY = "AIzaSyC00O9wx8vrFnLRkBDjTEn1QdQwS59WVGo"
openai.api_key = OPENAI_API_KEY

class CodeLearningApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.professional_mode = False  # Track the mode
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("AI-Powered Code Learning")
        self.setGeometry(100, 100, 1200, 700)
        
        # Tabs for different sections
        self.tabs = QTabWidget()
        self.home_tab = QWidget()
        self.lesson_tab = QWidget()
        self.code_editor_tab = QWidget()
        
        self.tabs.addTab(self.home_tab, "Home")
        self.tabs.addTab(self.lesson_tab, "Lessons")
        self.tabs.addTab(self.code_editor_tab, "Code Editor")
        
        # Setup Home Page
        self.setupHomePage()
        self.setupLessonPage()
        self.setupCodeEditor()
        
        self.setCentralWidget(self.tabs)
    
    def setupHomePage(self):
        layout = QVBoxLayout()
        self.welcome_label = QLabel("What can I help with?")
        self.welcome_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.welcome_label.setAlignment(Qt.AlignCenter)
        
        # Search/Input Bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ask AI for coding help...")
        self.search_input.setStyleSheet("padding: 10px; font-size: 14px;")
        
        self.search_button = QPushButton("Search")
        self.search_button.setStyleSheet("background-color: #0078D7; color: white; font-weight: bold;")
        self.search_button.clicked.connect(self.ask_ai)
        
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        
        # Sidebar: History and Language Selection
        self.history_list = QListWidget()
        self.history_list.addItem("Your coding history will appear here...")
        self.language_list = QListWidget()
        self.language_list.addItem("Select a Language:")
        self.language_list.addItem("Python")
        self.language_list.addItem("JavaScript")
        self.language_list.addItem("Java")
        self.language_list.addItem("C++")
        
        sidebar_layout = QVBoxLayout()
        sidebar_layout.addWidget(QLabel("History"))
        sidebar_layout.addWidget(self.history_list)
        sidebar_layout.addWidget(QLabel("Programming Languages"))
        sidebar_layout.addWidget(self.language_list)
        
        # Professional Mode Toggle
        self.professional_mode_checkbox = QCheckBox("Enable Professional Mode")
        self.professional_mode_checkbox.stateChanged.connect(self.toggle_professional_mode)
        sidebar_layout.addWidget(self.professional_mode_checkbox)
        
        main_layout = QHBoxLayout()
        main_layout.addLayout(sidebar_layout, 2)
        main_layout.addLayout(layout, 5)
        
        layout.addWidget(self.welcome_label)
        layout.addLayout(search_layout)
        
        self.home_tab.setLayout(main_layout)
    
    def setupLessonPage(self):
        layout = QVBoxLayout()
        self.lesson_label = QLabel("AI-Powered Lessons")
        self.lesson_label.setFont(QFont("Arial", 16, QFont.Bold))
        
        self.lesson_input = QTextEdit()
        self.get_lesson_button = QPushButton("Get Lesson")
        self.get_lesson_button.clicked.connect(self.get_lesson_from_ai)
        self.lesson_output = QTextEdit()
        self.lesson_output.setReadOnly(True)
        
        layout.addWidget(self.lesson_label)
        layout.addWidget(self.lesson_input)
        layout.addWidget(self.get_lesson_button)
        layout.addWidget(self.lesson_output)
        self.lesson_tab.setLayout(layout)
    
    def setupCodeEditor(self):
        layout = QVBoxLayout()
        self.code_editor_label = QLabel("Write and Run Python Code:")
        self.code_input = QTextEdit()
        self.run_code_button = QPushButton("Run Code")
        self.run_code_button.clicked.connect(self.execute_code)
        self.code_output = QTextEdit()
        self.code_output.setReadOnly(True)

        layout.addWidget(self.code_editor_label)
        layout.addWidget(self.code_input)
        layout.addWidget(self.run_code_button)
        layout.addWidget(self.code_output)
        self.code_editor_tab.setLayout(layout)

    def toggle_professional_mode(self, state):
        """Toggle Professional Mode and update the UI accordingly."""
        self.professional_mode = state == Qt.Checked
        self.update_ui_for_professional_mode()

    def update_ui_for_professional_mode(self):
        """Update the UI based on whether Professional Mode is enabled."""
        if self.professional_mode:
            # Enhance the UI for Professional Mode
            self.code_editor_label.setText("Professional Code Editor (Python):")
            self.code_input.setStyleSheet("background-color: #f0f0f0; font-family: 'Courier New'; font-size: 14px;")
            self.code_output.setStyleSheet("background-color: #f0f0f0; font-family: 'Courier New'; font-size: 14px;")
            self.run_code_button.setText("Execute Code Professionally")
            self.run_code_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        else:
            # Revert to Standard Mode
            self.code_editor_label.setText("Write and Run Python Code:")
            self.code_input.setStyleSheet("")
            self.code_output.setStyleSheet("")
            self.run_code_button.setText("Run Code")
            self.run_code_button.setStyleSheet("")

    def get_lesson_from_ai(self):
        topic = self.lesson_input.toPlainText()
        if topic.strip():
            response = self.get_openai_response(f"Explain {topic} in an interactive way with examples.")
            self.lesson_output.setPlainText(response)

    def execute_code(self):
        code = self.code_input.toPlainText()
        try:
            exec_globals = {}
            exec(code, exec_globals)
            self.code_output.setPlainText("Code executed successfully.")
        except Exception as e:
            self.code_output.setPlainText(f"Error: {str(e)}")

    def ask_ai(self):
        question = self.search_input.text()
        if question.strip():
            response = self.get_openai_response(question)
            self.history_list.addItem(f"You: {question}")
            self.history_list.addItem(f"AI: {response}")

    def get_openai_response(self, question):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": question}]
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"Error: {str(e)}"

    def toggle_dark_mode(self, enabled):
        palette = QPalette()
        if enabled:
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
        else:
            palette.setColor(QPalette.Window, Qt.white)
            palette.setColor(QPalette.WindowText, Qt.black)
        self.setPalette(palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CodeLearningApp()
    window.show()
    sys.exit(app.exec_())