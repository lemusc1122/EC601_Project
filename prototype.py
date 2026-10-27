# ─────────────────────────────────────────────
# Quantum Circuit Builder desktop learning prototype.
# Install and run instructions live in README.md and gettingStarted.md.
# The local simulator works without Qiskit; Qiskit adds circuit diagrams and
# the example-circuit simulation. IBM hardware access is handled separately.
# User-facing languages: English, Spanish, and Modern Standard Arabic.
# Research references are indexed in SPRINT1.md; the BB84 citation is linked
# directly from the cryptography screen.
# ─────────────────────────────────────────────

# ─────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────
import sys
import re
import random
import secrets
import math
from html import escape as html_escape
from collections import Counter
from datetime import datetime
from io import BytesIO
from pathlib import Path

from PySide6.QtCore import Qt, Signal, QTimer, QSize, QMimeData
from PySide6.QtGui  import QFont, QPixmap, QPainter, QPen, QColor, QIcon, QDrag
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog, QLabel, QComboBox,
    QPushButton, QToolButton, QVBoxLayout, QHBoxLayout, QFormLayout,
    QGridLayout, QScrollArea, QFrame, QTextBrowser, QPlainTextEdit, QTabWidget,
    QLineEdit, QCheckBox, QSlider, QTableWidget, QTableWidgetItem, QHeaderView
)

try:
    from PySide6.QtTextToSpeech import QTextToSpeech
    from PySide6.QtCore import QLocale
except ImportError:
    QTextToSpeech = None
    QLocale = None

try:
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
except ImportError:
    QuantumCircuit = None
    Statevector    = None


# ─────────────────────────────────────────────
# SHARED STYLES  
# ─────────────────────────────────────────────
APP_STYLE = """
QWidget {
    background-color: #f5f7f8;
    color: #243238;
}
QDialog {
    background-color: #f5f7f8;
}
QFrame {
    background-color: #ffffff;
    border: 1px solid #dfe7e8;
    border-radius: 8px;
}
QScrollArea {
    background-color: #f5f7f8;
    border: none;
}
QScrollArea > QWidget > QWidget {
    background-color: #f5f7f8;
}
QTextBrowser {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    color: #1a1a1a;
}
QPlainTextEdit {
    background-color: #ffffff;
    border: 1px solid #dfe7e8;
    border-radius: 6px;
    padding: 8px;
    color: #243238;
}
QTabWidget::pane {
    border: 1px solid #dfe7e8;
    border-radius: 6px;
    background: #f5f7f8;
    top: -1px;
}
QTabBar::tab {
    background: #e7edef;
    color: #243238;
    padding: 9px 18px;
    margin-right: 3px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}
QTabBar::tab:selected {
    background: #ffffff;
    color: #176b65;
    font-weight: bold;
}
QComboBox {
    background-color: #ffffff;
    color: #1a1a1a;
    border: 1px solid #cccccc;
    border-radius: 4px;
    padding: 4px 8px;
    min-height: 28px;
}
QComboBox::drop-down { border: none; }
QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #1a1a1a;
    selection-background-color: #247f78;
    selection-color: white;
    border: 1px solid #cccccc;
}
QLabel {
    background-color: transparent;
    color: #1a1a1a;
}
QScrollBar:vertical {
    background: #e0e0e0; width: 10px; border-radius: 5px;
}
QScrollBar::handle:vertical {
    background: #b0b0b0; border-radius: 5px; min-height: 20px;
}
QScrollBar:horizontal {
    background: #e0e0e0; height: 10px; border-radius: 5px;
}
QScrollBar::handle:horizontal {
    background: #b0b0b0; border-radius: 5px; min-width: 20px;
}
"""

BUTTON_STYLE_GREEN = """
QPushButton {
    background-color: #247f78; color: white;
    border-radius: 7px; padding: 10px 14px; border: none;
}
QPushButton:hover   { background-color: #30978d; }
QPushButton:pressed { background-color: #1b625d; }
"""

BUTTON_STYLE_BACK = """
QPushButton {
    background-color: #e7edef; color: #243238;
    border: 1px solid #d1dcde; border-radius: 8px; padding: 8px;
}
QPushButton:hover   { background-color: #dbe6e8; }
QPushButton:pressed { background-color: #ccd9db; }
"""


# ─────────────────────────────────────────────
# TRANSLATIONS
# ─────────────────────────────────────────────
TRANSLATIONS = {
    "English": {
        "title": "Qiskit Quantum Circuit Builder", "main": "⚛️ Quantum Circuit Builder",
        "country": "Country:", "region": "State / Province:", "language": "Preferred Language:",
        "continue": "✔ Continue", "experience": "Experience Level:",
        "begin": "▶ Begin Tutorial", "back": "◀ Back", "ready": "Status: Ready ✅",
        "running": "Selected: {value}", "choose_circuit": "Choose a circuit to explore:",
        "explore": "▶ Explore Circuit", "operators": "⚛️ Quantum Operators Guide",
        "circuit": "🔌 YOUR SELECTED CIRCUIT", "novice": "Brand new",
        "school": "Secondary-School Level", "university": "University Level",
        "description": "Explanation", "circuit_help": "Circuit overview",
        "matrix_label": "Gate Matrix:",
        "simulation": "▶ Theory & Local Simulation", "close": "✕ Close",
        "close_application": "✕ Close Application", "shots": "Number of circuit runs:",
        "run": "▶ Run Local Simulation", "show_code": "▶ Show Qiskit Code",
        "hide_code": "▼ Hide Qiskit Code",
        "welcome": "Quantum Circuit Builder — Welcome",
        "diagram_tooltip": "Graphical quantum circuit diagram",
        "diagram_error": "For graphical diagrams, install 'qiskit[visualization]' and matplotlib.",
        "qiskit_missing": "Qiskit not installed. Install it to build and simulate circuits.",
        "tab_main": "App", "tab_feedback": "Feedback",
        "feedback_title": "Send feedback", "feedback_prompt": "Tell us what worked, what was confusing, or what you would like changed.",
        "feedback_send": "Submit feedback", "feedback_empty": "Write a few words before submitting.",
        "feedback_saved": "Saved as an open issue in Feedback/.",
        "feedback_error": "Could not save feedback. Check that this folder is writable.",
        "feedback_issue_title": "Feedback issue", "feedback_status_label": "Status",
        "feedback_open_label": "Open", "feedback_submitted_label": "Submitted",
        "feedback_screen_label": "Screen", "feedback_language_label": "Interface language",
        "feedback_text_heading": "Feedback",
        "operator_chart_hint": "Select a gate image to open its explanation.",
        "cryptography": "🔐 Quantum Cryptography",
        "playground": "🧩 Two-Qubit Playground",
    },
    "Español": {
        "title": "Constructor de Circuitos Cuánticos Qiskit", "main": "⚛️ Constructor de Circuitos Cuánticos",
        "country": "País:", "region": "Estado / Provincia:", "language": "Idioma preferido:",
        "continue": "✔ Continuar", "experience": "Nivel de experiencia:", "begin": "▶ Comenzar tutorial",
        "back": "◀ Atrás", "ready": "Estado: Listo ✅", "running": "Seleccionado: {value}",
        "choose_circuit": "Elige un circuito para explorar:", "explore": "▶ Explorar circuito",
        "operators": "⚛️ Guía de Operadores Cuánticos", "circuit": "🔌 TU CIRCUITO SELECCIONADO",
        "novice": "Desde cero", "school": "Nivel secundaria", "university": "Nivel universitario",
        "description": "Explicación", "circuit_help": "Resumen del circuito",
        "matrix_label": "Matriz de la Puerta:",
        "simulation": "▶ Teoría y simulación local", "close": "✕ Cerrar",
        "close_application": "✕ Cerrar aplicación", "shots": "Número de mediciones:",
        "run": "▶ Ejecutar simulación local", "show_code": "▶ Mostrar código Qiskit",
        "hide_code": "▼ Ocultar código Qiskit",
        "welcome": "Constructor de circuitos cuánticos — Bienvenida",
        "diagram_tooltip": "Diagrama visual del circuito cuántico",
        "diagram_error": "Para ver diagramas, instala 'qiskit[visualization]' y matplotlib.",
        "qiskit_missing": "Qiskit no está instalado. Instálalo para crear y simular circuitos.",
        "tab_main": "Aplicación", "tab_feedback": "Comentarios",
        "feedback_title": "Enviar comentarios", "feedback_prompt": "Cuéntanos qué funcionó, qué resultó confuso o qué te gustaría cambiar.",
        "feedback_send": "Enviar comentarios", "feedback_empty": "Escribe un comentario antes de enviarlo.",
        "feedback_saved": "Guardado como incidencia abierta en Feedback/.",
        "feedback_error": "No se pudieron guardar los comentarios. Comprueba que la carpeta permita escritura.",
        "feedback_issue_title": "Incidencia de comentarios", "feedback_status_label": "Estado",
        "feedback_open_label": "Abierta", "feedback_submitted_label": "Enviada",
        "feedback_screen_label": "Pantalla", "feedback_language_label": "Idioma de la interfaz",
        "feedback_text_heading": "Comentarios",
        "operator_chart_hint": "Selecciona la imagen de una puerta para ver su explicación.",
        "cryptography": "🔐 Criptografía cuántica",
        "playground": "🧩 Zona de dos qubits",
    },
    "Français": {
        "title": "Constructeur de Circuits Quantiques Qiskit", "main": "⚛️ Constructeur de Circuits Quantiques",
        "country": "Pays :", "region": "État / Province :", "language": "Langue préférée :",
        "continue": "✔ Continuer", "experience": "Niveau d'expérience :", "begin": "▶ Commencer le tutoriel",
        "back": "◀ Retour", "ready": "Statut : Prêt ✅", "running": "Sélection : {value}",
        "choose_circuit": "Choisissez un circuit à explorer :", "explore": "▶ Explorer le circuit",
        "operators": "⚛️ Guide des opérateurs quantiques", "circuit": "🔌 VOTRE CIRCUIT SÉLECTIONNÉ",
        "novice": "Débutant", "school": "Niveau secondaire", "university": "Niveau universitaire",
        "description": "Explication", "circuit_help": "Présentation du circuit",
        "matrix_label": "Matrice de la Porte :",
    },
    "Deutsch": {
        "title": "Qiskit Quantenschaltkreis-Builder", "main": "⚛️ Quantenschaltkreis-Builder",
        "country": "Land:", "region": "Bundesland / Provinz:", "language": "Bevorzugte Sprache:",
        "continue": "✔ Weiter", "experience": "Erfahrungsstufe:", "begin": "▶ Tutorial starten",
        "back": "◀ Zurück", "ready": "Status: Bereit ✅", "running": "Ausgewählt: {value}",
        "choose_circuit": "Schaltkreis auswählen:", "explore": "▶ Schaltkreis erkunden",
        "operators": "⚛️ Leitfaden für Quantenoperatoren", "circuit": "🔌 IHR AUSGEWÄHLTER SCHALTKREIS",
        "novice": "Anfänger", "school": "Sekundarstufe", "university": "Universitätsniveau",
        "description": "Erklärung", "circuit_help": "Schaltkreisübersicht",
        "matrix_label": "Gatter-Matrix:",
    },
    "日本語": {
        "title": "Qiskit 量子回路ビルダー", "main": "⚛️ 量子回路ビルダー",
        "country": "国：", "region": "州・地域：", "language": "希望する言語：",
        "continue": "✔ 続ける", "experience": "経験レベル：", "begin": "▶ チュートリアル開始",
        "back": "◀ 戻る", "ready": "状態：準備完了 ✅", "running": "選択：{value}",
        "choose_circuit": "探索する量子回路を選択：", "explore": "▶ 回路を探索",
        "operators": "⚛️ 量子演算子ガイド", "circuit": "🔌 選択した量子回路",
        "novice": "初心者", "school": "中学・高校レベル", "university": "大学レベル",
        "description": "説明", "circuit_help": "回路の概要",
        "matrix_label": "ゲート行列：",
    },
    "中文": {
        "title": "Qiskit 量子电路构建器", "main": "⚛️ 量子电路构建器",
        "country": "国家：", "region": "州 / 省：", "language": "首选语言：",
        "continue": "✔ 继续", "experience": "经验水平：", "begin": "▶ 开始教程",
        "back": "◀ 返回", "ready": "状态：准备就绪 ✅", "running": "已选择：{value}",
        "choose_circuit": "选择要探索的量子电路：", "explore": "▶ 探索电路",
        "operators": "⚛️ 量子算符指南", "circuit": "🔌 您选择的电路",
        "novice": "新手级别", "school": "中学级别", "university": "大学级别",
        "description": "说明", "circuit_help": "电路概览",
        "matrix_label": "量子门矩阵：",
    },
    "हिन्दी": {
        "title": "Qiskit क्वांटम सर्किट बिल्डर", "main": "⚛️ क्वांटम सर्किट बिल्डर",
        "country": "देश:", "region": "राज्य / प्रांत:", "language": "पसंदीदा भाषा:",
        "continue": "✔ जारी रखें", "experience": "अनुभव स्तर:", "begin": "▶ ट्यूटोरियल शुरू करें",
        "back": "◀ वापस", "ready": "स्थिति: तैयार ✅", "running": "चयनित: {value}",
        "choose_circuit": "अन्वेषण के लिए सर्किट चुनें:", "explore": "▶ सर्किट का अन्वेषण करें",
        "operators": "⚛️ क्वांटम ऑपरेटर गाइड", "circuit": "🔌 आपका चयनित सर्किट",
        "novice": "नौसिखिया स्तर", "school": "माध्यमिक विद्यालय स्तर", "university": "विश्वविद्यालय स्तर",
        "description": "व्याख्या", "circuit_help": "सर्किट का सारांश",
        "matrix_label": "गेट मैट्रिक्स:",
    },
    "Português": {
        "title": "Construtor de Circuitos Quânticos Qiskit", "main": "⚛️ Construtor de Circuitos Quânticos",
        "country": "País:", "region": "Estado / Província:", "language": "Idioma preferido:",
        "continue": "✔ Continuar", "experience": "Nível de experiência:", "begin": "▶ Iniciar tutorial",
        "back": "◀ Voltar", "ready": "Status: Pronto ✅", "running": "Selecionado: {value}",
        "choose_circuit": "Escolha um circuito para explorar:", "explore": "▶ Explorar circuito",
        "operators": "⚛️ Guia de Operadores Quânticos", "circuit": "🔌 SEU CIRCUITO SELECIONADO",
        "novice": "Nível iniciante", "school": "Nível ensino médio", "university": "Nível universitário",
        "description": "Explicação", "circuit_help": "Visão geral do circuito",
        "matrix_label": "Matriz da Porta:",
    },
}

TRANSLATIONS["العربية"] = {
    "title": "منشئ الدوائر الكمية", "main": "⚛️ منشئ الدوائر الكمية",
    "country": "البلد:", "region": "الولاية / المنطقة:", "language": "اللغة المفضلة:",
    "continue": "✔ متابعة", "experience": "مستوى الخبرة:", "begin": "▶ ابدأ الدرس",
    "back": "◀ رجوع", "ready": "الحالة: جاهز ✅", "running": "المحدد: {value}",
    "choose_circuit": "اختر دائرة لاستكشافها:", "explore": "▶ استكشف الدائرة",
    "operators": "⚛️ دليل البوابات والعمليات الكمية", "circuit": "🔌 الدائرة المحددة",
    "novice": "مبتدئ تمامًا", "school": "مستوى المدرسة الثانوية", "university": "مستوى جامعي",
    "description": "الشرح", "circuit_help": "نظرة عامة على الدائرة",
    "matrix_label": "مصفوفة البوابة:", "simulation": "▶ النظرية والمحاكاة المحلية",
    "close": "✕ إغلاق", "close_application": "✕ إغلاق التطبيق",
    "shots": "عدد قياسات المحاكاة:", "run": "▶ شغّل المحاكاة المحلية",
    "show_code": "▶ أظهر كود Qiskit", "hide_code": "▼ أخفِ كود Qiskit",
    "welcome": "منشئ الدوائر الكمية — مرحبًا",
    "diagram_tooltip": "مخطط مرئي للدائرة الكمية",
    "diagram_error": "لعرض المخططات، ثبّت 'qiskit[visualization]' وmatplotlib.",
    "qiskit_missing": "حزمة Qiskit غير مثبتة. ثبّتها لإنشاء الدوائر ومحاكاتها.",
    "tab_main": "التطبيق", "tab_feedback": "الملاحظات",
    "feedback_title": "أرسل ملاحظاتك", "feedback_prompt": "أخبرنا بما أعجبك، وما كان مربكًا، وما الذي تقترح تغييره.",
    "feedback_send": "إرسال الملاحظات", "feedback_empty": "اكتب ملاحظاتك قبل الإرسال.",
    "feedback_saved": "حُفظت الملاحظات كمسألة مفتوحة في مجلد Feedback/.",
    "feedback_error": "تعذّر حفظ الملاحظات. تحقّق من صلاحية الكتابة في المجلد.",
    "feedback_issue_title": "ملاحظة المستخدم", "feedback_status_label": "الحالة",
    "feedback_open_label": "مفتوحة", "feedback_submitted_label": "تاريخ الإرسال",
    "feedback_screen_label": "الشاشة", "feedback_language_label": "لغة الواجهة",
    "feedback_text_heading": "الملاحظات",
    "operator_chart_hint": "اختر صورة بوابة لفتح شرحها.",
    "cryptography": "🔐 التشفير الكمي",
    "playground": "🧩 مساحة بناء دائرة بكيوبتين",
}
LANGUAGES = ["English", "Español", "العربية"]
TRANSLATIONS = {language: TRANSLATIONS[language] for language in LANGUAGES}
FEEDBACK_SOURCE_LABELS = {
    "English": {
        "welcome": "Welcome", "experience": "Experience selection",
        "circuit": "Circuit selection", "operator": "Operator guide",
        "operator_detail": "Operator explanation", "cryptography": "Quantum cryptography / BB84",
        "playground": "Two-qubit circuit playground", "simulation": "Theory and local simulation",
    },
    "Español": {
        "welcome": "Bienvenida", "experience": "Selección de experiencia",
        "circuit": "Selección de circuito", "operator": "Guía de operadores",
        "operator_detail": "Explicación del operador", "cryptography": "Criptografía cuántica / BB84",
        "playground": "Zona de circuitos de dos qubits", "simulation": "Teoría y simulación local",
    },
    "العربية": {
        "welcome": "الترحيب", "experience": "اختيار مستوى الخبرة",
        "circuit": "اختيار الدائرة", "operator": "دليل البوابات",
        "operator_detail": "شرح البوابة", "cryptography": "التشفير الكمي / BB84",
        "playground": "مساحة دائرة بكيوبتين", "simulation": "النظرية والمحاكاة المحلية",
    },
}
COUNTRIES  = {
    "United States": ["Alabama","Alaska","Arizona","California","Florida",
                      "Massachusetts","New York","Texas","Other / N/A"],
    "Canada":        ["Alberta","British Columbia","Ontario","Quebec","Other / N/A"],
    "United Kingdom":["England","Northern Ireland","Scotland","Wales","Other / N/A"],
    "India":         ["Delhi","Gujarat","Karnataka","Maharashtra","Tamil Nadu","Other / N/A"],
    "Other":         ["Not applicable"],
}
COUNTRY_LABELS = {
    "English": {
        "United States": "United States", "Canada": "Canada",
        "United Kingdom": "United Kingdom", "India": "India", "Other": "Other",
    },
    "Español": {
        "United States": "Estados Unidos", "Canada": "Canadá",
        "United Kingdom": "Reino Unido", "India": "India", "Other": "Otro",
    },
    "العربية": {
        "United States": "الولايات المتحدة", "Canada": "كندا",
        "United Kingdom": "المملكة المتحدة", "India": "الهند", "Other": "أخرى",
    },
}

REGION_LABELS = {
    "Español": {
        "New York": "Nueva York",
        "British Columbia": "Columbia Británica",
        "England": "Inglaterra", "Northern Ireland": "Irlanda del Norte",
        "Scotland": "Escocia", "Wales": "Gales",
    },
    "العربية": {
        "Alabama": "ألاباما", "Alaska": "ألاسكا", "Arizona": "أريزونا",
        "California": "كاليفورنيا", "Florida": "فلوريدا",
        "Massachusetts": "ماساتشوستس", "New York": "نيويورك", "Texas": "تكساس",
        "Alberta": "ألبرتا", "British Columbia": "كولومبيا البريطانية",
        "Ontario": "أونتاريو", "Quebec": "كيبيك",
        "England": "إنجلترا", "Northern Ireland": "أيرلندا الشمالية",
        "Scotland": "اسكتلندا", "Wales": "ويلز",
        "Delhi": "دلهي", "Gujarat": "غوجارات", "Karnataka": "كارناتاكا",
        "Maharashtra": "ماهاراشترا", "Tamil Nadu": "تاميل نادو",
    },
}


# ─────────────────────────────────────────────
# OPERATOR CONTENT
# Tuple: (symbol, name, novice_desc, school_desc, university_desc)
# ─────────────────────────────────────────────
OPERATORS = [
    ("SINGLE-QUBIT GATES", [
        ("H",  "Hadamard",
         "Creates an even mix of |0⟩ and |1⟩ when applied to |0⟩.",
         "H|0⟩=(|0⟩+|1⟩)/√2. It creates an equal superposition from a computational-basis state.",
         "H = 1/√2 [[1,1],[1,-1]]. Unitary and Hermitian (H²=I); exchanges X and Z measurement bases."),
        ("X",  "Pauli-X / NOT",
         "Flips |0⟩ to |1⟩ and |1⟩ to |0⟩, like a switch.",
         "X swaps the computational basis states; acts like a classical NOT on basis states.",
         "X = [[0,1],[1,0]] = σx; π rotation about the Bloch-sphere X axis, up to global phase."),
        ("Y",  "Pauli-Y",
         "Flips the qubit and also changes its phase.",
         "Y maps |0⟩ to i|1⟩ and |1⟩ to -i|0⟩.",
         "Y = [[0,-i],[i,0]] = σy; Pauli operator, π rotation about Y up to global phase."),
        ("Z",  "Pauli-Z",
         "Leaves |0⟩ alone and changes the phase of |1⟩.",
         "Z|0⟩=|0⟩ and Z|1⟩=-|1⟩; changes relative phase, not measurement probabilities immediately.",
         "Z=diag(1,-1)=σz. Phase-flip operator; generator of rotations around the Z axis."),
        ("S",  "S phase gate",
         "Adds a quarter-turn phase to the |1⟩ part of a state.",
         "S=diag(1,i), equivalent to a π/2 phase rotation; S²=Z.",
         "S=T²=diag(1,i) is a Clifford gate; conjugation maps X to Y and leaves Z invariant."),
        ("T",  "T gate",
         "Adds a smaller phase change than the S gate.",
         "T=diag(1,e^(iπ/4)); supplies a π/4 phase rotation.",
         "T is a non-Clifford π/8 gate; with Clifford operations it supports universal fault-tolerant QC."),
        ("SX", "Square-root of X",
         "Performs half of an X-like rotation; applying it twice gives X up to global phase.",
         "SX²=X up to a physically unobservable global phase.",
         "SX=(I-iX)/√2; hardware-native SX and RZ gates are common on IBM systems."),
    ]),
    ("ROTATION GATES", [
        ("RX", "X-axis rotation",
         "Rotates a qubit around the X axis by an angle you choose.",
         "RX(θ) rotates the Bloch vector by θ about X.",
         "RX(θ)=exp(-iθX/2); parameterized rotations are used in variational algorithms such as VQE and QAOA."),
        ("RY", "Y-axis rotation",
         "Rotates a qubit around the Y axis by a chosen angle.",
         "RY(θ) rotates around Y and has real matrix entries.",
         "RY(θ)=exp(-iθY/2); combined with RZ supports Euler-angle decompositions of single-qubit unitaries."),
        ("RZ", "Z-axis rotation",
         "Changes the relative phase by rotating around the Z axis.",
         "RZ(θ) applies opposite phase factors to |0⟩ and |1⟩.",
         "RZ(θ)=diag(e^{-iθ/2},e^{iθ/2}); can be implemented virtually on superconducting hardware."),
        ("P",  "Phase gate",
         "Adds a selectable phase to the |1⟩ part of the state.",
         "P(θ)=diag(1,e^{iθ}); S and T are special angles.",
         "P(θ) is a U(1) phase operation; optimizable using gradient or parameter-shift methods."),
    ]),
    ("MULTI-QUBIT GATES", [
        ("CX",   "CNOT / controlled-X",
         "If the control qubit is 1, flip the target qubit. This can entangle qubits.",
         "CX maps |c,t⟩ to |c,t XOR c⟩. Hadamard followed by CX creates a Bell state.",
         "CX=|0⟩⟨0|⊗I+|1⟩⟨1|⊗X; entangling two-qubit gate, universal with arbitrary one-qubit gates."),
        ("CZ",   "CZ / controlled-Z",
         "Flips the phase of the |11⟩ component only; both qubits act symmetrically.",
         "CZ applies a Z gate to the target when the control is |1⟩; symmetric in its two qubits.",
         "CZ=diag(1,1,1,-1) in the computational basis; Clifford gate used as oracle in Grover search."),
        ("SWAP", "SWAP",
         "Exchanges the states stored in two qubits.",
         "SWAP|a,b⟩=|b,a⟩ and is commonly decomposed into three CX gates.",
         "SWAP=(I⊗I+X⊗X+Y⊗Y+Z⊗Z)/2; routing swaps can dominate overhead on limited-connectivity devices."),
        ("CCX",  "Toffoli / controlled-controlled-X",
         "Flips the target only when both control qubits are 1.",
         "CCX performs a reversible AND-like operation on computational-basis states.",
         "Three-qubit reversible gate; decompositions use multiple entangling and single-qubit gates."),
        ("CSWAP","Fredkin / controlled-SWAP",
         "Swaps two target qubits only when the control is 1.",
         "CSWAP conditionally exchanges two qubit states and is used in the SWAP test.",
         "Fredkin is a controlled permutation gate; preserves the target pair's Hamming weight."),
    ]),
    ("CIRCUIT OPERATIONS", [
        ("Measure","Measurement",
         "Reads a qubit as 0 or 1; the result is probabilistic for a superposition.",
         "For α|0⟩+β|1⟩, measurement yields 0 with probability |α|² and 1 with probability |β|².",
         "Computational-basis measurement follows the Born rule; non-unitary, stores outcomes in classical bits."),
        ("Reset",  "Reset",
         "Returns a qubit to |0⟩.",
         "Reset is a non-unitary operation that prepares the qubit in |0⟩.",
         "Reset is a quantum channel; implementations may use measurement+conditional correction or dissipation."),
        ("Barrier","Barrier",
         "A marker that separates circuit sections and constrains compiler rearrangement.",
         "A barrier is a compiler directive, not a physical quantum operation.",
         "Barriers constrain transpiler optimization across a circuit boundary."),
    ]),
    ("CLASSICAL CONTROL", [
        ("If",     "Classical condition",
         "Choose an operation based on an earlier measurement result.",
         "Classical feed-forward applies gates conditionally on classical bits.",
         "Dynamic circuits combine classical control flow with quantum operations for adaptive correction."),
        ("For",    "Repeated circuit / loop",
         "Repeats a group of operations.",
         "A repeated subcircuit can implement iterative algorithms or repeated gate sequences.",
         "Loop constructs describe parameterized circuit families; compilation depends on the target interface."),
        ("Unitary","Unitary operation",
         "A custom operation that preserves valid quantum-state probabilities.",
         "A unitary matrix U obeys U†U=I and can represent a reversible quantum operation.",
         "An n-qubit unitary is a 2ⁿ×2ⁿ matrix satisfying U†U=I; synthesis decomposes it into basis gates."),
    ]),
]

# A short plain-language primer shown before the gate reference cards.
BEGINNER_PRIMER = {
    "English": (
        "Picture a qubit as a tiny arrow. Gates can turn it, and its direction helps set the chances of measurement results.\n"
        "Superposition: like a coin in motion, more than one result is possible. The coin is only an analogy: a qubit can show wave-like interference between possibilities.\n"
        "A gate: a controlled move of the arrow. H prepares two equally likely results if measured right away; later gates can change those chances. X flips 0 and 1; Z changes phase.\n"
        "Entanglement: two qubits can share one quantum state. In this circuit's Bell pair, the shown measurement results always match, but neither qubit sends a message to the other.\n"
        "Coherence: like ripples keeping their rhythm, the wave-like pattern stays intact. Later gates can make parts reinforce or cancel, changing the chances of results. Noise is like a splash that scrambles the pattern.\n"
        "Measurement: asks for one result and changes the state. Reset returns the qubit to its starting state; a barrier is just a circuit marker."
    ),
    "Español": (
        "Imagina un qubit como una flecha pequeña. Las puertas pueden girarla, y su dirección influye en las probabilidades de los resultados al medir.\n"
        "Superposición: como una moneda en movimiento, hay varios resultados posibles. Es solo una comparación: un qubit puede mostrar interferencia ondulatoria entre posibilidades.\n"
        "Una puerta es un movimiento controlado de la flecha. H prepara dos resultados igual de probables si se mide enseguida; otras puertas pueden cambiar esas probabilidades. X intercambia 0 y 1; Z cambia la fase.\n"
        "Entrelazamiento: dos qubits pueden compartir un estado cuántico. En el par de Bell de este circuito, los resultados de la medición mostrada siempre coinciden, pero ningún qubit envía un mensaje al otro.\n"
        "Coherencia: como ondas que conservan el ritmo, el patrón ondulatorio sigue intacto. Otras puertas pueden hacer que algunas partes se refuercen o se cancelen y así cambiar las probabilidades. El ruido altera el patrón, como una salpicadura.\n"
        "Medir da un resultado y cambia el estado. Reiniciar devuelve el qubit a su estado inicial; una barrera solo marca una sección del circuito."
    ),
    "العربية": (
        "للتقريب، تخيّل الكيوبت سهمًا صغيرًا. تغيّر البوابات اتجاهه، ويساعد اتجاهه في تحديد فرص نتائج القياس.\n"
        "التراكب: يشبه قطعة نقدية تتحرك، إذ توجد نتائج محتملة متعددة. لكنه تشبيه فقط؛ فالكيوبت يُظهر تداخلًا موجيًا بين الاحتمالات.\n"
        "البوابة حركة تغيّر حالة الكيوبت. تهيّئ H نتيجتين متساويتين في الاحتمال إذا قِيس الكيوبت مباشرة؛ ويمكن للبوابات اللاحقة تغيير هذه الفرص. تبدّل X القيمتين 0 و1، وتغيّر Z الطور.\n"
        "التشابك: قد يشترك كيوبتان في حالة كمية واحدة. في حالة بيل التي تنشئها هذه الدائرة تتطابق نتيجتا القياس المعروض دائمًا، لكن أيًّا من الكيوبتين لا يرسل رسالة إلى الآخر.\n"
        "التماسك: يشبه موجات تحافظ على إيقاعها؛ فيبقى النمط الموجي محفوظًا. قد تجعل بوابات لاحقة أجزاءً تتعزز أو تلغي بعضها، فتتغير فرص النتائج. والضوضاء كرشة ماء تفسد النمط.\n"
        "القياس يعطي نتيجة ويغيّر الحالة. إعادة الضبط تعيد الكيوبت إلى حالة البداية، والحاجز علامة لتنظيم الدائرة فقط."
    ),
}

BRAND_NEW_CIRCUITS = {
    "English": {
        "heading": "How this circuit works",
        "The Bell State Circuit (Entanglement)": {
            "description": "This circuit prepares two equally likely possibilities, then links the qubits in one shared quantum state. Their measurement results always match: both are 0 or both are 1. Neither qubit sends a message to the other.",
            "steps": "1. Start with both qubits at zero.\n2. Create two possible paths for the first qubit.\n3. Link the qubits with a controlled flip.\n4. Measure them; the results match.",
        },
        "Three-Qubit GHZ State Circuit": {
            "description": "The first qubit creates two shared possibilities. It then passes that connection to the other qubits, so all three measurement results match.",
            "steps": "1. Start all three qubits at zero.\n2. Create two shared possibilities.\n3. Connect the first qubit to each of the others.\n4. Measure all three; their results match.",
        },
        "Two-Qubit Grover Search Circuit": {
            "description": "This circuit searches four possible answers for one marked answer. It marks the target, then shifts the odds so a measurement finds that answer in the ideal case.",
            "steps": "1. Give all four answers an equal chance.\n2. Mark the target answer.\n3. Shift the odds toward that answer.\n4. Measure to read the answer.",
        },
    },
    "Español": {
        "heading": "Cómo funciona este circuito",
        "The Bell State Circuit (Entanglement)": {
            "description": "Primero prepara dos posibilidades igual de probables y después conecta los qubits en un mismo estado cuántico. Al medirlos, los resultados siempre coinciden: ambos son 0 o ambos son 1. Ningún qubit envía un mensaje al otro.",
            "steps": "1. Empieza con ambos qubits en cero.\n2. Crea dos posibilidades para el primero.\n3. Conecta los qubits con un cambio controlado.\n4. Mídelos; los resultados coinciden.",
        },
        "Three-Qubit GHZ State Circuit": {
            "description": "El primer qubit crea dos posibilidades compartidas y conecta los otros dos. Por eso coinciden los resultados de las tres mediciones.",
            "steps": "1. Empieza con los tres qubits en cero.\n2. Crea dos posibilidades compartidas.\n3. Conecta el primer qubit con cada uno de los otros.\n4. Mide los tres; los resultados coinciden.",
        },
        "Two-Qubit Grover Search Circuit": {
            "description": "El circuito busca una respuesta marcada entre cuatro opciones. La marca ayuda a desplazar las probabilidades hacia esa respuesta para que la medición la encuentre en el caso ideal.",
            "steps": "1. Da la misma oportunidad a las cuatro respuestas.\n2. Marca la respuesta buscada.\n3. Desplaza las probabilidades hacia ella.\n4. Mide para leer la respuesta.",
        },
    },
    "العربية": {
        "heading": "كيف تعمل هذه الدائرة",
        "The Bell State Circuit (Entanglement)": {
            "description": "تهيّئ الدائرة احتمالين متساويين، ثم تربط الكيوبتين في حالة كمية مشتركة. عند القياس تتطابق النتيجتان دائمًا: إما 0 لكليهما أو 1 لكليهما. ولا يرسل أيٌّ من الكيوبتين رسالة إلى الآخر.",
            "steps": "1. ابدأ والكيوبتان عند الصفر.\n2. أنشئ احتمالين للكيوبت الأول.\n3. اربط الكيوبتين بقلب مشروط.\n4. قِسهما؛ تتطابق النتيجتان.",
        },
        "Three-Qubit GHZ State Circuit": {
            "description": "ينشئ الكيوبت الأول احتمالين مشتركين، ثم يربط الكيوبتين الآخرين به. لذلك تتطابق نتائج قياس الكيوبتات الثلاثة.",
            "steps": "1. ابدأ والكيوبتات الثلاثة عند الصفر.\n2. أنشئ احتمالين مشتركين.\n3. اربط الكيوبت الأول بكل واحد من الآخرين.\n4. قِس الكيوبتات الثلاثة؛ تتطابق النتائج.",
        },
        "Two-Qubit Grover Search Circuit": {
            "description": "تبحث الدائرة عن إجابة محددة بين أربع إجابات. تضع علامة على الهدف ثم تغيّر الاحتمالات لصالحه، بحيث يعثر عليه القياس في الحالة المثالية.",
            "steps": "1. امنح الإجابات الأربع فرصًا متساوية.\n2. ضع علامة على الإجابة المطلوبة.\n3. غيّر الاحتمالات لصالحها.\n4. قِس لقراءة الإجابة.",
        },
    },
}

ARABIC_BEGINNER_GATES = {
    "H": ("بوابة هادامارد", "تتيح احتمالين متساويين، مثل عملة تتحرك. لكن الكيوبت، بخلاف العملة العادية، يُظهر أيضًا تداخلًا بين الاحتمالات."),
    "X": ("بوابة X / تبديل", "تبدّل 0 و1، مثل مفتاح يغيّر وضعه."),
    "Y": ("بوابة Y", "تبدّل الحالة وتغيّر طورها؛ تخيّل تدوير السهم حول محور آخر."),
    "Z": ("بوابة Z", "تغيّر طور الجزء المرتبط بـ1، مثل تغيير توقيت موجة من دون تغيير فرص القياس فورًا."),
    "S": ("بوابة S", "تضيف تغييرًا صغيرًا في الطور؛ كخطوة قصيرة على ساعة الموجة."),
    "T": ("بوابة T", "تضيف تغييرًا أصغر في الطور من S."),
    "SX": ("الجذر التربيعي لـX", "تنفّذ نصف تأثير X؛ تطبيقها مرتين يعطي X."),
    "RX": ("دوران حول X", "تدير سهم الحالة حول محور X بزاوية تختارها."),
    "RY": ("دوران حول Y", "تدير سهم الحالة حول محور Y بزاوية تختارها."),
    "RZ": ("دوران حول Z", "تدير الحالة حول محور Z، فتؤثر أساسًا في الطور."),
    "P": ("بوابة الطور", "تضيف مقدارًا تختاره من الطور إلى الجزء المرتبط بـ1."),
    "CX": ("بوابة X المتحكَّم بها", "تغيّر الهدف فقط إذا كان الكيوبت المتحكّم في الحالة 1؛ مثل مفتاح أمان."),
    "CZ": ("بوابة Z المتحكَّم بها", "تضع علامة طور مشتركة عندما يكون كلا الكيوبتين في حالة التفعيل؛ لا تبدّل القيم مباشرة."),
    "SWAP": ("بوابة التبادل", "تبادل حالتي كيوبتين، مثل تبديل ما في صندوقين."),
    "CCX": ("بوابة توفولي", "تبدّل الهدف عندما يكون المفتاحان كلاهما في الحالة 1."),
    "CSWAP": ("بوابة التبادل المتحكَّم بها", "تبادل كيوبتين فقط عندما يكون كيوبت التحكّم في الحالة 1."),
    "Measure": ("القياس", "يقرأ الكيوبت ويعطي نتيجة واحدة؛ وقد تختلف النتائج عند تكرار التجربة."),
    "Reset": ("إعادة الضبط", "يعيد الكيوبت إلى حالة البداية التي تقابل الصفر، مثل إعادة قطعة اللعبة إلى البداية."),
    "Barrier": ("حاجز تنظيمي", "علامة تقسّم الرسم إلى أجزاء؛ لا تغيّر الحالة بنفسها."),
    "If": ("شرط كلاسيكي", "ينفّذ خطوة لاحقة بناءً على نتيجة قياس سابقة."),
    "For": ("تكرار", "يعيد مجموعة خطوات، مثل تكرار حركة في وصفة."),
    "Unitary": ("عملية وحدوية", "تحوّل الحالة مع الحفاظ على مجموع الاحتمالات عند 100%."),
}


# ─────────────────────────────────────────────
# OPERATOR TRANSLATIONS
# ─────────────────────────────────────────────
BRAND_NEW_OPERATOR_EXPLANATIONS = {
    "English": {
        "H": "Like a coin in motion, it keeps two possible outcomes in play. A qubit can also show interference, unlike an ordinary coin.",
        "X": "Like flipping a light switch: it changes the qubit from one basic value to the other.",
        "Y": "Flips the qubit and also shifts the timing of its wave-like pattern.",
        "Z": "Keeps the immediate odds the same but changes wave timing, which can affect later gates.",
        "S": "Adds a quarter-turn to the wave timing. It is a larger phase step than T.",
        "T": "Adds a small step to the wave timing, like a finer adjustment than S.",
        "SX": "Makes half of an X-like turn. Doing it twice has the effect of X.",
        "RX": "Turns the qubit's state arrow around the X direction by a chosen amount.",
        "RY": "Turns the qubit's state arrow around the Y direction by a chosen amount.",
        "RZ": "Turns the qubit around the Z direction, changing the timing of its wave-like pattern.",
        "P": "Lets you choose how much to shift the wave timing.",
        "CX": "A controlled switch: the target flips only when the control qubit is on. It can link two qubits together.",
        "CZ": "Adds a hidden phase mark only when both qubits are on. The mark can affect later steps.",
        "SWAP": "Exchanges the states of two qubits, like swapping what is stored in two boxes.",
        "CCX": "A two-key switch: the target flips only when both control qubits are on.",
        "CSWAP": "Exchanges two target qubits only when the control qubit is on.",
        "Measure": "Reads the qubit and gives one result. Repeating the experiment can give different results.",
        "Reset": "Returns the qubit to its starting state, like putting a game piece back at the beginning.",
        "Barrier": "A divider in the circuit picture. It organizes steps but does not change the qubits.",
        "If": "Chooses the next action based on an earlier measurement result.",
        "For": "Repeats a group of steps, like repeating a move in a set of instructions.",
        "Unitary": "A reversible change that keeps all possible measurement chances adding up to 100%.",
    },
    "Español": {
        "H": "Como una moneda en movimiento, mantiene dos resultados posibles. A diferencia de una moneda común, un qubit también puede mostrar interferencia.",
        "X": "Como un interruptor: cambia el qubit de un valor básico al otro.",
        "Y": "Cambia el qubit y también desplaza el ritmo de su patrón ondulatorio.",
        "Z": "Mantiene iguales las probabilidades inmediatas, pero cambia el ritmo de la onda y puede afectar pasos posteriores.",
        "S": "Añade un cuarto de giro al ritmo de la onda. Es un cambio de fase mayor que T.",
        "T": "Añade un pequeño cambio al ritmo de la onda, más fino que el de S.",
        "SX": "Hace medio giro parecido al de X. Aplicarlo dos veces produce el efecto de X.",
        "RX": "Gira la flecha que representa el estado del qubit alrededor del eje X.",
        "RY": "Gira la flecha que representa el estado del qubit alrededor del eje Y.",
        "RZ": "Gira el qubit alrededor del eje Z y cambia el ritmo de su patrón ondulatorio.",
        "P": "Permite elegir cuánto cambiar el ritmo de la onda.",
        "CX": "Un interruptor controlado: el objetivo cambia solo si el qubit de control está activo. Puede enlazar dos qubits.",
        "CZ": "Añade una marca de fase oculta solo cuando ambos qubits están activos. Puede afectar pasos posteriores.",
        "SWAP": "Intercambia los estados de dos qubits, como cambiar lo guardado en dos cajas.",
        "CCX": "Un interruptor de dos llaves: el objetivo cambia solo si ambos controles están activos.",
        "CSWAP": "Intercambia dos qubits objetivo solo cuando el qubit de control está activo.",
        "Measure": "Lee el qubit y da un resultado. Al repetir el experimento pueden aparecer resultados distintos.",
        "Reset": "Devuelve el qubit a su estado inicial, como colocar una ficha al comienzo del juego.",
        "Barrier": "Es una división en el dibujo del circuito. Ordena los pasos, pero no cambia los qubits.",
        "If": "Elige la siguiente acción según un resultado de medición anterior.",
        "For": "Repite un grupo de pasos, como repetir un movimiento de unas instrucciones.",
        "Unitary": "Un cambio reversible que mantiene en 100 % la suma de las probabilidades de todos los resultados.",
    },
    "العربية": {
        symbol: details[1] for symbol, details in ARABIC_BEGINNER_GATES.items()
    },
}

OPERATOR_LOCALIZATIONS = {
    "Español": {
        "categories": ["PUERTAS DE UN SOLO QUBIT","PUERTAS DE ROTACIÓN",
                        "PUERTAS DE VARIOS QUBITS","OPERACIONES DEL CIRCUITO","CONTROL CLÁSICO"],
        "levels": ["Desde cero: ","Nivel de secundaria: ","Nivel universitario: "],
        "gates": {
            "H":      ("Hadamard",             ["Crea una combinación equilibrada de |0⟩ y |1⟩ cuando se aplica a |0⟩.","H|0⟩=(|0⟩+|1⟩)/√2. Crea una superposición equilibrada.","H = 1/√2 [[1,1],[1,-1]]. Unitario y hermítico (H²=I), intercambia bases X y Z."]),
            "X":      ("Pauli-X / NOT",        ["Intercambia |0⟩ y |1⟩, como un interruptor.","Intercambia estados de base; operación NOT clásica.","X = [[0,1],[1,0]] = σx; rotación de π alrededor de X, salvo fase global."]),
            "Y":      ("Pauli-Y",              ["Invierte el qubit y cambia su fase.","Y transforma |0⟩ en i|1⟩ y |1⟩ en -i|0⟩.","Y = [[0,-i],[i,0]] = σy; rotación de π alrededor de Y, salvo fase global."]),
            "Z":      ("Pauli-Z",              ["Deja |0⟩ sin cambios y cambia la fase de |1⟩.","Z|0⟩=|0⟩ y Z|1⟩=-|1⟩; cambia la fase relativa.","Z=diag(1,-1)=σz. Operación de cambio de fase."]),
            "S":      ("Puerta de fase S",     ["Añade un cuarto de vuelta de fase a la parte |1⟩.","S=diag(1,i); rotación de fase de π/2; S²=Z.","S=T²=diag(1,i) es una puerta Clifford."]),
            "T":      ("Puerta T",             ["Añade un cambio de fase menor que la puerta S.","T=diag(1,e^(iπ/4)); rotación de fase de π/4.","T es una puerta π/8 no Clifford para computación universal."]),
            "SX":     ("Raíz cuadrada de X",   ["Media rotación similar a X; dos veces equivale a X.","SX²=X salvo fase global inobservable.","SX=(I-iX)/√2; puertas nativas en sistemas IBM."]),
            "RX":     ("Rotación alrededor de X",["Rota el qubit alrededor del eje X.","RX(θ) rota el vector de Bloch θ alrededor de X.","RX(θ)=exp(-iθX/2); usado en VQE y QAOA."]),
            "RY":     ("Rotación alrededor de Y",["Rota el qubit alrededor del eje Y.","RY(θ) rota alrededor de Y; elementos de matriz reales.","RY(θ)=exp(-iθY/2); junto con RZ permite descomposición de Euler."]),
            "RZ":     ("Rotación alrededor de Z",["Cambia la fase relativa por rotación alrededor de Z.","RZ(θ) aplica factores de fase opuestos a |0⟩ y |1⟩.","RZ(θ)=diag(e^{-iθ/2},e^{iθ/2}); a menudo virtual en hardware."]),
            "P":      ("Puerta de fase",       ["Añade una fase seleccionable a la parte |1⟩.","P(θ)=diag(1,e^{iθ}); S y T son ángulos particulares.","P(θ) es una operación de fase U(1); optimizable por gradientes."]),
            "CX":     ("CNOT / X controlada",  ["Si el control es 1, invierte el qubit objetivo.","CX transforma |c,t⟩ en |c,t XOR c⟩.","CX=|0⟩⟨0|⊗I+|1⟩⟨1|⊗X; puerta entrelazante universal."]),
            "CZ":     ("CZ / Z controlada",    ["Invierte la fase de |11⟩; ambos qubits actúan simétricamente.","CZ aplica Z al objetivo cuando el control es |1⟩.","CZ=diag(1,1,1,-1); puerta Clifford usada como oráculo en Grover."]),
            "SWAP":   ("Intercambio SWAP",     ["Intercambia los estados de dos qubits.","SWAP|a,b⟩=|b,a⟩; se descompone en tres CX.","SWAP=(I⊗I+X⊗X+Y⊗Y+Z⊗Z)/2."]),
            "CCX":    ("Toffoli",              ["Invierte el objetivo solo cuando ambos controles son 1.","CCX: operación reversible tipo AND.","Puerta reversible de tres qubits."]),
            "CSWAP":  ("Fredkin / SWAP controlada",["Intercambia dos qubits cuando el control es 1.","CSWAP: intercambio condicional.","Puerta de permutación controlada."]),
            "Measure":("Medición",             ["Lee un qubit como 0 o 1; probabilístico en superposición.","Para α|0⟩+β|1⟩: 0 con |α|², 1 con |β|².","Medición sigue la regla de Born; no unitaria."]),
            "Reset":  ("Reinicio",             ["Devuelve un qubit al estado |0⟩.","Operación no unitaria que prepara |0⟩.","Canal cuántico; medición y corrección condicional."]),
            "Barrier":("Barrera",              ["Separa secciones del circuito.","Directiva del compilador; no es operación física.","Limita las optimizaciones del transpiler."]),
            "If":     ("Condición clásica",    ["Elige una operación según resultado de medición.","Retroalimentación clásica condicional.","Circuitos dinámicos para medición adaptativa."]),
            "For":    ("Bucle",                ["Repite un grupo de operaciones.","Algoritmos iterativos.","Familias de circuitos parametrizados."]),
            "Unitary":("Operación unitaria",   ["Preserva probabilidades del estado cuántico.","U†U=I; operación reversible.","Matriz 2ⁿ×2ⁿ; síntesis en puertas de base."]),
        },
    },
    "Français": {
        "categories": ["PORTES À UN SEUL QUBIT","PORTES DE ROTATION",
                        "PORTES MULTI-QUBITS","OPÉRATIONS DU CIRCUIT","CONTRÔLE CLASSIQUE"],
        "levels": ["Niveau débutant : ","Niveau secondaire : ","Niveau universitaire : "],
        "gates": {
            "H":      ("Hadamard",             ["Crée un mélange équilibré de |0⟩ et |1⟩ appliquée à |0⟩.","H|0⟩=(|0⟩+|1⟩)/√2. Superposition égale.","H = 1/√2 [[1,1],[1,-1]]. Unitaire et hermitienne (H²=I)."]),
            "X":      ("Pauli-X / NON",        ["Échange |0⟩ et |1⟩ comme un interrupteur.","Échange les états de base; agit comme NON classique.","X = [[0,1],[1,0]] = σx; rotation de π autour de X."]),
            "Y":      ("Pauli-Y",              ["Inverse le qubit et modifie sa phase.","Y envoie |0⟩ vers i|1⟩ et |1⟩ vers -i|0⟩.","Y = [[0,-i],[i,0]] = σy; rotation de π autour de Y."]),
            "Z":      ("Pauli-Z",              ["Laisse |0⟩ inchangé et modifie la phase de |1⟩.","Z|0⟩=|0⟩ et Z|1⟩=-|1⟩.","Z=diag(1,-1)=σz. Changement de phase."]),
            "S":      ("Porte de phase S",     ["Ajoute un quart de tour de phase à |1⟩.","S=diag(1,i); rotation de phase π/2; S²=Z.","S=T²=diag(1,i) est une porte Clifford."]),
            "T":      ("Porte T",              ["Ajoute un changement de phase plus petit que S.","T=diag(1,e^(iπ/4)); rotation de phase π/4.","T est une porte π/8 non-Clifford."]),
            "SX":     ("Racine carrée de X",   ["Demi-rotation de type X; deux fois donne X.","SX²=X à une phase globale près.","SX=(I-iX)/√2; portes natives sur systèmes IBM."]),
            "RX":     ("Rotation autour de X", ["Fait tourner le qubit autour de X.","RX(θ) fait tourner le vecteur de Bloch de θ.","RX(θ)=exp(-iθX/2); utilisé dans VQE et QAOA."]),
            "RY":     ("Rotation autour de Y", ["Fait tourner le qubit autour de Y.","RY(θ) a des éléments de matrice réels.","RY(θ)=exp(-iθY/2); décompositions d'Euler avec RZ."]),
            "RZ":     ("Rotation autour de Z", ["Modifie la phase relative par rotation autour de Z.","RZ(θ) applique des facteurs de phase opposés.","RZ(θ)=diag(e^{-iθ/2},e^{iθ/2}); souvent virtuelle."]),
            "P":      ("Porte de phase",       ["Ajoute une phase réglable à |1⟩.","P(θ)=diag(1,e^{iθ}); S et T sont des cas particuliers.","P(θ) est une opération de phase U(1)."]),
            "CX":     ("CNOT / X contrôlé",    ["Si le contrôle vaut 1, inverse la cible.","CX transforme |c,t⟩ en |c,t XOR c⟩.","CX=|0⟩⟨0|⊗I+|1⟩⟨1|⊗X; porte intriquante universelle."]),
            "CZ":     ("CZ / Z contrôlé",      ["Inverse la phase de |11⟩; symétrique.","CZ applique Z à la cible quand le contrôle est |1⟩.","CZ=diag(1,1,1,-1); porte Clifford, oracle de Grover."]),
            "SWAP":   ("Échange SWAP",         ["Échange les états de deux qubits.","SWAP|a,b⟩=|b,a⟩; trois CX.","SWAP=(I⊗I+X⊗X+Y⊗Y+Z⊗Z)/2."]),
            "CCX":    ("Toffoli",              ["Inverse la cible si les deux contrôles valent 1.","CCX: opération réversible de type ET.","Porte réversible à trois qubits."]),
            "CSWAP":  ("Fredkin / SWAP contrôlé",["Échange deux qubits si le contrôle vaut 1.","CSWAP: échange conditionnel.","Porte de permutation contrôlée."]),
            "Measure":("Mesure",               ["Lit le qubit comme 0 ou 1; probabiliste.","Pour α|0⟩+β|1⟩: 0 avec |α|², 1 avec |β|².","Mesure suit la règle de Born; non unitaire."]),
            "Reset":  ("Réinitialisation",     ["Ramène un qubit à |0⟩.","Opération non unitaire préparant |0⟩.","Canal quantique; mesure et correction conditionnelle."]),
            "Barrier":("Barrière",             ["Sépare des sections du circuit.","Directive du compilateur.","Limite l'optimisation du transpileur."]),
            "If":     ("Condition classique",  ["Choisit une opération selon un résultat de mesure.","Rétroaction classique conditionnelle.","Circuits dynamiques pour mesure adaptative."]),
            "For":    ("Boucle",               ["Répète un groupe d'opérations.","Algorithmes itératifs.","Familles de circuits paramétrés."]),
            "Unitary":("Opération unitaire",   ["Préserve les probabilités d'état.","U†U=I; opération réversible.","Matrice 2ⁿ×2ⁿ; décomposée en portes de base."]),
        },
    },
    "Deutsch": {
        "categories": ["EIN-QUBIT-GATTER","ROTATIONSGATTER",
                        "MEHR-QUBIT-GATTER","SCHALTKREISOPERATIONEN","KLASSISCHE STEUERUNG"],
        "levels": ["Anfängerniveau: ","Sekundarstufe: ","Universitätsniveau: "],
        "gates": {
            "H":      ("Hadamard",                ["Erzeugt gleichmäßige Mischung aus |0⟩ und |1⟩.","H|0⟩=(|0⟩+|1⟩)/√2. Gleichmäßige Superposition.","H = 1/√2 [[1,1],[1,-1]]. Unitär und hermitesch (H²=I)."]),
            "X":      ("Pauli-X / NICHT",         ["Vertauscht |0⟩ und |1⟩ wie ein Schalter.","Vertauscht Rechenbasiszustände; klassische NICHT-Operation.","X = [[0,1],[1,0]] = σx; π-Drehung um X."]),
            "Y":      ("Pauli-Y",                 ["Kippt das Qubit und ändert seine Phase.","Y bildet |0⟩ auf i|1⟩ und |1⟩ auf -i|0⟩ ab.","Y = [[0,-i],[i,0]] = σy; π-Drehung um Y."]),
            "Z":      ("Pauli-Z",                 ["Lässt |0⟩ unverändert, ändert Phase von |1⟩.","Z|0⟩=|0⟩ und Z|1⟩=-|1⟩.","Z=diag(1,-1)=σz. Phasenflip-Gatter."]),
            "S":      ("S-Phasengatter",          ["Fügt dem |1⟩-Anteil eine Vierteldrehung hinzu.","S=diag(1,i); π/2-Phasendrehung; S²=Z.","S=T²=diag(1,i) ist ein Clifford-Gatter."]),
            "T":      ("T-Gatter",                ["Ändert die Phase weniger stark als S.","T=diag(1,e^(iπ/4)); π/4-Phasendrehung.","T ist ein Nicht-Clifford-π/8-Gatter."]),
            "SX":     ("Quadratwurzel von X",     ["Halbe X-Drehung; zweimal = X bis auf globale Phase.","SX²=X bis auf unbeobachtbare globale Phase.","SX=(I-iX)/√2; native Gatter auf IBM-Systemen."]),
            "RX":     ("Drehung um X",            ["Dreht das Qubit um X mit gewähltem Winkel.","RX(θ) dreht Bloch-Vektor um θ um X.","RX(θ)=exp(-iθX/2); in VQE und QAOA verwendet."]),
            "RY":     ("Drehung um Y",            ["Dreht das Qubit um Y.","RY(θ) dreht um Y; reelle Matrixeinträge.","RY(θ)=exp(-iθY/2); Euler-Zerlegung mit RZ."]),
            "RZ":     ("Drehung um Z",            ["Ändert relative Phase durch Drehung um Z.","RZ(θ) wendet entgegengesetzte Phasenfaktoren an.","RZ(θ)=diag(e^{-iθ/2},e^{iθ/2}); oft virtuell."]),
            "P":      ("Phasengatter",            ["Fügt einstellbare Phase zu |1⟩ hinzu.","P(θ)=diag(1,e^{iθ}); S und T als Spezialfälle.","P(θ) ist U(1)-Phasenoperation."]),
            "CX":     ("CNOT / kontrolliertes X", ["Kontrolle=1: Ziel-Qubit kippen.","CX bildet |c,t⟩ auf |c,t XOR c⟩ ab.","CX=|0⟩⟨0|⊗I+|1⟩⟨1|⊗X; verschränkendes universelles Gatter."]),
            "CZ":     ("CZ / kontrolliertes Z",   ["Kippt Phase von |11⟩; beide Qubits symmetrisch.","CZ wendet Z auf Ziel an wenn Kontrolle |1⟩.","CZ=diag(1,1,1,-1); Clifford-Gatter, Grover-Orakel."]),
            "SWAP":   ("SWAP-Austausch",          ["Tauscht Zustände zweier Qubits.","SWAP|a,b⟩=|b,a⟩; drei CX-Gatter.","SWAP=(I⊗I+X⊗X+Y⊗Y+Z⊗Z)/2."]),
            "CCX":    ("Toffoli",                 ["Kippt Ziel wenn beide Kontrollen 1.","CCX: reversible AND-Operation.","Drei-Qubit reversibles Gatter."]),
            "CSWAP":  ("Fredkin / CSWAP",         ["Tauscht Ziel-Qubits wenn Kontrolle 1.","CSWAP: bedingter Austausch.","Kontrolliertes Permutationsgatter."]),
            "Measure":("Messung",                 ["Liest Qubit als 0 oder 1; probabilistisch.","Born-Regel: 0 mit |α|², 1 mit |β|².","Nicht-unitäre Rechenbasisprojektion."]),
            "Reset":  ("Zurücksetzen",            ["Setzt Qubit auf |0⟩.","Nicht-unitäre Vorbereitung von |0⟩.","Quantenkanal; Messung mit Korrektur."]),
            "Barrier":("Barriere",                ["Trennt Schaltkreisabschnitte.","Compiler-Anweisung.","Begrenzt Transpiler-Optimierungen."]),
            "If":     ("Klassische Bedingung",    ["Wählt Operation anhand Messergebnis.","Klassische Rückkopplung.","Dynamische Schaltkreise für Anpassung."]),
            "For":    ("Schleife",                ["Wiederholt Operationen.","Iterative Algorithmen.","Parametrisierte Schaltkreisfamilien."]),
            "Unitary":("Unitäre Operation",       ["Erhält Zustandswahrscheinlichkeiten.","U†U=I; reversibel.","2ⁿ×2ⁿ Matrix; Zerlegung in Basistoren."]),
        },
    },
    "日本語": {
        "categories": ["単一量子ビットゲート","回転ゲート","多量子ビットゲート","回路操作","古典制御"],
        "levels": ["初級：","中学・高校レベル：","大学レベル："],
        "gates": {
            "H":      ("アダマールゲート",         ["|0⟩に適用すると等しい重ね合わせを作ります。","H|0⟩=(|0⟩+|1⟩)/√2。","H = 1/√2 [[1,1],[1,-1]]。ユニタリかつエルミート（H²=I）。"]),
            "X":      ("パウリX / NOT",           ["スイッチのように|0⟩と|1⟩を入れ替えます。","計算基底を交換；NOT演算。","X = [[0,1],[1,0]] = σx; X軸周りπ回転。"]),
            "Y":      ("パウリY",                 ["量子ビットを反転し位相も変えます。","Yは|0⟩をi|1⟩に、|1⟩を-i|0⟩に写します。","Y = [[0,-i],[i,0]] = σy; Y軸周りπ回転。"]),
            "Z":      ("パウリZ",                 ["|0⟩はそのままで|1⟩の位相を変えます。","Z|0⟩=|0⟩、Z|1⟩=-|1⟩。","Z=diag(1,-1)=σz。位相反転演算子。"]),
            "S":      ("S位相ゲート",             ["状態の|1⟩成分に位相の1/4回転を加えます。","S=diag(1,i)、π/2位相回転；S²=Z。","S=T²=diag(1,i)はクリフォードゲート。"]),
            "T":      ("Tゲート",                 ["Sゲートより小さな位相変化を加えます。","T=diag(1,e^(iπ/4))、π/4位相回転。","非クリフォードπ/8ゲート。"]),
            "SX":     ("Xの平方根",               ["X様回転の半分；2回で全体位相を除いてX。","SX²=X（不可観測な全体位相を除く）。","SX=(I-iX)/√2；IBMシステムのネイティブゲート。"]),
            "RX":     ("X軸回転",                 ["指定角度でX軸周りに回転します。","RX(θ)はブロッホベクトルをθ回転します。","RX(θ)=exp(-iθX/2)；VQE・QAOAに使用。"]),
            "RY":     ("Y軸回転",                 ["指定角度でY軸周りに回転します。","RY(θ)はY軸周りに回転；実数行列。","RY(θ)=exp(-iθY/2)；RZと組み合わせてオイラー分解。"]),
            "RZ":     ("Z軸回転",                 ["Z軸周りの回転で相対位相を変えます。","RZ(θ)は反対の位相因子を適用。","RZ(θ)=diag(e^{-iθ/2},e^{iθ/2})；仮想実装可能。"]),
            "P":      ("位相ゲート",              ["選択した位相を|1⟩成分に加えます。","P(θ)=diag(1,e^{iθ})；SとTは特定角度。","U(1)位相操作；勾配法で最適化可能。"]),
            "CX":     ("CNOT / 制御X",            ["制御=1なら標的を反転。もつれを作れます。","CXは|c,t⟩を|c,t XOR c⟩に写します。","CX=|0⟩⟨0|⊗I+|1⟩⟨1|⊗X；万能もつれゲート。"]),
            "CZ":     ("CZ / 制御Z",              ["|11⟩成分のみ位相を反転；対称。","制御が|1⟩のとき標的にZを適用。","CZ=diag(1,1,1,-1)；グローバー探索のオラクル。"]),
            "SWAP":   ("SWAP交換",                ["2つの量子ビットの状態を交換します。","SWAP|a,b⟩=|b,a⟩；3つのCXに分解。","SWAP=(I⊗I+X⊗X+Y⊗Y+Z⊗Z)/2。"]),
            "CCX":    ("Toffoli",                 ["両方の制御が1のとき標的を反転。","CCX：可逆AND演算。","可逆三量子ビットゲート。"]),
            "CSWAP":  ("Fredkin / CSWAP",         ["制御が1のとき2つの標的を交換。","CSWAP：条件付き交換。","制御置換ゲート。"]),
            "Measure":("測定",                    ["確率的に0または1を読み取ります。","α|0⟩+β|1⟩：0は|α|²、1は|β|²。","ボルン則に従う非ユニタリ投影。"]),
            "Reset":  ("リセット",                ["量子ビットを|0⟩に戻します。","非ユニタリで|0⟩に準備。","量子チャネル；測定と条件付き補正。"]),
            "Barrier":("バリア",                  ["回路の区切りを示します。","コンパイラ指示；物理操作ではない。","トランスパイラ最適化を制限。"]),
            "If":     ("古典条件",                ["測定結果に応じて操作を選びます。","古典フィードフォワード。","動的回路；適応測定と補正。"]),
            "For":    ("ループ",                  ["操作を繰り返します。","反復アルゴリズム向け。","パラメータ付き回路族。"]),
            "Unitary":("ユニタリ操作",            ["有効な確率を保つカスタム操作。","U†U=I；可逆操作。","2ⁿ×2ⁿ行列；基底ゲートへ分解。"]),
        },
    },
    "中文": {
        "categories": ["单量子比特门","旋转门","多量子比特门","电路操作","经典控制"],
        "levels": ["入门级：","中学级：","大学级："],
        "gates": {
            "H":      ("阿达马门",    ["作用于|0⟩时创建等幅叠加。","H|0⟩=(|0⟩+|1⟩)/√2。","H = 1/√2 [[1,1],[1,-1]]。酉且厄米（H²=I）。"]),
            "X":      ("泡利X / 非门",["像开关一样交换|0⟩和|1⟩。","交换计算基态；类似经典非门。","X = [[0,1],[1,0]] = σx；绕X轴旋转π。"]),
            "Y":      ("泡利Y",       ["翻转量子比特并改变相位。","Y将|0⟩映射为i|1⟩，|1⟩映射为-i|0⟩。","Y = [[0,-i],[i,0]] = σy；绕Y轴旋转π。"]),
            "Z":      ("泡利Z",       ["保持|0⟩不变并改变|1⟩的相位。","Z|0⟩=|0⟩且Z|1⟩=-|1⟩。","Z=diag(1,-1)=σz。相位翻转算符。"]),
            "S":      ("S相位门",     ["给|1⟩分量增加四分之一圈相位。","S=diag(1,i)，π/2相位旋转；S²=Z。","S=T²=diag(1,i)是Clifford门。"]),
            "T":      ("T门",         ["带来比S门更小的相位变化。","T=diag(1,e^(iπ/4))，π/4相位旋转。","非Clifford的π/8门。"]),
            "SX":     ("X的平方根门", ["类X旋转的一半；两次等于X。","SX²=X（相差全局相位）。","SX=(I-iX)/√2；IBM系统原生门。"]),
            "RX":     ("绕X轴旋转",   ["按指定角度绕X轴旋转。","RX(θ)使布洛赫向量绕X旋转θ。","RX(θ)=exp(-iθX/2)；用于VQE和QAOA。"]),
            "RY":     ("绕Y轴旋转",   ["按指定角度绕Y轴旋转。","RY(θ)绕Y旋转；实数矩阵元素。","RY(θ)=exp(-iθY/2)；与RZ组合实现欧拉分解。"]),
            "RZ":     ("绕Z轴旋转",   ["通过绕Z旋转改变相对相位。","RZ(θ)对|0⟩和|1⟩施加相反相位因子。","RZ(θ)=diag(e^{-iθ/2},e^{iθ/2})；可虚拟实现。"]),
            "P":      ("相位门",      ["给|1⟩分量添加可选相位。","P(θ)=diag(1,e^{iθ})；S和T是特例。","U(1)相位操作；可用梯度法优化。"]),
            "CX":     ("CNOT / 受控X门",["控制=1时翻转目标。可纠缠量子比特。","CX将|c,t⟩映射为|c,t XOR c⟩。","CX=|0⟩⟨0|⊗I+|1⟩⟨1|⊗X；通用纠缠门。"]),
            "CZ":     ("CZ / 受控Z门",["仅翻转|11⟩分量的相位；对称。","控制为|1⟩时对目标应用Z。","CZ=diag(1,1,1,-1)；Grover搜索的预言机。"]),
            "SWAP":   ("交换门",      ["交换两量子比特状态。","SWAP|a,b⟩=|b,a⟩；分解为三个CX。","SWAP=(I⊗I+X⊗X+Y⊗Y+Z⊗Z)/2。"]),
            "CCX":    ("Toffoli门",   ["两控制均为1时翻转目标。","CCX：可逆AND操作。","三量子比特可逆门。"]),
            "CSWAP":  ("Fredkin门",   ["控制为1时交换两目标。","CSWAP：条件交换。","受控置换门。"]),
            "Measure":("测量",        ["概率性读取0或1。","α|0⟩+β|1⟩：0概率|α|²，1概率|β|²。","遵循玻恩规则的非酉投影。"]),
            "Reset":  ("重置",        ["将量子比特恢复到|0⟩。","制备|0⟩的非酉操作。","量子信道；测量加条件校正。"]),
            "Barrier":("屏障",        ["标记电路边界。","编译器指令；非物理操作。","限制跨边界的转译优化。"]),
            "If":     ("经典条件",    ["根据测量结果选择操作。","经典前馈；条件应用量子门。","动态电路；自适应测量与纠错。"]),
            "For":    ("循环",        ["重复一组操作。","用于迭代算法。","参数化电路族。"]),
            "Unitary":("酉操作",      ["保持概率的自定义操作。","U†U=I；可逆量子操作。","2ⁿ×2ⁿ矩阵；分解为基门。"]),
        },
    },
    "हिन्दी": {
        "categories": ["एकल-क्यूबिट गेट","घूर्णन गेट","बहु-क्यूबिट गेट","सर्किट क्रियाएँ","क्लासिकल नियंत्रण"],
        "levels": ["शुरुआती स्तर: ","माध्यमिक स्तर: ","विश्वविद्यालय स्तर: "],
        "gates": {
            "H":      ("हैडामार्ड गेट",    ["|0⟩ पर लगाने से बराबर सुपरपोज़िशन बनता है।","H|0⟩=(|0⟩+|1⟩)/√2।","H = 1/√2 [[1,1],[1,-1]]। यूनिटरी और हर्मिटियन (H²=I)।"]),
            "X":      ("पाउली-X / NOT",    ["स्विच की तरह |0⟩ और |1⟩ बदलता है।","कम्प्यूटेशनल आधार बदलता है; NOT जैसा।","X = [[0,1],[1,0]] = σx; X-अक्ष पर π घूर्णन।"]),
            "Y":      ("पाउली-Y",          ["क्यूबिट पलटता है और फेज़ भी बदलता है।","Y, |0⟩ को i|1⟩ और |1⟩ को -i|0⟩ में बदलता है।","Y = [[0,-i],[i,0]] = σy; Y-अक्ष पर π घूर्णन।"]),
            "Z":      ("पाउली-Z",          ["|0⟩ वैसा ही रहता है; |1⟩ का फेज़ बदलता है।","Z|0⟩=|0⟩, Z|1⟩=-|1⟩।","Z=diag(1,-1)=σz। फेज़-फ्लिप ऑपरेटर।"]),
            "S":      ("S फेज़ गेट",       ["|1⟩ भाग में 1/4 चक्र फेज़ जोड़ता है।","S=diag(1,i); π/2 फेज़ घूर्णन; S²=Z।","S=T²=diag(1,i) Clifford गेट है।"]),
            "T":      ("T गेट",            ["S से छोटा फेज़ परिवर्तन।","T=diag(1,e^(iπ/4)); π/4 फेज़ घूर्णन।","Non-Clifford π/8 गेट।"]),
            "SX":     ("X का वर्गमूल",     ["X जैसा आधा घूर्णन; दो बार = X।","SX²=X (वैश्विक फेज़ को छोड़कर)।","SX=(I-iX)/√2; IBM नेटिव गेट।"]),
            "RX":     ("X-अक्ष घूर्णन",   ["चुने गए कोण से X-अक्ष पर घुमाता है।","RX(θ) ब्लॉख वेक्टर को θ घुमाता है।","RX(θ)=exp(-iθX/2); VQE और QAOA में उपयोग।"]),
            "RY":     ("Y-अक्ष घूर्णन",   ["Y-अक्ष पर घुमाता है।","RY(θ) Y के चारों ओर घूमता है; वास्तविक मैट्रिक्स।","RY(θ)=exp(-iθY/2); Euler विघटन।"]),
            "RZ":     ("Z-अक्ष घूर्णन",   ["Z-अक्ष के चारों ओर सापेक्ष फेज़ बदलता है।","RZ(θ) |0⟩ और |1⟩ पर विपरीत फेज़ लगाता है।","RZ(θ)=diag(e^{-iθ/2},e^{iθ/2}); वर्चुअल लागू।"]),
            "P":      ("फेज़ गेट",         ["|1⟩ भाग में चुना हुआ फेज़ जोड़ता है।","P(θ)=diag(1,e^{iθ}); S और T विशेष कोण।","U(1) फेज़ ऑपरेशन।"]),
            "CX":     ("CNOT / नियंत्रित-X",["Control=1 तो target पलटता है।","CX, |c,t⟩ को |c,t XOR c⟩ में बदलता है।","CX=|0⟩⟨0|⊗I+|1⟩⟨1|⊗X; सार्वभौमिक entangling गेट।"]),
            "CZ":     ("CZ / नियंत्रित-Z", ["केवल |11⟩ घटक का फेज़ पलटता है; सममित।","Control |1⟩ होने पर Z गेट target पर लागू।","CZ=diag(1,1,1,-1); Grover search में oracle।"]),
            "SWAP":   ("SWAP अदला-बदली",   ["दो क्यूबिट की अवस्थाएँ बदलता है।","SWAP|a,b⟩=|b,a⟩; तीन CX में विघटित।","SWAP=(I⊗I+X⊗X+Y⊗Y+Z⊗Z)/2।"]),
            "CCX":    ("Toffoli",          ["दोनों control=1 तो target पलटता है।","CCX: reversible AND।","तीन-क्यूबिट reversible गेट।"]),
            "CSWAP":  ("Fredkin / CSWAP",  ["Control=1 तो दो target बदलता है।","CSWAP: शर्त-सहित अदला-बदली।","नियंत्रित permutation गेट।"]),
            "Measure":("मापन",             ["संभाव्य रूप से 0 या 1 पढ़ता है।","Born rule: 0 की संभावना |α|², 1 की |β|²।","Non-unitary computational-basis projection।"]),
            "Reset":  ("रीसेट",            ["क्यूबिट को |0⟩ में वापस लाता है।","|0⟩ में non-unitary तैयारी।","Quantum channel; measurement + correction।"]),
            "Barrier":("बैरियर",           ["सर्किट के हिस्सों के बीच निशान।","Compiler directive; भौतिक operation नहीं।","Transpiler optimization सीमित।"]),
            "If":     ("क्लासिकल शर्त",   ["मापन परिणाम के आधार पर operation चुनता है।","Classical feed-forward।","Dynamic circuits।"]),
            "For":    ("लूप",              ["Operations का समूह दोहराता है।","Iterative algorithms।","Parameterized circuit families।"]),
            "Unitary":("यूनिटरी ऑपरेशन", ["Valid संभावनाएँ बनाए रखता है।","U†U=I; reversible।","2ⁿ×2ⁿ matrix; basis gates में विघटन।"]),
        },
    },
    "Português": {
        "categories": ["PORTAS DE UM ÚNICO QUBIT","PORTAS DE ROTAÇÃO",
                        "PORTAS DE MÚLTIPLOS QUBITS","OPERAÇÕES DO CIRCUITO","CONTROLE CLÁSSICO"],
        "levels": ["Nível iniciante: ","Nível do ensino médio: ","Nível universitário: "],
        "gates": {
            "H":      ("Porta Hadamard",     ["Cria mistura equilibrada de |0⟩ e |1⟩ aplicada a |0⟩.","H|0⟩=(|0⟩+|1⟩)/√2. Superposição igual.","H = 1/√2 [[1,1],[1,-1]]. Unitária e hermitiana (H²=I)."]),
            "X":      ("Pauli-X / NÃO",      ["Troca |0⟩ e |1⟩ como interruptor.","Troca estados de base; age como NÃO clássico.","X = [[0,1],[1,0]] = σx; rotação de π em torno de X."]),
            "Y":      ("Pauli-Y",            ["Inverte qubit e altera fase.","Y transforma |0⟩ em i|1⟩ e |1⟩ em -i|0⟩.","Y = [[0,-i],[i,0]] = σy; rotação de π em torno de Y."]),
            "Z":      ("Pauli-Z",            ["Mantém |0⟩ e muda fase de |1⟩.","Z|0⟩=|0⟩ e Z|1⟩=-|1⟩.","Z=diag(1,-1)=σz. Inversão de fase."]),
            "S":      ("Porta de fase S",    ["Adiciona quarto de volta de fase a |1⟩.","S=diag(1,i); rotação de fase π/2; S²=Z.","S=T²=diag(1,i) é porta Clifford."]),
            "T":      ("Porta T",            ["Adiciona mudança de fase menor que S.","T=diag(1,e^(iπ/4)); rotação de fase π/4.","T é porta π/8 não-Clifford."]),
            "SX":     ("Raiz quadrada de X", ["Metade de rotação X; duas vezes = X.","SX²=X exceto fase global.","SX=(I-iX)/√2; portas nativas em IBM."]),
            "RX":     ("Rotação em torno de X",["Gira qubit em torno de X.","RX(θ) gira vetor de Bloch por θ.","RX(θ)=exp(-iθX/2); usado em VQE e QAOA."]),
            "RY":     ("Rotação em torno de Y",["Gira qubit em torno de Y.","RY(θ) tem entradas reais.","RY(θ)=exp(-iθY/2); decomposições de Euler com RZ."]),
            "RZ":     ("Rotação em torno de Z",["Muda fase relativa por rotação em Z.","RZ(θ) aplica fatores de fase opostos.","RZ(θ)=diag(e^{-iθ/2},e^{iθ/2}); virtual em hardware."]),
            "P":      ("Porta de fase",      ["Adiciona fase escolhida a |1⟩.","P(θ)=diag(1,e^{iθ}); S e T são casos especiais.","Operação de fase U(1)."]),
            "CX":     ("CNOT / X controlado",["Controle=1: inverte alvo. Pode entrelaçar.","CX transforma |c,t⟩ em |c,t XOR c⟩.","CX=|0⟩⟨0|⊗I+|1⟩⟨1|⊗X; porta entrelaçante universal."]),
            "CZ":     ("CZ / Z controlado",  ["Inverte fase de |11⟩ apenas; simétrico.","CZ aplica Z ao alvo quando controle é |1⟩.","CZ=diag(1,1,1,-1); porta Clifford, oráculo de Grover."]),
            "SWAP":   ("Troca SWAP",         ["Troca estados de dois qubits.","SWAP|a,b⟩=|b,a⟩; três CX.","SWAP=(I⊗I+X⊗X+Y⊗Y+Z⊗Z)/2."]),
            "CCX":    ("Toffoli",            ["Inverte alvo se ambos controles = 1.","CCX: AND reversível.","Porta reversível de três qubits."]),
            "CSWAP":  ("Fredkin / CSWAP",    ["Troca dois alvos se controle = 1.","CSWAP: troca condicional.","Porta de permutação controlada."]),
            "Measure":("Medição",            ["Lê qubit como 0 ou 1; probabilístico.","Para α|0⟩+β|1⟩: 0 com |α|², 1 com |β|².","Medição não unitária; segue regra de Born."]),
            "Reset":  ("Reinicialização",    ["Retorna qubit a |0⟩.","Operação não unitária para preparar |0⟩.","Canal quântico; medição e correção condicional."]),
            "Barrier":("Barreira",           ["Separa partes do circuito.","Diretiva do compilador; não é operação física.","Restringe otimizações do transpiler."]),
            "If":     ("Condição clássica",  ["Escolhe operação por resultado de medição.","Feed-forward clássico.","Circuitos dinâmicos; medição adaptativa."]),
            "For":    ("Circuito repetido",  ["Repete grupo de operações.","Algoritmos iterativos.","Famílias de circuitos parametrizados."]),
            "Unitary":("Operação unitária",  ["Preserva probabilidades do estado.","U†U=I; reversível.","Matriz 2ⁿ×2ⁿ; síntese em portas de base."]),
        },
    },
}

# Arabic content is intentionally limited to the initial prototype scope.
OPERATOR_LOCALIZATIONS["العربية"] = {
    "categories": ["بوابات كيوبت واحد", "بوابات الدوران", "بوابات متعددة الكيوبتات",
                   "عمليات الدائرة", "التحكم الكلاسيكي"],
    "levels": ["مبتدئ تمامًا: ", "مستوى المدرسة الثانوية: ", "مستوى جامعي: "],
    "gates": {
        "H": ("بوابة هادامارد", [ARABIC_BEGINNER_GATES["H"][1], "تحوّل |0⟩ إلى (|0⟩+|1⟩)/√2 وتنشئ تراكبًا متساويًا.", "H=1/√2[[1,1],[1,−1]]. بوابة وحدوية وهرميتية، حيث H²=I، وتبدّل قاعدتي قياس X وZ."]),
        "X": ("بوابة باولي X / NOT", [ARABIC_BEGINNER_GATES["X"][1], "تبدّل حالتي الأساس |0⟩ و|1⟩.", "X=[[0,1],[1,0]]=σx؛ دوران بزاوية π حول محور X، حتى طور كلي غير قابل للرصد."]),
        "Y": ("بوابة باولي Y", [ARABIC_BEGINNER_GATES["Y"][1], "تحوّل |0⟩ إلى i|1⟩ و|1⟩ إلى −i|0⟩.", "Y=[[0,−i],[i,0]]=σy؛ دوران بزاوية π حول محور Y، حتى طور كلي."]),
        "Z": ("بوابة باولي Z", [ARABIC_BEGINNER_GATES["Z"][1], "تترك |0⟩ كما هي وتحول |1⟩ إلى −|1⟩؛ يتغير الطور النسبي.", "Z=diag(1,−1)=σz؛ مولّد دورانات محور Z وبوابة قلب طور."]),
        "S": ("بوابة الطور S", [ARABIC_BEGINNER_GATES["S"][1], "S=diag(1,i)، وتطبيقها مرتين يعطي Z.", "بوابة Clifford بزاوية طور π/2؛ تبدّل X إلى Y بالإقتران وتبقي Z ثابتة."]),
        "T": ("بوابة T", [ARABIC_BEGINNER_GATES["T"][1], "T=diag(1,e^(iπ/4)) وتضيف طورًا مقداره π/4.", "بوابة غير Clifford؛ مع بوابات Clifford تتيح مجموعة عمليات عامة للحوسبة الكمية."]),
        "SX": ("الجذر التربيعي لـX", [ARABIC_BEGINNER_GATES["SX"][1], "تطبيق SX مرتين يكافئ X حتى طور كلي.", "SX=(I−iX)/√2؛ بوابة أساسية في بعض عتاد الحوسبة الكمية."]),
        "RX": ("دوران حول X", [ARABIC_BEGINNER_GATES["RX"][1], "RX(θ) يدير متجه الحالة بزاوية θ حول X.", "RX(θ)=exp(−iθX/2)؛ دوران مولّد بمصفوفة باولي X."]),
        "RY": ("دوران حول Y", [ARABIC_BEGINNER_GATES["RY"][1], "RY(θ) يدير متجه الحالة بزاوية θ حول Y.", "RY(θ)=exp(−iθY/2)؛ مع RZ يتيح تمثيل الدورانات العامة لكيبوت واحد."]),
        "RZ": ("دوران حول Z", [ARABIC_BEGINNER_GATES["RZ"][1], "RZ(θ) يضيف عاملَي طور متعاكسين إلى |0⟩ و|1⟩.", "RZ(θ)=diag(e^(−iθ/2),e^(iθ/2))؛ ويمكن تنفيذه كتغيير طور افتراضي في بعض العتاد."]),
        "P": ("بوابة الطور P", [ARABIC_BEGINNER_GATES["P"][1], "P(θ)=diag(1,e^(iθ))؛ وتمثل S وT زوايا خاصة.", "تحوّل طور U(1)؛ وتظهر في خوارزميات التحسين الكمي."]),
        "CX": ("بوابة X المتحكَّم بها / CNOT", [ARABIC_BEGINNER_GATES["CX"][1], "تحوّل |c,t⟩ إلى |c,t XOR c⟩، ويمكنها إنشاء التشابك.", "CX=|0⟩⟨0|⊗I+|1⟩⟨1|⊗X؛ بوابة متشابكة، وهي مع بوابات كيوبت واحد تكوّن مجموعة عامة."]),
        "CZ": ("بوابة Z المتحكَّم بها", [ARABIC_BEGINNER_GATES["CZ"][1], "تغيّر إشارة مركبة |11⟩ فقط؛ وهي متناظرة بين الكيوبتين.", "CZ=diag(1,1,1,−1)؛ بوابة Clifford متشابكة وتُستخدم في خوارزمية غروفر."]),
        "SWAP": ("بوابة التبادل", [ARABIC_BEGINNER_GATES["SWAP"][1], "SWAP|a,b⟩=|b,a⟩؛ ويمكن تركيبها من ثلاث بوابات CX.", "SWAP=(I⊗I+X⊗X+Y⊗Y+Z⊗Z)/2؛ قد تزيد كلفة التوجيه في العتاد محدود الاتصال."]),
        "CCX": ("بوابة توفولي CCX", [ARABIC_BEGINNER_GATES["CCX"][1], "تنفّذ AND قابلًا للعكس على حالتي الأساس.", "بوابة قابلة للعكس بثلاثة كيوبتات؛ يتطلب تركيبها عدة بوابات أحادية وثنائية."]),
        "CSWAP": ("بوابة فريدكين CSWAP", [ARABIC_BEGINNER_GATES["CSWAP"][1], "تبادل مشروط يحافظ على عدد الواحدات في زوج الهدف.", "بوابة تبديل مضبوطة؛ تُستخدم في اختبار SWAP لمقارنة الحالات."]),
        "Measure": ("القياس", [ARABIC_BEGINNER_GATES["Measure"][1], "إذا كانت الحالة α|0⟩+β|1⟩، فاحتمالا النتيجتين هما |α|² و|β|².", "قياس في القاعدة الحسابية وفق قاعدة بورن؛ عملية غير وحدوية تسجل النتيجة في بت كلاسيكي."]),
        "Reset": ("إعادة الضبط", [ARABIC_BEGINNER_GATES["Reset"][1], "عملية غير وحدوية تهيّئ الكيوبت إلى |0⟩.", "قناة كمية؛ قد تنفّذ بالقياس ثم تصحيح مشروط أو عبر الاسترخاء."]),
        "Barrier": ("الحاجز", [ARABIC_BEGINNER_GATES["Barrier"][1], "توجيه للمترجم يفصل مقاطع الدائرة، وليس عملية فيزيائية.", "يقيّد تحسينات المترجم وإعادة ترتيب البوابات عبر حدود المقطع."]),
        "If": ("شرط كلاسيكي", [ARABIC_BEGINNER_GATES["If"][1], "تطبيق بوابة اعتمادًا على نتيجة قياس سابقة.", "تحكم كلاسيكي لاحق للقياس؛ أساس الدوائر الديناميكية والتصحيح التكيفي."]),
        "For": ("حلقة تكرار", [ARABIC_BEGINNER_GATES["For"][1], "تكرّر مجموعة عمليات، مثل تكرار خطوات خوارزمية.", "بنية تحكم تصف عائلة من الدوائر؛ يعتمد فكّها على واجهة التنفيذ."]),
        "Unitary": ("عملية وحدوية", [ARABIC_BEGINNER_GATES["Unitary"][1], "تحوّل الحالة مع الحفاظ على مجموع الاحتمالات عند 100%.", "مصفوفة U تحقق U†U=I وتمثل عملية عكسية تحافظ على معيار الحالة."]),
    },
}
OPERATOR_LOCALIZATIONS = {
    language: OPERATOR_LOCALIZATIONS[language]
    for language in LANGUAGES if language in OPERATOR_LOCALIZATIONS
}


# ─────────────────────────────────────────────
# CIRCUITS
# ─────────────────────────────────────────────
CIRCUITS = {
    "The Bell State Circuit (Entanglement)": {
        "description": "A two-qubit entangled state. Apply H to qubit 0, then CX with qubit 0 as control and qubit 1 as target. The ideal state is (|00⟩ + |11⟩)/√2.",
        "steps": "1. Start in |00⟩\n2. H on qubit 0\n3. CX(0 → 1)\n4. Measure both qubits.",
    },
    "Three-Qubit GHZ State Circuit": {
        "description": "A three-qubit entangled state. Apply H to qubit 0, then CX from qubit 0 to qubits 1 and 2. The ideal state is (|000⟩ + |111⟩)/√2.",
        "steps": "1. Start in |000⟩\n2. H on qubit 0\n3. CX(0 → 1)\n4. CX(0 → 2)\n5. Measure all qubits.",
    },
    "Two-Qubit Grover Search Circuit": {
        "description": "A 2-qubit quantum search (N=4 states) targeting |11⟩. The oracle (CZ gate) marks |11⟩ with a phase flip. The Grover diffusion operator amplifies |11⟩ to probability 1 in a single iteration.",
        "steps": "1. Start in |00⟩\n2. H⊗H: equal superposition of all 4 states\n3. CZ oracle: phase-flip |11⟩\n4. H⊗H → X⊗X → CZ → X⊗X → H⊗H: diffusion operator\n5. Measure: expect |11⟩ with probability 1",
    },
}

# Keep the canonical names as the single source of truth for circuit dispatch.
BELL_CIRCUIT, GHZ_CIRCUIT, GROVER_CIRCUIT = CIRCUITS


# ─────────────────────────────────────────────
# CIRCUIT LOCALIZATIONS
# ─────────────────────────────────────────────
CIRCUIT_LOCALIZATIONS = {
    "Español": {
        "The Bell State Circuit (Entanglement)": {
            "title": "Circuito del estado de Bell (entrelazamiento)",
            "description": "Un estado entrelazado de dos qubits. Aplica H al qubit 0 y después CX. El estado ideal es (|00⟩ + |11⟩)/√2.",
            "steps": "1. Comienza en |00⟩\n2. Aplica H al qubit 0\n3. Aplica CX (0 → 1)\n4. Mide ambos qubits.",
        },
        "Three-Qubit GHZ State Circuit": {
            "title": "Circuito del estado GHZ de tres qubits",
            "description": "Un estado entrelazado de tres qubits. El estado ideal es (|000⟩ + |111⟩)/√2.",
            "steps": "1. Comienza en |000⟩\n2. Aplica H al qubit 0\n3. Aplica CX (0 → 1)\n4. Aplica CX (0 → 2)\n5. Mide todos los qubits.",
        },
        "Two-Qubit Grover Search Circuit": {
            "title": "Circuito de búsqueda de Grover de dos qubits",
            "description": "Algoritmo de búsqueda cuántica para 2 qubits (4 estados) con objetivo |11⟩. El oráculo CZ marca |11⟩ con cambio de fase. El operador de difusión amplifica |11⟩ a probabilidad 1 en una sola iteración.",
            "steps": "1. Comienza en |00⟩\n2. H⊗H: superposición igual\n3. Oráculo CZ: invierte fase de |11⟩\n4. H⊗H → X⊗X → CZ → X⊗X → H⊗H: difusión\n5. Mide: |11⟩ con probabilidad 1",
        },
    },
    "Français": {
        "The Bell State Circuit (Entanglement)": {
            "title": "Circuit de l'état de Bell (intrication)",
            "description": "Un état intriqué à deux qubits. L'état idéal est (|00⟩ + |11⟩)/√2.",
            "steps": "1. Commencer dans |00⟩\n2. Appliquer H au qubit 0\n3. Appliquer CX (0 → 1)\n4. Mesurer les deux qubits.",
        },
        "Three-Qubit GHZ State Circuit": {
            "title": "Circuit de l'état GHZ à trois qubits",
            "description": "Un état intriqué à trois qubits. L'état idéal est (|000⟩ + |111⟩)/√2.",
            "steps": "1. Commencer dans |000⟩\n2. Appliquer H au qubit 0\n3. Appliquer CX (0 → 1)\n4. Appliquer CX (0 → 2)\n5. Mesurer tous les qubits.",
        },
        "Two-Qubit Grover Search Circuit": {
            "title": "Circuit de recherche de Grover à deux qubits",
            "description": "Algorithme de recherche quantique pour 2 qubits (4 états) ciblant |11⟩. L'oracle CZ marque |11⟩ avec un déphasage. L'opérateur de diffusion amplifie |11⟩ à probabilité 1 en une itération.",
            "steps": "1. Commencer dans |00⟩\n2. H⊗H : superposition égale\n3. Oracle CZ : inverser la phase de |11⟩\n4. H⊗H → X⊗X → CZ → X⊗X → H⊗H : diffusion\n5. Mesurer : |11⟩ avec probabilité 1",
        },
    },
    "Deutsch": {
        "The Bell State Circuit (Entanglement)": {
            "title": "Bell-Zustands-Schaltkreis (Verschränkung)",
            "description": "Ein verschränkter Zustand aus zwei Qubits. Der ideale Zustand ist (|00⟩ + |11⟩)/√2.",
            "steps": "1. Mit |00⟩ beginnen\n2. H auf Qubit 0\n3. CX (0 → 1)\n4. Beide Qubits messen.",
        },
        "Three-Qubit GHZ State Circuit": {
            "title": "Drei-Qubit-GHZ-Zustands-Schaltkreis",
            "description": "Ein verschränkter Zustand aus drei Qubits. Der ideale Zustand ist (|000⟩ + |111⟩)/√2.",
            "steps": "1. Mit |000⟩ beginnen\n2. H auf Qubit 0\n3. CX (0 → 1)\n4. CX (0 → 2)\n5. Alle Qubits messen.",
        },
        "Two-Qubit Grover Search Circuit": {
            "title": "Zwei-Qubit-Grover-Suchschaltkreis",
            "description": "Quantensuchalgorithmus für 2 Qubits (4 Zustände) mit Zielzustand |11⟩. Das CZ-Orakel markiert |11⟩ mit Phasensprung. Der Diffusionsoperator verstärkt |11⟩ in einer Iteration auf Wahrscheinlichkeit 1.",
            "steps": "1. Mit |00⟩ beginnen\n2. H⊗H: Gleichgewichts-Superposition\n3. CZ-Orakel: Phase von |11⟩ umkehren\n4. H⊗H → X⊗X → CZ → X⊗X → H⊗H: Diffusion\n5. Messen: |11⟩ mit Wahrscheinlichkeit 1",
        },
    },
    "日本語": {
        "The Bell State Circuit (Entanglement)": {
            "title": "ベル状態回路（量子もつれ）",
            "description": "2量子ビットのもつれ状態。理想状態は(|00⟩ + |11⟩)/√2。",
            "steps": "1. |00⟩から開始\n2. 量子ビット0にH\n3. CX（0 → 1）\n4. 両量子ビットを測定。",
        },
        "Three-Qubit GHZ State Circuit": {
            "title": "3量子ビットGHZ状態回路",
            "description": "3量子ビットのもつれ状態。理想状態は(|000⟩ + |111⟩)/√2。",
            "steps": "1. |000⟩から開始\n2. 量子ビット0にH\n3. CX（0 → 1）\n4. CX（0 → 2）\n5. 全量子ビットを測定。",
        },
        "Two-Qubit Grover Search Circuit": {
            "title": "2量子ビットグローバー探索回路",
            "description": "2量子ビット（4状態）の量子探索アルゴリズム、目標状態は|11⟩。CZオラクルが|11⟩に位相反転を施し、拡散演算子が1回の反復で確率1に増幅します。",
            "steps": "1. |00⟩から開始\n2. H⊗H：等しい重ね合わせ\n3. CZオラクル：|11⟩の位相を反転\n4. H⊗H → X⊗X → CZ → X⊗X → H⊗H：拡散\n5. 測定：|11⟩が確率1で得られる",
        },
    },
    "中文": {
        "The Bell State Circuit (Entanglement)": {
            "title": "贝尔态电路（量子纠缠）",
            "description": "两量子比特纠缠态。理想态为(|00⟩ + |11⟩)/√2。",
            "steps": "1. 从|00⟩开始\n2. 对量子比特0应用H\n3. 应用CX（0 → 1）\n4. 测量两个量子比特。",
        },
        "Three-Qubit GHZ State Circuit": {
            "title": "三量子比特GHZ态电路",
            "description": "三量子比特纠缠态。理想态为(|000⟩ + |111⟩)/√2。",
            "steps": "1. 从|000⟩开始\n2. 对量子比特0应用H\n3. 应用CX（0 → 1）\n4. 应用CX（0 → 2）\n5. 测量所有量子比特。",
        },
        "Two-Qubit Grover Search Circuit": {
            "title": "双量子比特Grover搜索电路",
            "description": "针对2量子比特（4个态）、目标态|11⟩的量子搜索算法。CZ预言机用相位翻转标记|11⟩，扩散算符在一次迭代内将其概率放大至1。",
            "steps": "1. 从|00⟩开始\n2. H⊗H：等幅叠加\n3. CZ预言机：翻转|11⟩的相位\n4. H⊗H → X⊗X → CZ → X⊗X → H⊗H：扩散\n5. 测量：期望|11⟩以概率1出现",
        },
    },
    "हिन्दी": {
        "The Bell State Circuit (Entanglement)": {
            "title": "बेल स्टेट सर्किट (क्वांटम उलझाव)",
            "description": "दो क्यूबिट की उलझी हुई अवस्था। आदर्श अवस्था (|00⟩ + |11⟩)/√2 है।",
            "steps": "1. |00⟩ से शुरू\n2. क्यूबिट 0 पर H\n3. CX (0 → 1)\n4. दोनों क्यूबिट का मापन।",
        },
        "Three-Qubit GHZ State Circuit": {
            "title": "तीन-क्यूबिट GHZ स्टेट सर्किट",
            "description": "तीन क्यूबिट की उलझी हुई अवस्था। आदर्श अवस्था (|000⟩ + |111⟩)/√2 है।",
            "steps": "1. |000⟩ से शुरू\n2. क्यूबिट 0 पर H\n3. CX (0 → 1)\n4. CX (0 → 2)\n5. सभी क्यूबिट का मापन।",
        },
        "Two-Qubit Grover Search Circuit": {
            "title": "दो-क्यूबिट ग्रोवर सर्च सर्किट",
            "description": "2 क्यूबिट (4 अवस्थाओं) का क्वांटम खोज एल्गोरिदम, लक्ष्य |11⟩। CZ ओरेकल |11⟩ को फेज़ फ्लिप से चिह्नित करता है। एक पुनरावृत्ति में संभावना 1 तक बढ़ाता है।",
            "steps": "1. |00⟩ से शुरू\n2. H⊗H: समान सुपरपोज़िशन\n3. CZ ओरेकल: |11⟩ का फेज़ पलटें\n4. H⊗H → X⊗X → CZ → X⊗X → H⊗H: डिफ्यूज़न\n5. मापन: |11⟩ की संभावना 1",
        },
    },
    "Português": {
        "The Bell State Circuit (Entanglement)": {
            "title": "Circuito do estado de Bell (entrelaçamento)",
            "description": "Estado entrelaçado de dois qubits. Estado ideal: (|00⟩ + |11⟩)/√2.",
            "steps": "1. Comece em |00⟩\n2. H no qubit 0\n3. CX (0 → 1)\n4. Meça os dois qubits.",
        },
        "Three-Qubit GHZ State Circuit": {
            "title": "Circuito do estado GHZ de três qubits",
            "description": "Estado entrelaçado de três qubits. Estado ideal: (|000⟩ + |111⟩)/√2.",
            "steps": "1. Comece em |000⟩\n2. H no qubit 0\n3. CX (0 → 1)\n4. CX (0 → 2)\n5. Meça todos os qubits.",
        },
        "Two-Qubit Grover Search Circuit": {
            "title": "Circuito de busca de Grover de dois qubits",
            "description": "Algoritmo de busca quântica para 2 qubits (4 estados) com alvo |11⟩. O oráculo CZ marca |11⟩ com inversão de fase. O operador de difusão amplifica |11⟩ para probabilidade 1 em uma iteração.",
            "steps": "1. Comece em |00⟩\n2. H⊗H: superposição igual\n3. Oráculo CZ: inverter fase de |11⟩\n4. H⊗H → X⊗X → CZ → X⊗X → H⊗H: difusão\n5. Medir: |11⟩ com probabilidade 1",
        },
    },
}

CIRCUIT_LOCALIZATIONS["العربية"] = {
    BELL_CIRCUIT: {
        "title": "دائرة حالة بيل (التشابك)",
        "description": "تبدأ الدائرة بكيوبتين في الحالة |00⟩. تنشئ H تراكبًا على الكيوبت الأول، ثم تربط CX الكيوبتين. في الحالة المثالية نحصل على (|00⟩ + |11⟩)/√2.",
        "steps": "1. ابدأ بالحالة |00⟩\n2. طبّق H على الكيوبت 0\n3. طبّق CX من 0 إلى 1\n4. قِس الكيوبتين.",
    },
    GHZ_CIRCUIT: {
        "title": "دائرة حالة GHZ بثلاثة كيوبتات",
        "description": "تربط الدائرة ثلاثة كيوبتات في حالة مشتركة. الحالة المثالية هي (|000⟩ + |111⟩)/√2.",
        "steps": "1. ابدأ بالحالة |000⟩\n2. طبّق H على الكيوبت 0\n3. طبّق CX من 0 إلى 1 ثم من 0 إلى 2\n4. قِس الكيوبتات الثلاثة.",
    },
    GROVER_CIRCUIT: {
        "title": "دائرة بحث غروفر بكيوبتين",
        "description": "تبحث الدائرة بين أربع حالات عن الحالة |11⟩. يميّزها CZ، ثم تزيد خطوة الانتشار احتمال ظهورها إلى 1 في المحاكاة المثالية.",
        "steps": "1. ابدأ بالحالة |00⟩\n2. طبّق H على الكيوبتين لإنشاء تراكب متساوٍ\n3. طبّق CZ لتمييز |11⟩\n4. طبّق خطوة الانتشار\n5. قِس؛ النتيجة المتوقعة |11⟩.",
    },
}
CIRCUIT_LOCALIZATIONS = {
    language: CIRCUIT_LOCALIZATIONS[language]
    for language in LANGUAGES if language in CIRCUIT_LOCALIZATIONS
}

SIMULATION_COPY = {
    "English": {
        "window": "Quantum Theory & Local Simulation",
        "title": "⚛️ Theoretical Expectations & Local Simulation",
        "beginner_window": "Circuit Walkthrough & Local Simulation",
        "beginner_title": "⚛️ What this circuit does",
        "beginner_intro": "Circuit: {name}\nThe explanation below shows what to expect in an ideal simulation. The simulator runs locally on this computer.",
        "intro": "Circuit: {name}\nThe theory below is the ideal noiseless prediction. The simulator runs locally on this computer.",
        "theory_heading": "Gate-by-gate theoretical expectations",
        "grover_heading": "Gate-by-gate theoretical expectations (Grover Search)",
        "initial": "Initial state", "expected": "Expected", "target": "Target state",
        "circuit_heading": "Selected quantum circuit", "shots": "Number of circuit runs:",
        "run": "▶ Run Local Simulation", "show_code": "▶ Show Qiskit Code",
        "hide_code": "▼ Hide Qiskit Code", "close": "✕ Close Application",
        "back": "◀ Back", "placeholder": "Click Run Local Simulation to see sampled measurement counts.",
        "ready": "Status: Ready — simulation stays on this laptop.",
        "diagram_error": "Circuit diagram unavailable. Install matplotlib and Qiskit visualization support.",
        "no_qiskit": "Qiskit is not installed.\n\nInstall with: python -m pip install 'qiskit[visualization]' matplotlib",
        "unavailable": "This circuit is unavailable. Install Qiskit first.",
        "unavailable_status": "Simulation unavailable: install Qiskit first.",
        "result_title": "LOCAL STATEVECTOR SIMULATION — {shots:,} circuit runs",
        "beginner_result_title": "LOCAL CIRCUIT SIMULATION — {shots:,} measurements",
        "amplitudes": "Final state amplitudes:", "outcome": "Outcome", "theory_column": "Theory",
        "count": "Sample count", "observed": "Observed",
        "result_note": "Theory = exact ideal probability; Observed = this run's sampled fraction.",
        "complete": "Simulation complete: {shots:,} circuit runs. No cloud or hardware used.",
        "exact_probabilities": "Exact probabilities:",
        "circuit_label": "Circuit:", "measurement_counts": "Measurement counts",
        "code_comment": "Simulate the ideal circuit locally and sample measurements.",
        "shots_hint": "Choose 100, 1000, or 10000.",
        "theory": {
            "bell": "<h3>Gate-by-gate theoretical expectations</h3><p><b>Initial state:</b> |00⟩.</p><p><b>1. H on qubit 0</b><br>Creates (|00⟩+|10⟩)/√2. Each branch has probability 1/2.</p><p><b>2. CNOT (0→1)</b><br>Final Bell state |Φ⁺⟩ = (|00⟩+|11⟩)/√2.</p><p><b>Expected:</b> P(00)=1/2, P(11)=1/2, P(01)=P(10)=0.</p>",
            "ghz": "<h3>Gate-by-gate theoretical expectations</h3><p><b>Initial state:</b> |000⟩.</p><p><b>1. H on qubit 0</b><br>(|000⟩+|100⟩)/√2.</p><p><b>2. CNOT (0→1)</b><br>(|000⟩+|110⟩)/√2.</p><p><b>3. CNOT (0→2)</b><br>|GHZ⟩ = (|000⟩+|111⟩)/√2.</p><p><b>Expected:</b> P(000)=1/2, P(111)=1/2; all other outcomes 0.</p>",
            "grover": "<h3>Gate-by-gate theoretical expectations (Grover Search)</h3><p><b>Target state:</b> |11⟩. N=4 states, k=1 marked. Optimal iterations = 1.</p><p><b>1. H⊗H</b><br>(|00⟩+|01⟩+|10⟩+|11⟩)/2. Each state has probability 1/4.</p><p><b>2. CZ oracle</b><br>Phase-flips |11⟩; probabilities stay the same.</p><p><b>3. Diffusion</b><br>Reflects amplitudes around their average. The three unmarked states cancel, leaving |11⟩.</p><p><b>Expected:</b> P(11)=1. One iteration is optimal for four states with one target.</p>",
        },
    },
    "Español": {
        "window": "Teoría cuántica y simulación local",
        "title": "⚛️ Predicciones teóricas y simulación local",
        "beginner_window": "Recorrido del circuito y simulación local",
        "beginner_title": "⚛️ Qué hace este circuito",
        "beginner_intro": "Circuito: {name}\nLa explicación muestra qué esperar en una simulación ideal. El simulador se ejecuta en este equipo.",
        "intro": "Circuito: {name}\nLa teoría muestra la predicción ideal, sin ruido. El simulador se ejecuta en este equipo.",
        "theory_heading": "Predicciones teóricas paso a paso",
        "grover_heading": "Predicciones teóricas paso a paso (búsqueda de Grover)",
        "initial": "Estado inicial", "expected": "Resultado esperado", "target": "Estado objetivo",
        "circuit_heading": "Circuito cuántico seleccionado", "shots": "Número de mediciones:",
        "run": "▶ Ejecutar simulación local", "show_code": "▶ Mostrar código Qiskit",
        "hide_code": "▼ Ocultar código Qiskit", "close": "✕ Cerrar aplicación",
        "back": "◀ Atrás", "placeholder": "Ejecuta la simulación local para ver los conteos de mediciones.",
        "ready": "Estado: lista la simulación local en este equipo.",
        "diagram_error": "No se puede mostrar el diagrama. Instala matplotlib y el soporte de visualización de Qiskit.",
        "no_qiskit": "Qiskit no está instalado.\n\nInstálalo con: python -m pip install 'qiskit[visualization]' matplotlib",
        "unavailable": "Este circuito no está disponible. Instala Qiskit primero.",
        "unavailable_status": "Simulación no disponible: instala Qiskit.",
        "result_title": "SIMULACIÓN LOCAL DE VECTOR DE ESTADO — {shots:,} mediciones",
        "beginner_result_title": "SIMULACIÓN LOCAL DEL CIRCUITO — {shots:,} mediciones",
        "amplitudes": "Amplitudes del estado final:", "outcome": "Resultado", "theory_column": "Teoría",
        "count": "Conteo", "observed": "Proporción observada",
        "result_note": "Teoría = probabilidad ideal exacta; proporción observada = fracción obtenida en esta ejecución.",
        "complete": "Simulación completada: {shots:,} mediciones. Sin nube ni hardware.",
        "exact_probabilities": "Probabilidades exactas:",
        "circuit_label": "Circuito:", "measurement_counts": "Conteos de mediciones",
        "code_comment": "Simula el circuito ideal localmente y toma muestras de las mediciones.",
        "shots_hint": "Elige 100, 1000 o 10000.",
        "theory": {
            "bell": "<h3>Predicciones teóricas paso a paso</h3><p><b>Estado inicial:</b> |00⟩.</p><p><b>1. H en el qubit 0</b><br>Crea (|00⟩+|10⟩)/√2. Cada posibilidad tiene probabilidad 1/2.</p><p><b>2. CNOT (0→1)</b><br>Estado de Bell final |Φ⁺⟩ = (|00⟩+|11⟩)/√2.</p><p><b>Resultado esperado:</b> P(00)=1/2, P(11)=1/2, P(01)=P(10)=0.</p>",
            "ghz": "<h3>Predicciones teóricas paso a paso</h3><p><b>Estado inicial:</b> |000⟩.</p><p><b>1. H en el qubit 0</b><br>(|000⟩+|100⟩)/√2.</p><p><b>2. CNOT (0→1)</b><br>(|000⟩+|110⟩)/√2.</p><p><b>3. CNOT (0→2)</b><br>|GHZ⟩ = (|000⟩+|111⟩)/√2.</p><p><b>Resultado esperado:</b> P(000)=1/2, P(111)=1/2; las demás son 0.</p>",
            "grover": "<h3>Predicciones teóricas paso a paso (búsqueda de Grover)</h3><p><b>Estado objetivo:</b> |11⟩. Hay 4 estados y 1 objetivo. El número óptimo de iteraciones es 1.</p><p><b>1. H⊗H</b><br>Crea una superposición uniforme; cada estado tiene probabilidad 1/4.</p><p><b>2. Oráculo CZ</b><br>Cambia la fase de |11⟩, pero no las probabilidades todavía.</p><p><b>3. Difusión</b><br>Refleja las amplitudes respecto a su promedio. Los tres estados no objetivo se cancelan y queda |11⟩.</p><p><b>Resultado esperado:</b> P(11)=1. Una iteración es óptima para cuatro estados y un objetivo.</p>",
        },
    },
    "العربية": {
        "window": "نظرية الكم والمحاكاة المحلية",
        "title": "⚛️ التوقعات النظرية والمحاكاة المحلية",
        "beginner_window": "شرح الدائرة والمحاكاة المحلية",
        "beginner_title": "⚛️ ماذا تفعل هذه الدائرة",
        "beginner_intro": "الدائرة: {name}\nيعرض الشرح النتائج المتوقعة في محاكاة مثالية. تعمل المحاكاة على هذا الجهاز.",
        "intro": "الدائرة: {name}\nتعرض النظرية التوقع المثالي من دون ضوضاء. تعمل المحاكاة على هذا الجهاز.",
        "theory_heading": "التوقعات النظرية خطوة بخطوة",
        "grover_heading": "التوقعات النظرية خطوة بخطوة (بحث غروفر)",
        "initial": "الحالة الابتدائية", "expected": "النتيجة المتوقعة", "target": "الحالة الهدف",
        "circuit_heading": "الدائرة الكمية المحددة", "shots": "عدد مرات القياس:",
        "run": "▶ شغّل المحاكاة المحلية", "show_code": "▶ أظهر كود Qiskit",
        "hide_code": "▼ أخفِ كود Qiskit", "close": "✕ إغلاق التطبيق",
        "back": "◀ رجوع", "placeholder": "شغّل المحاكاة المحلية لعرض عدد مرات ظهور كل نتيجة.",
        "ready": "الحالة: المحاكاة جاهزة وتعمل على هذا الجهاز.",
        "diagram_error": "تعذّر عرض مخطط الدائرة. ثبّت matplotlib ودعم عرض الدوائر في Qiskit.",
        "no_qiskit": "حزمة Qiskit غير مثبتة.\n\nثبّتها بالأمر: python -m pip install 'qiskit[visualization]' matplotlib",
        "unavailable": "هذه الدائرة غير متاحة. ثبّت Qiskit أولًا.",
        "unavailable_status": "المحاكاة غير متاحة: ثبّت Qiskit أولًا.",
        "result_title": "محاكاة محلية لمتجه الحالة — {shots:,} قياسًا",
        "beginner_result_title": "محاكاة محلية للدائرة — {shots:,} قياسًا",
        "amplitudes": "سعات الحالة النهائية:", "outcome": "النتيجة", "theory_column": "النظرية",
        "count": "عدد مرات الظهور", "observed": "النسبة المرصودة",
        "result_note": "النظرية = الاحتمال المثالي الدقيق؛ المرصود = النسبة التي ظهرت في هذه المحاكاة.",
        "complete": "اكتملت المحاكاة: {shots:,} قياسًا. لم تُستخدم سحابة أو أجهزة كمومية.",
        "exact_probabilities": "الاحتمالات الدقيقة:",
        "circuit_label": "الدائرة:", "measurement_counts": "أعداد نتائج القياس",
        "code_comment": "حاكِ الدائرة المثالية محليًا وخذ عينات من نتائج القياس.",
        "shots_hint": "اختر 100 أو 1000 أو 10000.",
        "theory": {
            "bell": "<h3>التوقعات النظرية خطوة بخطوة</h3><p><b>الحالة الابتدائية:</b> |00⟩.</p><p><b>1. البوابة H على الكيوبت 0</b><br>تنشئ الحالة (|00⟩+|10⟩)/√2، واحتمال كل فرع 1/2.</p><p><b>2. بوابة CNOT (من 0 إلى 1)</b><br>الناتج حالة بيل |Φ⁺⟩ = (|00⟩+|11⟩)/√2.</p><p><b>النتيجة المتوقعة:</b> P(00)=1/2 وP(11)=1/2، أما P(01)=P(10)=0.</p>",
            "ghz": "<h3>التوقعات النظرية خطوة بخطوة</h3><p><b>الحالة الابتدائية:</b> |000⟩.</p><p><b>1. البوابة H على الكيوبت 0</b><br>(|000⟩+|100⟩)/√2.</p><p><b>2. بوابة CNOT من 0 إلى 1</b><br>(|000⟩+|110⟩)/√2.</p><p><b>3. بوابة CNOT من 0 إلى 2</b><br>حالة GHZ هي |GHZ⟩ = (|000⟩+|111⟩)/√2.</p><p><b>النتيجة المتوقعة:</b> احتمال |000⟩ يساوي 1/2 واحتمال |111⟩ يساوي 1/2؛ وبقية النتائج احتمالها صفر.</p>",
            "grover": "<h3>التوقعات النظرية خطوة بخطوة (بحث غروفر)</h3><p><b>الحالة الهدف:</b> |11⟩. توجد أربع حالات وهدف واحد؛ وعدد التكرارات الأمثل هو 1.</p><p><b>1. تطبيق H على الكيوبتين</b><br>ينشئ تراكبًا متساويًا، واحتمال كل حالة 1/4.</p><p><b>2. بوابة CZ</b><br>تعكس طور |11⟩، من دون تغيير الاحتمالات بعد.</p><p><b>3. خطوة الانتشار</b><br>تعكس السعات حول متوسطها. تلغي الحالات الثلاث غير المستهدفة بعضها، وتبقى |11⟩.</p><p><b>النتيجة المتوقعة:</b> احتمال |11⟩ يساوي 1. تكرار واحد أمثل لأربع حالات وهدف واحد.</p>",
        },
    },
}

AUDIO_COPY = {
    "English": {
        "off": "🔇 Audio walkthrough: Off", "on": "🔊 Audio walkthrough: On",
        "intro": "Audio walkthrough started. This circuit has {count} operations.",
        "step": "Step {step} of {count}. {gate}, on qubits {qubits}. {description} {parameters}",
        "playground_results": "At measurement, the ideal outcomes are {results} (Qubit 1, then Qubit 0).",
        "complete": "Audio walkthrough complete.",
        "stopped": "Audio walkthrough stopped.",
        "unknown": "This is an operation named {gate}.",
        "no_voice": "Speech audio is unavailable for this language. Enable an English, Spanish, or Arabic system voice.",
        "no_module": "Speech support is not installed with this PySide6 setup.",
        "no_circuit": "There is no circuit available to narrate.",
    },
    "Español": {
        "off": "🔇 Guía de audio: desactivada", "on": "🔊 Guía de audio: activada",
        "intro": "Comienza la guía de audio. Este circuito tiene {count} operaciones.",
        "step": "Paso {step} de {count}. {gate}, en los qubits {qubits}. {description} {parameters}",
        "playground_results": "Al medir, los resultados ideales son {results} (primero qubit 1 y luego qubit 0).",
        "complete": "Terminó la guía de audio.",
        "stopped": "Se detuvo la guía de audio.",
        "unknown": "Esta es una operación llamada {gate}.",
        "no_voice": "No hay voz disponible para este idioma. Activa una voz del sistema en inglés, español o árabe.",
        "no_module": "Esta instalación de PySide6 no incluye la función de voz.",
        "no_circuit": "No hay ningún circuito disponible para narrar.",
    },
    "العربية": {
        "off": "🔇 الشرح الصوتي: متوقف", "on": "🔊 الشرح الصوتي: يعمل",
        "intro": "بدأ الشرح الصوتي. تحتوي هذه الدائرة على {count} عملية.",
        "step": "الخطوة {step} من {count}. {gate} على الكيوبتات {qubits}. {description} {parameters}",
        "playground_results": "عند القياس، النتائج المثالية هي {results} (الكيوبت 1 ثم الكيوبت 0).",
        "complete": "اكتمل الشرح الصوتي.",
        "stopped": "توقف الشرح الصوتي.",
        "unknown": "هذه عملية باسم {gate}.",
        "no_voice": "لا يوجد صوت متاح بهذه اللغة. فعّل صوتًا للنظام بالعربية أو الإسبانية أو الإنجليزية.",
        "no_module": "ميزة النطق غير متاحة في تثبيت PySide6 الحالي.",
        "no_circuit": "لا توجد دائرة متاحة لشرحها صوتيًا.",
    },
}

CRYPTO_COPY = {
    "English": {
        "window": "Quantum Cryptography — BB84 and One-Time Pad",
        "title": "🔐 Polarized-photon key exchange",
        "intro": "Enter a short word. Alice and Bob will use a BB84-style exchange to create a shared key, then demonstrate a one-time pad.",
        "protocol": "For every pulse, Alice chooses a random bit and a random basis: horizontal/vertical or diagonal. Bob independently chooses a basis to measure it. They announce their bases publicly, keep matching rounds, and compare a sample for errors.",
        "note": "Teaching simulation only: pulses are modeled on this computer. Real BB84 needs an authenticated classical channel, error correction, privacy amplification, and a security analysis. Do not use this demo to protect real messages.",
        "input_label": "Word or short phrase:", "input_hint": "Type up to 24 characters",
        "eve": "Add Eve (intercept and resend pulses)", "run": "▶ Run key exchange and encrypt",
        "live_heading": "Live pulse stream",
        "live_note": "The animation loops through up to the first {preview_limit} pulses; the table below shows every pulse sent.",
        "animation_play": "▶ Play animation", "animation_pause": "Ⅱ Pause animation",
        "animation_empty": "Run an exchange to watch the pulses travel from Alice to Bob.",
        "animation_status": "Pulse {index} of {total} • {actor}'s bit {bit} • {basis}",
        "speed_slow": "Slower", "speed_fast": "Faster", "speed_label": "Pulse speed:",
        "alice": "Alice", "bob": "Bob", "eve_label": "Eve",
        "pulse_heading": "Transmitted pulses — each row shows Alice’s polarization",
        "table_privacy_note": "Teaching view: the table reveals Alice's and Bob's private results, including key bits, to explain each round. In real BB84, they reveal only the test sample for comparison and keep key bits private.",
        "result_heading": "Exchange results", "back": "◀ Back",
        "ready": "Enter text and run the local BB84 demonstration.",
        "empty": "Enter a word or short phrase first.",
        "too_long": "This demo supports up to 24 characters (up to 96 UTF-8 bytes). Try a shorter phrase.",
        "columns": ["Pulse", "Alice bit", "Alice basis", "Polarized pulse", "Eve", "Bob basis", "Bob result", "Round"],
        "horizontal": "Horizontal (0°)", "vertical": "Vertical (90°)",
        "diagonal": "Diagonal (+45°)", "antidiagonal": "Diagonal (135°)",
        "rect_basis": "Horizontal / vertical", "diag_basis": "Diagonal",
        "no_eve": "—", "eve_value": "{basis}, result {bit}",
        "discard": "Discard: bases differ", "sample": "Public error check",
        "key": "Kept for shared key", "protocol_abort": "Key exchange aborted",
        "success": "Message: {message}\nMessage length: {bits} bits\nPolarized pulses sent: {pulses}\nMatching measurement bases: {matched}\nPublic error-check sample: {sample} rounds; {errors} errors ({error_rate:.0%})\nShared key bits used once: {key_bits}\nOne-time-pad ciphertext (hex): {ciphertext}\n\nBob decrypted: {recovered}\n\nThe example assumes idealized key reconciliation after the sample check.",
        "abort": "Eavesdropping check found {errors} errors in {sample} publicly compared rounds ({error_rate:.0%}). Alice and Bob abort and do not use a key or decrypt the message.",
        "citation": "Protocol source: <a href='https://doi.org/10.1016/j.tcs.2014.05.025'>Bennett & Brassard, “Quantum cryptography: Public key distribution and coin tossing,” originally published in 1984 and reprinted in Theoretical Computer Science 560 (2014), pp. 7–11</a>.",
    },
    "Español": {
        "window": "Criptografía cuántica — BB84 y cifrado de un solo uso",
        "title": "🔐 Intercambio de claves con fotones polarizados",
        "intro": "Escribe una palabra breve. Alice y Bob usarán un intercambio tipo BB84 para crear una clave compartida y demostrar el cifrado de un solo uso.",
        "protocol": "Para cada pulso, Alice elige un bit y una base al azar: horizontal/vertical o diagonal. Bob elige al azar una base para medirlo. Después anuncian públicamente las bases, conservan las rondas coincidentes y comparan una muestra para buscar errores.",
        "note": "Simulación educativa: los pulsos se modelan en este equipo. El BB84 real requiere un canal clásico autenticado, corrección de errores, amplificación de privacidad y un análisis de seguridad. No uses esta demostración para proteger mensajes reales.",
        "input_label": "Palabra o frase corta:", "input_hint": "Escribe hasta 24 caracteres",
        "eve": "Añadir a Eve (interceptar y reenviar pulsos)", "run": "▶ Intercambiar claves y cifrar",
        "live_heading": "Flujo de pulsos en directo",
        "live_note": "La animación recorre hasta los primeros {preview_limit} pulsos; la tabla muestra todos los pulsos enviados.",
        "animation_play": "▶ Reproducir animación", "animation_pause": "Ⅱ Pausar animación",
        "animation_empty": "Ejecuta un intercambio para ver los pulsos viajar de Alice a Bob.",
        "animation_status": "Pulso {index} de {total} • bit {bit} de {actor} • {basis}",
        "speed_slow": "Más lento", "speed_fast": "Más rápido", "speed_label": "Velocidad del pulso:",
        "alice": "Alice", "bob": "Bob", "eve_label": "Eve",
        "pulse_heading": "Pulsos transmitidos — cada fila muestra la polarización de Alice",
        "table_privacy_note": "Vista educativa: la tabla revela los resultados privados de Alice y Bob, incluidos los bits de la clave, para explicar cada ronda. En el BB84 real solo se revela la muestra de prueba para compararla; los bits de la clave se mantienen en privado.",
        "result_heading": "Resultados del intercambio", "back": "◀ Atrás",
        "ready": "Escribe un texto y ejecuta la demostración local de BB84.",
        "empty": "Escribe primero una palabra o frase corta.",
        "too_long": "La demostración admite hasta 24 caracteres (hasta 96 bytes UTF-8). Prueba una frase más corta.",
        "columns": ["Pulso", "Bit Alice", "Base Alice", "Pulso polarizado", "Eve", "Base Bob", "Resultado Bob", "Ronda"],
        "horizontal": "Horizontal (0°)", "vertical": "Vertical (90°)",
        "diagonal": "Diagonal (+45°)", "antidiagonal": "Diagonal (135°)",
        "rect_basis": "Horizontal / vertical", "diag_basis": "Diagonal",
        "no_eve": "—", "eve_value": "{basis}, resultado {bit}",
        "discard": "Descartar: bases distintas", "sample": "Comprobación pública de errores",
        "key": "Se conserva para la clave compartida", "protocol_abort": "Intercambio de claves cancelado",
        "success": "Mensaje: {message}\nLongitud del mensaje: {bits} bits\nPulsos polarizados enviados: {pulses}\nBases de medición coincidentes: {matched}\nMuestra pública: {sample} rondas; {errors} errores ({error_rate:.0%})\nBits de clave usados una sola vez: {key_bits}\nTexto cifrado con el método de un solo uso (hex): {ciphertext}\n\nMensaje descifrado por Bob: {recovered}\n\nEl ejemplo supone una reconciliación idealizada de la clave después de comprobar la muestra.",
        "abort": "La comprobación detectó {errors} errores en {sample} rondas comparadas públicamente ({error_rate:.0%}). Alice y Bob cancelan el intercambio y no usan una clave ni descifran el mensaje.",
        "citation": "Fuente del protocolo: <a href='https://doi.org/10.1016/j.tcs.2014.05.025'>Bennett y Brassard, “Quantum cryptography: Public key distribution and coin tossing”, publicado originalmente en 1984 y reeditado en Theoretical Computer Science 560 (2014), pp. 7–11</a>.",
    },
    "العربية": {
        "window": "التشفير الكمي — BB84 ودفتر الاستخدام الواحد",
        "title": "🔐 تبادل المفاتيح بفوتونات مستقطبة",
        "intro": "أدخل كلمة قصيرة. سيستخدم أليس وبوب تبادلًا وفق BB84 لإنشاء مفتاح مشترك، ثم يوضحان التشفير بدفتر الاستخدام الواحد.",
        "protocol": "لكل نبضة، يختار أليس بتًا وقاعدة عشوائيًا: أفقي/عمودي أو قطري. ويختار بوب قاعدة عشوائية لقياسها. ثم يعلنان القواعد عبر قناة عامة، ويحتفظان بالجولات المتطابقة، ويقارنان عينة للبحث عن الأخطاء.",
        "note": "محاكاة تعليمية: نمثّل النبضات على هذا الجهاز. يتطلب BB84 الحقيقي قناة كلاسيكية موثّقة، وتصحيح الأخطاء، وتعزيز الخصوصية، وتحليلًا أمنيًا. لا تستخدم هذه التجربة لحماية رسائل حقيقية.",
        "input_label": "كلمة أو عبارة قصيرة:", "input_hint": "اكتب حتى 24 محرفًا",
        "eve": "إضافة إيف (اعتراض النبضات وإعادة إرسالها)", "run": "▶ تبادل المفتاح وتشفير الرسالة",
        "live_heading": "مسار النبضات المباشر",
        "live_note": "تعرض الحركة أول {preview_limit} نبضة كحد أقصى، بينما يعرض الجدول أدناه كل النبضات المرسلة.",
        "animation_play": "▶ تشغيل الحركة", "animation_pause": "Ⅱ إيقاف الحركة مؤقتًا",
        "animation_empty": "شغّل التبادل لمشاهدة انتقال النبضات من أليس إلى بوب.",
        "animation_status": "النبضة {index} من {total} • بت {actor}: {bit} • {basis}",
        "speed_slow": "أبطأ", "speed_fast": "أسرع", "speed_label": "سرعة النبضة:",
        "alice": "أليس", "bob": "بوب", "eve_label": "إيف",
        "pulse_heading": "النبضات المرسلة — يعرض كل صف استقطاب أليس",
        "table_privacy_note": "عرض تعليمي: يكشف الجدول نتيجتي أليس وبوب الخاصتين، بما فيهما بتات المفتاح، لشرح كل جولة. في BB84 الحقيقي يكشفان عينة الفحص فقط للمقارنة، ويحافظان على سرية بتات المفتاح.",
        "result_heading": "نتائج التبادل", "back": "◀ رجوع",
        "ready": "أدخل نصًا ثم شغّل تجربة BB84 المحلية.",
        "empty": "أدخل كلمة أو عبارة قصيرة أولًا.",
        "too_long": "تقبل التجربة حتى 24 محرفًا (حتى 96 بايتًا بترميز UTF-8). جرّب عبارة أقصر.",
        "columns": ["النبضة", "بت أليس", "قاعدة أليس", "نبضة مستقطبة", "إيف", "قاعدة بوب", "نتيجة بوب", "الجولة"],
        "horizontal": "أفقي (0°)", "vertical": "عمودي (90°)",
        "diagonal": "قطري (+45°)", "antidiagonal": "قطري (135°)",
        "rect_basis": "أفقي / عمودي", "diag_basis": "قطري",
        "no_eve": "—", "eve_value": "{basis}، النتيجة {bit}",
        "discard": "تُستبعد: القاعدتان مختلفتان", "sample": "فحص علني للأخطاء",
        "key": "تُحفظ ضمن المفتاح المشترك", "protocol_abort": "أُلغي تبادل المفتاح",
        "success": "الرسالة: {message}\nطول الرسالة: {bits} بتًا\nالنبضات المستقطبة المرسلة: {pulses}\nقواعد القياس المتطابقة: {matched}\nعينة الفحص العلني: {sample} جولة؛ {errors} أخطاء ({error_rate:.0%})\nبتات المفتاح المستخدمة مرة واحدة: {key_bits}\nالنص المشفّر بطريقة الاستخدام الواحد (ست عشري): {ciphertext}\n\nفكّ بوب التشفير: {recovered}\n\nيفترض المثال تسوية مثالية للمفتاح بعد فحص العينة.",
        "abort": "كشف الفحص {errors} أخطاء ضمن {sample} جولة قورنت علنًا ({error_rate:.0%}). يلغي أليس وبوب التبادل ولا يستخدمان مفتاحًا أو يفكان الرسالة.",
        "citation": "مصدر البروتوكول: <a href='https://doi.org/10.1016/j.tcs.2014.05.025'>Bennett وBrassard، “Quantum cryptography: Public key distribution and coin tossing”، نُشر أصلًا عام 1984 وأُعيد نشره في Theoretical Computer Science، المجلد 560 (2014)، الصفحات 7–11</a>.",
    },
}

MAX_CRYPTO_MESSAGE_CHARS = 24
MAX_CRYPTO_MESSAGE_BYTES = 96
MAX_ANIMATED_PULSES = 32

PLAYGROUND_COPY = {
    "English": {
        "window": "Two-Qubit Circuit Playground",
        "title": "🧩 Build a two-qubit circuit",
        "intro": "Drag gates onto either wire. Exact probabilities update as you build. Then run local measurements to compare the sampled results with the prediction.",
        "single_heading": "One-qubit gates",
        "two_heading": "Two-qubit gates",
        "wire_zero": "Qubit 0", "wire_one": "Qubit 1",
        "canvas_accessible": "Two-qubit circuit canvas with draggable gate slots",
        "canvas_empty_accessible": "The circuit is empty.",
        "canvas_gate_accessible": "Time step {step}: {gate} on {wire}.",
        "canvas_both_wires": "both qubits",
        "audio_qubit_join": "and",
        "canvas_hint": "Drop a gate in a column to set its place in the circuit. Click a gate to remove it. The canvas allows up to 20 time steps.",
        "palette_hint": "Click a gate to select it for keyboard-accessible placement, or drag it onto a wire. Rotation gates use a preset angle of π/2. CX uses Qubit 0 as control and Qubit 1 as target. Both qubits are measured at the end.",
        "target_wire": "Place a one-qubit gate on:", "add_gate": "Add selected gate",
        "selected_gate": "Selected: {gate}", "select_gate": "Select a gate from the palette first.",
        "clear": "Clear circuit", "undo": "Undo last gate", "run": "▶ Run local measurements",
        "bell_example": "Load Bell-state example (H → CX)",
        "bell_example_tooltip": "Available when the circuit is empty. Clear current gates to enable it.",
        "bell_example_loaded": "Bell-state example loaded: H then CX creates correlated outcomes.",
        "show_all_gates": "Show all gates", "show_basic_gates": "Show only H, X, and CX",
        "beginner_palette_hint": "Start with H, X, and CX. Select this control to reveal the other gates.",
        "nothing_to_undo": "There are no gates to remove.",
        "back": "◀ Back", "shots": "Number of circuit runs:",
        "result_heading": "Exact prediction and local results",
        "probability_hint": "Exact probability is the ideal chance for an outcome. Observed share is its count divided by the number of runs. More runs usually bring the observed share closer to the prediction.",
        "outcome": "Measurement result", "exact": "Exact probability",
        "count": "Sample count", "observed": "Observed share",
        "ready": "Add gates to see the exact prediction, then run local measurements to compare.",
        "empty": "No gates yet: both qubits start at 0.",
        "local_note": "The built-in simulator runs on this computer with ideal gates and no device noise. No cloud service or quantum hardware is used. Results are listed in Qubit 1, then Qubit 0 order.",
        "added": "Added {gate} to time step {step}.",
        "removed": "Removed {gate}.", "cleared": "Circuit cleared.",
        "full": "The circuit has reached its 20 time-step limit. Remove a gate or clear the circuit.",
        "gate_names": {
            "H": "Hadamard", "X": "Bit flip", "Y": "Y rotation", "Z": "Phase flip",
            "S": "S phase", "T": "T phase", "RX": "X rotation (π/2)",
            "RY": "Y rotation (π/2)", "RZ": "Z rotation (π/2)",
            "CX": "Controlled X", "CZ": "Controlled Z", "SWAP": "Swap qubits",
        },
    },
    "Español": {
        "window": "Zona de circuitos de dos qubits",
        "title": "🧩 Crea un circuito de dos qubits",
        "intro": "Arrastra puertas a cualquiera de las líneas. Las probabilidades exactas se actualizan mientras construyes. Después ejecuta mediciones locales para comparar los resultados con la predicción.",
        "single_heading": "Puertas de un qubit",
        "two_heading": "Puertas de dos qubits",
        "wire_zero": "Qubit 0", "wire_one": "Qubit 1",
        "canvas_accessible": "Lienzo del circuito de dos qubits con espacios para puertas",
        "canvas_empty_accessible": "El circuito está vacío.",
        "canvas_gate_accessible": "Paso {step}: {gate} en {wire}.",
        "canvas_both_wires": "ambos qubits",
        "audio_qubit_join": "y",
        "canvas_hint": "Suelta una puerta en una columna para elegir su posición. Haz clic en una puerta para quitarla. El circuito admite hasta 20 pasos.",
        "palette_hint": "Haz clic en una puerta para seleccionarla y añadirla con el teclado, o arrástrala a una línea. Las rotaciones usan un ángulo fijo de π/2. CX usa el qubit 0 como control y el qubit 1 como objetivo. Ambos qubits se miden al final.",
        "target_wire": "Añadir la puerta de un qubit a:", "add_gate": "Añadir puerta seleccionada",
        "selected_gate": "Seleccionada: {gate}", "select_gate": "Selecciona primero una puerta de la lista.",
        "clear": "Vaciar circuito", "undo": "Deshacer última puerta", "run": "▶ Ejecutar mediciones locales",
        "bell_example": "Cargar ejemplo de estado Bell (H → CX)",
        "bell_example_tooltip": "Disponible cuando el circuito está vacío. Vacía las puertas actuales para activarlo.",
        "bell_example_loaded": "Ejemplo Bell cargado: H y después CX crean resultados correlacionados.",
        "show_all_gates": "Mostrar todas las puertas", "show_basic_gates": "Mostrar solo H, X y CX",
        "beginner_palette_hint": "Empieza con H, X y CX. Pulsa este control para mostrar las demás puertas.",
        "nothing_to_undo": "No hay puertas que quitar.",
        "back": "◀ Atrás", "shots": "Número de mediciones:",
        "result_heading": "Predicción exacta y resultados locales",
        "probability_hint": "La probabilidad exacta es la oportunidad ideal de cada resultado. La proporción observada es su conteo dividido por el número de mediciones. Con más mediciones, suele acercarse a la predicción.",
        "outcome": "Resultado de medición", "exact": "Probabilidad exacta",
        "count": "Conteo", "observed": "Proporción observada",
        "ready": "Añade puertas para ver la predicción exacta y ejecuta mediciones locales para compararla.",
        "empty": "Aún no hay puertas: ambos qubits empiezan en 0.",
        "local_note": "El simulador integrado funciona en este equipo con puertas ideales y sin ruido del dispositivo. No se usa la nube ni hardware cuántico. Los resultados se muestran primero para el qubit 1 y después para el qubit 0.",
        "added": "Se añadió {gate} en el paso {step}.",
        "removed": "Se quitó {gate}.", "cleared": "Se vació el circuito.",
        "full": "El circuito alcanzó el límite de 20 pasos. Quita una puerta o vacía el circuito.",
        "gate_names": {
            "H": "Hadamard", "X": "Cambio de bit", "Y": "Rotación Y", "Z": "Cambio de fase",
            "S": "Fase S", "T": "Fase T", "RX": "Rotación X (π/2)",
            "RY": "Rotación Y (π/2)", "RZ": "Rotación Z (π/2)",
            "CX": "X controlada", "CZ": "Z controlada", "SWAP": "Intercambio de qubits",
        },
    },
    "العربية": {
        "window": "مساحة بناء دائرة بكيوبتين",
        "title": "🧩 ابنِ دائرة بكيوبتين",
        "intro": "اسحب البوابات إلى أي من السلكين. تتحدّث الاحتمالات الدقيقة أثناء البناء. ثم شغّل قياسات محلية لمقارنة النتائج بالتوقع.",
        "single_heading": "بوابات كيوبت واحد",
        "two_heading": "بوابات كيوبتين",
        "wire_zero": "الكيوبت 0", "wire_one": "الكيوبت 1",
        "canvas_accessible": "مساحة دائرة بكيوبتين وخانات لإضافة البوابات بالسحب",
        "canvas_empty_accessible": "الدائرة فارغة.",
        "canvas_gate_accessible": "الخطوة {step}: {gate} على {wire}.",
        "canvas_both_wires": "الكيوبتين معًا",
        "audio_qubit_join": "و",
        "canvas_hint": "أفلِت البوابة في عمود لتحديد موضعها. انقر بوابة لإزالتها. تستوعب الدائرة 20 خطوة كحد أقصى.",
        "palette_hint": "انقر بوابة لتحديدها وإضافتها بلوحة المفاتيح، أو اسحبها إلى سلك. تستخدم بوابات الدوران زاوية ثابتة π/2. تستخدم CX الكيوبت 0 للتحكم وتستهدف الكيوبت 1. يُقاس الكيوبتان في نهاية الدائرة.",
        "target_wire": "أضف بوابة الكيوبت الواحد إلى:", "add_gate": "أضف البوابة المحددة",
        "selected_gate": "المحدد: {gate}", "select_gate": "حدّد بوابة من القائمة أولًا.",
        "clear": "امسح الدائرة", "undo": "تراجع عن آخر بوابة", "run": "▶ شغّل قياسات محلية",
        "bell_example": "حمّل مثال حالة بيل (H ثم CX)",
        "bell_example_tooltip": "يتاح المثال عندما تكون الدائرة فارغة. امسح البوابات الحالية لتفعيله.",
        "bell_example_loaded": "حُمّل مثال بيل: تنشئ H ثم CX نتائج مترابطة.",
        "show_all_gates": "اعرض كل البوابات", "show_basic_gates": "اعرض H وX وCX فقط",
        "beginner_palette_hint": "ابدأ بالبوابات H وX وCX. استخدم هذا الزر لإظهار بقية البوابات.",
        "nothing_to_undo": "لا توجد بوابات لإزالتها.",
        "back": "◀ رجوع", "shots": "عدد القياسات:",
        "result_heading": "التوقع الدقيق والنتائج المحلية",
        "probability_hint": "الاحتمال الدقيق هو فرصة النتيجة في الحالة المثالية. النسبة المرصودة هي عدد ظهورها مقسومًا على عدد القياسات. غالبًا ما تقترب النسبة من التوقع عند زيادة القياسات.",
        "outcome": "نتيجة القياس", "exact": "الاحتمال الدقيق",
        "count": "عدد مرات الظهور", "observed": "النسبة المرصودة",
        "ready": "أضف بوابات لعرض التوقع الدقيق، ثم شغّل قياسات محلية للمقارنة.",
        "empty": "لا توجد بوابات بعد؛ يبدأ الكيوبتان عند 0.",
        "local_note": "يعمل المحاكي المدمج على هذا الجهاز ببوابات مثالية ومن دون إضافة ضوضاء الأجهزة. لا تُستخدم خدمة سحابية أو أجهزة كمية. تُعرض النتائج بترتيب الكيوبت 1 ثم الكيوبت 0.",
        "added": "أُضيفت {gate} في الخطوة {step}.",
        "removed": "أُزيلت: {gate}.", "cleared": "مُسحت الدائرة.",
        "full": "بلغت الدائرة حد 20 خطوة. أزل بوابة أو امسح الدائرة.",
        "gate_names": {
            "H": "بوابة هادامارد", "X": "قلب البت", "Y": "دوران Y", "Z": "قلب الطور",
            "S": "طور S", "T": "طور T", "RX": "دوران X (π/2)",
            "RY": "دوران Y (π/2)", "RZ": "دوران Z (π/2)",
            "CX": "بوابة X المتحكَّم بها", "CZ": "بوابة Z المتحكَّم بها", "SWAP": "تبادل الكيوبتين",
        },
    },
}

PLAYGROUND_SINGLE_GATES = ("H", "X", "Y", "Z", "S", "T", "RX", "RY", "RZ")
PLAYGROUND_TWO_QUBIT_GATES = ("CX", "CZ", "SWAP")


def simulate_two_qubit_circuit(slots):
    """Return exact Qubit-1/Qubit-0 probabilities for supported playground gates."""
    # The array index stores Qubit 0 in its low bit and Qubit 1 in its high bit.
    state = [1 + 0j, 0j, 0j, 0j]
    angle = math.pi / 2
    cosine, sine = math.cos(angle / 2), math.sin(angle / 2)
    single_qubit_gates = {
        "H": ((1 / math.sqrt(2), 1 / math.sqrt(2)),
              (1 / math.sqrt(2), -1 / math.sqrt(2))),
        "X": ((0, 1), (1, 0)),
        "Y": ((0, -1j), (1j, 0)),
        "Z": ((1, 0), (0, -1)),
        "S": ((1, 0), (0, 1j)),
        "T": ((1, 0), (0, complex(math.cos(math.pi / 4), math.sin(math.pi / 4)))),
        "RX": ((cosine, -1j * sine), (-1j * sine, cosine)),
        "RY": ((cosine, -sine), (sine, cosine)),
        "RZ": ((complex(math.cos(-angle / 2), math.sin(-angle / 2)), 0),
               (0, complex(math.cos(angle / 2), math.sin(angle / 2)))),
    }

    def apply_single(gate, qubit):
        matrix = single_qubit_gates[gate]
        mask = 1 << qubit
        for index in range(4):
            if index & mask:
                continue
            zero, one = state[index], state[index | mask]
            state[index] = matrix[0][0] * zero + matrix[0][1] * one
            state[index | mask] = matrix[1][0] * zero + matrix[1][1] * one

    for slot in slots:
        if "both" in slot:
            gate = slot["both"]
            if gate == "CX":
                for index in range(4):
                    if (index & 0b01) and not (index & 0b10):
                        partner = index | 2
                        state[index], state[partner] = state[partner], state[index]
            elif gate == "CZ":
                state[3] *= -1
            elif gate == "SWAP":
                state[1], state[2] = state[2], state[1]
            continue
        # Operations on separate wires in the same column commute.
        for qubit in (0, 1):
            gate = slot.get(qubit)
            if gate is not None:
                apply_single(gate, qubit)

    probabilities = {
        format(index, "02b"): abs(amplitude) ** 2
        for index, amplitude in enumerate(state)
    }
    normalization = sum(probabilities.values())
    return {outcome: probability / normalization
            for outcome, probability in probabilities.items()}


# ─────────────────────────────────────────────
# GATE MATRICES
# Tuple: (display_label, prefactor, rows)
# ─────────────────────────────────────────────
GATE_MATRICES = {
    # ── Single-qubit gates (2 × 2) ──
    "H":    ("H",        "1/√2 ×",  [["1",  "1"],
                                      ["1", "−1"]]),
    "X":    ("X",        "",        [["0",  "1"],
                                      ["1",  "0"]]),
    "Y":    ("Y",        "",        [["0", "−i"],
                                      ["i",  "0"]]),
    "Z":    ("Z",        "",        [["1",  "0"],
                                      ["0", "−1"]]),
    "S":    ("S",        "",        [["1",  "0"],
                                      ["0",  "i"]]),
    "T":    ("T",        "",        [["1",     "0"      ],
                                      ["0", "e^(iπ/4)"]]),
    "SX":   ("SX",      "½ ×",     [["1+i", "1−i"],
                                      ["1−i", "1+i"]]),
    # ── Rotation gates (2 × 2, parameterised) ──
    "RX":   ("RX(θ)",   "",        [["cos(θ/2)",    "−i·sin(θ/2)"],
                                      ["−i·sin(θ/2)", "cos(θ/2)"  ]]),
    "RY":   ("RY(θ)",   "",        [["cos(θ/2)",   "−sin(θ/2)"],
                                      ["sin(θ/2)",    "cos(θ/2)" ]]),
    "RZ":   ("RZ(θ)",   "",        [["e^(−iθ/2)", "0"         ],
                                      ["0",          "e^(iθ/2)" ]]),
    "P":    ("P(θ)",    "",        [["1",  "0"     ],
                                      ["0", "e^(iθ)"]]),
    # ── Two-qubit gates (4 × 4) ──
    "CX":   ("CX",      "",        [["1","0","0","0"],
                                      ["0","1","0","0"],
                                      ["0","0","0","1"],
                                      ["0","0","1","0"]]),
    "CZ":   ("CZ",      "",        [["1","0","0", "0"],
                                      ["0","1","0", "0"],
                                      ["0","0","1", "0"],
                                      ["0","0","0","−1"]]),
    "SWAP": ("SWAP",    "",        [["1","0","0","0"],
                                      ["0","0","1","0"],
                                      ["0","1","0","0"],
                                      ["0","0","0","1"]]),
}

# Cache so each matrix image is only rendered once
_MATRIX_CACHE = {}


# ─────────────────────────────────────────────
# MATRIX RENDERING
# Draws each gate's matrix as a proper 2-D visual image using matplotlib.
# ─────────────────────────────────────────────
def render_gate_matrix_image(symbol):
    """Render a gate matrix as a clean 2-D bracketed image (QPixmap or None)."""
    if symbol not in GATE_MATRICES:
        return None
    if symbol in _MATRIX_CACHE:
        return _MATRIX_CACHE[symbol]
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return None

    label, prefactor, rows = GATE_MATRICES[symbol]
    n_rows = len(rows)
    n_cols = max(len(r) for r in rows)

    max_len = max(len(str(e)) for row in rows for e in row)
    cell_w  = max(0.52, min(1.40, max_len * 0.155))
    cell_h  = 0.46 if n_rows <= 2 else 0.38

    bkt_w = 0.18
    lbl_w = max(0.60, len(label) * 0.160) + 0.18
    pre_w = max(0.40, len(prefactor) * 0.148) + 0.10 if prefactor else 0.0
    pad_x = 0.14
    pad_y = 0.24

    mat_w = n_cols * cell_w
    mat_h = n_rows * cell_h
    fig_w = pad_x + lbl_w + pre_w + bkt_w * 2 + mat_w + pad_x
    fig_h = mat_h + pad_y * 2

    fig = None
    try:
        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
        ax.set_xlim(0, fig_w)
        ax.set_ylim(0, fig_h)
        ax.axis('off')
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')

        y_c = fig_h / 2.0
        x = pad_x
        ax.text(x, y_c, f"{label} =", ha='left', va='center',
                fontsize=13, fontweight='bold', fontstyle='italic', color='#1a1a1a')
        x += lbl_w

        if prefactor:
            ax.text(x, y_c, prefactor, ha='left', va='center',
                    fontsize=12, color='#1a1a1a')
            x += pre_w

        y_top = fig_h - pad_y * 0.55
        y_bot = pad_y * 0.55
        lw    = 2.0
        arm   = bkt_w * 0.78

        ax.plot([x + arm, x, x, x + arm], [y_top, y_top, y_bot, y_bot],
                color='#1a1a1a', linewidth=lw,
                solid_capstyle='butt', solid_joinstyle='miter')
        x += bkt_w

        row_step = (y_top - y_bot) / n_rows
        for r_idx, row in enumerate(rows):
            y = y_top - (r_idx + 0.5) * row_step
            for c_idx, elem in enumerate(row):
                xi = x + (c_idx + 0.5) * cell_w
                ax.text(xi, y, str(elem), ha='center', va='center',
                        fontsize=10 if n_rows > 2 else 11,
                        color='#1a1a1a', fontfamily='DejaVu Sans')
        x += mat_w

        ax.plot([x, x + arm, x + arm, x], [y_top, y_top, y_bot, y_bot],
                color='#1a1a1a', linewidth=lw,
                solid_capstyle='butt', solid_joinstyle='miter')

        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=155,
                    bbox_inches='tight', pad_inches=0.07, facecolor='white')
        pixmap = QPixmap()
        if pixmap.loadFromData(buffer.getvalue(), 'PNG') and not pixmap.isNull():
            _MATRIX_CACHE[symbol] = pixmap
            return pixmap
    except Exception:
        return None
    finally:
        if fig is not None:
            try:
                plt.close(fig)
            except Exception:
                pass
    return None


# ─────────────────────────────────────────────
# LATEX EQUATION RENDERING
# Used for non-matrix inline formulas (state vectors, identities, etc.)
# ─────────────────────────────────────────────
try:
    from matplotlib.mathtext import math_to_image
    LATEX_RENDERING_AVAILABLE = True
except ImportError:
    math_to_image             = None
    LATEX_RENDERING_AVAILABLE = False


def extract_equations(text):
    """Extract equation-sized snippets from technical prose (non-matrix)."""
    patterns = [
        r'\bS=T²=diag\(1,i\)',
        r'\bZ=diag\(1,-1\)=σz',
        r'\bCX\s*=\s*\|0⟩⟨0\|⊗I\+\|1⟩⟨1\|⊗X',
        r'\bCZ\s*=\s*diag\(1,1,1,-1\)',
        r'\bSWAP\s*=\s*\(I⊗I\+X⊗X\+Y⊗Y\+Z⊗Z\)/2',
        r'\|c,t⟩\s+(?:to|en|vers|in|へ|映射为|में)\s+\|c,t XOR c⟩',
        r'\([^()\n]*\|[^|\n]*⟩[^()\n]*\)\s*/\s*√\s*\d+',
        r'α\|0⟩\s*\+\s*β\|1⟩',
        r'\bU†U\s*=\s*I\b|\bH²\s*=\s*I\b|\bS²\s*=\s*Z\b|\bSX²\s*=\s*X\b',
        r'\|[01]{2,3}⟩\s*\+\s*\|[01]{2,3}⟩',
        r'\b2ⁿ×2ⁿ\b',
        r'\|α\|²|\|β\|²',
    ]
    found = []
    for pattern in patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            candidate = match.group(0).strip().rstrip(" ,;:")
            if candidate and candidate not in found:
                found.append(candidate)
    return [item for item in found
            if not any(item != other and item in other for other in found)]


def text_without_rendered_equations(text):
    """Return prose with extracted equation strings replaced by spaces."""
    cleaned = text
    for formula in sorted(extract_equations(text), key=len, reverse=True):
        cleaned = cleaned.replace(formula, " ")
    cleaned = re.sub(r"\s+([,.;:!?，。；！？])", r"\1", cleaned)
    cleaned = re.sub(r"([.!?。])\s*([.!?。])+", r"\1", cleaned)
    cleaned = re.sub(r"\(\s*\)", "", cleaned)
    cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)
    cleaned = re.sub(r"^[\s.,;:!?，。；！？।]+", "", cleaned)
    return cleaned.strip()


def to_mathtext(formula):
    """Convert compact Unicode quantum notation to Matplotlib MathText."""
    value = formula.strip().rstrip(".。")
    value = re.sub(r"\|([^|⟩]+)⟩", r"|\1\\rangle", value)
    value = re.sub(r"⟨([^⟨|]+)\|", r"\\langle \1|", value)
    value = value.replace("√2", r"\sqrt{2}").replace("√", r"\sqrt{}")
    value = value.replace("θ", r"\theta ").replace("π", r"\pi ")
    value = value.replace("α", r"\alpha ").replace("β", r"\beta ")
    value = value.replace("σx", r"\sigma_x").replace("σy", r"\sigma_y").replace("σz", r"\sigma_z")
    value = value.replace("†", r"^{\dagger}").replace("ⁿ", "^n").replace("²", "^2")
    value = value.replace("×", r"\times ").replace("⊗", r"\otimes ")
    value = value.replace("→", r"\to ").replace("XOR", r"\mathrm{XOR}")
    value = re.sub(r"\s+(?:to|en|vers|in|へ|映射为|में)\s+",
                   lambda m: r" \to ", value, flags=re.IGNORECASE)
    # ── FIX: these two MUST use lambdas. A raw string like r"\mathrm{diag}("
    #    as the replacement makes re.sub raise "bad escape \m" / "\e",
    #    which crashed the Bell and GHZ circuit pages. ──
    value = re.sub(r"\bdiag\(", lambda m: r"\mathrm{diag}(", value)
    value = re.sub(r"\bexp\(",  lambda m: r"\exp(", value)
    value = re.sub(r"e\^\(([^()]*)\)", lambda m: "e^{" + m.group(1) + "}", value)
    value = value.replace("=", r" = ").replace("/", r" / ")
    return value


def render_equation_pixmap(formula):
    """Render a simple formula as a PNG QPixmap via mathtext. Never raises."""
    if not LATEX_RENDERING_AVAILABLE:
        return None
    try:
        # to_mathtext is inside the try block so a bad formula can never crash the app
        latex  = to_mathtext(formula)
        buffer = BytesIO()
        math_to_image("$" + latex + "$", buffer, dpi=180, format="png", color="black")
        pixmap = QPixmap()
        if pixmap.loadFromData(buffer.getvalue(), "PNG"):
            return pixmap
    except Exception:
        return None
    return None


def add_equation_images(layout, source_text):
    """Add rendered equation images for formulas found in the text. Never raises."""
    try:
        formulas = extract_equations(source_text)
    except Exception:
        return
    for formula in formulas:
        if "[[" in formula:          # matrices are handled by render_gate_matrix_image
            continue
        try:
            pixmap = render_equation_pixmap(formula)
            if pixmap is not None and not pixmap.isNull():
                equation = QLabel()
                equation.setPixmap(pixmap)
                equation.setAlignment(Qt.AlignmentFlag.AlignLeft)
                equation.setToolTip(formula)
                equation.setStyleSheet(
                    "background: #f8f8f8; padding: 5px; "
                    "border-radius: 4px; border: 1px solid #e0e0e0;"
                )
                layout.addWidget(equation)
        except Exception:
            continue


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def build_circuit(circuit_name):
    """Build and return the Qiskit QuantumCircuit for the given canonical name."""
    if QuantumCircuit is None:
        return None
    if circuit_name == BELL_CIRCUIT:
        qc = QuantumCircuit(2, name="Bell State")
        qc.h(0); qc.cx(0, 1)
    elif circuit_name == GHZ_CIRCUIT:
        qc = QuantumCircuit(3, name="GHZ State")
        qc.h(0); qc.cx(0, 1); qc.cx(0, 2)
    elif circuit_name == GROVER_CIRCUIT:
        qc = QuantumCircuit(2, name="Grover Search")
        qc.h([0, 1])
        qc.cz(0, 1)
        qc.h([0, 1]); qc.x([0, 1])
        qc.cz(0, 1)
        qc.x([0, 1]); qc.h([0, 1])
    else:
        return None
    return qc


def render_circuit_pixmap(qc):
    """Render a Qiskit circuit diagram as a QPixmap (matplotlib backend)."""
    if qc is None:
        return None
    buffer = BytesIO(); figure = None
    try:
        figure = qc.draw(output="mpl", fold=-1,
                         style={"backgroundcolor": "#ffffff"})
        figure.savefig(buffer, format="png", dpi=160,
                       bbox_inches="tight", facecolor="white")
        pixmap = QPixmap()
        if pixmap.loadFromData(buffer.getvalue(), "PNG") and not pixmap.isNull():
            return pixmap
    except Exception:
        return None
    finally:
        if figure is not None:
            try:
                import matplotlib.pyplot as plt
                plt.close(figure)
            except Exception:
                pass
    return None


def generate_qiskit_code(circuit_name, language="English"):
    """Return runnable local Qiskit code for the selected example circuit."""
    copy = SIMULATION_COPY.get(language, SIMULATION_COPY["English"])
    localized = CIRCUIT_LOCALIZATIONS.get(language, {}).get(
        circuit_name, CIRCUITS.get(circuit_name, {}))
    circuit_title = localized.get("title", circuit_name)
    circuit_label = copy["circuit_label"]
    measurement_label = copy["measurement_counts"]
    probabilities_label = copy["exact_probabilities"]
    if circuit_name == BELL_CIRCUIT:
        circuit = f"""qc = QuantumCircuit(2, name={circuit_title!r})
qc.h(0)
qc.cx(0, 1)"""
    elif circuit_name == GHZ_CIRCUIT:
        circuit = f"""qc = QuantumCircuit(3, name={circuit_title!r})
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 2)"""
    elif circuit_name == GROVER_CIRCUIT:
        circuit = f"""qc = QuantumCircuit(2, name={circuit_title!r})
qc.h([0, 1])
qc.cz(0, 1)
qc.h([0, 1])
qc.x([0, 1])
qc.cz(0, 1)
qc.x([0, 1])
qc.h([0, 1])"""
    else:
        raise ValueError(f"Unsupported circuit: {circuit_name!r}")
    return (
        "from qiskit import QuantumCircuit\n"
        "from qiskit.quantum_info import Statevector\n\n"
        f"{circuit}\n\n"
        f"# {copy['code_comment']}\n"
        f"shots = 1000  # {copy['shots_hint']}\n"
        "state = Statevector.from_instruction(qc)\n"
        "counts = state.sample_counts(shots=shots)\n"
        f'print("{circuit_label}")\n'
        "print(qc.draw())\n"
        f'print(f"{measurement_label} ({{shots}}): {{counts}}")\n'
        f'print("{probabilities_label}", state.probabilities_dict())\n'
    )


def experience_index(experience_text, t):
    if experience_text == t["novice"]:  return 0
    if experience_text == t["school"]:  return 1
    return 2


def set_language_direction(widget, language):
    direction = (Qt.LayoutDirection.RightToLeft if language == "العربية"
                 else Qt.LayoutDirection.LeftToRight)
    widget.setLayoutDirection(direction)


def configure_combo(combo):
    """Size the combo and popup for their longest option without eliding text."""
    combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
    combo.view().setTextElideMode(Qt.TextElideMode.ElideNone)
    longest = max(
        (combo.fontMetrics().horizontalAdvance(combo.itemText(i))
         for i in range(combo.count())), default=0)
    width = longest + 48
    combo.setMinimumWidth(max(combo.minimumWidth(), width))
    combo.view().setMinimumWidth(width)


def feedback_source_label(source, language):
    """Translate the screen context recorded with a submitted issue."""
    source_names = FEEDBACK_SOURCE_LABELS[language]
    source_ids = {
        "Welcome": "welcome", "Experience selection": "experience",
        "Circuit selection": "circuit", "Two-qubit circuit playground": "playground",
        "Quantum cryptography / BB84": "cryptography",
    }
    source_label = source_names.get(source_ids.get(source, ""), source)
    source_prefixes = (
        ("Operator guide: ", "operator"),
        ("Operator explanation: ", "operator_detail"),
        ("Simulation: ", "simulation"),
    )
    for prefix, source_key in source_prefixes:
        if not source.startswith(prefix):
            continue
        source_label = source_names[source_key]
        detail = source[len(prefix):]
        localized_circuit = (CIRCUIT_LOCALIZATIONS
                             .get(language, {})
                             .get(detail, {}).get("title", detail))
        if source_key in {"operator", "simulation"}:
            source_label = f"{source_label}: {localized_circuit}"
        elif source_key == "operator_detail":
            if language == "English":
                gate_name = next((name for _, gates in OPERATORS
                                  for symbol, name, *_ in gates
                                  if symbol == detail), detail)
            else:
                gate_name = OPERATOR_LOCALIZATIONS[language]["gates"].get(
                    detail, (detail, []))[0]
            source_label = f"{source_label}: {gate_name}"
        break
    return source_label


def build_feedback_issue(source, language, submitted, feedback):
    """Format a localized Markdown issue without performing filesystem I/O."""
    strings = TRANSLATIONS[language]
    return (
        f"# {strings['feedback_issue_title']}\n\n"
        f"- {strings['feedback_status_label']}: {strings['feedback_open_label']}\n"
        f"- {strings['feedback_submitted_label']}: {submitted.isoformat(timespec='seconds')}\n"
        f"- {strings['feedback_screen_label']}: {feedback_source_label(source, language)}\n"
        f"- {strings['feedback_language_label']}: {language}\n\n"
        f"## {strings['feedback_text_heading']}\n\n"
        f"{feedback}\n"
    )


def create_feedback_page(language, source):
    """Create a translated form that saves a local Markdown issue."""
    copy = TRANSLATIONS[language]
    page = QWidget()
    layout = QVBoxLayout(page)
    layout.setContentsMargins(28, 24, 28, 24)
    layout.setSpacing(12)

    heading = QLabel()
    heading.setFont(QFont("Arial", 17, QFont.Weight.Bold))
    prompt = QLabel()
    prompt.setWordWrap(True)
    editor = QPlainTextEdit()
    editor.setMinimumHeight(180)
    send_button = QPushButton()
    send_button.setStyleSheet(BUTTON_STYLE_GREEN)
    status = QLabel()
    active_language = [language]
    status.setWordWrap(True)

    layout.addWidget(heading)
    layout.addWidget(prompt)
    layout.addWidget(editor, 1)
    layout.addWidget(send_button)
    layout.addWidget(status)

    def refresh_text(selected_language):
        active_language[0] = selected_language
        strings = TRANSLATIONS[selected_language]
        heading.setText(strings["feedback_title"])
        prompt.setText(strings["feedback_prompt"])
        editor.setPlaceholderText(strings["feedback_prompt"])
        editor.setAccessibleName(strings["feedback_title"])
        send_button.setText(strings["feedback_send"])
        if status.text() in {
            TRANSLATIONS["English"]["feedback_empty"],
            TRANSLATIONS["Español"]["feedback_empty"],
            TRANSLATIONS["العربية"]["feedback_empty"],
            TRANSLATIONS["English"]["feedback_saved"],
            TRANSLATIONS["Español"]["feedback_saved"],
            TRANSLATIONS["العربية"]["feedback_saved"],
            TRANSLATIONS["English"]["feedback_error"],
            TRANSLATIONS["Español"]["feedback_error"],
            TRANSLATIONS["العربية"]["feedback_error"],
        }:
            status.clear()

    def submit_feedback():
        selected_language = active_language[0]
        feedback = editor.toPlainText().strip()
        if not feedback:
            status.setText(TRANSLATIONS[selected_language]["feedback_empty"])
            return
        submitted = datetime.now().astimezone()
        issue_folder = Path(__file__).resolve().parent / "Feedback"
        issue_path = issue_folder / (
            f"feedback-{submitted.strftime('%Y%m%d-%H%M%S-%f')}.md")
        issue_text = build_feedback_issue(
            source, selected_language, submitted, feedback)
        try:
            issue_folder.mkdir(parents=True, exist_ok=True)
            issue_path.write_text(issue_text, encoding="utf-8")
        except OSError:
            status.setText(TRANSLATIONS[selected_language]["feedback_error"])
            return
        editor.clear()
        status.setText(TRANSLATIONS[selected_language]["feedback_saved"])

    send_button.clicked.connect(submit_feedback)
    refresh_text(language)
    return page, refresh_text


def install_feedback_tab(window, language, source):
    """Wrap a window's current page with a shared top-level Feedback tab."""
    current_page = window.takeCentralWidget()
    tabs = QTabWidget(window)
    tabs.addTab(current_page, TRANSLATIONS[language]["tab_main"])
    feedback_page, _ = create_feedback_page(language, source)
    tabs.addTab(feedback_page, TRANSLATIONS[language]["tab_feedback"])
    window.setCentralWidget(tabs)


def audio_walkthrough_lines(qc, language):
    """Describe each Qiskit instruction in order for optional speech playback."""
    copy = AUDIO_COPY.get(language, AUDIO_COPY["English"])
    descriptions = {}
    if language == "English":
        descriptions = {
            symbol: (name, novice)
            for _, gates in OPERATORS
            for symbol, name, novice, _school, _university in gates
        }
    else:
        descriptions = OPERATOR_LOCALIZATIONS.get(language, {}).get("gates", {})

    aliases = {
        "measure": "Measure", "measure_all": "Measure", "if_else": "If",
        "for_loop": "For", "while_loop": "For", "unitary": "Unitary",
    }
    symbol_by_name = {
        symbol.casefold(): symbol
        for _, gates in OPERATORS
        for symbol, *_ in gates
    }
    symbol_by_name.update({alias: symbol for alias, symbol in aliases.items()})

    instructions = list(qc.data)
    lines = [copy["intro"].format(count=len(instructions))]
    for index, instruction in enumerate(instructions, start=1):
        operation = instruction.operation
        operation_name = operation.name
        symbol = symbol_by_name.get(operation_name.casefold())
        qubits = ", ".join(str(qc.find_bit(bit).index) for bit in instruction.qubits)
        if not qubits:
            qubits = {
                "English": "all qubits", "Español": "todos los qubits",
                "العربية": "جميع الكيوبتات",
            }.get(language, "all qubits")

        if symbol in descriptions:
            gate_name, explanation = descriptions[symbol]
            if language != "English":
                gate_name, levels = descriptions[symbol]
            explanation = BRAND_NEW_OPERATOR_EXPLANATIONS[language].get(
                symbol, explanation)
            explanation = explanation.rstrip(".。؛")
        else:
            gate_name = operation_name
            explanation = copy["unknown"].format(gate=operation_name)

        parameter_values = []
        for value in operation.params:
            if isinstance(value, (int, float)):
                parameter_values.append(f"{value:.3g}")
            else:
                parameter_values.append(str(value))
        parameters = ""
        if parameter_values:
            parameter_prefix = {
                "English": "Parameters:", "Español": "Parámetros:",
                "العربية": "المعاملات:",
            }.get(language, "Parameters:")
            parameters = f"{parameter_prefix} {', '.join(parameter_values)}"
        lines.append(copy["step"].format(
            step=index, count=len(instructions), gate=gate_name,
            qubits=qubits, description=explanation, parameters=parameters,
        ))
    lines.append(copy["complete"])
    return lines


def playground_audio_walkthrough_lines(slots, language):
    """Narrate the gates in a student-built circuit without requiring Qiskit."""
    copy = AUDIO_COPY[language]
    playground_copy = PLAYGROUND_COPY[language]
    operations = []
    for slot in slots:
        if "both" in slot:
            qubits = f"{playground_copy['wire_zero']} " \
                     f"{playground_copy['audio_qubit_join']} " \
                     f"{playground_copy['wire_one']}"
            operations.append((slot["both"], qubits))
            continue
        for wire in (0, 1):
            if wire in slot:
                qubit = playground_copy["wire_zero" if wire == 0 else "wire_one"]
                operations.append((slot[wire], qubit))
    lines = [copy["intro"].format(count=len(operations))]
    for index, (symbol, qubits) in enumerate(operations, start=1):
        name = BRAND_NEW_OPERATOR_EXPLANATIONS[language][symbol]
        lines.append(copy["step"].format(
            step=index, count=len(operations),
            gate=playground_copy["gate_names"][symbol],
            qubits=qubits, description=name, parameters="",
        ))
    probabilities = simulate_two_qubit_circuit(slots)
    results = ", ".join(
        f"{outcome}: {probability:.0%}"
        for outcome, probability in probabilities.items()
        if probability > 1e-9
    )
    lines.append(copy["playground_results"].format(results=results))
    lines.append(copy["complete"])
    return lines


# ─────────────────────────────────────────────
# WINDOW 1 - QUESTIONNAIRE
# ─────────────────────────────────────────────
class QuestionnaireDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(560)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowCloseButtonHint)

        self.country  = QComboBox()
        self.region   = QComboBox()
        self.language = QComboBox(); self.language.addItems(LANGUAGES)
        configure_combo(self.language)
        self.country.currentIndexChanged.connect(self.update_regions)
        self.language.currentTextChanged.connect(self.update_dialog_language)
        self.refresh_country_options(self.language.currentText())
        self.update_regions()

        self.content_page = QWidget()
        layout = QVBoxLayout(self.content_page)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(16)

        self.title_label = QLabel()
        self.title_label.setFont(QFont("Arial", 19, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        form = QFormLayout(); form.setSpacing(10)
        self.country_label = QLabel()
        self.region_label = QLabel()
        self.language_label = QLabel()
        form.addRow(self.country_label, self.country)
        form.addRow(self.region_label, self.region)
        form.addRow(self.language_label, self.language)
        layout.addLayout(form)

        self.continue_button = QPushButton()
        self.continue_button.setStyleSheet(BUTTON_STYLE_GREEN)
        self.continue_button.clicked.connect(self.accept)
        layout.addWidget(self.continue_button)

        self.tabs = QTabWidget(self)
        self.tabs.addTab(self.content_page, TRANSLATIONS["English"]["tab_main"])
        feedback_page, self.feedback_refresh = create_feedback_page(
            self.language.currentText(), "Welcome")
        self.tabs.addTab(feedback_page, TRANSLATIONS["English"]["tab_feedback"])
        root_layout = QVBoxLayout(self)
        root_layout.addWidget(self.tabs)
        self.update_dialog_language(self.language.currentText())

    def update_dialog_language(self, language):
        t = TRANSLATIONS.get(language, TRANSLATIONS["English"])
        self.setWindowTitle(t["welcome"])
        self.title_label.setText(t["main"])
        self.country_label.setText(t["country"])
        self.region_label.setText(t["region"])
        self.language_label.setText(t["language"])
        self.continue_button.setText(t["continue"])
        self.tabs.setTabText(0, t["tab_main"])
        self.tabs.setTabText(1, t["tab_feedback"])
        self.feedback_refresh(language)
        set_language_direction(self, language)
        self.refresh_country_options(language)

    def refresh_country_options(self, language):
        selected = self.country.currentData()
        labels = COUNTRY_LABELS.get(language, COUNTRY_LABELS["English"])
        self.country.blockSignals(True)
        self.country.clear()
        for key in COUNTRIES:
            self.country.addItem(labels[key], key)
        index = self.country.findData(selected)
        self.country.setCurrentIndex(index if index >= 0 else 0)
        self.country.blockSignals(False)
        configure_combo(self.country)
        self.update_regions()

    def update_regions(self, *_):
        country = self.country.currentData()
        language = self.language.currentText()
        other_label = {
            "English": "Other / N/A", "Español": "Otro / No aplica",
            "العربية": "أخرى / لا ينطبق",
        }.get(language, "Other / N/A")
        not_applicable = {
            "English": "Not applicable", "Español": "No aplica",
            "العربية": "لا ينطبق",
        }.get(language, "Not applicable")
        region_labels = REGION_LABELS.get(language, {})
        self.region.clear()
        regions = COUNTRIES.get(country, ["Not applicable"])
        self.region.addItems([
            other_label if item == "Other / N/A" else
            not_applicable if item == "Not applicable" else
            region_labels.get(item, item)
            for item in regions
        ])
        configure_combo(self.region)

    def get_answers(self):
        return {
            "country":  self.country.currentText(),
            "state":    self.region.currentText(),
            "language": self.language.currentText(),
        }


# ─────────────────────────────────────────────
# WINDOW 2 - EXPERIENCE LEVEL
# ─────────────────────────────────────────────
class MainWindow(QMainWindow):
    back_requested = Signal()
    next_requested = Signal(str)

    def __init__(self, answers):
        super().__init__()
        self.answers = answers
        self.t = TRANSLATIONS.get(answers["language"], TRANSLATIONS["English"])
        set_language_direction(self, answers["language"])
        self._closing_for_navigation = False
        self.setWindowTitle(self.t["title"])
        self.setMinimumSize(720, 420)

        central = QWidget(); self.setCentralWidget(central)
        layout  = QVBoxLayout(central)
        layout.setContentsMargins(35, 30, 35, 30); layout.setSpacing(18)

        title = QLabel(self.t["main"])
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        layout.addWidget(title)

        summary = QLabel(
            f"📍 {answers['state']}, {answers['country']}  |  🌐 {answers['language']}")
        summary.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary.setStyleSheet("color: #666666;")
        layout.addWidget(summary)

        self.experience = QComboBox()
        self.experience.addItems(
            [self.t["novice"], self.t["school"], self.t["university"]])
        configure_combo(self.experience)
        row = QHBoxLayout()
        row.addWidget(QLabel(self.t["experience"]))
        row.addWidget(self.experience)
        layout.addLayout(row)

        begin = QPushButton(self.t["begin"])
        begin.setStyleSheet(BUTTON_STYLE_GREEN)
        begin.clicked.connect(self.begin_tutorial)
        layout.addWidget(begin)

        back = QPushButton(self.t["back"])
        back.setStyleSheet(BUTTON_STYLE_BACK)
        back.clicked.connect(self.go_back)
        layout.addWidget(back)

        self.status = QLabel(self.t["ready"])
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status)
        install_feedback_tab(self, answers["language"], "Experience selection")

    def go_back(self):
        self._closing_for_navigation = True; self.close(); self.back_requested.emit()

    def begin_tutorial(self):
        chosen = self.experience.currentText()
        self._closing_for_navigation = True; self.close()
        self.next_requested.emit(chosen)

    def closeEvent(self, event):
        event.accept()
        if not self._closing_for_navigation:
            QApplication.quit()


class GateDragButton(QToolButton):
    """Palette button that starts a drag carrying a gate symbol."""
    def __init__(self, symbol, name, concept, parent=None):
        super().__init__(parent)
        self.symbol = symbol
        self.press_position = None
        self.setText(name)
        self.setIcon(QIcon(render_operator_icon(symbol)))
        self.setIconSize(QSize(74, 50))
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.setCheckable(True)
        self.setToolTip(f"{name}\n\n{concept}")
        self.setAccessibleName(f"{symbol}: {name}")
        self.setAccessibleDescription(concept)
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        label_width = self.fontMetrics().horizontalAdvance(name)
        self.setFixedSize(max(142, label_width + 26), 98)
        self.setStyleSheet(
            "QToolButton { background: white; border: 1px solid #dfe7e8; "
            "border-radius: 8px; padding: 4px; }"
            "QToolButton:hover { background: #f0f8f7; border-color: #247f78; }"
            "QToolButton:checked { background: #e1f1ee; border: 2px solid #176b65; }"
        )

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.press_position = event.position().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (self.press_position is None or
                not (event.buttons() & Qt.MouseButton.LeftButton) or
                (event.position().toPoint() - self.press_position).manhattanLength()
                < QApplication.startDragDistance()):
            return
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setData("application/x-quantum-gate", self.symbol.encode("ascii"))
        drag.setMimeData(mime_data)
        drag.setPixmap(self.icon().pixmap(self.iconSize()))
        drag.exec(Qt.DropAction.CopyAction)
        self.press_position = None


class TwoQubitCircuitCanvas(QWidget):
    """Paint a small two-wire circuit and accept palette gate drops."""
    circuit_changed = Signal()
    notice_changed = Signal(str)
    MAX_STEPS = 20

    def __init__(self, copy, parent=None):
        super().__init__(parent)
        self.copy = copy
        self.slots = [{} for _ in range(6)]
        self.gate_history = []
        self.setAcceptDrops(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAccessibleName(copy["canvas_accessible"])
        self.setMinimumHeight(222)
        self.setMinimumWidth(self.sizeHint().width())
        self.resize(self.sizeHint())
        self._update_accessible_summary()
        self.setStyleSheet(
            "background: #ffffff; border: 1px solid #dfe7e8; border-radius: 8px;")

    def sizeHint(self):
        return QSize(max(720, 154 + max(6, len(self.slots)) * 88), 222)

    def _update_extent(self):
        self.setMinimumWidth(self.sizeHint().width())
        self.resize(self.sizeHint())
        self.updateGeometry()
        self.update()
        self._update_accessible_summary()

    def _update_accessible_summary(self):
        entries = []
        for index, slot in enumerate(self.slots):
            if "both" in slot:
                entries.append(self.copy["canvas_gate_accessible"].format(
                    step=index + 1,
                    gate=self.copy["gate_names"][slot["both"]],
                    wire=self.copy["canvas_both_wires"],
                ))
            else:
                for wire in (0, 1):
                    if wire in slot:
                        entries.append(self.copy["canvas_gate_accessible"].format(
                            step=index + 1,
                            gate=self.copy["gate_names"][slot[wire]],
                            wire=self.copy["wire_zero" if wire == 0 else "wire_one"],
                        ))
        self.setAccessibleDescription(" ".join(entries) if entries else
                                       self.copy["canvas_empty_accessible"])

    def clear_circuit(self):
        self.slots = [{} for _ in range(6)]
        self.gate_history.clear()
        self._update_extent()
        self.circuit_changed.emit()
        self.notice_changed.emit(self.copy["cleared"])

    def _trim_empty_columns(self):
        while len(self.slots) > 6 and not self.slots[-1]:
            self.slots.pop()

    def remove_last_gate(self):
        while self.gate_history:
            step, wire, symbol = self.gate_history.pop()
            if (step >= len(self.slots) or
                    self.slots[step].get(wire) != symbol):
                continue
            del self.slots[step][wire]
            self._trim_empty_columns()
            self._update_extent()
            self.circuit_changed.emit()
            self.notice_changed.emit(self.copy["removed"].format(
                gate=self.copy["gate_names"][symbol]))
            return
        self.notice_changed.emit(self.copy["nothing_to_undo"])

    def append_gate(self, symbol, target_wire=0):
        latest_step = max(
            (index for index, slot in enumerate(self.slots) if slot), default=-1)
        start_step = max(0, latest_step)
        step = next((index for index in range(start_step, self.MAX_STEPS)
                     if self._can_place(symbol, target_wire, index)), None)
        if step is None:
            self.notice_changed.emit(self.copy["full"])
            return False
        while len(self.slots) <= step:
            self.slots.append({})
        if symbol in PLAYGROUND_TWO_QUBIT_GATES:
            self.slots[step]["both"] = symbol
            wire = "both"
        else:
            self.slots[step][target_wire] = symbol
            wire = target_wire
        self.gate_history.append((step, wire, symbol))
        self._update_extent()
        self.circuit_changed.emit()
        self.notice_changed.emit(self.copy["added"].format(
            gate=self.copy["gate_names"][symbol], step=step + 1))
        return True

    def dragEnterEvent(self, event):
        mime = event.mimeData()
        if mime.hasFormat("application/x-quantum-gate"):
            symbol = bytes(mime.data("application/x-quantum-gate")).decode(
                "ascii", errors="ignore")
            if symbol in PLAYGROUND_SINGLE_GATES + PLAYGROUND_TWO_QUBIT_GATES:
                event.acceptProposedAction()
                return
        event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-quantum-gate"):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        mime = event.mimeData()
        if not mime.hasFormat("application/x-quantum-gate"):
            event.ignore()
            return
        symbol = bytes(mime.data("application/x-quantum-gate")).decode(
            "ascii", errors="ignore")
        if symbol not in PLAYGROUND_SINGLE_GATES + PLAYGROUND_TWO_QUBIT_GATES:
            event.ignore()
            return

        position = event.position().toPoint()
        requested_step = max(0, round((position.x() - 140) / 88))
        target_wire = 0 if position.y() < self.height() / 2 else 1
        step = next((index for index in range(requested_step, self.MAX_STEPS)
                     if self._can_place(symbol, target_wire, index)), None)
        if step is None:
            self.notice_changed.emit(self.copy["full"])
            event.ignore()
            return
        while len(self.slots) <= step:
            self.slots.append({})
        if symbol in PLAYGROUND_TWO_QUBIT_GATES:
            self.slots[step]["both"] = symbol
            wire = "both"
        else:
            self.slots[step][target_wire] = symbol
            wire = target_wire
        self.gate_history.append((step, wire, symbol))
        self._update_extent()
        self.circuit_changed.emit()
        self.notice_changed.emit(self.copy["added"].format(
            gate=self.copy["gate_names"][symbol], step=step + 1))
        event.acceptProposedAction()

    def _can_place(self, symbol, wire, step):
        if step >= self.MAX_STEPS:
            return False
        slot = self.slots[step] if step < len(self.slots) else {}
        if symbol in PLAYGROUND_TWO_QUBIT_GATES:
            return not slot
        return "both" not in slot and wire not in slot

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            position = event.position().toPoint()
            requested_step = round((position.x() - 140) / 88)
            wire = 0 if position.y() < self.height() / 2 else 1
            if 0 <= requested_step < len(self.slots):
                slot = self.slots[requested_step]
                x_center = 140 + requested_step * 88
                removed = None
                if "both" in slot and abs(position.x() - x_center) <= 20:
                    if 54 <= position.y() <= 188:
                        removed = slot.pop("both")
                        removed_wire = "both"
                elif abs(position.x() - x_center) <= 30:
                    y_center = 82 if wire == 0 else 160
                    if abs(position.y() - y_center) <= 24:
                        removed = slot.pop(wire, None)
                        removed_wire = wire
                if removed:
                    for history_index in range(len(self.gate_history) - 1, -1, -1):
                        if self.gate_history[history_index] == (
                                requested_step, removed_wire, removed):
                            self.gate_history.pop(history_index)
                            break
                    self._trim_empty_columns()
                    self._update_extent()
                    self.circuit_changed.emit()
                    self.notice_changed.emit(self.copy["removed"].format(
                        gate=self.copy["gate_names"][removed]))
                    return
        super().mousePressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#ffffff"))
        y_positions = (82, 160)
        painter.setFont(QFont("Arial", 10, QFont.Weight.DemiBold))
        painter.setPen(QColor("#44575a"))
        painter.drawText(16, y_positions[0] + 4, self.copy["wire_zero"])
        painter.drawText(16, y_positions[1] + 4, self.copy["wire_one"])
        painter.setPen(QPen(QColor("#e6eeee"), 1, Qt.PenStyle.DashLine))
        for step in range(max(6, len(self.slots))):
            x = 140 + step * 88
            painter.drawLine(x, 45, x, 194)
        painter.setPen(QPen(QColor("#8aa5a3"), 2))
        painter.drawLine(100, y_positions[0], self.width() - 20, y_positions[0])
        painter.drawLine(100, y_positions[1], self.width() - 20, y_positions[1])

        for step in range(max(6, len(self.slots))):
            x = 140 + step * 88
            painter.setPen(QColor("#91a3a5"))
            painter.setFont(QFont("Arial", 8))
            painter.drawText(x - 12, 35, str(step + 1))
            slot = self.slots[step] if step < len(self.slots) else {}
            if "both" in slot:
                self._paint_two_qubit_gate(painter, slot["both"], x, y_positions)
            else:
                for wire in (0, 1):
                    if wire in slot:
                        self._paint_single_gate(
                            painter, slot[wire], x, y_positions[wire])
        painter.end()

    @staticmethod
    def _paint_single_gate(painter, symbol, x, y):
        rect = (x - 29, y - 22, 58, 44)
        painter.setPen(QPen(QColor("#247f78"), 2))
        painter.setBrush(QColor("#e8f3f1"))
        painter.drawRoundedRect(*rect, 7, 7)
        painter.setPen(QColor("#176b65"))
        painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        painter.drawText(*rect, Qt.AlignmentFlag.AlignCenter, symbol)

    @staticmethod
    def _paint_two_qubit_gate(painter, symbol, x, ys):
        top, bottom = ys
        painter.setPen(QPen(QColor("#247f78"), 2))
        if symbol == "CX":
            painter.drawLine(x, top, x, bottom)
            painter.setBrush(QColor("#176b65"))
            painter.drawEllipse(x - 7, top - 7, 14, 14)
            painter.setBrush(QColor("#ffffff"))
            painter.drawEllipse(x - 17, bottom - 17, 34, 34)
            painter.drawLine(x - 11, bottom, x + 11, bottom)
            painter.drawLine(x, bottom - 11, x, bottom + 11)
        elif symbol == "CZ":
            painter.drawLine(x, top, x, bottom)
            painter.setBrush(QColor("#176b65"))
            painter.drawEllipse(x - 7, top - 7, 14, 14)
            painter.drawEllipse(x - 7, bottom - 7, 14, 14)
        else:  # SWAP
            painter.drawLine(x, top, x, bottom)
            for y in ys:
                painter.drawLine(x - 10, y - 10, x + 10, y + 10)
                painter.drawLine(x - 10, y + 10, x + 10, y - 10)


class TwoQubitPlaygroundWindow(QMainWindow):
    back_requested = Signal()

    def __init__(self, answers):
        super().__init__()
        self.answers = answers
        self.language = answers["language"]
        self.copy = PLAYGROUND_COPY[self.language]
        experience_text = answers.get(
            "experience", TRANSLATIONS[self.language]["novice"])
        self.brand_new_mode = experience_index(
            experience_text, TRANSLATIONS[self.language]) == 0
        self.audio_copy = AUDIO_COPY[self.language]
        self._speech = None
        self._audio_active = False
        self._audio_lines = []
        self._audio_index = 0
        self._closing_for_navigation = False
        set_language_direction(self, self.language)
        self.setWindowTitle(self.copy["window"])
        self.setMinimumSize(980, 760)
        self.resize(1180, 940)

        root = QWidget()
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(20, 16, 20, 16)
        outer.setSpacing(10)
        title = QLabel(self.copy["title"])
        title.setFont(QFont("Arial", 19, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        outer.addWidget(scroll, 1)
        content = QWidget()
        body = QVBoxLayout(content)
        body.setSpacing(10)
        scroll.setWidget(content)

        intro = QLabel(self.copy["intro"])
        intro.setWordWrap(True)
        body.addWidget(intro)
        self.bell_example_button = QPushButton(self.copy["bell_example"])
        self.bell_example_button.setStyleSheet(BUTTON_STYLE_BACK)
        self.bell_example_button.setToolTip(self.copy["bell_example_tooltip"])
        self.bell_example_button.clicked.connect(self.load_bell_example)
        example_row = QHBoxLayout()
        example_row.addStretch(1)
        example_row.addWidget(self.bell_example_button)
        example_row.addStretch(1)
        body.addLayout(example_row)
        self.selected_palette_gate = None
        self.palette_buttons = {}
        self.advanced_palette_buttons = []
        self._add_palette(body, self.copy["single_heading"], PLAYGROUND_SINGLE_GATES)
        self._add_palette(body, self.copy["two_heading"], PLAYGROUND_TWO_QUBIT_GATES)
        if self.brand_new_mode:
            self.gate_filter_button = QPushButton(self.copy["show_all_gates"])
            self.gate_filter_button.setCheckable(True)
            self.gate_filter_button.setStyleSheet(BUTTON_STYLE_BACK)
            self.gate_filter_button.setToolTip(self.copy["beginner_palette_hint"])
            self.gate_filter_button.toggled.connect(self.toggle_advanced_gates)
            filter_row = QHBoxLayout()
            filter_row.addStretch(1)
            filter_row.addWidget(self.gate_filter_button)
            filter_row.addStretch(1)
            body.addLayout(filter_row)
            self.toggle_advanced_gates(False)
        palette_hint = QLabel(self.copy["palette_hint"])
        palette_hint.setWordWrap(True)
        palette_hint.setStyleSheet("color: #5c6264;")
        body.addWidget(palette_hint)

        keyboard_row = QHBoxLayout()
        keyboard_row.addWidget(QLabel(self.copy["target_wire"]))
        self.target_wire = QComboBox()
        self.target_wire.addItem(self.copy["wire_zero"], 0)
        self.target_wire.addItem(self.copy["wire_one"], 1)
        configure_combo(self.target_wire)
        keyboard_row.addWidget(self.target_wire)
        self.add_selected_button = QPushButton(self.copy["add_gate"])
        self.add_selected_button.setStyleSheet(
            BUTTON_STYLE_GREEN +
            "QPushButton:disabled { background: #d8e2e1; color: #536261; }")
        self.add_selected_button.setEnabled(False)
        self.add_selected_button.clicked.connect(self.add_selected_gate)
        keyboard_row.addWidget(self.add_selected_button)
        body.addLayout(keyboard_row)

        canvas_hint = QLabel(self.copy["canvas_hint"])
        canvas_hint.setWordWrap(True)
        body.addWidget(canvas_hint)
        self.canvas_scroll = QScrollArea()
        self.canvas_scroll.setWidgetResizable(True)
        self.canvas_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.canvas = TwoQubitCircuitCanvas(self.copy)
        self.canvas_scroll.setWidget(self.canvas)
        body.addWidget(self.canvas_scroll)
        self.status = QLabel(self.copy["ready"])
        self.status.setWordWrap(True)
        body.addWidget(self.status)
        self.canvas.circuit_changed.connect(self._circuit_changed)
        self.canvas.notice_changed.connect(self.status.setText)

        controls = QHBoxLayout()
        controls.addWidget(QLabel(self.copy["shots"]))
        self.shots = QComboBox()
        self.shots.addItems(["100", "1,000", "10,000"])
        configure_combo(self.shots)
        self.shots.setCurrentIndex(1)
        controls.addWidget(self.shots)
        clear_button = QPushButton(self.copy["clear"])
        clear_button.setStyleSheet(
            "QPushButton { background: #e7edef; color: #243238; border: 1px solid #d1dcde; "
            "border-radius: 7px; padding: 9px 14px; }"
            "QPushButton:hover { background: #dbe6e8; }")
        clear_button.clicked.connect(self.canvas.clear_circuit)
        controls.addWidget(clear_button)
        self.undo_button = QPushButton(self.copy["undo"])
        self.undo_button.setStyleSheet(
            "QPushButton { background: #e7edef; color: #243238; border: 1px solid #d1dcde; "
            "border-radius: 7px; padding: 9px 14px; }"
            "QPushButton:hover { background: #dbe6e8; }"
            "QPushButton:disabled { color: #586667; background: #e4eaeb; }")
        self.undo_button.setEnabled(False)
        self.undo_button.clicked.connect(self.canvas.remove_last_gate)
        controls.addWidget(self.undo_button)
        run_button = QPushButton(self.copy["run"])
        run_button.setStyleSheet(BUTTON_STYLE_GREEN)
        run_button.clicked.connect(self.run_local_simulation)
        controls.addWidget(run_button)
        body.addLayout(controls)

        self.audio_button = QPushButton(self.audio_copy["off"])
        self.audio_button.setCheckable(True)
        self.audio_button.setStyleSheet(BUTTON_STYLE_BACK)
        self.audio_button.toggled.connect(self.toggle_audio_walkthrough)
        audio_row = QHBoxLayout()
        audio_row.addStretch(1)
        audio_row.addWidget(self.audio_button)
        audio_row.addStretch(1)
        body.addLayout(audio_row)

        heading = QLabel(self.copy["result_heading"])
        heading.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        body.addWidget(heading)
        probability_hint = QLabel(self.copy["probability_hint"])
        probability_hint.setWordWrap(True)
        probability_hint.setStyleSheet("color: #5c6264;")
        body.addWidget(probability_hint)
        self.results_table = QTableWidget(4, 4)
        self.results_table.setHorizontalHeaderLabels([
            self.copy["outcome"], self.copy["exact"],
            self.copy["count"], self.copy["observed"],
        ])
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents)
        body.addWidget(self.results_table)
        local_note = QLabel(self.copy["local_note"])
        local_note.setWordWrap(True)
        local_note.setStyleSheet("color: #5c6264;")
        body.addWidget(local_note)

        back = QPushButton(self.copy["back"])
        back.setStyleSheet(BUTTON_STYLE_BACK)
        back.clicked.connect(self.go_back)
        outer.addWidget(back)
        self._set_result_table([0.0] * 4, None, None)
        self.refresh_exact_probabilities()
        install_feedback_tab(self, self.language, "Two-qubit circuit playground")

    def _circuit_changed(self):
        if self._audio_active:
            self._stop_audio_walkthrough()
        self.undo_button.setEnabled(any(self.canvas.slots))
        self.bell_example_button.setEnabled(not any(self.canvas.slots))
        self.refresh_exact_probabilities()

    def load_bell_example(self):
        if any(self.canvas.slots):
            return
        self.canvas.slots[0][0] = "H"
        self.canvas.slots[1]["both"] = "CX"
        self.canvas.gate_history = [(0, 0, "H"), (1, "both", "CX")]
        self.canvas._update_extent()
        self.canvas.circuit_changed.emit()
        self.canvas.notice_changed.emit(self.copy["bell_example_loaded"])

    def _add_palette(self, layout, heading_text, symbols):
        heading = QLabel(heading_text)
        heading.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(heading)
        host = QWidget()
        grid = QGridLayout(host)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(8)
        grid.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        for index, symbol in enumerate(symbols):
            name = self.copy["gate_names"][symbol]
            concept = BRAND_NEW_OPERATOR_EXPLANATIONS[self.language][symbol]
            button = GateDragButton(symbol, name, concept)
            button.clicked.connect(
                lambda _checked=False, gate=symbol: self.select_palette_gate(gate))
            self.palette_buttons[symbol] = button
            grid.addWidget(button, index // 5, index % 5)
            basic_gates = {"H", "X", "CX"}
            if self.brand_new_mode and symbol not in basic_gates:
                button.setVisible(False)
                self.advanced_palette_buttons.append(button)
        layout.addWidget(host)

    def toggle_advanced_gates(self, show_all):
        for button in self.advanced_palette_buttons:
            button.setVisible(show_all)
        if (not show_all and self.selected_palette_gate not in
                {None, "H", "X", "CX"} and hasattr(self, "add_selected_button")):
            hidden_selection = self.selected_palette_gate
            self.selected_palette_gate = None
            self.palette_buttons[hidden_selection].setChecked(False)
            self.add_selected_button.setEnabled(False)
            if hasattr(self, "status"):
                self.status.setText(
                    self.copy["empty"] if not any(self.canvas.slots)
                    else self.copy["ready"])
        self.gate_filter_button.setText(
            self.copy["show_basic_gates"] if show_all
            else self.copy["show_all_gates"])

    def select_palette_gate(self, symbol):
        self.selected_palette_gate = symbol
        for gate, button in self.palette_buttons.items():
            button.setChecked(gate == symbol)
        self.add_selected_button.setEnabled(True)
        self.status.setText(self.copy["selected_gate"].format(
            gate=self.copy["gate_names"][symbol]))

    def add_selected_gate(self):
        if self.selected_palette_gate is None:
            self.status.setText(self.copy["select_gate"])
            return
        self.canvas.append_gate(
            self.selected_palette_gate, self.target_wire.currentData())

    def refresh_exact_probabilities(self):
        probabilities = simulate_two_qubit_circuit(self.canvas.slots)
        exact = [float(probabilities.get(outcome, 0.0))
                 for outcome in ("00", "01", "10", "11")]
        self._set_result_table(exact, None, None)
        self.status.setText(self.copy["empty"] if not any(self.canvas.slots)
                            else self.copy["ready"])

    def _set_result_table(self, probabilities, counts, shots):
        outcomes = ("00", "01", "10", "11")
        self.results_table.setUpdatesEnabled(False)
        for row, (outcome, probability) in enumerate(zip(outcomes, probabilities)):
            values = [outcome, f"{probability:.1%}", "—", "—"]
            if counts is not None and shots:
                count = counts.get(outcome, 0)
                values[2] = f"{count:,}"
                values[3] = f"{count / shots:.1%}"
            for column, value in enumerate(values):
                self.results_table.setItem(row, column, QTableWidgetItem(value))
        self.results_table.setUpdatesEnabled(True)

    def run_local_simulation(self):
        probabilities = simulate_two_qubit_circuit(self.canvas.slots)
        shots = int(self.shots.currentText().replace(",", ""))
        outcomes = tuple(probabilities)
        sampled_outcomes = random.choices(
            outcomes, weights=tuple(probabilities.values()), k=shots)
        counts = Counter(sampled_outcomes)
        exact = [float(probabilities.get(outcome, 0.0))
                 for outcome in ("00", "01", "10", "11")]
        self._set_result_table(exact, counts, shots)
        self.status.setText(self.copy["local_note"])

    def _set_audio_button(self, checked):
        self.audio_button.blockSignals(True)
        self.audio_button.setChecked(checked)
        self.audio_button.setText(
            self.audio_copy["on"] if checked else self.audio_copy["off"])
        self.audio_button.blockSignals(False)

    def _stop_audio_walkthrough(self):
        self._audio_active = False
        if self._speech is not None:
            self._speech.stop()
        self._set_audio_button(False)

    def toggle_audio_walkthrough(self, enabled):
        self.audio_button.setText(
            self.audio_copy["on"] if enabled else self.audio_copy["off"])
        if not enabled:
            was_active = self._audio_active
            self._stop_audio_walkthrough()
            if was_active:
                self.status.setText(self.audio_copy["stopped"])
            return
        if QTextToSpeech is None or QLocale is None:
            self.status.setText(self.audio_copy["no_module"])
            self._set_audio_button(False)
            return
        if not any(self.canvas.slots):
            self.status.setText(self.audio_copy["no_circuit"])
            self._set_audio_button(False)
            return
        try:
            if self._speech is None:
                self._speech = QTextToSpeech(self)
                self._speech.stateChanged.connect(self._on_speech_state_changed)
            locale_name = {
                "English": "en_US", "Español": "es_ES", "العربية": "ar_SA",
            }[self.language]
            requested_locale = QLocale(locale_name)
            self._speech.setLocale(requested_locale)
            requested_language = requested_locale.language()
            matching_voices = [
                voice for voice in self._speech.availableVoices()
                if voice.locale().language() == requested_language
            ]
            if not matching_voices:
                self._speech.stop()
                self.status.setText(self.audio_copy["no_voice"])
                self._set_audio_button(False)
                return
            self._speech.setVoice(matching_voices[0])
            self._audio_lines = playground_audio_walkthrough_lines(
                self.canvas.slots, self.language)
            self._audio_index = 0
            self._audio_active = True
            self.status.setText(self._audio_lines[0])
            self._speak_next_audio_line()
        except Exception:
            self._audio_active = False
            if self._speech is not None:
                self._speech.stop()
            self.status.setText(self.audio_copy["no_voice"])
            self._set_audio_button(False)

    def _on_speech_state_changed(self, state):
        if self._audio_active and state == QTextToSpeech.State.Error:
            self._audio_active = False
            self.status.setText(self.audio_copy["no_voice"])
            self._set_audio_button(False)
            return
        if self._audio_active and state == QTextToSpeech.State.Ready:
            QTimer.singleShot(100, self._speak_next_audio_line)

    def _speak_next_audio_line(self):
        if not self._audio_active:
            return
        if self._audio_index >= len(self._audio_lines):
            self._audio_active = False
            self.status.setText(self.audio_copy["complete"])
            self._set_audio_button(False)
            return
        line = self._audio_lines[self._audio_index]
        self._audio_index += 1
        self.status.setText(line)
        self._speech.say(line)

    def go_back(self):
        self._closing_for_navigation = True
        self.close()
        self.back_requested.emit()

    def closeEvent(self, event):
        self._audio_active = False
        if self._speech is not None:
            self._speech.stop()
        event.accept()
        if not self._closing_for_navigation:
            QApplication.quit()


# ─────────────────────────────────────────────
# WINDOW 3 - CIRCUIT SELECTION
# ─────────────────────────────────────────────
class CircuitWindow(QMainWindow):
    back_requested = Signal()
    next_requested = Signal(str)
    cryptography_requested = Signal()
    playground_requested = Signal()

    # ── Localized circuit names (index matches CIRCUITS key order) ──
    CIRCUIT_NAMES_BY_LANGUAGE = {
        "English":  ["The Bell State Circuit (Entanglement)",
                     "Three-Qubit GHZ State Circuit",
                     "Two-Qubit Grover Search Circuit"],
        "Español":  ["El Circuito de Estado Bell (Entrelazamiento)",
                     "Circuito de Estado GHZ de Tres Qubits",
                     "Circuito de Búsqueda de Grover de Dos Qubits"],
        "العربية": ["دائرة حالة بيل (التشابك)",
                     "دائرة حالة GHZ بثلاثة كيوبتات",
                     "دائرة بحث غروفر بكيوبتين"],
    }
    CANONICAL_NAMES = list(CIRCUITS.keys())

    def __init__(self, answers):
        super().__init__()
        self.answers = answers
        self.t = TRANSLATIONS.get(answers["language"], TRANSLATIONS["English"])
        set_language_direction(self, answers["language"])
        self._closing_for_navigation = False
        self.setWindowTitle(self.t["title"]); self.setMinimumSize(760, 470)

        central = QWidget(); self.setCentralWidget(central)
        layout  = QVBoxLayout(central)
        layout.setContentsMargins(35, 30, 35, 30); layout.setSpacing(18)

        title = QLabel(self.t["main"])
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        layout.addWidget(title)

        summary = QLabel(
            f"📍 {answers['state']}, {answers['country']}  |  "
            f"🌐 {answers['language']}  |  🎓 {answers['experience']}")
        summary.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary.setStyleSheet("color: #666666;")
        layout.addWidget(summary)

        layout.addWidget(QLabel(self.t["choose_circuit"]))
        self.circuit = QComboBox()
        names = self.CIRCUIT_NAMES_BY_LANGUAGE.get(
            answers["language"], self.CIRCUIT_NAMES_BY_LANGUAGE["English"])
        self.circuit.addItems(names)
        configure_combo(self.circuit)
        layout.addWidget(self.circuit)

        explore = QPushButton(self.t["explore"])
        explore.setStyleSheet(BUTTON_STYLE_GREEN)
        explore.clicked.connect(self.explore)
        layout.addWidget(explore)

        crypto = QPushButton(self.t["cryptography"])
        crypto.setStyleSheet(BUTTON_STYLE_GREEN)
        crypto.clicked.connect(self.open_cryptography)
        layout.addWidget(crypto)

        playground = QPushButton(self.t["playground"])
        playground.setStyleSheet(BUTTON_STYLE_GREEN)
        playground.clicked.connect(self.open_playground)
        layout.addWidget(playground)

        back = QPushButton(self.t["back"])
        back.setStyleSheet(BUTTON_STYLE_BACK)
        back.clicked.connect(self.go_back)
        layout.addWidget(back)

        self.status = QLabel(self.t["ready"])
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status)
        install_feedback_tab(self, answers["language"], "Circuit selection")

    def canonical_circuit_name(self):
        idx = self.circuit.currentIndex()
        return self.CANONICAL_NAMES[idx] if 0 <= idx < len(self.CANONICAL_NAMES) \
               else self.CANONICAL_NAMES[0]

    def go_back(self):
        self._closing_for_navigation = True; self.close(); self.back_requested.emit()

    def explore(self):
        self._closing_for_navigation = True; self.close()
        self.next_requested.emit(self.canonical_circuit_name())

    def open_cryptography(self):
        self._closing_for_navigation = True; self.close()
        self.cryptography_requested.emit()

    def open_playground(self):
        self._closing_for_navigation = True; self.close()
        self.playground_requested.emit()

    def closeEvent(self, event):
        event.accept()
        if not self._closing_for_navigation:
            QApplication.quit()


# ─────────────────────────────────────────────
# WINDOW 4 - QUANTUM OPERATORS GUIDE + SELECTED CIRCUIT
# ─────────────────────────────────────────────
def render_operator_icon(symbol):
    """Draw a small native gate icon for the clickable operator chart."""
    pixmap = QPixmap(112, 78)
    pixmap.fill(QColor("#e8f3f1"))
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(QColor("#b9d6d2"))
    painter.setBrush(QColor("#e8f3f1"))
    painter.drawRoundedRect(2, 2, 108, 74, 12, 12)
    font = QFont("Arial", 21 if len(symbol) <= 3 else 15, QFont.Weight.Bold)
    painter.setFont(font)
    painter.setPen(QColor("#176b65"))
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, symbol)
    painter.end()
    return pixmap


def render_operator_concept(symbol):
    """Draw a simple circuit-like picture for Brand new operator explanations."""
    pixmap = QPixmap(520, 138)
    pixmap.fill(QColor("#f8fbfb"))
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    teal, muted = QColor("#247f78"), QColor("#8aa5a3")
    painter.setPen(QPen(muted, 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
    multi = symbol in {"CX", "CZ", "SWAP", "CCX", "CSWAP"}
    three_wire = symbol in {"CCX", "CSWAP"}
    ys = [35, 69, 103] if three_wire else ([45, 92] if multi else [69])
    for y in ys:
        painter.drawLine(32, y, 488, y)
        painter.setBrush(QColor("#ffffff")); painter.setPen(QPen(teal, 2))
        painter.drawEllipse(22, y - 10, 20, 20)
        painter.drawEllipse(478, y - 10, 20, 20)

    cx = 260
    if symbol == "H":
        painter.setPen(QPen(teal, 3)); painter.drawLine(32, 69, 226, 69)
        painter.drawLine(294, 69, 488, 42); painter.drawLine(294, 69, 488, 96)
        painter.setBrush(QColor("#dcefeb")); painter.setPen(QPen(teal, 2))
        painter.drawRoundedRect(226, 49, 68, 40, 10, 10)
        painter.setPen(teal); painter.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        painter.drawText(226, 49, 68, 40, Qt.AlignmentFlag.AlignCenter, "H")
        for y in (42, 96):
            painter.setBrush(teal); painter.drawEllipse(480, y - 5, 10, 10)
    elif symbol in {"Measure", "Reset"}:
        painter.setPen(QPen(teal, 3)); painter.drawLine(32, 69, 225, 69)
        painter.drawLine(295, 69, 488, 69)
        painter.setBrush(QColor("#dcefeb")); painter.setPen(QPen(teal, 2))
        painter.drawRoundedRect(225, 45, 70, 48, 10, 10)
        if symbol == "Measure":
            painter.setPen(QPen(teal, 2))
            painter.drawArc(238, 53, 44, 30, 0, 180 * 16)
            painter.drawLine(260, 78, 270, 60)
            painter.setBrush(teal); painter.drawEllipse(256, 74, 8, 8)
            painter.setPen(QPen(teal, 2)); painter.drawLine(260, 93, 260, 115)
            painter.drawLine(260, 115, 224, 125); painter.drawLine(260, 115, 296, 125)
            painter.setBrush(teal); painter.drawEllipse(218, 120, 10, 10)
            painter.drawEllipse(291, 120, 10, 10)
        else:
            painter.setPen(teal); painter.setFont(QFont("Arial", 18, QFont.Weight.Bold))
            painter.drawText(225, 45, 70, 48, Qt.AlignmentFlag.AlignCenter, "↶")
    elif symbol in {"Barrier"}:
        painter.setPen(QPen(teal, 3, Qt.PenStyle.DashLine)); painter.drawLine(cx, 27, cx, 111)
    elif multi:
        painter.setPen(QPen(teal, 3)); painter.drawLine(cx, ys[0], cx, ys[-1])
        if symbol in {"CX", "CZ", "CCX", "CSWAP"}:
            painter.setBrush(teal); painter.setPen(QPen(teal, 2))
            painter.drawEllipse(cx - 7, ys[0] - 7, 14, 14)
        if symbol == "CX":
            painter.setPen(QPen(teal, 3)); painter.drawLine(cx - 11, ys[1], cx + 11, ys[1])
            painter.drawLine(cx, ys[1] - 11, cx, ys[1] + 11)
        elif symbol == "CCX":
            painter.setBrush(teal); painter.drawEllipse(cx - 7, ys[1] - 7, 14, 14)
            painter.setPen(QPen(teal, 3)); painter.drawLine(cx - 11, ys[2], cx + 11, ys[2])
            painter.drawLine(cx, ys[2] - 11, cx, ys[2] + 11)
        elif symbol == "CZ":
            painter.setBrush(teal); painter.drawEllipse(cx - 7, ys[1] - 7, 14, 14)
        elif symbol == "CSWAP":
            for y in ys[1:]:
                painter.setPen(QPen(teal, 3))
                painter.drawLine(cx - 10, y - 9, cx + 10, y + 9)
                painter.drawLine(cx - 10, y + 9, cx + 10, y - 9)
        else:
            for y in ys:
                painter.setPen(QPen(teal, 3)); painter.drawLine(cx - 10, y - 9, cx + 10, y + 9)
                painter.drawLine(cx - 10, y + 9, cx + 10, y - 9)
    elif symbol in {"If", "For"}:
        painter.setPen(QPen(teal, 3)); painter.drawLine(32, 69, 215, 69)
        painter.drawLine(215, 69, 255, 42); painter.drawLine(255, 42, 305, 42)
        painter.drawLine(215, 69, 255, 96); painter.drawLine(255, 96, 305, 96)
        painter.drawLine(305, 42, 488, 42); painter.drawLine(305, 96, 488, 96)
        if symbol == "For":
            painter.drawArc(224, 35, 60, 64, 30 * 16, 290 * 16)
    elif symbol in {"Y", "Z", "S", "T", "P", "RZ"}:
        painter.setPen(QPen(teal, 3)); painter.drawLine(32, 69, 220, 69)
        painter.drawLine(300, 69, 488, 69)
        painter.drawArc(226, 35, 68, 68, 35 * 16, 285 * 16)
        painter.drawLine(279, 39, 294, 39); painter.drawLine(294, 39, 290, 53)
    elif symbol in {"RX", "RY", "SX"}:
        painter.setPen(QPen(teal, 3)); painter.drawLine(32, 69, 220, 69)
        painter.drawLine(300, 69, 488, 69)
        painter.drawArc(226, 35, 68, 68, 25 * 16, 300 * 16)
        painter.drawLine(279, 39, 294, 39); painter.drawLine(294, 39, 290, 53)
    elif symbol == "Unitary":
        painter.setPen(QPen(teal, 3)); painter.drawLine(32, 69, 210, 69)
        painter.drawLine(310, 69, 488, 69)
        painter.setBrush(QColor("#dcefeb")); painter.setPen(QPen(teal, 2))
        painter.drawRoundedRect(210, 38, 100, 62, 10, 10)
        painter.setPen(QPen(teal, 3)); painter.drawLine(234, 57, 286, 57)
        painter.drawLine(286, 57, 277, 50); painter.drawLine(286, 57, 277, 64)
        painter.drawLine(286, 81, 234, 81)
        painter.drawLine(234, 81, 243, 74); painter.drawLine(234, 81, 243, 88)
    else:
        painter.setPen(QPen(teal, 3)); painter.drawLine(32, 69, 226, 69)
        painter.drawLine(294, 69, 488, 69)
        painter.setBrush(QColor("#dcefeb")); painter.setPen(QPen(teal, 2))
        painter.drawRoundedRect(226, 45, 68, 48, 10, 10)
        painter.setPen(teal); painter.setFont(QFont("Arial", 15, QFont.Weight.Bold))
        painter.drawText(226, 45, 68, 48, Qt.AlignmentFlag.AlignCenter, symbol)
    painter.end()
    return pixmap


class OperatorDetailDialog(QDialog):
    def __init__(self, language, symbol, name, experience, detailed_description):
        super().__init__()
        self.t = TRANSLATIONS[language]
        set_language_direction(self, language)
        self.setWindowTitle(f"{symbol} — {name}")
        self.setMinimumSize(560, 430)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(14)
        title = QLabel(f"{symbol} — {name}")
        title.setFont(QFont("Arial", 19, QFont.Weight.Bold))
        layout.addWidget(title)

        concept = BRAND_NEW_OPERATOR_EXPLANATIONS[language][symbol]
        if experience == 0:
            illustration = QLabel()
            illustration.setPixmap(render_operator_concept(symbol))
            illustration.setAlignment(Qt.AlignmentFlag.AlignCenter)
            illustration.setAccessibleName({
                "English": f"Concept illustration for {name}",
                "Español": f"Ilustración conceptual de {name}",
                "العربية": f"رسم توضيحي لمفهوم {name}",
            }[language])
            layout.addWidget(illustration)
        concept_label = QLabel(concept)
        concept_label.setWordWrap(True)
        concept_label.setStyleSheet(
            "background: #e8f3f1; padding: 14px; border: 1px solid #cbdedb; "
            "border-radius: 8px; font-size: 14px;"
        )
        layout.addWidget(concept_label)

        if experience > 0 and detailed_description:
            detail_heading = QLabel(
                f"{self.t['description']} — "
                f"{self.t['school'] if experience == 1 else self.t['university']}:")
            detail_heading.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            layout.addWidget(detail_heading)
            detail = QLabel(text_without_rendered_equations(detailed_description))
            detail.setWordWrap(True)
            layout.addWidget(detail)
            add_equation_images(layout, detailed_description)
            matrix = render_gate_matrix_image(symbol)
            if matrix is not None and not matrix.isNull():
                matrix_label = QLabel()
                matrix_label.setPixmap(matrix)
                layout.addWidget(matrix_label)

        layout.addStretch(1)
        close = QPushButton(self.t["close"])
        close.setStyleSheet(BUTTON_STYLE_BACK)
        close.clicked.connect(self.accept)
        layout.addWidget(close)

        main_tab = QScrollArea()
        main_tab.setWidgetResizable(True)
        main_tab.setWidget(page)
        tabs = QTabWidget(self)
        tabs.addTab(main_tab, self.t["tab_main"])
        feedback_page, _ = create_feedback_page(
            language, f"Operator explanation: {symbol}")
        tabs.addTab(feedback_page, self.t["tab_feedback"])
        dialog_layout = QVBoxLayout(self)
        dialog_layout.setContentsMargins(0, 0, 0, 0)
        dialog_layout.addWidget(tabs)


class OperatorsWindow(QMainWindow):
    back_requested       = Signal()
    simulation_requested = Signal()

    def __init__(self, answers, circuit_name):
        super().__init__()
        self.answers      = answers
        self.circuit_name = circuit_name
        self.t            = TRANSLATIONS.get(answers["language"], TRANSLATIONS["English"])
        set_language_direction(self, answers["language"])
        self._closing_for_navigation = False
        self.level        = experience_index(answers["experience"], self.t)
        self.setWindowTitle(self.t["operators"])
        self.setMinimumSize(940, 760); self.resize(1080, 920)

        root  = QWidget(); self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(20, 18, 20, 18); outer.setSpacing(12)

        # ── Title ──
        title = QLabel(self.t["operators"])
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(title)

        summary = QLabel(
            f"📍 {answers['state']}, {answers['country']}  |  "
            f"🌐 {answers['language']}  |  🎓 {answers['experience']}")
        summary.setAlignment(Qt.AlignmentFlag.AlignCenter)
        summary.setStyleSheet("color: #666666;")
        outer.addWidget(summary)

        # ── Scrollable content ──
        scroll  = QScrollArea(); scroll.setWidgetResizable(True); outer.addWidget(scroll, 1)
        content = QWidget()
        content_layout = QVBoxLayout(content); content_layout.setSpacing(12)
        scroll.setWidget(content)

        primer = QLabel(BEGINNER_PRIMER.get(answers["language"], BEGINNER_PRIMER["English"]))
        primer.setWordWrap(True)
        primer.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        primer.setStyleSheet(
            "background: #e8f3f1; color: #243238; padding: 14px; "
            "border: 1px solid #cbdedb; border-radius: 8px; line-height: 1.4;"
        )
        content_layout.addWidget(primer)
        hint = QLabel(self.t["operator_chart_hint"])
        hint.setStyleSheet("color: #506269; padding: 2px 4px;")
        content_layout.addWidget(hint)

        localized = OPERATOR_LOCALIZATIONS.get(answers["language"])
        self.detail_windows = []
        tile_columns = 4

        for cat_idx, (_category, items) in enumerate(OPERATORS):
            category_name = (
                localized["categories"][cat_idx] if localized else _category)
            heading = QLabel(category_name)
            heading.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            heading.setStyleSheet(
                "background: #e8f3f1; padding: 9px; border-radius: 6px; border: none;")
            content_layout.addWidget(heading)

            grid_host = QWidget()
            grid = QGridLayout(grid_host)
            grid.setContentsMargins(2, 2, 2, 8)
            grid.setHorizontalSpacing(14)
            grid.setVerticalSpacing(12)

            for index, (symbol, name, _novice, school, university) in enumerate(items):
                if localized and symbol in localized["gates"]:
                    display_name, descriptions = localized["gates"][symbol]
                    detailed_description = descriptions[self.level] if self.level else ""
                else:
                    display_name = name
                    detailed_description = school if self.level == 1 else university

                tile = QFrame()
                tile.setStyleSheet(
                    "QFrame { background: #ffffff; border: 1px solid #dfe7e8; "
                    "border-radius: 8px; }"
                )
                tile_layout = QVBoxLayout(tile)
                tile_layout.setContentsMargins(8, 8, 8, 8)
                tile_layout.setSpacing(5)

                image_button = QToolButton()
                image_button.setIcon(QIcon(render_operator_icon(symbol)))
                image_button.setIconSize(QSize(112, 78))
                image_button.setFixedSize(132, 94)
                image_button.setToolTip(display_name)
                image_button.setAccessibleName(f"{symbol}: {display_name}")
                image_button.setCursor(Qt.CursorShape.PointingHandCursor)
                image_button.setStyleSheet(
                    "QToolButton { background: transparent; border: none; padding: 0; }"
                    "QToolButton:hover { background: #f0f8f7; border-radius: 6px; }"
                    "QToolButton:focus { border: 2px solid #247f78; border-radius: 6px; }"
                )
                image_button.clicked.connect(
                    lambda _checked=False, s=symbol, n=display_name, d=detailed_description:
                    self.open_operator_detail(s, n, d))
                tile_layout.addWidget(image_button, 0, Qt.AlignmentFlag.AlignCenter)

                name_label = QLabel(display_name)
                name_label.setWordWrap(True)
                name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                name_label.setStyleSheet("background: transparent; border: none; font-weight: 600;")
                tile_layout.addWidget(name_label)
                grid.addWidget(tile, index // tile_columns, index % tile_columns)

            content_layout.addWidget(grid_host)

        # ── Selected circuit section ──
        circuit_heading = QLabel(self.t["circuit"])
        circuit_heading.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        circuit_heading.setStyleSheet(
            "background: #e8f3f1; padding: 9px; border-radius: 5px; border: none;")
        content_layout.addWidget(circuit_heading)

        if self.level == 0:
            display_circuit = BRAND_NEW_CIRCUITS[answers["language"]][circuit_name]
            display_title = (CIRCUIT_LOCALIZATIONS
                             .get(answers["language"], {})
                             .get(circuit_name, CIRCUITS[circuit_name])
                             .get("title", circuit_name))
            circuit_description = display_circuit["description"]
            circuit_steps = display_circuit["steps"]
        else:
            circuit_data = CIRCUITS[circuit_name]
            localized_circuits = CIRCUIT_LOCALIZATIONS.get(answers["language"], {})
            display_circuit = localized_circuits.get(circuit_name, circuit_data)
            circuit_description = display_circuit["description"]
            circuit_steps = display_circuit["steps"]
            display_title = display_circuit.get("title", circuit_name)

        circuit_text = QLabel(
            f"{display_title}\n\n"
            f"{text_without_rendered_equations(circuit_description)}\n\n"
            f"{text_without_rendered_equations(circuit_steps)}")
        circuit_text.setWordWrap(True)
        circuit_text.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse)
        content_layout.addWidget(circuit_text)
        if self.level > 0:
            add_equation_images(content_layout,
                                f"{circuit_description}\n{circuit_steps}")

        # ── Circuit diagram ──
        qc = build_circuit(circuit_name)
        if qc is not None:
            cpix = render_circuit_pixmap(qc)
            if cpix is not None:
                diagram = QLabel()
                diagram.setPixmap(cpix)
                diagram.setAlignment(Qt.AlignmentFlag.AlignCenter)
                diagram.setMinimumHeight(cpix.height() + 16)
                diagram.setToolTip(self.t["diagram_tooltip"])
            else:
                diagram = QLabel(
                    qc.draw(output="text", fold=-1).__str__()
                    + "\n\n" + self.t["diagram_error"])
                diagram.setFont(QFont("Menlo", 11))
                diagram.setTextInteractionFlags(
                    Qt.TextInteractionFlag.TextSelectableByMouse)
        else:
            diagram = QLabel(self.t["qiskit_missing"])
        diagram.setWordWrap(True)
        diagram.setStyleSheet(
            "background: #f7f7f7; padding: 10px; border: 1px solid #e0e0e0;")
        content_layout.addWidget(diagram)

        # ── Buttons ──
        buttons  = QHBoxLayout()
        back_btn = QPushButton(self.t["back"])
        back_btn.setStyleSheet(BUTTON_STYLE_BACK)
        back_btn.clicked.connect(self.go_back)
        buttons.addWidget(back_btn)

        sim_btn = QPushButton(self.t.get("simulation", "▶ Theory & Local Simulation"))
        sim_btn.setStyleSheet(BUTTON_STYLE_GREEN)
        sim_btn.clicked.connect(self.open_simulation)
        buttons.addWidget(sim_btn)

        close_btn = QPushButton(self.t.get("close", "✕ Close"))
        close_btn.setStyleSheet(BUTTON_STYLE_BACK)
        close_btn.clicked.connect(self.close_application)
        buttons.addWidget(close_btn)
        outer.addLayout(buttons)
        install_feedback_tab(
            self, answers["language"], f"Operator guide: {circuit_name}")

    def open_operator_detail(self, symbol, display_name, detailed_description):
        dialog = OperatorDetailDialog(
            self.answers["language"], symbol, display_name,
            self.level, detailed_description)
        self.detail_windows.append(dialog)
        dialog.finished.connect(
            lambda _result, window=dialog:
            self.detail_windows.remove(window) if window in self.detail_windows else None)
        dialog.show()

    def go_back(self):
        self._closing_for_navigation = True; self.close(); self.back_requested.emit()

    def open_simulation(self):
        self._closing_for_navigation = True; self.close()
        self.simulation_requested.emit()

    def close_application(self):
        self._closing_for_navigation = True; self.close(); QApplication.quit()

    def closeEvent(self, event):
        for dialog in tuple(self.detail_windows):
            dialog.close()
        event.accept()
        if not self._closing_for_navigation:
            QApplication.quit()


# ─────────────────────────────────────────────
# WINDOW 5 - POLARIZATION-BASED BB84 TEACHING DEMO
# ─────────────────────────────────────────────
class PulseStreamWidget(QWidget):
    """Loop a drawing of the pulses in the most recent BB84 exchange."""
    def __init__(self, labels, parent=None):
        super().__init__(parent)
        self.labels = labels
        self.records = []
        self.index = 0
        self.progress = 0.0
        self.step = 0.0158
        self.setMinimumHeight(142)
        self.setAccessibleName(labels["accessible_name"])
        self.setAccessibleDescription(labels["empty"])
        self.timer = QTimer(self)
        self.timer.setInterval(30)
        self.timer.timeout.connect(self.advance)

    def set_records(self, records):
        self.records = records
        self.index = 0
        self.progress = 0.0
        self._update_accessible_description()
        self.update()

    def advance(self):
        if not self.records:
            return
        self.progress += self.step
        if self.progress >= 1.0:
            self.progress = 0.0
            self.index = (self.index + 1) % len(self.records)
        self._update_accessible_description()
        self.update()

    def _update_accessible_description(self):
        if not self.records:
            self.setAccessibleDescription(self.labels["empty"])
            return
        record = self.records[self.index]
        resent_segment = (
            record["eve_basis"] is not None and self.progress >= 0.5)
        bit = record["eve_bit"] if resent_segment else record["alice_bit"]
        actor = self.labels["eve"] if resent_segment else self.labels["alice"]
        basis_name = "rect_basis" if (
            (resent_segment and record["eve_basis"] == "rectilinear") or
            (not resent_segment and record["alice_basis"] == "rectilinear")
        ) else "diag_basis"
        self.setAccessibleDescription(self.labels["status"].format(
            index=self.index + 1, total=len(self.records),
            actor=actor, bit=bit, basis=self.labels[basis_name]))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#f8fbfb"))
        width, height = self.width(), self.height()
        left, right = 66, width - 66
        y = 72
        eve_present = bool(self.records and self.records[self.index]["eve_basis"] is not None)
        eve_x = (left + right) / 2
        painter.setPen(QColor("#3a5053"))
        painter.setFont(QFont("Arial", 10, QFont.Weight.DemiBold))
        painter.drawText(12, 27, self.labels["alice"])
        painter.drawText(round(right - 35), 27, self.labels["bob"])
        if eve_present:
            painter.drawText(round(eve_x - 22), 27, self.labels["eve"])
        painter.setPen(QPen(QColor("#a7bfbc"), 3, Qt.PenStyle.SolidLine,
                            Qt.PenCapStyle.RoundCap))
        painter.drawLine(round(left), y, round(right), y)
        for x in (left, right):
            painter.setBrush(QColor("#ffffff")); painter.setPen(QPen(QColor("#247f78"), 2))
            painter.drawEllipse(round(x - 8), y - 8, 16, 16)
        if eve_present:
            painter.setBrush(QColor("#ffffff")); painter.setPen(QPen(QColor("#c17a35"), 2))
            painter.drawRect(round(eve_x - 10), y - 10, 20, 20)
        if self.records:
            record = self.records[self.index]
            resent_segment = eve_present and self.progress >= 0.5
            start = eve_x if eve_present and self.progress >= 0.5 else left
            end = right if not eve_present or self.progress >= 0.5 else eve_x
            local_progress = self.progress * 2 if eve_present and self.progress < 0.5 else (
                (self.progress - 0.5) * 2 if eve_present else self.progress)
            x = start + (end - start) * local_progress
            painter.setBrush(QColor("#35a89d")); painter.setPen(QPen(QColor("#176b65"), 2))
            painter.drawEllipse(round(x - 12), y - 12, 24, 24)
            angle = record["resent_angle"] if resent_segment else record["angle"]
            radians = math.radians(angle)
            dx, dy = 8 * math.cos(radians), -8 * math.sin(radians)
            painter.setPen(QPen(QColor("#ffffff"), 2.5, Qt.PenStyle.SolidLine,
                                Qt.PenCapStyle.RoundCap))
            painter.drawLine(round(x - dx), round(y - dy), round(x + dx), round(y + dy))
            status = self.labels["status"].format(
                index=self.index + 1, total=len(self.records),
                actor=self.labels["eve"] if resent_segment else self.labels["alice"],
                bit=(record["eve_bit"] if resent_segment else record["alice_bit"]),
                basis=self.labels[
                    "rect_basis" if (resent_segment and record["eve_basis"] == "rectilinear")
                    or (not resent_segment and record["alice_basis"] == "rectilinear")
                    else "diag_basis"])
            painter.setPen(QColor("#506269")); painter.setFont(QFont("Arial", 10))
            painter.drawText(self.rect().adjusted(8, 104, -8, -4),
                             Qt.AlignmentFlag.AlignCenter, status)
        else:
            painter.setPen(QColor("#506269")); painter.setFont(QFont("Arial", 10))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter,
                             self.labels["empty"])
        painter.end()


def render_polarization_icon(angle):
    """Draw one photon pulse with its polarization axis."""
    pixmap = QPixmap(56, 42)
    pixmap.fill(QColor("#f8fbfb"))
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(QColor("#b9d6d2"))
    painter.setBrush(QColor("#ffffff"))
    painter.drawRoundedRect(1, 1, 54, 40, 7, 7)
    radians = math.radians(angle)
    dx, dy = 15 * math.cos(radians), -15 * math.sin(radians)
    painter.setPen(QColor("#247f78"))
    painter.drawLine(round(28 - dx), round(21 - dy), round(28 + dx), round(21 + dy))
    painter.setBrush(QColor("#176b65"))
    painter.drawEllipse(24, 17, 8, 8)
    painter.end()
    return pixmap


class CryptographyWindow(QMainWindow):
    back_requested = Signal()

    POLARIZATION_STATES = {
        ("rectilinear", 0): ("H", 0),
        ("rectilinear", 1): ("V", 90),
        ("diagonal", 0): ("D", 45),
        ("diagonal", 1): ("A", 135),
    }

    def __init__(self, answers):
        super().__init__()
        self.answers = answers
        self.language = answers["language"]
        self.copy = CRYPTO_COPY[self.language]
        self._closing_for_navigation = False
        set_language_direction(self, self.language)
        self.setWindowTitle(self.copy["window"])
        self.setMinimumSize(980, 760)
        self.resize(1180, 920)

        root = QWidget()
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(20, 16, 20, 16)
        outer.setSpacing(10)

        title = QLabel(self.copy["title"])
        title.setFont(QFont("Arial", 19, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        outer.addWidget(scroll, 1)
        content = QWidget()
        body = QVBoxLayout(content)
        body.setSpacing(10)
        scroll.setWidget(content)

        intro = QLabel(self.copy["intro"])
        intro.setWordWrap(True)
        body.addWidget(intro)
        protocol = QLabel(self.copy["protocol"])
        protocol.setWordWrap(True)
        protocol.setStyleSheet(
            "background: #e8f3f1; padding: 12px; border: 1px solid #cbdedb; "
            "border-radius: 8px;"
        )
        body.addWidget(protocol)
        note = QLabel(self.copy["note"])
        note.setWordWrap(True)
        note.setStyleSheet("color: #5c6264; padding: 2px 4px;")
        body.addWidget(note)

        citation = QLabel(self.copy["citation"])
        citation.setWordWrap(True)
        citation.setOpenExternalLinks(True)
        body.addWidget(citation)

        input_row = QHBoxLayout()
        input_row.addWidget(QLabel(self.copy["input_label"]))
        self.message_input = QLineEdit()
        # Qt counts UTF-16 code units; reserve two per Python code point,
        # then enforce the code-point limit below.
        self.message_input.setMaxLength(MAX_CRYPTO_MESSAGE_CHARS * 2)
        self.message_input.textEdited.connect(self.limit_message_characters)
        self.message_input.textEdited.connect(self._on_message_edited)
        self.message_input.setPlaceholderText(self.copy["input_hint"])
        input_row.addWidget(self.message_input, 1)
        body.addLayout(input_row)

        controls = QHBoxLayout()
        self.eve_toggle = QCheckBox(self.copy["eve"])
        controls.addWidget(self.eve_toggle)
        self.run_button = QPushButton(self.copy["run"])
        self.run_button.setStyleSheet(BUTTON_STYLE_GREEN)
        self.run_button.clicked.connect(self.run_exchange)
        controls.addWidget(self.run_button)
        body.addLayout(controls)

        animation_heading = QLabel(self.copy["live_heading"])
        animation_heading.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        body.addWidget(animation_heading)
        animation_note = QLabel(self.copy["live_note"].format(
            preview_limit=MAX_ANIMATED_PULSES))
        animation_note.setWordWrap(True)
        animation_note.setStyleSheet("color: #5c6264; padding: 2px 4px;")
        body.addWidget(animation_note)
        self.pulse_animation = PulseStreamWidget({
            "alice": self.copy["alice"], "bob": self.copy["bob"],
            "eve": self.copy["eve_label"],
            "empty": self.copy["animation_empty"],
            "accessible_name": self.copy["live_heading"],
            "status": self.copy["animation_status"],
            "rect_basis": self.copy["rect_basis"],
            "diag_basis": self.copy["diag_basis"],
        })
        self.pulse_animation.setStyleSheet(
            "background: #f8fbfb; border: 1px solid #dfe7e8; border-radius: 8px;")
        body.addWidget(self.pulse_animation)
        self.animation_button = QPushButton(self.copy["animation_play"])
        self.animation_button.setStyleSheet(BUTTON_STYLE_BACK)
        self.animation_button.setCheckable(True)
        self.animation_button.setEnabled(False)
        self.animation_button.toggled.connect(self.toggle_animation)
        animation_controls = QHBoxLayout()
        animation_controls.addWidget(self.animation_button)
        animation_controls.addSpacing(14)
        animation_controls.addWidget(QLabel(self.copy["speed_label"]))
        animation_controls.addWidget(QLabel(self.copy["speed_slow"]))
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(1, 10)
        self.speed_slider.setValue(3)
        self.speed_slider.setSingleStep(1)
        self.speed_slider.setPageStep(2)
        self.speed_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.setAccessibleName(self.copy["speed_label"])
        self.speed_slider.setToolTip(self.copy["speed_label"])
        self.speed_slider.valueChanged.connect(self.set_animation_speed)
        animation_controls.addWidget(self.speed_slider, 1)
        animation_controls.addWidget(QLabel(self.copy["speed_fast"]))
        body.addLayout(animation_controls)
        self.set_animation_speed(self.speed_slider.value())

        results_heading = QLabel(self.copy["result_heading"])
        results_heading.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        body.addWidget(results_heading)
        self.results = QTextBrowser()
        self.results.setMinimumHeight(150)
        self.results.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.results.setPlainText(self.copy["ready"])
        body.addWidget(self.results)

        pulse_heading = QLabel(self.copy["pulse_heading"])
        pulse_heading.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        body.addWidget(pulse_heading)
        privacy_note = QLabel(self.copy["table_privacy_note"])
        privacy_note.setWordWrap(True)
        privacy_note.setStyleSheet("color: #5c6264; padding: 2px 4px;")
        body.addWidget(privacy_note)
        self.pulse_table = QTableWidget(0, len(self.copy["columns"]))
        self.pulse_table.setHorizontalHeaderLabels(self.copy["columns"])
        self.pulse_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.pulse_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.pulse_table.setAlternatingRowColors(True)
        self.pulse_table.verticalHeader().setVisible(False)
        self.pulse_table.setIconSize(QSize(50, 38))
        self.pulse_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive)
        body.addWidget(self.pulse_table, 1)

        controls_bottom = QHBoxLayout()
        back = QPushButton(self.copy["back"])
        back.setStyleSheet(BUTTON_STYLE_BACK)
        back.clicked.connect(self.go_back)
        controls_bottom.addWidget(back)
        body.addLayout(controls_bottom)

        self.polarization_icons = {
            label: QIcon(render_polarization_icon(angle))
            for (_basis, _bit), (label, angle) in self.POLARIZATION_STATES.items()
        }
        install_feedback_tab(self, self.language, "Quantum cryptography / BB84")

    def _basis_label(self, basis):
        return self.copy["rect_basis"] if basis == "rectilinear" else self.copy["diag_basis"]

    @staticmethod
    def _measure(encoded_bit, encoded_basis, measurement_basis):
        if encoded_basis == measurement_basis:
            return encoded_bit
        return secrets.randbits(1)

    def limit_message_characters(self, text):
        if len(text) <= MAX_CRYPTO_MESSAGE_CHARS:
            return
        limited = text[:MAX_CRYPTO_MESSAGE_CHARS]
        cursor_units = len(limited.encode("utf-16-le")) // 2
        cursor_position = self.message_input.cursorPosition()
        self.message_input.blockSignals(True)
        self.message_input.setText(limited)
        self.message_input.setCursorPosition(min(
            cursor_position, cursor_units))
        self.message_input.blockSignals(False)

    def _clear_previous_exchange_view(self):
        self.pulse_animation.timer.stop()
        self.pulse_animation.set_records([])
        self.animation_button.blockSignals(True)
        self.animation_button.setChecked(False)
        self.animation_button.setEnabled(False)
        self.animation_button.setText(self.copy["animation_play"])
        self.animation_button.blockSignals(False)
        self.pulse_table.setRowCount(0)

    def _on_message_edited(self, _text):
        if self.pulse_animation.records or self.pulse_table.rowCount():
            self._clear_previous_exchange_view()
            self.results.setPlainText(self.copy["ready"])

    def run_exchange(self):
        self._clear_previous_exchange_view()
        message = self.message_input.text()
        if not message:
            self.results.setPlainText(self.copy["empty"])
            return

        message_bytes = message.encode("utf-8")
        if (len(message) > MAX_CRYPTO_MESSAGE_CHARS or
                len(message_bytes) > MAX_CRYPTO_MESSAGE_BYTES):
            self.results.setPlainText(self.copy["too_long"])
            return
        message_bits = [
            (byte >> shift) & 1
            for byte in message_bytes
            for shift in range(7, -1, -1)
        ]

        records = []
        required_message_bits = len(message_bits)
        # Generate enough pulses for the key and a 32-round public sample,
        # with margin for the random basis matches. The former 4x batch
        # produced many unnecessary table rows for longer messages.
        batch_size = max(64, required_message_bits * 2 + 128)
        while True:
            for _ in range(batch_size):
                alice_bit = secrets.randbits(1)
                alice_basis = secrets.choice(("rectilinear", "diagonal"))
                polarization, angle = self.POLARIZATION_STATES[(alice_basis, alice_bit)]

                eve_basis = None
                eve_bit = None
                resent_bit = alice_bit
                resent_basis = alice_basis
                if self.eve_toggle.isChecked():
                    eve_basis = secrets.choice(("rectilinear", "diagonal"))
                    eve_bit = self._measure(alice_bit, alice_basis, eve_basis)
                    resent_bit, resent_basis = eve_bit, eve_basis

                bob_basis = secrets.choice(("rectilinear", "diagonal"))
                bob_bit = self._measure(resent_bit, resent_basis, bob_basis)
                resent_angle = self.POLARIZATION_STATES[
                    (resent_basis, resent_bit)][1]
                records.append({
                    "alice_bit": alice_bit,
                    "alice_basis": alice_basis,
                    "polarization": polarization,
                    "angle": angle,
                    "eve_basis": eve_basis,
                    "eve_bit": eve_bit,
                    "bob_basis": bob_basis,
                    "bob_bit": bob_bit,
                    "resent_angle": resent_angle,
                })

            matched = [
                index for index, record in enumerate(records)
                if record["alice_basis"] == record["bob_basis"]
            ]
            if len(matched) >= required_message_bits + 8:
                break
            batch_size = max(32, required_message_bits * 2)

        sample_count = min(32, max(8, len(matched) // 5),
                           len(matched) - required_message_bits)
        sample_indices = set(secrets.SystemRandom().sample(matched, sample_count))
        error_count = sum(
            records[index]["alice_bit"] != records[index]["bob_bit"]
            for index in sample_indices
        )
        error_rate = error_count / sample_count
        eavesdropping_detected = self.eve_toggle.isChecked() and error_rate > 0.11
        key_indices = [index for index in matched if index not in sample_indices]

        self._populate_pulse_table(records, matched, sample_indices,
                                   eavesdropping_detected)
        self.pulse_animation.set_records(records[:MAX_ANIMATED_PULSES])
        self.animation_button.setEnabled(True)
        self.animation_button.setChecked(True)

        if eavesdropping_detected:
            self.results.setPlainText(self.copy["abort"].format(
                errors=error_count, sample=sample_count, error_rate=error_rate))
            return

        alice_key = [records[index]["alice_bit"] for index in key_indices]
        # This teaching model treats classical key reconciliation as ideal.
        bob_key = alice_key
        one_time_pad = bob_key[:required_message_bits]
        cipher_bits = [bit ^ key_bit for bit, key_bit in zip(message_bits, one_time_pad)]
        cipher_bytes = bytes(
            sum(cipher_bits[start + offset] << (7 - offset) for offset in range(8))
            for start in range(0, len(cipher_bits), 8)
        )
        recovered_bytes = bytes(
            cipher ^ sum(one_time_pad[start + offset] << (7 - offset)
                         for offset in range(8))
            for start, cipher in zip(range(0, len(one_time_pad), 8), cipher_bytes)
        )
        recovered_message = recovered_bytes.decode("utf-8")
        self.results.setPlainText(self.copy["success"].format(
            message=message, bits=required_message_bits, pulses=len(records),
            matched=len(matched), sample=sample_count, errors=error_count,
            error_rate=error_rate, key_bits=required_message_bits,
            ciphertext=cipher_bytes.hex(" "), recovered=recovered_message,
        ))

    def _populate_pulse_table(self, records, matched_indices, sample_indices,
                              exchange_aborted):
        matched_set = set(matched_indices)
        self.pulse_table.setUpdatesEnabled(False)
        try:
            self.pulse_table.setRowCount(len(records))
            for row, record in enumerate(records):
                if row not in matched_set:
                    round_label = self.copy["discard"]
                elif row in sample_indices:
                    round_label = (self.copy["protocol_abort"] if exchange_aborted
                                   else self.copy["sample"])
                else:
                    round_label = (self.copy["protocol_abort"] if exchange_aborted
                                   else self.copy["key"])

                eve_text = self.copy["no_eve"]
                if record["eve_basis"] is not None:
                    eve_text = self.copy["eve_value"].format(
                        basis=self._basis_label(record["eve_basis"]),
                        bit=record["eve_bit"],
                    )
                polarization_label = self.copy[{
                    "H": "horizontal", "V": "vertical",
                    "D": "diagonal", "A": "antidiagonal",
                }[record["polarization"]]]
                row_items = [
                    QTableWidgetItem(str(row + 1)),
                    QTableWidgetItem(str(record["alice_bit"])),
                    QTableWidgetItem(self._basis_label(record["alice_basis"])),
                    QTableWidgetItem(polarization_label),
                    QTableWidgetItem(eve_text),
                    QTableWidgetItem(self._basis_label(record["bob_basis"])),
                    QTableWidgetItem(str(record["bob_bit"])),
                    QTableWidgetItem(round_label),
                ]
                row_items[3].setIcon(self.polarization_icons[record["polarization"]])
                row_items[3].setToolTip(f"{polarization_label} — {record['angle']}°")
                for column, item in enumerate(row_items):
                    self.pulse_table.setItem(row, column, item)
            # Do one content measurement after population instead of after
            # every cell insertion. Keep the full translated labels visible.
            self.pulse_table.resizeColumnsToContents()
        finally:
            self.pulse_table.setUpdatesEnabled(True)
        self.pulse_table.scrollToTop()

    def toggle_animation(self, playing):
        if playing and self.pulse_animation.records:
            self.pulse_animation.timer.start()
            self.animation_button.setText(self.copy["animation_pause"])
        else:
            self.pulse_animation.timer.stop()
            if playing:
                self.animation_button.blockSignals(True)
                self.animation_button.setChecked(False)
                self.animation_button.blockSignals(False)
            self.animation_button.setText(self.copy["animation_play"])

    def set_animation_speed(self, value):
        # Slider level 1 takes about five seconds per pulse; level 10 takes
        # about six tenths of a second. The default is close to two seconds.
        self.pulse_animation.step = 0.006 + (value - 1) * 0.0049

    def go_back(self):
        self._closing_for_navigation = True
        self.close()
        self.back_requested.emit()

    def closeEvent(self, event):
        self.pulse_animation.timer.stop()
        event.accept()
        if not self._closing_for_navigation:
            QApplication.quit()


# ─────────────────────────────────────────────
# WINDOW 6 - THEORY & LOCAL SIMULATION
# ─────────────────────────────────────────────
class SimulationWindow(QMainWindow):
    back_requested = Signal()

    def __init__(self, answers, circuit_name):
        super().__init__()
        self.answers      = answers
        self.circuit_name = circuit_name
        self.t            = TRANSLATIONS.get(answers["language"], TRANSLATIONS["English"])
        self.level        = experience_index(answers["experience"], self.t)
        set_language_direction(self, answers["language"])
        self.copy = SIMULATION_COPY[answers["language"]]
        self.audio_copy = AUDIO_COPY[answers["language"]]
        self._speech = None
        self._audio_active = False
        self._audio_lines = []
        self._audio_index = 0
        self._closing_for_navigation = False
        self.setWindowTitle(
            self.copy["beginner_window"] if self.level == 0
            else self.copy["window"])
        self.setMinimumSize(940, 720); self.resize(1080, 880)

        root  = QWidget(); self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(20, 18, 20, 18); outer.setSpacing(10)

        title = QLabel(
            self.copy["beginner_title"] if self.level == 0
            else self.copy["title"])
        title.setFont(QFont("Arial", 19, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(title)

        loc_title = (CIRCUIT_LOCALIZATIONS
                     .get(answers["language"], {})
                     .get(circuit_name, CIRCUITS[circuit_name])
                     .get("title", circuit_name))
        intro_copy = (self.copy["beginner_intro"] if self.level == 0
                      else self.copy["intro"])
        intro = QLabel(intro_copy.format(name=loc_title))
        intro.setWordWrap(True); outer.addWidget(intro)

        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        outer.addWidget(scroll, 1)
        body = QWidget(); body_layout = QVBoxLayout(body)
        body_layout.setSpacing(12); scroll.setWidget(body)

        theory = QTextBrowser()
        theory.setOpenExternalLinks(False); theory.setMinimumHeight(260)

        if circuit_name == BELL_CIRCUIT:
            theory_key = "bell"
            formulas = "|Φ⁺⟩ = (|00⟩+|11⟩)/√2\nP(00) = P(11) = 1/2"

        elif circuit_name == GHZ_CIRCUIT:
            theory_key = "ghz"
            formulas = "|GHZ⟩ = (|000⟩+|111⟩)/√2\nP(000) = P(111) = 1/2"

        else:
            theory_key = "grover"
            formulas = ("(|00⟩+|01⟩+|10⟩+|11⟩)/2\n"
                        "(|00⟩+|01⟩+|10⟩-|11⟩)/2\n"
                        "P(11) = 1; P(00) = P(01) = P(10) = 0")
        if self.level == 0:
            beginner_circuit = BRAND_NEW_CIRCUITS[answers["language"]][circuit_name]
            beginner_steps = beginner_circuit["steps"].replace("\n", "<br>")
            theory.setHtml(
                f"<h3>{BRAND_NEW_CIRCUITS[answers['language']]['heading']}</h3>"
                f"<p>{beginner_circuit['description']}</p>"
                f"<p>{beginner_steps}</p>")
            formulas = ""
        else:
            theory.setHtml(self.copy["theory"][theory_key])

        body_layout.addWidget(theory)
        if formulas:
            add_equation_images(body_layout, formulas)

        # ── Circuit diagram for the selected example ──
        circuit_heading = QLabel(self.copy["circuit_heading"])
        circuit_heading.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        body_layout.addWidget(circuit_heading)
        self.circuit_image = QLabel()
        self.circuit_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.circuit_image.setMinimumHeight(90)
        self.circuit_image.setStyleSheet(
            "background: white; border: 1px solid #e0e0e0; padding: 6px;")
        diagram_qc = build_circuit(self.circuit_name)
        diagram_pixmap = render_circuit_pixmap(diagram_qc)
        if diagram_pixmap is not None and not diagram_pixmap.isNull():
            self.circuit_image.setPixmap(diagram_pixmap.scaled(
                900, 180, Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation))
        else:
            self.circuit_image.setText(
                self.copy["diagram_error"])
            self.circuit_image.setWordWrap(True)
        body_layout.addWidget(self.circuit_image)

        # ── Simulation controls ──
        ctrl = QHBoxLayout()
        ctrl.addWidget(QLabel(self.t.get("shots", "Number of circuit runs:")))
        self.shots = QComboBox()
        self.shots.addItems(["100", "1,000", "10,000"])
        configure_combo(self.shots)
        self.shots.setCurrentIndex(1)
        ctrl.addWidget(self.shots)
        run_btn = QPushButton(self.t.get("run", "▶ Run Local Simulation"))
        run_btn.setStyleSheet(BUTTON_STYLE_GREEN)
        run_btn.clicked.connect(self.run_simulation)
        ctrl.addWidget(run_btn)
        self.audio_button = QPushButton(self.audio_copy["off"])
        self.audio_button.setCheckable(True)
        self.audio_button.setStyleSheet(BUTTON_STYLE_GREEN)
        self.audio_button.toggled.connect(self.toggle_audio_walkthrough)
        ctrl.addWidget(self.audio_button)
        body_layout.addLayout(ctrl)

        self.result = QTextBrowser()
        self.result.setMinimumHeight(200)
        self.result.setPlaceholderText(self.copy["placeholder"])
        self.result.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        body_layout.addWidget(self.result)

        # Optional, expandable source code panel.
        self.code_toggle = QPushButton(self.t.get("show_code", "▶ Show Qiskit Code"))
        self.code_toggle.setCheckable(True)
        self.code_toggle.setStyleSheet(BUTTON_STYLE_GREEN)
        self.code_toggle.toggled.connect(self.toggle_code)
        body_layout.addWidget(self.code_toggle)
        self.code_view = QTextBrowser()
        self.code_view.setFont(QFont("Menlo", 10))
        self.code_view.setLineWrapMode(QTextBrowser.LineWrapMode.NoWrap)
        self.code_view.setPlainText(
            generate_qiskit_code(self.circuit_name, answers["language"]))
        self.code_view.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.code_view.setMinimumHeight(220)
        self.code_view.setVisible(False)
        body_layout.addWidget(self.code_view)

        self.status = QLabel(self.copy["ready"])
        self.status.setWordWrap(True)
        outer.addWidget(self.status)

        # ── Buttons ──
        buttons = QHBoxLayout()
        back_btn = QPushButton(self.copy["back"])
        back_btn.setStyleSheet(BUTTON_STYLE_BACK)
        back_btn.clicked.connect(self.go_back)
        buttons.addWidget(back_btn)
        close_btn = QPushButton(self.t.get("close_application", "✕ Close Application"))
        close_btn.setStyleSheet(BUTTON_STYLE_BACK)
        close_btn.clicked.connect(self.close_application)
        buttons.addWidget(close_btn)
        outer.addLayout(buttons)
        install_feedback_tab(
            self, answers["language"], f"Simulation: {circuit_name}")

    def toggle_code(self, visible):
        self.code_view.setVisible(visible)
        self.code_toggle.setText(
            self.t.get("hide_code", "▼ Hide Qiskit Code") if visible else
            self.t.get("show_code", "▶ Show Qiskit Code"))

    def _set_audio_button(self, checked):
        self.audio_button.blockSignals(True)
        self.audio_button.setChecked(checked)
        self.audio_button.setText(
            self.audio_copy["on"] if checked else self.audio_copy["off"])
        self.audio_button.blockSignals(False)

    def toggle_audio_walkthrough(self, enabled):
        self.audio_button.setText(
            self.audio_copy["on"] if enabled else self.audio_copy["off"])
        if not enabled:
            was_active = self._audio_active
            self._audio_active = False
            if self._speech is not None:
                self._speech.stop()
            if was_active:
                self.status.setText(self.audio_copy["stopped"])
            return

        if QTextToSpeech is None or QLocale is None:
            self.status.setText(self.audio_copy["no_module"])
            self._set_audio_button(False)
            return

        qc = build_circuit(self.circuit_name)
        if qc is None:
            self.status.setText(self.audio_copy["no_circuit"])
            self._set_audio_button(False)
            return

        try:
            if self._speech is None:
                self._speech = QTextToSpeech(self)
                self._speech.stateChanged.connect(self._on_speech_state_changed)
            locale_name = {
                "English": "en_US", "Español": "es_ES", "العربية": "ar_SA",
            }[self.answers["language"]]
            requested_locale = QLocale(locale_name)
            self._speech.setLocale(requested_locale)
            requested_language = requested_locale.language()
            matching_voices = [
                voice for voice in self._speech.availableVoices()
                if voice.locale().language() == requested_language
            ]
            if not matching_voices:
                self._speech.stop()
                self.status.setText(self.audio_copy["no_voice"])
                self._set_audio_button(False)
                return
            self._speech.setVoice(matching_voices[0])
            self._audio_lines = audio_walkthrough_lines(qc, self.answers["language"])
            self._audio_index = 0
            self._audio_active = True
            self.status.setText(self._audio_lines[0])
            self._speak_next_audio_line()
        except Exception:
            self._audio_active = False
            if self._speech is not None:
                self._speech.stop()
            self.status.setText(self.audio_copy["no_voice"])
            self._set_audio_button(False)

    def _on_speech_state_changed(self, state):
        if self._audio_active and state == QTextToSpeech.State.Error:
            self._audio_active = False
            self.status.setText(self.audio_copy["no_voice"])
            self._set_audio_button(False)
            return
        if self._audio_active and state == QTextToSpeech.State.Ready:
            QTimer.singleShot(100, self._speak_next_audio_line)

    def _speak_next_audio_line(self):
        if not self._audio_active:
            return
        if self._audio_index >= len(self._audio_lines):
            self._audio_active = False
            self.status.setText(self.audio_copy["complete"])
            self._set_audio_button(False)
            return
        line = self._audio_lines[self._audio_index]
        self._audio_index += 1
        self._speech.say(line)

    def run_simulation(self):
        if QuantumCircuit is None or Statevector is None:
            self.result.setPlainText(self.copy["no_qiskit"])
            self.status.setText(self.copy["unavailable_status"])
            return
        qc            = build_circuit(self.circuit_name)
        if qc is None:
            self.result.setPlainText(self.copy["unavailable"])
            self.status.setText(self.copy["unavailable_status"])
            return
        state         = Statevector.from_instruction(qc)
        probabilities = state.probabilities_dict()
        shots         = int(self.shots.currentText().replace(",", ""))
        outcomes      = list(probabilities.keys())
        weights       = [float(probabilities[k]) for k in outcomes]
        samples       = random.choices(outcomes, weights=weights, k=shots)
        counts        = Counter(samples)
        width         = qc.num_qubits
        all_outcomes  = [format(i, f"0{width}b") for i in range(2 ** width)]
        rows = []
        for outcome in all_outcomes:
            prob  = float(probabilities.get(outcome, 0.0))
            count = counts.get(outcome, 0)
            rows.append((outcome, f"{prob:.1%}", f"{count:,}", f"{count/shots:.1%}"))
        result_title = (
            self.copy["beginner_result_title"] if self.level == 0
            else self.copy["result_title"]
        ).format(shots=shots)
        result_html = [
            "<html><body style='font-family: sans-serif; color: #243238;'>",
            f"<h3>{html_escape(result_title)}</h3>",
        ]
        if self.level > 0:
            state_lines = [
                f"|{lbl}⟩: {amp.real:+.4f}{amp.imag:+.4f}i"
                for lbl, amp in state.to_dict().items()
                if abs(amp) > 1e-10
            ]
            result_html.extend([
                f"<p><b>{html_escape(self.copy['amplitudes'])}</b></p>",
                f"<pre>{html_escape(chr(10).join(state_lines))}</pre>",
            ])
        headers = (self.copy["outcome"], self.copy["theory_column"],
                   self.copy["count"], self.copy["observed"])
        cell_alignment = (
            "right" if self.answers["language"] == "العربية" else "left")
        result_html.append(
            "<table style='border-collapse: collapse; width: 100%;'>"
            "<thead><tr>" + "".join(
                f"<th style='text-align: {cell_alignment}; background: #e8f3f1; "
                f"padding: 8px; border-bottom: 1px solid #cbdedb;'>"
                f"{html_escape(header)}</th>" for header in headers
            ) + "</tr></thead><tbody>"
        )
        for row in rows:
            result_html.append(
                "<tr>" + "".join(
                    f"<td style='text-align: {cell_alignment}; padding: 7px 8px; "
                    f"border-bottom: 1px solid #e6eeee;'>"
                    f"{html_escape(value)}</td>" for value in row
                ) + "</tr>"
            )
        result_html.extend([
            "</tbody></table>",
            f"<p style='color: #5c6264;'>{html_escape(self.copy['result_note'])}</p>",
            "</body></html>",
        ])
        self.result.setHtml("".join(result_html))
        self.status.setText(self.copy["complete"].format(shots=shots))

    def go_back(self):
        self._closing_for_navigation = True; self.close(); self.back_requested.emit()

    def close_application(self):
        self._closing_for_navigation = True; self.close(); QApplication.quit()

    def closeEvent(self, event):
        if self._speech is not None:
            self._audio_active = False
            self._speech.stop()
        event.accept()
        if not self._closing_for_navigation:
            QApplication.quit()


# ─────────────────────────────────────────────
# APP CONTROLLER - WINDOW NAVIGATION
# ─────────────────────────────────────────────
def launch_questionnaire():
    dialog = QuestionnaireDialog()
    if dialog.exec() != QDialog.DialogCode.Accepted:
        QApplication.quit(); return
    launch_main(dialog.get_answers())


def launch_main(answers):
    window = MainWindow(answers)
    window.back_requested.connect(launch_questionnaire)
    window.next_requested.connect(
        lambda exp: launch_circuit({**answers, "experience": exp}))
    window.show(); app._main_window = window


def launch_circuit(answers):
    window = CircuitWindow(answers)
    window.back_requested.connect(
        lambda: launch_main({k: answers[k] for k in ("country","state","language")}))
    window.next_requested.connect(
        lambda cname: launch_operators(answers, cname))
    window.cryptography_requested.connect(
        lambda: launch_cryptography(answers))
    window.playground_requested.connect(
        lambda: launch_playground(answers))
    window.show(); app._circuit_window = window


def launch_cryptography(answers):
    window = CryptographyWindow(answers)
    window.back_requested.connect(lambda: launch_circuit(answers))
    window.show(); app._cryptography_window = window


def launch_playground(answers):
    window = TwoQubitPlaygroundWindow(answers)
    window.back_requested.connect(lambda: launch_circuit(answers))
    window.show(); app._playground_window = window


def launch_operators(answers, circuit_name):
    window = OperatorsWindow(answers, circuit_name)
    window.back_requested.connect(lambda: launch_circuit(answers))
    window.simulation_requested.connect(
        lambda: launch_simulation(answers, circuit_name))
    window.show(); app._operators_window = window


def launch_simulation(answers, circuit_name):
    window = SimulationWindow(answers, circuit_name)
    window.back_requested.connect(
        lambda: launch_operators(answers, circuit_name))
    window.show(); app._simulation_window = window


# ─────────────────────────────────────────────
# MAIN - APP ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    # ── Apply light grey theme across all windows ──
    app.setStyleSheet(APP_STYLE)

    launch_questionnaire()
    sys.exit(app.exec())
