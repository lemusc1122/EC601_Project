# ─────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────
import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QDialog,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


# ─────────────────────────────────────────────
# SHARED STYLES
# One place to control the look of buttons
# ─────────────────────────────────────────────
BUTTON_STYLE_GREEN = """
    QPushButton {
        background-color: #2e7d32;
        color: white;
        border-radius: 8px;
        padding: 8px;
    }
    QPushButton:hover {
        background-color: #43a047;
    }
    QPushButton:pressed {
        background-color: #1b5e20;
    }
"""

BUTTON_STYLE_BACK = """
    QPushButton {
        background-color: #7d2e32;
        color: gray;
        border: 1px solid gray;
        border-radius: 8px;
        padding: 8px;
    }
    QPushButton:hover {
        background-color: #a04343;
    }
    QPushButton:pressed {
        background-color: #5E1B1B;
    }
"""


# ─────────────────────────────────────────────
# TRANSLATIONS DICTIONARY
# Keys are written in their NATIVE language
# To add a new language - add a new key block
# ─────────────────────────────────────────────
TRANSLATIONS = {

    # ── English ──
    "English": {
        "window_title"       : "Qiskit Quantum Circuit Builder",
        "main_title"         : "⚛️ Quantum Circuit Builder",
        "experience_label"   : "Experience Level:",
        "continue_button"    : "✔  Continue",
        "run_button"         : "▶  Begin Tutorial",
        "back_button"        : "◀  Back",
        "status_ready"       : "Status: Ready ✅",
        "status_running"     : "⚙️ Beginning tutorial at {experience} level",
        "experience_options" : [
            "Novice Level",
            "Secondary-School Level",
            "University Level"
        ],
    },

    # ── Spanish / Español ──
    "Español": {
        "window_title"       : "Constructor de Circuitos Cuánticos Qiskit",
        "main_title"         : "⚛️ Constructor de Circuitos Cuánticos",
        "experience_label"   : "Nivel de Experiencia:",
        "continue_button"    : "✔  Continuar",
        "run_button"         : "▶  Comenzar Tutorial",
        "back_button"        : "◀  Atrás",
        "status_ready"       : "Estado: Listo ✅",
        "status_running"     : "⚙️ Comenzando tutorial en nivel {experience}",
        "experience_options" : [
            "Nivel Novato",
            "Nivel Secundaria",
            "Nivel Universitario"
        ],
    },
}


# ─────────────────────────────────────────────
# QUESTIONNAIRE DIALOG - WINDOW 1
# ─────────────────────────────────────────────
class QuestionnaireDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Welcome to Quantum Circuit Builder")
        self.setMinimumSize(500, 400)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        self.setLayout(layout)

        # ── Welcome Title ──
        title = QLabel("Welcome! 👋")
        title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Let's customize your experience.\nPlease answer a few quick questions:")
        subtitle.setFont(QFont("Arial", 11))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        # ── Question 1 - Country ──
        q1_label = QLabel("1. What country are you from?")
        q1_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        layout.addWidget(q1_label)

        self.country_dropdown = QComboBox()
        self.country_dropdown.addItems([
            "United States",
            "Canada",
            "United Kingdom",
            "Australia",
            "Germany",
            "France",
            "Japan",
            "China",
            "India",
            "Brazil",
            "Other"
        ])
        self.country_dropdown.setFixedHeight(35)
        self.country_dropdown.currentTextChanged.connect(self.update_states)
        layout.addWidget(self.country_dropdown)

        # ── Question 2 - State / Province ──
        q2_label = QLabel("2. What state/province are you from?")
        q2_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        layout.addWidget(q2_label)

        self.state_dropdown = QComboBox()
        self.state_dropdown.setFixedHeight(35)
        layout.addWidget(self.state_dropdown)

        # Initialize states for default country
        self.update_states(self.country_dropdown.currentText())

        # ── Question 3 - Preferred Language ──
        # Options shown in their native language
        q3_label = QLabel("3. What is your preferred language?")
        q3_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        layout.addWidget(q3_label)

        self.language_dropdown = QComboBox()
        self.language_dropdown.addItems(list(TRANSLATIONS.keys()))
        self.language_dropdown.setFixedHeight(35)

        # ── Connect language change to update continue button ──
        self.language_dropdown.currentTextChanged.connect(self.update_continue_button)
        layout.addWidget(self.language_dropdown)

        # ── Continue Button ──
        self.continue_button = QPushButton(
            TRANSLATIONS["English"]["continue_button"]
        )
        self.continue_button.setFixedHeight(45)
        self.continue_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.continue_button.setStyleSheet(BUTTON_STYLE_GREEN)
        self.continue_button.clicked.connect(self.accept)
        layout.addWidget(self.continue_button)

    # ── Update Continue Button Text Based on Language ──
    def update_continue_button(self, language):
        t = TRANSLATIONS.get(language, TRANSLATIONS["English"])
        self.continue_button.setText(t["continue_button"])

    # ── Dynamically Update States Based on Country ──
    def update_states(self, country):
        self.state_dropdown.clear()
        states = {
            "United States": [
                "Alabama", "Alaska", "Arizona", "Arkansas", "California",
                "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
                "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
                "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
                "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
                "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
                "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
                "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
                "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
                "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
            ],
            "Canada": [
                "Alberta", "British Columbia", "Manitoba", "New Brunswick",
                "Newfoundland and Labrador", "Northwest Territories", "Nova Scotia",
                "Nunavut", "Ontario", "Prince Edward Island",
                "Quebec", "Saskatchewan", "Yukon"
            ],
            "United Kingdom": [
                "England", "Scotland", "Wales", "Northern Ireland"
            ],
            "Australia": [
                "New South Wales", "Victoria", "Queensland",
                "Western Australia", "South Australia",
                "Tasmania", "ACT", "Northern Territory"
            ],
            "Germany": [
                "Baden-Württemberg", "Bavaria", "Berlin", "Brandenburg",
                "Bremen", "Hamburg", "Hesse", "Lower Saxony",
                "Mecklenburg-Vorpommern", "North Rhine-Westphalia",
                "Rhineland-Palatinate", "Saarland", "Saxony",
                "Saxony-Anhalt", "Schleswig-Holstein", "Thuringia"
            ],
            "France": [
                "Auvergne-Rhône-Alpes", "Bourgogne-Franche-Comté",
                "Bretagne", "Centre-Val de Loire", "Corse", "Grand Est",
                "Hauts-de-France", "Île-de-France", "Normandie",
                "Nouvelle-Aquitaine", "Occitanie",
                "Pays de la Loire", "Provence-Alpes-Côte d'Azur"
            ],
            "Japan": [
                "Hokkaido", "Tohoku", "Kanto", "Chubu",
                "Kinki", "Chugoku", "Shikoku", "Kyushu"
            ],
            "China": [
                "Beijing", "Shanghai", "Guangdong", "Sichuan",
                "Zhejiang", "Jiangsu", "Shandong", "Hubei", "Hunan", "Other"
            ],
            "India": [
                "Andhra Pradesh", "Delhi", "Gujarat", "Karnataka",
                "Kerala", "Maharashtra", "Punjab", "Rajasthan",
                "Tamil Nadu", "Uttar Pradesh", "West Bengal", "Other"
            ],
            "Brazil": [
                "Amazonas", "Bahia", "Ceará", "Minas Gerais",
                "Pará", "Paraná", "Rio de Janeiro",
                "Rio Grande do Sul", "Santa Catarina", "São Paulo", "Other"
            ],
        }
        self.state_dropdown.addItems(states.get(country, ["N/A"]))

    # ── Collect Answers ──
    def get_answers(self):
        return {
            "country"  : self.country_dropdown.currentText(),
            "state"    : self.state_dropdown.currentText(),
            "language" : self.language_dropdown.currentText(),
        }


# ─────────────────────────────────────────────
# MAIN WINDOW - WINDOW 2
# ─────────────────────────────────────────────
class MainWindow(QMainWindow):

    # ── Signal to notify controller to go back ──
    back_requested = Signal()

    def __init__(self, answers):
        super().__init__()

        self.answers     = answers

        # ── Flag to distinguish back button from X button ──
        self._going_back = False

        # ── Load translation based on selected language ──
        self.t = TRANSLATIONS.get(answers["language"], TRANSLATIONS["English"])

        # Window settings
        self.setWindowTitle(self.t["window_title"])
        self.setMinimumSize(650, 400)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)
        central_widget.setLayout(main_layout)

        # ── Title ──
        title_label = QLabel(self.t["main_title"])
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # ── User Summary Label ──
        summary = QLabel(
            f"📍 {self.answers['state']}, {self.answers['country']}  |  "
            f"🌐 {self.answers['language']}"
        )
        summary.setFont(QFont("Arial", 9))
        summary.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary.setStyleSheet("color: gray;")
        main_layout.addWidget(summary)

        # ── Dropdown - Experience Level ──
        experience_layout = QHBoxLayout()
        experience_label = QLabel(self.t["experience_label"])
        experience_label.setFont(QFont("Arial", 12))
        experience_label.setFixedWidth(200)

        self.experience_dropdown = QComboBox()
        self.experience_dropdown.addItems(self.t["experience_options"])
        self.experience_dropdown.setFixedHeight(35)

        experience_layout.addWidget(experience_label)
        experience_layout.addWidget(self.experience_dropdown)
        main_layout.addLayout(experience_layout)

        # ── Begin Tutorial Button ──
        self.begin_button = QPushButton(self.t["run_button"])
        self.begin_button.setFixedHeight(45)
        self.begin_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.begin_button.setStyleSheet(BUTTON_STYLE_GREEN)
        self.begin_button.clicked.connect(self.begin_tutorial)
        main_layout.addWidget(self.begin_button)

        # ── Back Button ──
        self.back_button = QPushButton(self.t["back_button"])
        self.back_button.setFixedHeight(40)
        self.back_button.setFont(QFont("Arial", 11))
        self.back_button.setStyleSheet(BUTTON_STYLE_BACK)
        self.back_button.clicked.connect(self.go_back)
        main_layout.addWidget(self.back_button)

        # ── Status Label ──
        self.status_label = QLabel(self.t["status_ready"])
        self.status_label.setFont(QFont("Arial", 10))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)

    # ── Close Event ──
    # X button = terminate Python entirely
    # Back button = just close window and return to Window 1
    def closeEvent(self, event):
        if not self._going_back:
            event.accept()
            sys.exit(0)
        event.accept()

    # ── Go Back to Window 1 ──
    def go_back(self):
        self._going_back = True
        self.close()
        self.back_requested.emit()

    # ── Begin Tutorial ──
    def begin_tutorial(self):
        experience = self.experience_dropdown.currentText()
        self.status_label.setText(
            self.t["status_running"].format(experience=experience)
        )


# ─────────────────────────────────────────────
# APP CONTROLLER
# Manages navigation between Window 1 and Window 2
# ─────────────────────────────────────────────
def show_questionnaire():
    dialog = QuestionnaireDialog()
    if dialog.exec() == QDialog.DialogCode.Accepted:
        # ── User clicked Continue - launch Window 2 ──
        answers = dialog.get_answers()
        window  = MainWindow(answers)
        window.back_requested.connect(show_questionnaire)
        window.show()

        # Store reference to prevent garbage collection
        app._main_window = window
    else:
        # ── User clicked X on Window 1 - terminate Python ──
        sys.exit(0)


# ─────────────────────────────────────────────
# MAIN - APP ENTRY POINT
# ─────────────────────────────────────────────
app = QApplication(sys.argv)
show_questionnaire()
sys.exit(app.exec())