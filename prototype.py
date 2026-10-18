# ─────────────────────────────────────────────
# Notes of software versions
# VS Code Version 1.108.2 (macOS Ventura 13.7.8)
# Python Version 3.11.5
# Numpy Version 1.26.4
# Matplotlib Version 3.7.2
# Qiskit Version 2.4.2
# PySide6 Version 6.11.2
#
# Automated Installer for Dependecies
# Execute the following before running this Pything script
# A. chmod +x install_dependencies.bash
# B. ./install_dependencies.bash   
# Note: what you should notice is that all the packages above will install and report 'Installation complete.'
#
# References
# Krantz, P., et al. Applied Physics Reviews, vol. 6, no. 2, 2019.
# Perlin, Michael A., et al. Physical Review X, 2026.
# Schwarze, Christopher R., et al. Optics Express, vol. 32, no. 19, 2024.
# Wang, Yuchen, et al. Frontiers in Physics, vol. 8, 2020.
# https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information
# ─────────────────────────────────────────────

# ─────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────
import sys
import re
from io import BytesIO

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui  import QFont, QPixmap
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog, QLabel, QComboBox,
    QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QScrollArea,
    QFrame, QTextBrowser
)

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
    background-color: #f0f0f0;
    color: #1a1a1a;
}
QDialog {
    background-color: #f0f0f0;
}
QFrame {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
}
QScrollArea {
    background-color: #f0f0f0;
    border: none;
}
QScrollArea > QWidget > QWidget {
    background-color: #f0f0f0;
}
QTextBrowser {
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    color: #1a1a1a;
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
    selection-background-color: #2e7d32;
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
    background-color: #2e7d32; color: white;
    border-radius: 8px; padding: 9px; border: none;
}
QPushButton:hover   { background-color: #43a047; }
QPushButton:pressed { background-color: #1b5e20; }
"""

BUTTON_STYLE_BACK = """
QPushButton {
    background-color: #7d2e2e; color: white;
    border: 1px solid #aaaaaa; border-radius: 8px; padding: 8px;
}
QPushButton:hover   { background-color: #e0e0e0; color: #333; }
QPushButton:pressed { background-color: #cccccc; }
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
        "circuit": "🔌 YOUR SELECTED CIRCUIT", "novice": "Novice Level",
        "school": "Secondary-School Level", "university": "University Level",
        "description": "Explanation", "circuit_help": "Circuit overview",
        "matrix_label": "Gate Matrix:",
    },
    "Español": {
        "title": "Constructor de Circuitos Cuánticos Qiskit", "main": "⚛️ Constructor de Circuitos Cuánticos",
        "country": "País:", "region": "Estado / Provincia:", "language": "Idioma preferido:",
        "continue": "✔ Continuar", "experience": "Nivel de experiencia:", "begin": "▶ Comenzar tutorial",
        "back": "◀ Atrás", "ready": "Estado: Listo ✅", "running": "Seleccionado: {value}",
        "choose_circuit": "Elige un circuito para explorar:", "explore": "▶ Explorar circuito",
        "operators": "⚛️ Guía de Operadores Cuánticos", "circuit": "🔌 TU CIRCUITO SELECCIONADO",
        "novice": "Nivel principiante", "school": "Nivel secundaria", "university": "Nivel universitario",
        "description": "Explicación", "circuit_help": "Resumen del circuito",
        "matrix_label": "Matriz de la Puerta:",
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

LANGUAGES = list(TRANSLATIONS.keys())
COUNTRIES  = {
    "United States": ["Alabama","Alaska","Arizona","California","Florida",
                      "Massachusetts","New York","Texas","Other / N/A"],
    "Canada":        ["Alberta","British Columbia","Ontario","Quebec","Other / N/A"],
    "United Kingdom":["England","Northern Ireland","Scotland","Wales","Other / N/A"],
    "India":         ["Delhi","Gujarat","Karnataka","Maharashtra","Tamil Nadu","Other / N/A"],
    "Other":         ["Not applicable"],
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


# ─────────────────────────────────────────────
# OPERATOR TRANSLATIONS
# ─────────────────────────────────────────────
OPERATOR_LOCALIZATIONS = {
    "Español": {
        "categories": ["PUERTAS DE UN SOLO QUBIT","PUERTAS DE ROTACIÓN",
                        "PUERTAS DE VARIOS QUBITS","OPERACIONES DEL CIRCUITO","CONTROL CLÁSICO"],
        "levels": ["Nivel principiante: ","Nivel de secundaria: ","Nivel universitario: "],
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
    if "Bell" in circuit_name:
        qc = QuantumCircuit(2, name="Bell State")
        qc.h(0); qc.cx(0, 1)
    elif "GHZ" in circuit_name:
        qc = QuantumCircuit(3, name="GHZ State")
        qc.h(0); qc.cx(0, 1); qc.cx(0, 2)
    elif "Grover" in circuit_name:
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


def generate_qiskit_code(circuit_name):
    """Return runnable local Qiskit code for the selected example circuit."""
    if "Bell" in circuit_name:
        circuit = """qc = QuantumCircuit(2, name="Bell State")
qc.h(0)
qc.cx(0, 1)"""
    elif "GHZ" in circuit_name:
        circuit = """qc = QuantumCircuit(3, name="GHZ State")
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 2)"""
    else:
        circuit = """qc = QuantumCircuit(2, name="Grover Search")
qc.h([0, 1])
qc.cz(0, 1)  # Oracle marks |11>
qc.h([0, 1])
qc.x([0, 1])
qc.cz(0, 1)
qc.x([0, 1])
qc.h([0, 1])"""
    return (
        "from qiskit import QuantumCircuit\n"
        "from qiskit.quantum_info import Statevector\n\n"
        f"{circuit}\n\n"
        "# Simulate the ideal circuit locally and sample measurements\n"
        "shots = 1000  # Change this to 100, 1000, or 10000\n"
        "state = Statevector.from_instruction(qc)\n"
        "counts = state.sample_counts(shots=shots)\n"
        'print("Circuit:")\n'
        "print(qc.draw())\n"
        'print(f"Measurement counts ({shots} shots): {counts}")\n'
        'print("Exact probabilities:", state.probabilities_dict())\n'
    )


def experience_index(experience_text, t):
    if experience_text == t["novice"]:  return 0
    if experience_text == t["school"]:  return 1
    return 2


# ─────────────────────────────────────────────
# WINDOW 1 - QUESTIONNAIRE
# ─────────────────────────────────────────────
class QuestionnaireDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quantum Circuit Builder - Welcome")
        self.setMinimumWidth(470)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowCloseButtonHint)

        self.country  = QComboBox(); self.country.addItems(COUNTRIES.keys())
        self.region   = QComboBox()
        self.language = QComboBox(); self.language.addItems(LANGUAGES)
        self.country.currentTextChanged.connect(self.update_regions)
        self.update_regions(self.country.currentText())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(16)

        title = QLabel("⚛️ Quantum Circuit Builder")
        title.setFont(QFont("Arial", 19, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        form = QFormLayout(); form.setSpacing(10)
        form.addRow("Country:",            self.country)
        form.addRow("State / Province:",   self.region)
        form.addRow("Preferred language:", self.language)
        layout.addLayout(form)

        btn = QPushButton("✔ Continue")
        btn.setStyleSheet(BUTTON_STYLE_GREEN)
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

    def update_regions(self, country):
        self.region.clear()
        self.region.addItems(COUNTRIES.get(country, ["Not applicable"]))

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
        self._closing_for_navigation = False
        self.setWindowTitle(self.t["title"])
        self.setMinimumSize(620, 350)

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


# ─────────────────────────────────────────────
# WINDOW 3 - CIRCUIT SELECTION
# ─────────────────────────────────────────────
class CircuitWindow(QMainWindow):
    back_requested = Signal()
    next_requested = Signal(str)

    # ── Localized circuit names (index matches CIRCUITS key order) ──
    CIRCUIT_NAMES_BY_LANGUAGE = {
        "English":  ["The Bell State Circuit (Entanglement)",
                     "Three-Qubit GHZ State Circuit",
                     "Two-Qubit Grover Search Circuit"],
        "Español":  ["El Circuito de Estado Bell (Entrelazamiento)",
                     "Circuito de Estado GHZ de Tres Qubits",
                     "Circuito de Búsqueda de Grover de Dos Qubits"],
        "Français": ["Le Circuit d'État de Bell (Intrication)",
                     "Circuit d'État GHZ à Trois Qubits",
                     "Circuit de Recherche de Grover à Deux Qubits"],
        "Deutsch":  ["Bell-Zustand-Schaltkreis (Verschränkung)",
                     "Drei-Qubit-GHZ-Zustand-Schaltkreis",
                     "Zwei-Qubit-Grover-Suchschaltkreis"],
        "日本語":   ["ベル状態回路（エンタングルメント）",
                     "3量子ビットGHZ状態回路",
                     "2量子ビットグローバー探索回路"],
        "中文":     ["贝尔态电路（纠缠）",
                     "三量子比特GHZ态电路",
                     "双量子比特Grover搜索电路"],
        "हिन्दी":   ["बेल स्टेट सर्किट (उलझाव)",
                     "तीन-क्यूबिट GHZ स्टेट सर्किट",
                     "दो-क्यूबिट ग्रोवर सर्च सर्किट"],
        "Português":["O Circuito de Estado Bell (Entrelaçamento)",
                     "Circuito de Estado GHZ de Três Qubits",
                     "Circuito de Busca de Grover de Dois Qubits"],
    }
    CANONICAL_NAMES = list(CIRCUITS.keys())

    def __init__(self, answers):
        super().__init__()
        self.answers = answers
        self.t = TRANSLATIONS.get(answers["language"], TRANSLATIONS["English"])
        self._closing_for_navigation = False
        self.setWindowTitle(self.t["title"]); self.setMinimumSize(650, 400)

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
        layout.addWidget(self.circuit)

        explore = QPushButton(self.t["explore"])
        explore.setStyleSheet(BUTTON_STYLE_GREEN)
        explore.clicked.connect(self.explore)
        layout.addWidget(explore)

        back = QPushButton(self.t["back"])
        back.setStyleSheet(BUTTON_STYLE_BACK)
        back.clicked.connect(self.go_back)
        layout.addWidget(back)

        self.status = QLabel(self.t["ready"])
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status)

    def canonical_circuit_name(self):
        idx = self.circuit.currentIndex()
        return self.CANONICAL_NAMES[idx] if 0 <= idx < len(self.CANONICAL_NAMES) \
               else self.CANONICAL_NAMES[0]

    def go_back(self):
        self._closing_for_navigation = True; self.close(); self.back_requested.emit()

    def explore(self):
        self._closing_for_navigation = True; self.close()
        self.next_requested.emit(self.canonical_circuit_name())

    def closeEvent(self, event):
        event.accept()
        if not self._closing_for_navigation:
            QApplication.quit()


# ─────────────────────────────────────────────
# WINDOW 4 - QUANTUM OPERATORS GUIDE + SELECTED CIRCUIT
# ─────────────────────────────────────────────
class OperatorsWindow(QMainWindow):
    back_requested       = Signal()
    simulation_requested = Signal()

    def __init__(self, answers, circuit_name):
        super().__init__()
        self.answers      = answers
        self.circuit_name = circuit_name
        self.t            = TRANSLATIONS.get(answers["language"], TRANSLATIONS["English"])
        self._closing_for_navigation = False
        self.level        = experience_index(answers["experience"], self.t)
        self.setWindowTitle(self.t["operators"])
        self.setMinimumSize(860, 700); self.resize(1020, 880)

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

        localized = OPERATOR_LOCALIZATIONS.get(answers["language"])

        for cat_idx, (category, items) in enumerate(OPERATORS):
            # ── Category heading ──
            disp_cat = localized["categories"][cat_idx] if localized else category
            heading  = QLabel(disp_cat)
            heading.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            heading.setStyleSheet(
                "background: #e8f5e9; padding: 8px; border-radius: 5px; border: none;")
            content_layout.addWidget(heading)

            for symbol, name, novice, school, university in items:
                # ── Gate card ──
                card        = QFrame(); card.setFrameShape(QFrame.Shape.StyledPanel)
                card_layout = QVBoxLayout(card); card_layout.setSpacing(8)

                # Localised name and description
                if localized and symbol in localized["gates"]:
                    display_name, descriptions = localized["gates"][symbol]
                    description = descriptions[self.level]
                    level_label = localized["levels"][self.level]
                else:
                    display_name = name
                    description  = (novice, school, university)[self.level]
                    level_label  = ""

                # Gate title
                gate_title = QLabel(f"{symbol}  —  {display_name}")
                gate_title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
                card_layout.addWidget(gate_title)

                # ── Proper 2-D matrix image ──
                matrix_pixmap = render_gate_matrix_image(symbol)
                if matrix_pixmap is not None and not matrix_pixmap.isNull():
                    mat_lbl_outer = QHBoxLayout()
                    mat_lbl = QLabel()
                    mat_lbl.setPixmap(matrix_pixmap)
                    mat_lbl.setAlignment(
                        Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                    mat_lbl.setStyleSheet(
                        "background: white; padding: 7px 12px; "
                        "border-radius: 6px; border: 1px solid #d8d8d8;")
                    mat_lbl.setToolTip(f"{self.t.get('matrix_label','Gate Matrix:')} {symbol}")
                    mat_lbl_outer.addWidget(mat_lbl)
                    mat_lbl_outer.addStretch()
                    card_layout.addLayout(mat_lbl_outer)

                # Description text (equations stripped out — rendered below)
                prose = text_without_rendered_equations(description)
                text_lbl = QLabel(f"{self.t['description']}: {level_label}{prose}")
                text_lbl.setWordWrap(True)
                card_layout.addWidget(text_lbl)

                # Inline equation images (non-matrix formulas)
                add_equation_images(card_layout, description)

                content_layout.addWidget(card)

        # ── Selected circuit section ──
        circuit_heading = QLabel(self.t["circuit"])
        circuit_heading.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        circuit_heading.setStyleSheet(
            "background: #e3f2fd; padding: 9px; border-radius: 5px; border: none;")
        content_layout.addWidget(circuit_heading)

        circuit_data        = CIRCUITS[circuit_name]
        localized_circuits  = CIRCUIT_LOCALIZATIONS.get(answers["language"], {})
        display_circuit     = localized_circuits.get(circuit_name, circuit_data)
        circuit_description = display_circuit["description"]
        circuit_steps       = display_circuit["steps"]
        display_title       = display_circuit.get("title", circuit_name)

        circuit_text = QLabel(
            f"{display_title}\n\n"
            f"{text_without_rendered_equations(circuit_description)}\n\n"
            f"{text_without_rendered_equations(circuit_steps)}")
        circuit_text.setWordWrap(True)
        circuit_text.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse)
        content_layout.addWidget(circuit_text)
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
                diagram.setToolTip("Graphical quantum circuit diagram")
            else:
                diagram = QLabel(
                    qc.draw(output="text", fold=-1).__str__()
                    + "\n\nFor graphical diagrams: "
                      "python -m pip install 'qiskit[visualization]'")
                diagram.setFont(QFont("Menlo", 11))
                diagram.setTextInteractionFlags(
                    Qt.TextInteractionFlag.TextSelectableByMouse)
        else:
            diagram = QLabel(
                "Qiskit not installed.\n"
                "Install: python -m pip install 'qiskit[visualization]'")
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

        sim_btn = QPushButton("▶ Theory & Local Simulation")
        sim_btn.setStyleSheet(BUTTON_STYLE_GREEN)
        sim_btn.clicked.connect(self.open_simulation)
        buttons.addWidget(sim_btn)

        close_btn = QPushButton("✕ Close")
        close_btn.setStyleSheet(BUTTON_STYLE_BACK)
        close_btn.clicked.connect(self.close_application)
        buttons.addWidget(close_btn)
        outer.addLayout(buttons)

    def go_back(self):
        self._closing_for_navigation = True; self.close(); self.back_requested.emit()

    def open_simulation(self):
        self._closing_for_navigation = True; self.close()
        self.simulation_requested.emit()

    def close_application(self):
        self._closing_for_navigation = True; self.close(); QApplication.quit()

    def closeEvent(self, event):
        event.accept()
        if not self._closing_for_navigation:
            QApplication.quit()


# ─────────────────────────────────────────────
# WINDOW 5 - THEORY & LOCAL SIMULATION
# ─────────────────────────────────────────────
class SimulationWindow(QMainWindow):
    back_requested = Signal()

    def __init__(self, answers, circuit_name):
        super().__init__()
        self.answers      = answers
        self.circuit_name = circuit_name
        self.t            = TRANSLATIONS.get(answers["language"], TRANSLATIONS["English"])
        self._closing_for_navigation = False
        self.setWindowTitle("Quantum Theory & Local Simulation")
        self.setMinimumSize(860, 660); self.resize(1020, 820)

        root  = QWidget(); self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(20, 18, 20, 18); outer.setSpacing(10)

        title = QLabel("⚛️ Theoretical Expectations & Local Simulation")
        title.setFont(QFont("Arial", 19, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(title)

        loc_title = (CIRCUIT_LOCALIZATIONS
                     .get(answers["language"], {})
                     .get(circuit_name, CIRCUITS[circuit_name])
                     .get("title", circuit_name))
        intro = QLabel(
            f"Circuit: {loc_title}\n"
            "The theory below is the ideal noiseless prediction. "
            "The simulator runs locally on this computer.")
        intro.setWordWrap(True); outer.addWidget(intro)

        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        outer.addWidget(scroll, 1)
        body = QWidget(); body_layout = QVBoxLayout(body)
        body_layout.setSpacing(12); scroll.setWidget(body)

        theory = QTextBrowser()
        theory.setOpenExternalLinks(False); theory.setMinimumHeight(260)

        if "Bell" in circuit_name:
            theory.setHtml("""
            <h3>Gate-by-gate theoretical expectations</h3>
            <p><b>Initial state:</b> |00⟩.</p>
            <p><b>1. H on qubit 0</b><br>
            Creates (|00⟩+|10⟩)/√2. Each branch has probability 1/2.</p>
            <p><b>2. CNOT (0→1)</b><br>
            Final Bell state |Φ⁺⟩ = (|00⟩+|11⟩)/√2.</p>
            <p><b>Expected:</b> P(00)=1/2, P(11)=1/2, P(01)=P(10)=0.</p>""")
            formulas = "|Φ⁺⟩ = (|00⟩+|11⟩)/√2\nP(00) = P(11) = 1/2"

        elif "GHZ" in circuit_name:
            theory.setHtml("""
            <h3>Gate-by-gate theoretical expectations</h3>
            <p><b>Initial state:</b> |000⟩.</p>
            <p><b>1. H on qubit 0</b><br>(|000⟩+|100⟩)/√2.</p>
            <p><b>2. CNOT(0→1)</b><br>(|000⟩+|110⟩)/√2.</p>
            <p><b>3. CNOT(0→2)</b><br>|GHZ⟩ = (|000⟩+|111⟩)/√2.</p>
            <p><b>Expected:</b> P(000)=1/2, P(111)=1/2; all other outcomes 0.</p>""")
            formulas = "|GHZ⟩ = (|000⟩+|111⟩)/√2\nP(000) = P(111) = 1/2"

        else:   # Grover
            theory.setHtml("""
            <h3>Gate-by-gate theoretical expectations (Grover Search)</h3>
            <p><b>Target state:</b> |11⟩. N=4 states, k=1 marked. Optimal iterations = 1.</p>
            <p><b>1. H⊗H</b><br>
            (|00⟩+|01⟩+|10⟩+|11⟩)/2. Each state: amplitude 1/2, probability 1/4.</p>
            <p><b>2. CZ Oracle</b><br>
            Phase-flips |11⟩: (|00⟩+|01⟩+|10⟩−|11⟩)/2. Probabilities unchanged.</p>
            <p><b>3. Diffusion (H⊗H → X⊗X → CZ → X⊗X → H⊗H)</b><br>
            Inversion about the mean. Mean amplitude = (1/2+1/2+1/2−1/2)/4 = 1/4.<br>
            New amplitudes: |00⟩, |01⟩, |10⟩ → 0; |11⟩ → 1.</p>
            <p><b>Expected:</b> P(11)=1, P(00)=P(01)=P(10)=0.<br>
            One iteration is theoretically optimal for N=4, k=1.</p>""")
            formulas = ("(|00⟩+|01⟩+|10⟩+|11⟩)/2\n"
                        "(|00⟩+|01⟩+|10⟩-|11⟩)/2\n"
                        "P(11) = 1; P(00) = P(01) = P(10) = 0")

        body_layout.addWidget(theory)
        add_equation_images(body_layout, formulas)

        # ── Circuit diagram for the selected example ──
        circuit_heading = QLabel("Selected quantum circuit")
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
                "Circuit diagram unavailable. Install matplotlib and Qiskit visualization support.")
            self.circuit_image.setWordWrap(True)
        body_layout.addWidget(self.circuit_image)

        # ── Simulation controls ──
        ctrl = QHBoxLayout()
        ctrl.addWidget(QLabel("Number of measurement shots:"))
        self.shots = QComboBox()
        self.shots.addItems(["100", "1,000", "10,000"])
        self.shots.setCurrentIndex(1)
        ctrl.addWidget(self.shots)
        run_btn = QPushButton("▶ Run Local Simulation")
        run_btn.setStyleSheet(BUTTON_STYLE_GREEN)
        run_btn.clicked.connect(self.run_simulation)
        ctrl.addWidget(run_btn)
        body_layout.addLayout(ctrl)

        self.result = QTextBrowser()
        self.result.setMinimumHeight(200)
        self.result.setPlaceholderText(
            "Click Run Local Simulation to see sampled measurement counts.")
        body_layout.addWidget(self.result)

        # Optional, expandable source code panel.
        self.code_toggle = QPushButton("▶ Show Qiskit Code")
        self.code_toggle.setCheckable(True)
        self.code_toggle.setStyleSheet(BUTTON_STYLE_GREEN)
        self.code_toggle.toggled.connect(self.toggle_code)
        body_layout.addWidget(self.code_toggle)
        self.code_view = QTextBrowser()
        self.code_view.setFont(QFont("Menlo", 10))
        self.code_view.setLineWrapMode(QTextBrowser.LineWrapMode.NoWrap)
        self.code_view.setPlainText(generate_qiskit_code(self.circuit_name))
        self.code_view.setMinimumHeight(220)
        self.code_view.setVisible(False)
        body_layout.addWidget(self.code_view)

        self.status = QLabel("Status: Ready — simulation stays on this laptop.")
        self.status.setWordWrap(True)
        outer.addWidget(self.status)

        # ── Buttons ──
        buttons = QHBoxLayout()
        back_btn = QPushButton(self.t["back"])
        back_btn.setStyleSheet(BUTTON_STYLE_BACK)
        back_btn.clicked.connect(self.go_back)
        buttons.addWidget(back_btn)
        close_btn = QPushButton("✕ Close Application")
        close_btn.setStyleSheet(BUTTON_STYLE_BACK)
        close_btn.clicked.connect(self.close_application)
        buttons.addWidget(close_btn)
        outer.addLayout(buttons)

    def toggle_code(self, visible):
        self.code_view.setVisible(visible)
        self.code_toggle.setText("▼ Hide Qiskit Code" if visible else "▶ Show Qiskit Code")

    def run_simulation(self):
        if QuantumCircuit is None or Statevector is None:
            self.result.setPlainText(
                "Qiskit not installed.\n\n"
                "python -m pip install 'qiskit[visualization]' matplotlib")
            self.status.setText("Simulation unavailable: install Qiskit first.")
            return
        import random
        qc            = build_circuit(self.circuit_name)
        state         = Statevector.from_instruction(qc)
        probabilities = state.probabilities_dict()
        shots         = int(self.shots.currentText().replace(",", ""))
        outcomes      = list(probabilities.keys())
        weights       = [float(probabilities[k]) for k in outcomes]
        samples       = random.choices(outcomes, weights=weights, k=shots)
        counts        = {k: samples.count(k) for k in sorted(set(samples))}
        width         = qc.num_qubits
        all_outcomes  = [format(i, f"0{width}b") for i in range(2 ** width)]
        rows = []
        for outcome in all_outcomes:
            prob  = float(probabilities.get(outcome, 0.0))
            count = counts.get(outcome, 0)
            rows.append(
                f"{outcome:<10} {prob:>10.1%} {count:>12} {count/shots:>12.1%}")
        state_lines = [
            f"|{lbl}⟩: {amp.real:+.4f}{amp.imag:+.4f}i"
            for lbl, amp in state.to_dict().items()
            if abs(amp) > 1e-10
        ]
        self.result.setPlainText(
            f"LOCAL STATEVECTOR SIMULATION — {shots:,} shots\n\n"
            f"Final state amplitudes:\n  " + "\n  ".join(state_lines) + "\n\n"
            f"{'Outcome':<10} {'Theory':>10} {'Sample count':>12} {'Observed':>12}\n"
            f"{'-'*48}\n" + "\n".join(rows) + "\n\n"
            "Theory = exact ideal probability; "
            "Observed = this run's sampled fraction.")
        self.status.setText(
            f"Simulation complete: {shots:,} shots. No cloud or hardware used.")

    def go_back(self):
        self._closing_for_navigation = True; self.close(); self.back_requested.emit()

    def close_application(self):
        self._closing_for_navigation = True; self.close(); QApplication.quit()

    def closeEvent(self, event):
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
    window.show(); app._circuit_window = window


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