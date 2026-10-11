# ─────────────────────────────────────────────
# Notes of software versions
# VS Code Version 1.108.2 (macOS Ventura 13.7.8)
# Python Version 3.11.5   (Python version)
# Numpy Version 1.26.4    (Data analysis library)
# Matplotlib Version 3.7.2 (Graphical library)
# Qiskit Version 2.4.2    (Quantum modeling SDK)
# PySide6 Version 6.11.2  (GUI API)

# References
# Krantz, P., et al. “A Quantum Engineer’s Guide to superconducting qubits.” Applied Physics Reviews, vol. 6, no. 2, 1 June 2019, https://doi.org/10.1063/1.5089550. 
# Perlin, Michael A., et al. “Fault-tolerant execution of error-corrected quantum algorithms.” Physical Review X, 9 Oct. 2026, https://doi.org/10.1103/gnq3-c2df. 
# Schwarze, Christopher R., et al. “Experimental demonstration of a grover-michelson interferometer.” Optics Express, vol. 32, no. 19, 6 Sept. 2024, p. 34116, https://doi.org/10.1364/oe.532364. 
# Wang, Yuchen, et al. “Qudits and high-dimensional quantum computing.” Frontiers in Physics, vol. 8, 10 Nov. 2020, https://doi.org/10.3389/fphy.2020.589504. 
# 
# https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/quantum-circuits/circuits
# https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/introduction 
# ─────────────────────────────────────────────

# ─────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────
import sys
import re
from io import BytesIO

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog, QLabel, QComboBox,
    QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QScrollArea,
    QFrame, QMessageBox, QTextBrowser
)

try:
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector
except ImportError:
    QuantumCircuit = None
    Statevector = None


# ─────────────────────────────────────────────
# SHARED STYLES
# ─────────────────────────────────────────────
BUTTON_STYLE_GREEN = """
QPushButton { background-color: #2e7d32; color: white; border-radius: 8px; padding: 9px; }
QPushButton:hover { background-color: #43a047; }
QPushButton:pressed { background-color: #1b5e20; }
"""
BUTTON_STYLE_BACK = """
QPushButton { background-color: transparent; color: gray; border: 1px solid gray; border-radius: 8px; padding: 8px; }
QPushButton:hover { background-color: #f0f0f0; color: #333; }
QPushButton:pressed { background-color: #e0e0e0; }
"""


# ─────────────────────────────────────────────
# TRANSLATIONS
# Keep interface text here so it is straightforward to edit.
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
    },
    "Français": {
        "title": "Constructeur de Circuits Quantiques Qiskit", "main": "⚛️ Constructeur de Circuits Quantiques",
        "country": "Pays :", "region": "État / Province :", "language": "Langue préférée :",
        "continue": "✔ Continuer", "experience": "Niveau d’expérience :", "begin": "▶ Commencer le tutoriel",
        "back": "◀ Retour", "ready": "Statut : Prêt ✅", "running": "Sélection : {value}",
        "choose_circuit": "Choisissez un circuit à explorer :", "explore": "▶ Explorer le circuit",
        "operators": "⚛️ Guide des opérateurs quantiques", "circuit": "🔌 VOTRE CIRCUIT SÉLECTIONNÉ",
        "novice": "Débutant", "school": "Niveau secondaire", "university": "Niveau universitaire",
        "description": "Explication", "circuit_help": "Présentation du circuit",
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
    },
}

LANGUAGES = list(TRANSLATIONS.keys())
COUNTRIES = {
    "United States": ["Alabama", "Alaska", "Arizona", "California", "Florida", "Massachusetts", "New York", "Texas", "Other / N/A"],
    "Canada": ["Alberta", "British Columbia", "Ontario", "Quebec", "Other / N/A"],
    "United Kingdom": ["England", "Northern Ireland", "Scotland", "Wales", "Other / N/A"],
    "India": ["Delhi", "Gujarat", "Karnataka", "Maharashtra", "Tamil Nadu", "Other / N/A"],
    "Other": ["Not applicable"],
}


# ─────────────────────────────────────────────
# OPERATOR CONTENT
# Edit descriptions here. Each operator has a novice, school, and university
# explanation so the GUI code stays separate from educational content.
# ─────────────────────────────────────────────
OPERATORS = [
    ("SINGLE-QUBIT GATES", [
        ("H", "Hadamard", "Creates an even mix of |0⟩ and |1⟩ when applied to |0⟩.", "H|0⟩=(|0⟩+|1⟩)/√2. It creates an equal superposition from a computational-basis state.", "H = 1/√2 [[1,1],[1,-1]]. It is unitary and Hermitian (H²=I), exchanging X and Z measurement bases."),
        ("X", "Pauli-X / NOT", "Flips |0⟩ to |1⟩ and |1⟩ to |0⟩, like a switch.", "X swaps the computational basis states and acts like a classical NOT operation on basis states.", "X = [[0,1],[1,0]] = σx; it implements a π rotation about the Bloch-sphere X axis, up to global phase."),
        ("Y", "Pauli-Y", "Flips the qubit and also changes its phase.", "Y maps |0⟩ to i|1⟩ and |1⟩ to -i|0⟩.", "Y = [[0,-i],[i,0]] = σy; it is a Pauli operator and corresponds to a π rotation about Y up to global phase."),
        ("Z", "Pauli-Z", "Leaves |0⟩ alone and changes the phase of |1⟩.", "Z|0⟩=|0⟩ and Z|1⟩=-|1⟩; it changes relative phase, not computational-basis probabilities immediately.", "Z=diag(1,-1)=σz. It is a phase-flip operator and a generator of rotations around the Bloch-sphere Z axis."),
        ("S", "S phase gate", "Adds a quarter-turn phase to the |1⟩ part of a state.", "S=diag(1,i), equivalent to a π/2 phase rotation; S²=Z.", "S=T²=diag(1,i) is a Clifford gate; conjugation maps X to Y and leaves Z invariant."),
        ("T", "T gate", "Adds a smaller phase change than the S gate.", "T=diag(1,e^(iπ/4)); it supplies a π/4 phase rotation.", "T is a non-Clifford π/8 gate and, together with Clifford operations, supports universal fault-tolerant computation."),
        ("SX", "Square-root of X", "Performs half of an X-like rotation; applying it twice gives X up to global phase.", "SX²=X up to a physically unobservable global phase.", "SX=(I-iX)/√2 under a common convention; hardware-native SX and RZ gates are common on IBM systems."),
    ]),
    ("ROTATION GATES", [
        ("RX", "X-axis rotation", "Rotates a qubit around the X axis by an angle you choose.", "RX(θ) rotates the Bloch vector by θ about X.", "RX(θ)=exp(-iθX/2); parameterized rotations are used in variational algorithms such as VQE and QAOA."),
        ("RY", "Y-axis rotation", "Rotates a qubit around the Y axis by a chosen angle.", "RY(θ) rotates around Y and has real matrix entries.", "RY(θ)=exp(-iθY/2); combined with RZ rotations it supports Euler-angle decompositions of single-qubit unitaries."),
        ("RZ", "Z-axis rotation", "Changes the relative phase by rotating around the Z axis.", "RZ(θ) applies opposite phase factors to |0⟩ and |1⟩.", "RZ(θ)=diag(e^{-iθ/2},e^{iθ/2}); it can often be implemented virtually through a frame change on superconducting hardware."),
        ("P", "Phase gate", "Adds a selectable phase to the |1⟩ part of the state.", "P(θ)=diag(1,e^{iθ}); S and T are special angles.", "P(θ) is a U(1) phase operation; parameterized phases can be optimized using gradient or parameter-shift methods."),
    ]),
    ("MULTI-QUBIT GATES", [
        ("CX", "CNOT / controlled-X", "If the control qubit is 1, flip the target qubit. This can entangle qubits.", "CX maps |c,t⟩ to |c,t XOR c⟩. A Hadamard followed by CX creates a Bell state.", "CX=|0⟩⟨0|⊗I+|1⟩⟨1|⊗X; an entangling two-qubit gate that, with arbitrary one-qubit gates, is universal."),
        ("SWAP", "SWAP", "Exchanges the states stored in two qubits.", "SWAP|a,b⟩=|b,a⟩ and is commonly decomposed into three CX gates.", "SWAP=(I⊗I+X⊗X+Y⊗Y+Z⊗Z)/2; routing swaps can dominate overhead on limited-connectivity devices."),
        ("CCX", "Toffoli / controlled-controlled-X", "Flips the target only when both control qubits are 1.", "CCX performs a reversible AND-like operation on computational-basis states.", "The Toffoli gate is a three-qubit reversible gate; decompositions use multiple entangling and single-qubit gates."),
        ("CSWAP", "Fredkin / controlled-SWAP", "Swaps two target qubits only when the control is 1.", "CSWAP conditionally exchanges two qubit states and is used in the SWAP test.", "Fredkin is a controlled permutation gate and preserves the target pair's Hamming weight."),
    ]),
    ("CIRCUIT OPERATIONS", [
        ("Measure", "Measurement", "Reads a qubit as 0 or 1; the result is probabilistic for a superposition.", "For α|0⟩+β|1⟩, measurement yields 0 with probability |α|² and 1 with probability |β|².", "Computational-basis measurement follows the Born rule; measurement is non-unitary and stores outcomes in classical bits."),
        ("Reset", "Reset", "Returns a qubit to |0⟩.", "Reset is a non-unitary operation that prepares the qubit in |0⟩.", "Reset is a quantum channel, not a unitary gate; implementations may use measurement and conditional correction or dissipation."),
        ("Barrier", "Barrier", "A marker that separates circuit sections and can constrain compiler rearrangement.", "A barrier is a compiler directive, not a physical quantum operation.", "Barriers constrain transpiler optimization across a circuit boundary and are useful for preserving intended layers."),
    ]),
    ("CLASSICAL CONTROL", [
        ("If", "Classical condition", "Choose an operation based on an earlier measurement result.", "Classical feed-forward applies gates conditionally on classical bits.", "Dynamic circuits combine classical control flow with quantum operations, enabling adaptive measurement and correction."),
        ("For", "Repeated circuit / loop", "Repeats a group of operations.", "A repeated subcircuit can implement iterative algorithms or repeated gate sequences.", "Loop constructs describe parameterized circuit families; backend support and compilation depend on the target interface."),
        ("Unitary", "Unitary operation", "A custom operation that preserves valid quantum-state probabilities.", "A unitary matrix U obeys U†U=I and can represent a reversible quantum operation.", "An n-qubit unitary is a 2ⁿ×2ⁿ matrix satisfying U†U=I; synthesis decomposes it into the target basis gates."),
    ]),
]


# ─────────────────────────────────────────────
# OPERATOR TRANSLATIONS
# Each gate's name and explanation is localized for every supported language.
# The selected experience level controls the translated explanation framing.
# Technical symbols and standard mathematical notation are kept unchanged.
# ─────────────────────────────────────────────
OPERATOR_LOCALIZATIONS = {
    "Español": {
        "categories": ["PUERTAS DE UN SOLO QUBIT", "PUERTAS DE ROTACIÓN", "PUERTAS DE VARIOS QUBITS", "OPERACIONES DEL CIRCUITO", "CONTROL CLÁSICO"],
        "levels": ["Nivel principiante: ", "Nivel de secundaria: ", "Nivel universitario: "],
        "gates": {
            "H": ("Hadamard", ["Crea una combinación equilibrada de |0⟩ y |1⟩ cuando se aplica a |0⟩.", "H|0⟩=(|0⟩+|1⟩)/√2. Crea una superposición equilibrada a partir de un estado de la base computacional.", "H = 1/√2 [[1,1],[1,-1]]. Es unitario y hermítico (H²=I), e intercambia las bases de medición X y Z."]),
            "X": ("Pauli-X / NOT", ["Intercambia |0⟩ y |1⟩, como un interruptor.", "Intercambia los estados de la base computacional y actúa como una operación NOT clásica en esos estados.", "X = [[0,1],[1,0]] = σx; implementa una rotación de π alrededor del eje X de la esfera de Bloch, salvo una fase global."]),
            "Y": ("Pauli-Y", ["Invierte el qubit y también cambia su fase.", "Y transforma |0⟩ en i|1⟩ y |1⟩ en -i|0⟩.", "Y = [[0,-i],[i,0]] = σy; es un operador de Pauli y corresponde a una rotación de π alrededor de Y, salvo una fase global."]),
            "Z": ("Pauli-Z", ["Deja |0⟩ sin cambios y cambia la fase de |1⟩.", "Z|0⟩=|0⟩ y Z|1⟩=-|1⟩; cambia la fase relativa, pero no de inmediato las probabilidades de la base computacional.", "Z=diag(1,-1)=σz. Es una operación de cambio de fase y genera rotaciones alrededor del eje Z de la esfera de Bloch."]),
            "S": ("Puerta de fase S", ["Añade un cuarto de vuelta de fase a la parte |1⟩ del estado.", "S=diag(1,i), equivalente a una rotación de fase de π/2; S²=Z.", "S=T²=diag(1,i) es una puerta Clifford; transforma X en Y por conjugación y deja Z invariante."]),
            "T": ("Puerta T", ["Añade un cambio de fase menor que la puerta S.", "T=diag(1,e^(iπ/4)); aplica una rotación de fase de π/4.", "T es una puerta π/8 no Clifford que, junto con operaciones Clifford, permite computación universal tolerante a fallos."]),
            "SX": ("Raíz cuadrada de X", ["Realiza media rotación similar a X; aplicarla dos veces equivale a X salvo una fase global.", "SX²=X salvo una fase global físicamente inobservable.", "SX=(I-iX)/√2 bajo una convención común; las puertas SX y RZ nativas del hardware son habituales en sistemas IBM."]),
            "RX": ("Rotación alrededor de X", ["Rota el qubit alrededor del eje X según el ángulo elegido.", "RX(θ) rota el vector de Bloch un ángulo θ alrededor de X.", "RX(θ)=exp(-iθX/2); las rotaciones parametrizadas se usan en algoritmos variacionales como VQE y QAOA."]),
            "RY": ("Rotación alrededor de Y", ["Rota el qubit alrededor del eje Y según el ángulo elegido.", "RY(θ) rota alrededor de Y y tiene elementos de matriz reales.", "RY(θ)=exp(-iθY/2); junto con RZ permite descomponer unitarias de un qubit mediante ángulos de Euler."]),
            "RZ": ("Rotación alrededor de Z", ["Cambia la fase relativa mediante una rotación alrededor del eje Z.", "RZ(θ) aplica factores de fase opuestos a |0⟩ y |1⟩.", "RZ(θ)=diag(e^{-iθ/2},e^{iθ/2}); en hardware superconductor suele implementarse virtualmente mediante un cambio de marco."]),
            "P": ("Puerta de fase", ["Añade una fase seleccionable a la parte |1⟩ del estado.", "P(θ)=diag(1,e^{iθ}); S y T corresponden a ángulos particulares.", "P(θ) es una operación de fase U(1); sus parámetros pueden optimizarse mediante gradientes o métodos de desplazamiento de parámetro."]),
            "CX": ("CNOT / X controlada", ["Si el qubit de control es 1, invierte el qubit objetivo. Esto puede entrelazar qubits.", "CX transforma |c,t⟩ en |c,t XOR c⟩. Una puerta Hadamard seguida de CX crea un estado de Bell.", "CX=|0⟩⟨0|⊗I+|1⟩⟨1|⊗X; es una puerta de dos qubits entrelazante que, con puertas arbitrarias de un qubit, es universal."]),
            "SWAP": ("Intercambio SWAP", ["Intercambia los estados almacenados en dos qubits.", "SWAP|a,b⟩=|b,a⟩ y suele descomponerse en tres puertas CX.", "SWAP=(I⊗I+X⊗X+Y⊗Y+Z⊗Z)/2; los intercambios de enrutamiento pueden añadir mucha sobrecarga en dispositivos con conectividad limitada."]),
            "CCX": ("Toffoli / X doblemente controlada", ["Invierte el objetivo solo cuando ambos qubits de control son 1.", "CCX realiza una operación reversible similar a AND en estados de la base computacional.", "La puerta Toffoli es reversible y de tres qubits; sus descomposiciones usan varias puertas entrelazantes y de un qubit."]),
            "CSWAP": ("Fredkin / SWAP controlada", ["Intercambia dos qubits objetivo solo cuando el control es 1.", "CSWAP intercambia condicionalmente dos estados de qubit y se utiliza en la prueba SWAP.", "Fredkin es una puerta de permutación controlada y conserva el peso de Hamming del par objetivo."]),
            "Measure": ("Medición", ["Lee un qubit como 0 o 1; en una superposición, el resultado es probabilístico.", "Para α|0⟩+β|1⟩, la medición produce 0 con probabilidad |α|² y 1 con probabilidad |β|².", "La medición en la base computacional sigue la regla de Born; no es unitaria y guarda los resultados en bits clásicos."]),
            "Reset": ("Reinicio", ["Devuelve un qubit al estado |0⟩.", "El reinicio es una operación no unitaria que prepara el qubit en |0⟩.", "El reinicio es un canal cuántico, no una puerta unitaria; puede usar medición y corrección condicional o disipación."]),
            "Barrier": ("Barrera", ["Es un marcador que separa secciones del circuito y puede limitar la reorganización del compilador.", "Una barrera es una directiva del compilador, no una operación cuántica física.", "Las barreras limitan las optimizaciones del transpiler a través de un límite del circuito y ayudan a conservar las capas previstas."]),
            "If": ("Condición clásica", ["Elige una operación según un resultado de medición anterior.", "La retroalimentación clásica aplica puertas de forma condicional según los bits clásicos.", "Los circuitos dinámicos combinan control clásico con operaciones cuánticas para permitir mediciones adaptativas y correcciones."]),
            "For": ("Circuito repetido / bucle", ["Repite un grupo de operaciones.", "Un subcircuito repetido puede implementar algoritmos iterativos o secuencias repetidas de puertas.", "Los bucles describen familias de circuitos parametrizados; el soporte y la compilación dependen de la interfaz de destino."]),
            "Unitary": ("Operación unitaria", ["Es una operación personalizada que conserva probabilidades válidas del estado cuántico.", "Una matriz unitaria U cumple U†U=I y puede representar una operación cuántica reversible.", "Una unitaria de n qubits es una matriz 2ⁿ×2ⁿ con U†U=I; la síntesis la descompone en puertas de la base de destino."]),
        },
    },
    "Français": {
        "categories": ["PORTES À UN SEUL QUBIT", "PORTES DE ROTATION", "PORTES MULTI-QUBITS", "OPÉRATIONS DU CIRCUIT", "CONTRÔLE CLASSIQUE"],
        "levels": ["Niveau débutant : ", "Niveau secondaire : ", "Niveau universitaire : "],
        "gates": {
            "H": ("Hadamard", ["Crée un mélange équilibré de |0⟩ et |1⟩ lorsqu’elle est appliquée à |0⟩.", "H|0⟩=(|0⟩+|1⟩)/√2. Elle crée une superposition égale à partir d’un état de la base computationnelle.", "H = 1/√2 [[1,1],[1,-1]]. Elle est unitaire et hermitienne (H²=I) et échange les bases de mesure X et Z."]),
            "X": ("Pauli-X / NON", ["Échange |0⟩ et |1⟩, comme un interrupteur.", "Échange les états de la base computationnelle et agit comme une opération NON classique sur ces états.", "X = [[0,1],[1,0]] = σx ; réalise une rotation de π autour de l’axe X de la sphère de Bloch, à une phase globale près."]),
            "Y": ("Pauli-Y", ["Inverse le qubit et modifie aussi sa phase.", "Y envoie |0⟩ vers i|1⟩ et |1⟩ vers -i|0⟩.", "Y = [[0,-i],[i,0]] = σy ; opérateur de Pauli correspondant à une rotation de π autour de Y, à une phase globale près."]),
            "Z": ("Pauli-Z", ["Laisse |0⟩ inchangé et modifie la phase de |1⟩.", "Z|0⟩=|0⟩ et Z|1⟩=-|1⟩ ; modifie la phase relative, pas immédiatement les probabilités de mesure dans la base computationnelle.", "Z=diag(1,-1)=σz. C’est une opération de changement de phase et un générateur de rotations autour de l’axe Z de la sphère de Bloch."]),
            "S": ("Porte de phase S", ["Ajoute un quart de tour de phase à la composante |1⟩ de l’état.", "S=diag(1,i), équivalente à une rotation de phase de π/2 ; S²=Z.", "S=T²=diag(1,i) est une porte Clifford ; par conjugaison, elle transforme X en Y et laisse Z invariant."]),
            "T": ("Porte T", ["Ajoute un changement de phase plus petit que la porte S.", "T=diag(1,e^(iπ/4)) ; applique une rotation de phase de π/4.", "T est une porte π/8 non-Clifford qui, avec les opérations Clifford, permet un calcul universel tolérant aux fautes."]),
            "SX": ("Racine carrée de X", ["Effectue une demi-rotation de type X ; l’appliquer deux fois donne X à une phase globale près.", "SX²=X à une phase globale physiquement inobservable près.", "Selon une convention courante, SX=(I-iX)/√2 ; les portes natives SX et RZ sont courantes sur les systèmes IBM."]),
            "RX": ("Rotation autour de X", ["Fait tourner le qubit autour de l’axe X selon l’angle choisi.", "RX(θ) fait tourner le vecteur de Bloch d’un angle θ autour de X.", "RX(θ)=exp(-iθX/2) ; les rotations paramétrées servent dans des algorithmes variationnels comme VQE et QAOA."]),
            "RY": ("Rotation autour de Y", ["Fait tourner le qubit autour de l’axe Y selon l’angle choisi.", "RY(θ) effectue une rotation autour de Y et possède des éléments de matrice réels.", "RY(θ)=exp(-iθY/2) ; avec RZ, elle permet les décompositions d’unitaires à un qubit par angles d’Euler."]),
            "RZ": ("Rotation autour de Z", ["Modifie la phase relative par une rotation autour de l’axe Z.", "RZ(θ) applique des facteurs de phase opposés à |0⟩ et |1⟩.", "RZ(θ)=diag(e^{-iθ/2},e^{iθ/2}) ; sur le matériel supraconducteur, elle peut souvent être réalisée virtuellement par un changement de référentiel."]),
            "P": ("Porte de phase", ["Ajoute une phase réglable à la composante |1⟩ de l’état.", "P(θ)=diag(1,e^{iθ}) ; S et T correspondent à des angles particuliers.", "P(θ) est une opération de phase U(1) ; ses paramètres peuvent être optimisés par des gradients ou la méthode du décalage de paramètre."]),
            "CX": ("CNOT / X contrôlé", ["Si le qubit de contrôle vaut 1, inverse le qubit cible. Cela peut intriquer les qubits.", "CX transforme |c,t⟩ en |c,t XOR c⟩. Une porte Hadamard suivie de CX crée un état de Bell.", "CX=|0⟩⟨0|⊗I+|1⟩⟨1|⊗X ; porte intriquante à deux qubits, universelle avec des portes arbitraires à un qubit."]),
            "SWAP": ("Échange SWAP", ["Échange les états stockés dans deux qubits.", "SWAP|a,b⟩=|b,a⟩ et se décompose souvent en trois portes CX.", "SWAP=(I⊗I+X⊗X+Y⊗Y+Z⊗Z)/2 ; les échanges de routage peuvent coûter cher sur les appareils à connectivité limitée."]),
            "CCX": ("Toffoli / X à double contrôle", ["Inverse la cible uniquement si les deux qubits de contrôle valent 1.", "CCX effectue une opération réversible de type ET sur les états de la base computationnelle.", "La porte Toffoli est une porte réversible à trois qubits ; ses décompositions utilisent plusieurs portes intriquantes et à un qubit."]),
            "CSWAP": ("Fredkin / SWAP contrôlé", ["Échange deux qubits cibles uniquement si le contrôle vaut 1.", "CSWAP échange conditionnellement deux états de qubit et sert dans le test SWAP.", "Fredkin est une porte de permutation contrôlée qui préserve le poids de Hamming de la paire cible."]),
            "Measure": ("Mesure", ["Lit un qubit comme 0 ou 1 ; pour une superposition, le résultat est probabiliste.", "Pour α|0⟩+β|1⟩, la mesure donne 0 avec la probabilité |α|² et 1 avec |β|².", "La mesure dans la base computationnelle suit la règle de Born ; elle est non unitaire et stocke les résultats dans des bits classiques."]),
            "Reset": ("Réinitialisation", ["Ramène un qubit à l’état |0⟩.", "La réinitialisation est une opération non unitaire qui prépare le qubit dans |0⟩.", "La réinitialisation est un canal quantique, pas une porte unitaire ; elle peut utiliser une mesure, une correction conditionnelle ou la dissipation."]),
            "Barrier": ("Barrière", ["Marque la séparation de sections du circuit et peut limiter leur réorganisation par le compilateur.", "Une barrière est une directive du compilateur, pas une opération quantique physique.", "Les barrières limitent l’optimisation du transpileur à travers une frontière du circuit et préservent les couches prévues."]),
            "If": ("Condition classique", ["Choisit une opération selon un résultat de mesure précédent.", "Le retour classique applique des portes conditionnées par les bits classiques.", "Les circuits dynamiques associent contrôle classique et opérations quantiques pour permettre des mesures adaptatives et des corrections."]),
            "For": ("Circuit répété / boucle", ["Répète un groupe d’opérations.", "Un sous-circuit répété peut mettre en œuvre des algorithmes itératifs ou des séquences de portes répétées.", "Les boucles décrivent des familles de circuits paramétrés ; la prise en charge dépend de l’interface cible et de la compilation."]),
            "Unitary": ("Opération unitaire", ["Opération personnalisée qui conserve des probabilités d’état quantique valides.", "Une matrice unitaire U vérifie U†U=I et peut représenter une opération quantique réversible.", "Une unitaire à n qubits est une matrice 2ⁿ×2ⁿ vérifiant U†U=I ; la synthèse la décompose en portes de la base cible."]),
        },
    },
    "Deutsch": {
        "categories": ["EIN-QUBIT-GATTER", "ROTATIONSGATTER", "MEHR-QUBIT-GATTER", "SCHALTKREISOPERATIONEN", "KLASSISCHE STEUERUNG"],
        "levels": ["Anfängerniveau: ", "Sekundarstufe: ", "Universitätsniveau: "],
        "gates": {
            "H": ("Hadamard", ["Erzeugt bei Anwendung auf |0⟩ eine gleichmäßige Mischung aus |0⟩ und |1⟩.", "H|0⟩=(|0⟩+|1⟩)/√2. Erzeugt aus einem Zustand der Rechenbasis eine gleichmäßige Superposition.", "H = 1/√2 [[1,1],[1,-1]]. H ist unitär und hermitesch (H²=I) und tauscht die X- und Z-Messbasen aus."]),
            "X": ("Pauli-X / NICHT", ["Vertauscht |0⟩ und |1⟩ wie ein Schalter.", "Vertauscht die Zustände der Rechenbasis und wirkt auf diese wie eine klassische NICHT-Operation.", "X = [[0,1],[1,0]] = σx; bewirkt bis auf eine globale Phase eine π-Drehung um die X-Achse der Bloch-Kugel."]),
            "Y": ("Pauli-Y", ["Kippt das Qubit um und verändert zusätzlich seine Phase.", "Y bildet |0⟩ auf i|1⟩ und |1⟩ auf -i|0⟩ ab.", "Y = [[0,-i],[i,0]] = σy; ein Pauli-Operator, der bis auf eine globale Phase einer π-Drehung um Y entspricht."]),
            "Z": ("Pauli-Z", ["Lässt |0⟩ unverändert und ändert die Phase von |1⟩.", "Z|0⟩=|0⟩ und Z|1⟩=-|1⟩; ändert die relative Phase, nicht unmittelbar die Messwahrscheinlichkeiten in der Rechenbasis.", "Z=diag(1,-1)=σz. Das Phasenflip-Gatter erzeugt Drehungen um die Z-Achse der Bloch-Kugel."]),
            "S": ("S-Phasengatter", ["Fügt dem |1⟩-Anteil des Zustands eine Vierteldrehung der Phase hinzu.", "S=diag(1,i), entsprechend einer Phasendrehung um π/2; S²=Z.", "S=T²=diag(1,i) ist ein Clifford-Gatter; durch Konjugation bildet es X auf Y ab und lässt Z unverändert."]),
            "T": ("T-Gatter", ["Ändert die Phase weniger stark als das S-Gatter.", "T=diag(1,e^(iπ/4)); führt eine Phasendrehung um π/4 aus.", "T ist ein Nicht-Clifford-π/8-Gatter und ermöglicht zusammen mit Clifford-Operationen universelle fehlertolerante Berechnung."]),
            "SX": ("Quadratwurzel von X", ["Führt eine halbe X-artige Drehung aus; zweimal angewendet ergibt es X bis auf eine globale Phase.", "SX²=X bis auf eine physikalisch unbeobachtbare globale Phase.", "Unter einer gängigen Konvention gilt SX=(I-iX)/√2; native SX- und RZ-Gatter sind auf IBM-Systemen verbreitet."]),
            "RX": ("Drehung um X", ["Dreht das Qubit um einen gewählten Winkel um die X-Achse.", "RX(θ) dreht den Bloch-Vektor um den Winkel θ um X.", "RX(θ)=exp(-iθX/2); parametrisierte Drehungen werden in variationalen Algorithmen wie VQE und QAOA verwendet."]),
            "RY": ("Drehung um Y", ["Dreht das Qubit um einen gewählten Winkel um die Y-Achse.", "RY(θ) dreht um Y und besitzt reelle Matrixeinträge.", "RY(θ)=exp(-iθY/2); zusammen mit RZ ermöglicht es Euler-Winkel-Zerlegungen von Ein-Qubit-Unitären."]),
            "RZ": ("Drehung um Z", ["Ändert die relative Phase durch eine Drehung um die Z-Achse.", "RZ(θ) wendet entgegengesetzte Phasenfaktoren auf |0⟩ und |1⟩ an.", "RZ(θ)=diag(e^{-iθ/2},e^{iθ/2}); auf supraleitender Hardware oft virtuell durch einen Rahmenwechsel implementierbar."]),
            "P": ("Phasengatter", ["Fügt dem |1⟩-Anteil eine einstellbare Phase hinzu.", "P(θ)=diag(1,e^{iθ}); S und T entsprechen speziellen Winkeln.", "P(θ) ist eine U(1)-Phasenoperation; Parameter lassen sich mit Gradienten- oder Parameter-Shift-Verfahren optimieren."]),
            "CX": ("CNOT / kontrolliertes X", ["Wenn das Steuer-Qubit 1 ist, kippt das Ziel-Qubit. Dadurch können Qubits verschränkt werden.", "CX bildet |c,t⟩ auf |c,t XOR c⟩ ab. Hadamard gefolgt von CX erzeugt einen Bell-Zustand.", "CX=|0⟩⟨0|⊗I+|1⟩⟨1|⊗X; ein verschränkendes Zwei-Qubit-Gatter, das mit beliebigen Ein-Qubit-Gattern universell ist."]),
            "SWAP": ("SWAP-Austausch", ["Tauscht die in zwei Qubits gespeicherten Zustände aus.", "SWAP|a,b⟩=|b,a⟩ und wird häufig in drei CX-Gatter zerlegt.", "SWAP=(I⊗I+X⊗X+Y⊗Y+Z⊗Z)/2; Routing-SWAPs können bei begrenzter Konnektivität erheblichen Aufwand verursachen."]),
            "CCX": ("Toffoli / doppelt kontrolliertes X", ["Kippt das Ziel nur, wenn beide Steuer-Qubits 1 sind.", "CCX führt auf Zuständen der Rechenbasis eine reversible, UND-ähnliche Operation aus.", "Das Toffoli-Gatter ist ein reversibles Drei-Qubit-Gatter; Zerlegungen verwenden mehrere verschränkende und Ein-Qubit-Gatter."]),
            "CSWAP": ("Fredkin / kontrolliertes SWAP", ["Tauscht zwei Ziel-Qubits nur aus, wenn das Steuer-Qubit 1 ist.", "CSWAP tauscht zwei Qubit-Zustände bedingt aus und wird beim SWAP-Test verwendet.", "Fredkin ist ein kontrolliertes Permutationsgatter und erhält das Hamming-Gewicht des Zielpaares."]),
            "Measure": ("Messung", ["Liest ein Qubit als 0 oder 1 aus; bei einer Superposition ist das Ergebnis probabilistisch.", "Für α|0⟩+β|1⟩ ergibt die Messung 0 mit Wahrscheinlichkeit |α|² und 1 mit |β|².", "Die Messung in der Rechenbasis folgt der Born-Regel; sie ist nicht unitär und speichert Ergebnisse in klassischen Bits."]),
            "Reset": ("Zurücksetzen", ["Setzt ein Qubit auf |0⟩ zurück.", "Reset ist eine nicht-unitäre Operation, die das Qubit in |0⟩ vorbereitet.", "Reset ist ein Quantenkanal, kein unitäres Gatter; die Umsetzung kann Messung mit bedingter Korrektur oder Dissipation nutzen."]),
            "Barrier": ("Barriere", ["Markiert die Trennung von Schaltkreisabschnitten und kann Umordnungen durch den Compiler einschränken.", "Eine Barriere ist eine Compiler-Anweisung, keine physikalische Quantenoperation.", "Barrieren begrenzen Transpiler-Optimierungen über eine Schaltkreisgrenze hinweg und helfen, geplante Ebenen zu erhalten."]),
            "If": ("Klassische Bedingung", ["Wählt eine Operation anhand eines früheren Messergebnisses aus.", "Klassische Rückkopplung wendet Gatter abhängig von klassischen Bits an.", "Dynamische Schaltkreise kombinieren klassische Steuerung und Quantenoperationen für adaptive Messung und Korrektur."]),
            "For": ("Wiederholter Schaltkreis / Schleife", ["Wiederholt eine Gruppe von Operationen.", "Ein wiederholtes Teilschaltwerk kann iterative Algorithmen oder wiederholte Gatterfolgen umsetzen.", "Schleifen beschreiben parametrisierte Schaltkreisfamilien; Unterstützung und Kompilierung hängen von der Ziel-Schnittstelle ab."]),
            "Unitary": ("Unitäre Operation", ["Eine benutzerdefinierte Operation, die gültige Wahrscheinlichkeiten des Quantenzustands erhält.", "Eine unitäre Matrix U erfüllt U†U=I und kann eine reversible Quantenoperation darstellen.", "Eine n-Qubit-Unitäre ist eine 2ⁿ×2ⁿ-Matrix mit U†U=I; die Synthese zerlegt sie in Gatter der Zielbasis."]),
        },
    },
    "日本語": {
        "categories": ["単一量子ビットゲート", "回転ゲート", "多量子ビットゲート", "回路操作", "古典制御"],
        "levels": ["初級：", "中学・高校レベル：", "大学レベル："],
        "gates": {
            "H": ("アダマールゲート", ["|0⟩に適用すると、|0⟩と|1⟩が等しい重ね合わせを作ります。", "H|0⟩=(|0⟩+|1⟩)/√2。計算基底の状態から等しい重ね合わせを作ります。", "H = 1/√2 [[1,1],[1,-1]]。ユニタリかつエルミート（H²=I）で、X基底とZ基底の測定を入れ替えます。"]),
            "X": ("パウリX / NOT", ["スイッチのように|0⟩と|1⟩を入れ替えます。", "計算基底の状態を交換し、それらに対して古典的なNOT演算として働きます。", "X = [[0,1],[1,0]] = σx。全体位相を除き、ブロッホ球のX軸周りにπ回転します。"]),
            "Y": ("パウリY", ["量子ビットを反転し、位相も変えます。", "Yは|0⟩をi|1⟩に、|1⟩を-i|0⟩に写します。", "Y = [[0,-i],[i,0]] = σy。パウリ演算子で、全体位相を除いてY軸周りのπ回転に相当します。"]),
            "Z": ("パウリZ", ["|0⟩はそのままにし、|1⟩の位相を変えます。", "Z|0⟩=|0⟩、Z|1⟩=-|1⟩。相対位相を変えますが、計算基底での確率は直ちには変わりません。", "Z=diag(1,-1)=σz。位相反転演算であり、ブロッホ球のZ軸周りの回転を生成します。"]),
            "S": ("S位相ゲート", ["状態の|1⟩成分に位相の4分の1回転を加えます。", "S=diag(1,i)で、π/2の位相回転に相当します。S²=Zです。", "S=T²=diag(1,i)はクリフォードゲートです。共役変換でXをYに写し、Zは不変にします。"]),
            "T": ("Tゲート", ["Sゲートより小さな位相変化を加えます。", "T=diag(1,e^(iπ/4))で、π/4の位相回転を与えます。", "Tは非クリフォードのπ/8ゲートで、クリフォード演算と組み合わせると万能な耐故障量子計算を実現できます。"]),
            "SX": ("Xの平方根", ["Xに似た回転の半分を行います。2回適用すると全体位相を除いてXになります。", "SX²=X（物理的に観測できない全体位相を除く）。", "一般的な規約ではSX=(I-iX)/√2です。SXとRZはIBM系システムでよく使われるネイティブゲートです。"]),
            "RX": ("X軸回転", ["指定した角度だけX軸の周りに量子ビットを回転します。", "RX(θ)はブロッホベクトルをX軸周りにθ回転させます。", "RX(θ)=exp(-iθX/2)。VQEやQAOAなどの変分アルゴリズムでパラメータ付き回転が使われます。"]),
            "RY": ("Y軸回転", ["指定した角度だけY軸の周りに量子ビットを回転します。", "RY(θ)はY軸周りに回転し、行列要素は実数です。", "RY(θ)=exp(-iθY/2)。RZ回転と組み合わせると、オイラー角による単一量子ビットユニタリの分解ができます。"]),
            "RZ": ("Z軸回転", ["Z軸周りの回転によって相対位相を変えます。", "RZ(θ)は|0⟩と|1⟩に反対向きの位相因子を適用します。", "RZ(θ)=diag(e^{-iθ/2},e^{iθ/2})。超伝導ハードウェアではフレーム変更により仮想的に実装できることが多いです。"]),
            "P": ("位相ゲート", ["状態の|1⟩成分に選択した位相を加えます。", "P(θ)=diag(1,e^{iθ})。SとTは特定の角度に対応します。", "P(θ)はU(1)位相操作です。勾配法やパラメータシフト法でパラメータを最適化できます。"]),
            "CX": ("CNOT / 制御X", ["制御量子ビットが1なら、標的量子ビットを反転します。量子ビットをもつれさせることがあります。", "CXは|c,t⟩を|c,t XOR c⟩に写します。アダマールの後にCXを使うとベル状態を作れます。", "CX=|0⟩⟨0|⊗I+|1⟩⟨1|⊗X。2量子ビットのもつれゲートで、任意の単一量子ビットゲートと合わせると万能です。"]),
            "SWAP": ("SWAP交換", ["2つの量子ビットに保存された状態を交換します。", "SWAP|a,b⟩=|b,a⟩で、通常は3つのCXゲートに分解できます。", "SWAP=(I⊗I+X⊗X+Y⊗Y+Z⊗Z)/2。接続性が限られたデバイスでは経路設定のSWAPが大きな負担になることがあります。"]),
            "CCX": ("Toffoli / 二重制御X", ["2つの制御量子ビットが両方1のときだけ標的を反転します。", "CCXは計算基底状態に対して可逆なANDに似た演算を行います。", "Toffoliは可逆な3量子ビットゲートです。分解には複数のもつれゲートと単一量子ビットゲートを使います。"]),
            "CSWAP": ("Fredkin / 制御SWAP", ["制御量子ビットが1のときだけ、2つの標的量子ビットを交換します。", "CSWAPは2つの量子ビット状態を条件付きで交換し、SWAPテストに使われます。", "Fredkinは制御付き置換ゲートで、標的ペアのハミング重みを保存します。"]),
            "Measure": ("測定", ["量子ビットを0または1として読み取ります。重ね合わせでは結果は確率的です。", "α|0⟩+β|1⟩を測定すると、0は確率|α|²、1は確率|β|²で得られます。", "計算基底測定はボルン則に従います。非ユニタリ操作で、結果を古典ビットに保存します。"]),
            "Reset": ("リセット", ["量子ビットを|0⟩に戻します。", "リセットは非ユニタリ操作で、量子ビットを|0⟩に準備します。", "リセットはユニタリゲートではなく量子チャネルです。測定と条件付き補正、または散逸を利用できます。"]),
            "Barrier": ("バリア", ["回路の区切りを示し、コンパイラによる並べ替えを制限することがあります。", "バリアはコンパイラ指示であり、物理的な量子操作ではありません。", "バリアは回路境界をまたぐトランスパイラ最適化を制限し、意図した層構造を保つのに役立ちます。"]),
            "If": ("古典条件", ["以前の測定結果に応じて操作を選びます。", "古典的フィードフォワードでは古典ビットの値に応じてゲートを適用します。", "動的回路は古典制御と量子操作を組み合わせ、適応的測定と補正を可能にします。"]),
            "For": ("反復回路 / ループ", ["操作のまとまりを繰り返します。", "反復サブ回路は反復アルゴリズムやゲート列の繰り返しに利用できます。", "ループ構文はパラメータ付き回路群を表します。対応状況とコンパイルは対象インターフェースに依存します。"]),
            "Unitary": ("ユニタリ操作", ["量子状態の有効な確率を保つカスタム操作です。", "ユニタリ行列UはU†U=Iを満たし、可逆な量子操作を表せます。", "n量子ビットのユニタリはU†U=Iを満たす2ⁿ×2ⁿ行列です。合成時に対象基底のゲートへ分解します。"]),
        },
    },
    "中文": {
        "categories": ["单量子比特门", "旋转门", "多量子比特门", "电路操作", "经典控制"],
        "levels": ["入门级：", "中学级：", "大学级："],
        "gates": {
            "H": ("阿达马门", ["作用于|0⟩时，会以相等的幅度形成|0⟩和|1⟩的叠加。", "H|0⟩=(|0⟩+|1⟩)/√2。它从计算基态创建等幅叠加态。", "H = 1/√2 [[1,1],[1,-1]]。它是酉且厄米的（H²=I），并交换X与Z测量基。"]),
            "X": ("泡利X / 非门", ["像开关一样交换|0⟩和|1⟩。", "它交换计算基态，作用类似于经典逻辑非门。", "X = [[0,1],[1,0]] = σx；除全局相位外，它相当于绕布洛赫球X轴旋转π。"]),
            "Y": ("泡利Y", ["翻转量子比特，同时改变其相位。", "Y将|0⟩映射为i|1⟩，将|1⟩映射为-i|0⟩。", "Y = [[0,-i],[i,0]] = σy，是泡利算符；除全局相位外，相当于绕Y轴旋转π。"]),
            "Z": ("泡利Z", ["保持|0⟩不变，并改变|1⟩的相位。", "Z|0⟩=|0⟩且Z|1⟩=-|1⟩；它改变相对相位，但不会立即改变计算基测量概率。", "Z=diag(1,-1)=σz。它是相位翻转算符，也是布洛赫球Z轴旋转的生成元。"]),
            "S": ("S相位门", ["给状态中的|1⟩分量增加四分之一圈的相位。", "S=diag(1,i)，相当于π/2相位旋转；S²=Z。", "S=T²=diag(1,i)是Clifford门；共轭变换将X映射为Y，并保持Z不变。"]),
            "T": ("T门", ["它带来的相位变化比S门更小。", "T=diag(1,e^(iπ/4))，执行π/4相位旋转。", "T是非Clifford的π/8门，与Clifford操作结合可支持通用容错量子计算。"]),
            "SX": ("X的平方根门", ["执行类似X旋转的一半；连续应用两次后，除全局相位外等于X。", "SX²=X（相差一个不可观测的全局相位）。", "在一种常用约定下，SX=(I-iX)/√2；SX和RZ是IBM系统常见的原生门。"]),
            "RX": ("绕X轴旋转", ["按指定角度绕X轴旋转量子比特。", "RX(θ)使布洛赫向量绕X轴旋转θ。", "RX(θ)=exp(-iθX/2)；参数化旋转用于VQE和QAOA等变分算法。"]),
            "RY": ("绕Y轴旋转", ["按指定角度绕Y轴旋转量子比特。", "RY(θ)绕Y轴旋转，其矩阵元素为实数。", "RY(θ)=exp(-iθY/2)；与RZ旋转结合，可通过欧拉角分解单量子比特酉操作。"]),
            "RZ": ("绕Z轴旋转", ["通过绕Z轴旋转改变相对相位。", "RZ(θ)对|0⟩和|1⟩施加相反的相位因子。", "RZ(θ)=diag(e^{-iθ/2},e^{iθ/2})；在超导硬件上通常可通过改变参考帧虚拟实现。"]),
            "P": ("相位门", ["给状态中的|1⟩分量添加可选相位。", "P(θ)=diag(1,e^{iθ})；S和T对应特定角度。", "P(θ)是U(1)相位操作；其参数可通过梯度法或参数移位法优化。"]),
            "CX": ("CNOT / 受控X门", ["当控制量子比特为1时，翻转目标量子比特。这可以使量子比特纠缠。", "CX将|c,t⟩映射为|c,t XOR c⟩。先使用阿达马门再使用CX可创建贝尔态。", "CX=|0⟩⟨0|⊗I+|1⟩⟨1|⊗X；它是双量子比特纠缠门，与任意单量子比特门结合可实现通用计算。"]),
            "SWAP": ("交换门 SWAP", ["交换两个量子比特中存储的状态。", "SWAP|a,b⟩=|b,a⟩，通常可分解为三个CX门。", "SWAP=(I⊗I+X⊗X+Y⊗Y+Z⊗Z)/2；在连接性有限的设备上，路由交换可能带来显著开销。"]),
            "CCX": ("Toffoli / 双重受控X门", ["只有两个控制量子比特都为1时，才翻转目标量子比特。", "CCX在计算基态上执行类似AND的可逆操作。", "Toffoli是三量子比特可逆门；分解时会使用多个纠缠门和单量子比特门。"]),
            "CSWAP": ("Fredkin / 受控交换门", ["只有控制量子比特为1时，才交换两个目标量子比特。", "CSWAP有条件地交换两个量子比特状态，可用于SWAP测试。", "Fredkin是受控置换门，并保持目标量子比特对的汉明重量。"]),
            "Measure": ("测量", ["读取量子比特的结果为0或1；若处于叠加态，结果具有概率性。", "对α|0⟩+β|1⟩进行测量，得到0的概率为|α|²，得到1的概率为|β|²。", "计算基测量遵循玻恩规则；它是非酉操作，并将结果存入经典比特。"]),
            "Reset": ("重置", ["将量子比特恢复到|0⟩。", "重置是非酉操作，会将量子比特制备到|0⟩。", "重置是量子信道而非酉门；实现方式可能包括测量与条件校正或耗散。"]),
            "Barrier": ("屏障", ["标记电路不同部分的边界，并可能限制编译器重新排序。", "屏障是编译器指令，不是物理量子操作。", "屏障限制跨越电路边界的转译器优化，有助于保留预期的电路层。"]),
            "If": ("经典条件", ["根据先前的测量结果选择操作。", "经典前馈会根据经典比特的值有条件地应用量子门。", "动态电路将经典控制流与量子操作结合，实现自适应测量和纠错。"]),
            "For": ("重复电路 / 循环", ["重复执行一组操作。", "重复子电路可用于迭代算法或重复门序列。", "循环结构描述参数化电路族；支持情况和编译方式取决于目标接口。"]),
            "Unitary": ("酉操作", ["一种自定义操作，可保持量子态概率的有效性。", "酉矩阵U满足U†U=I，可表示可逆的量子操作。", "n量子比特酉操作是满足U†U=I的2ⁿ×2ⁿ矩阵；综合过程会将其分解为目标基门。"]),
        },
    },
    "हिन्दी": {
        "categories": ["एकल-क्यूबिट गेट", "घूर्णन गेट", "बहु-क्यूबिट गेट", "सर्किट क्रियाएँ", "क्लासिकल नियंत्रण"],
        "levels": ["शुरुआती स्तर: ", "माध्यमिक स्तर: ", "विश्वविद्यालय स्तर: "],
        "gates": {
            "H": ("हैडामार्ड गेट", ["|0⟩ पर लगाने से |0⟩ और |1⟩ का बराबर सुपरपोज़िशन बनता है।", "H|0⟩=(|0⟩+|1⟩)/√2। यह कम्प्यूटेशनल-बेसिस अवस्था से बराबर सुपरपोज़िशन बनाता है।", "H = 1/√2 [[1,1],[1,-1]]। यह यूनिटरी और हर्मिटियन है (H²=I), तथा X और Z मापन आधारों को बदलता है।"]),
            "X": ("पाउली-X / NOT", ["स्विच की तरह |0⟩ और |1⟩ को बदल देता है।", "यह कम्प्यूटेशनल-बेसिस अवस्थाओं को बदलता है और उन पर क्लासिकल NOT की तरह काम करता है।", "X = [[0,1],[1,0]] = σx; वैश्विक फेज़ को छोड़कर ब्लॉख गोले के X-अक्ष पर π घूर्णन करता है।"]),
            "Y": ("पाउली-Y", ["क्यूबिट को पलटता है और उसका फेज़ भी बदलता है।", "Y, |0⟩ को i|1⟩ और |1⟩ को -i|0⟩ में बदलता है।", "Y = [[0,-i],[i,0]] = σy; यह पाउली ऑपरेटर है और वैश्विक फेज़ को छोड़कर Y-अक्ष पर π घूर्णन के बराबर है।"]),
            "Z": ("पाउली-Z", ["|0⟩ को वैसा ही रखता है और |1⟩ का फेज़ बदलता है।", "Z|0⟩=|0⟩ और Z|1⟩=-|1⟩; यह सापेक्ष फेज़ बदलता है, पर कम्प्यूटेशनल आधार की संभावनाएँ तुरंत नहीं बदलता।", "Z=diag(1,-1)=σz। यह फेज़-फ्लिप ऑपरेटर है और ब्लॉख गोले के Z-अक्ष के चारों ओर घूर्णन का जनक है।"]),
            "S": ("S फेज़ गेट", ["अवस्था के |1⟩ भाग में फेज़ का एक-चौथाई चक्कर जोड़ता है।", "S=diag(1,i), यानी π/2 फेज़ घूर्णन; S²=Z।", "S=T²=diag(1,i) एक Clifford गेट है; conjugation से X को Y में बदलता है और Z को अपरिवर्तित रखता है।"]),
            "T": ("T गेट", ["S गेट से छोटा फेज़ परिवर्तन जोड़ता है।", "T=diag(1,e^(iπ/4)); यह π/4 फेज़ घूर्णन देता है।", "T एक non-Clifford π/8 गेट है; Clifford क्रियाओं के साथ यह सार्वभौमिक fault-tolerant गणना में सहायक है।"]),
            "SX": ("X का वर्गमूल", ["X-जैसा आधा घूर्णन करता है; इसे दो बार लगाने पर वैश्विक फेज़ को छोड़कर X मिलता है।", "SX²=X, एक भौतिक रूप से अप्रेक्षणीय वैश्विक फेज़ को छोड़कर।", "एक सामान्य convention में SX=(I-iX)/√2; IBM प्रणालियों में native SX और RZ गेट आम हैं।"]),
            "RX": ("X-अक्ष घूर्णन", ["चुने गए कोण से क्यूबिट को X-अक्ष के चारों ओर घुमाता है।", "RX(θ), ब्लॉख वेक्टर को X के चारों ओर θ कोण से घुमाता है।", "RX(θ)=exp(-iθX/2); VQE और QAOA जैसे variational algorithms में parameterized rotations उपयोग होते हैं।"]),
            "RY": ("Y-अक्ष घूर्णन", ["चुने गए कोण से क्यूबिट को Y-अक्ष के चारों ओर घुमाता है।", "RY(θ), Y-अक्ष के चारों ओर घूमता है और इसकी matrix entries वास्तविक होती हैं।", "RY(θ)=exp(-iθY/2); RZ के साथ यह Euler-angle decomposition से single-qubit unitaries बनाने में मदद करता है।"]),
            "RZ": ("Z-अक्ष घूर्णन", ["Z-अक्ष के चारों ओर घुमाकर सापेक्ष फेज़ बदलता है।", "RZ(θ), |0⟩ और |1⟩ पर विपरीत phase factors लगाता है।", "RZ(θ)=diag(e^{-iθ/2},e^{iθ/2}); superconducting hardware पर frame change द्वारा इसे अक्सर virtual रूप से लागू किया जा सकता है।"]),
            "P": ("फेज़ गेट", ["अवस्था के |1⟩ भाग में चुना हुआ फेज़ जोड़ता है।", "P(θ)=diag(1,e^{iθ}); S और T विशेष कोणों के उदाहरण हैं।", "P(θ) एक U(1) phase operation है; इसके parameters को gradient या parameter-shift विधियों से optimize किया जा सकता है।"]),
            "CX": ("CNOT / नियंत्रित-X", ["यदि control क्यूबिट 1 है, तो target क्यूबिट पलटता है। इससे entanglement बन सकता है।", "CX, |c,t⟩ को |c,t XOR c⟩ में बदलता है। Hadamard के बाद CX लगाने से Bell state बनती है।", "CX=|0⟩⟨0|⊗I+|1⟩⟨1|⊗X; यह दो-क्यूबिट entangling gate है और arbitrary single-qubit gates के साथ universal है।"]),
            "SWAP": ("SWAP अदला-बदली", ["दो क्यूबिट में रखी अवस्थाओं को आपस में बदलता है।", "SWAP|a,b⟩=|b,a⟩; इसे अक्सर तीन CX gates में तोड़ा जाता है।", "SWAP=(I⊗I+X⊗X+Y⊗Y+Z⊗Z)/2; सीमित connectivity वाले उपकरणों पर routing swaps अतिरिक्त लागत बढ़ा सकते हैं।"]),
            "CCX": ("Toffoli / दोहरे नियंत्रण वाला X", ["Target को तभी पलटता है जब दोनों control क्यूबिट 1 हों।", "CCX computational-basis अवस्थाओं पर reversible AND-जैसी क्रिया करता है।", "Toffoli तीन-क्यूबिट reversible gate है; इसके decomposition में कई entangling और single-qubit gates होते हैं।"]),
            "CSWAP": ("Fredkin / नियंत्रित SWAP", ["Control क्यूबिट 1 होने पर ही दो target क्यूबिट बदलता है।", "CSWAP दो क्यूबिट अवस्थाओं को शर्त के अनुसार बदलता है और SWAP test में उपयोग होता है।", "Fredkin एक controlled permutation gate है और target pair का Hamming weight बनाए रखता है।"]),
            "Measure": ("मापन", ["क्यूबिट को 0 या 1 के रूप में पढ़ता है; superposition में परिणाम संभाव्य होता है।", "α|0⟩+β|1⟩ के लिए मापन में 0 की संभावना |α|² और 1 की संभावना |β|² होती है।", "Computational-basis measurement Born rule का पालन करता है; यह non-unitary है और परिणाम classical bits में रखता है।"]),
            "Reset": ("रीसेट", ["क्यूबिट को |0⟩ में वापस लाता है।", "Reset एक non-unitary क्रिया है जो क्यूबिट को |0⟩ में तैयार करती है।", "Reset एक quantum channel है, unitary gate नहीं; इसे measurement और conditional correction या dissipation से लागू किया जा सकता है।"]),
            "Barrier": ("बैरियर", ["सर्किट के हिस्सों के बीच निशान लगाता है और compiler की पुनर्व्यवस्था सीमित कर सकता है।", "Barrier compiler directive है, भौतिक quantum operation नहीं।", "Barriers circuit boundary के पार transpiler optimization को सीमित करते हैं और नियोजित layers सुरक्षित रखते हैं।"]),
            "If": ("क्लासिकल शर्त", ["पहले के measurement परिणाम के आधार पर operation चुनता है।", "Classical feed-forward, classical bits के आधार पर gates को शर्त सहित लागू करता है।", "Dynamic circuits classical control flow और quantum operations को मिलाकर adaptive measurement और correction संभव करते हैं।"]),
            "For": ("दोहराया सर्किट / लूप", ["operations के समूह को दोहराता है।", "दोहराया गया subcircuit iterative algorithms या repeated gate sequences लागू कर सकता है।", "Loop constructs parameterized circuit families बताते हैं; समर्थन और compilation target interface पर निर्भर करते हैं।"]),
            "Unitary": ("यूनिटरी ऑपरेशन", ["एक custom operation जो quantum state की वैध संभावनाएँ बनाए रखता है।", "Unitary matrix U के लिए U†U=I होता है और यह reversible quantum operation दर्शा सकती है।", "n-qubit unitary एक 2ⁿ×2ⁿ matrix है जिसमें U†U=I; synthesis इसे target basis gates में तोड़ता है।"]),
        },
    },
    "Português": {
        "categories": ["PORTAS DE UM ÚNICO QUBIT", "PORTAS DE ROTAÇÃO", "PORTAS DE MÚLTIPLOS QUBITS", "OPERAÇÕES DO CIRCUITO", "CONTROLE CLÁSSICO"],
        "levels": ["Nível iniciante: ", "Nível do ensino médio: ", "Nível universitário: "],
        "gates": {
            "H": ("Porta Hadamard", ["Cria uma mistura equilibrada de |0⟩ e |1⟩ quando aplicada a |0⟩.", "H|0⟩=(|0⟩+|1⟩)/√2. Cria uma superposição igual a partir de um estado da base computacional.", "H = 1/√2 [[1,1],[1,-1]]. É unitária e hermitiana (H²=I), e troca as bases de medição X e Z."]),
            "X": ("Pauli-X / NÃO", ["Troca |0⟩ e |1⟩, como um interruptor.", "Troca os estados da base computacional e age como uma operação NÃO clássica nesses estados.", "X = [[0,1],[1,0]] = σx; implementa uma rotação de π em torno do eixo X da esfera de Bloch, exceto por uma fase global."]),
            "Y": ("Pauli-Y", ["Inverte o qubit e também altera sua fase.", "Y transforma |0⟩ em i|1⟩ e |1⟩ em -i|0⟩.", "Y = [[0,-i],[i,0]] = σy; é um operador de Pauli e corresponde a uma rotação de π em torno de Y, exceto por fase global."]),
            "Z": ("Pauli-Z", ["Mantém |0⟩ inalterado e muda a fase de |1⟩.", "Z|0⟩=|0⟩ e Z|1⟩=-|1⟩; muda a fase relativa, mas não imediatamente as probabilidades na base computacional.", "Z=diag(1,-1)=σz. É uma operação de inversão de fase e gera rotações em torno do eixo Z da esfera de Bloch."]),
            "S": ("Porta de fase S", ["Adiciona um quarto de volta de fase à parte |1⟩ do estado.", "S=diag(1,i), equivalente a uma rotação de fase de π/2; S²=Z.", "S=T²=diag(1,i) é uma porta Clifford; por conjugação, transforma X em Y e mantém Z invariante."]),
            "T": ("Porta T", ["Adiciona uma mudança de fase menor que a porta S.", "T=diag(1,e^(iπ/4)); aplica uma rotação de fase de π/4.", "T é uma porta π/8 não-Clifford que, com operações Clifford, permite computação universal tolerante a falhas."]),
            "SX": ("Raiz quadrada de X", ["Faz metade de uma rotação semelhante a X; aplicada duas vezes, equivale a X exceto por uma fase global.", "SX²=X, exceto por uma fase global fisicamente inobservável.", "Em uma convenção comum, SX=(I-iX)/√2; portas nativas SX e RZ são comuns em sistemas IBM."]),
            "RX": ("Rotação em torno de X", ["Gira o qubit em torno do eixo X pelo ângulo escolhido.", "RX(θ) gira o vetor de Bloch por θ em torno de X.", "RX(θ)=exp(-iθX/2); rotações parametrizadas são usadas em algoritmos variacionais como VQE e QAOA."]),
            "RY": ("Rotação em torno de Y", ["Gira o qubit em torno do eixo Y pelo ângulo escolhido.", "RY(θ) gira em torno de Y e tem elementos reais na matriz.", "RY(θ)=exp(-iθY/2); junto com RZ, permite decomposições de unitariedades de um qubit por ângulos de Euler."]),
            "RZ": ("Rotação em torno de Z", ["Muda a fase relativa girando em torno do eixo Z.", "RZ(θ) aplica fatores de fase opostos a |0⟩ e |1⟩.", "RZ(θ)=diag(e^{-iθ/2},e^{iθ/2}); em hardware supercondutor, pode ser implementada virtualmente por uma mudança de referencial."]),
            "P": ("Porta de fase", ["Adiciona uma fase escolhida à parte |1⟩ do estado.", "P(θ)=diag(1,e^{iθ}); S e T correspondem a ângulos específicos.", "P(θ) é uma operação de fase U(1); seus parâmetros podem ser otimizados por gradientes ou métodos de deslocamento de parâmetro."]),
            "CX": ("CNOT / X controlado", ["Se o qubit de controle for 1, inverte o qubit-alvo. Isso pode entrelaçar qubits.", "CX transforma |c,t⟩ em |c,t XOR c⟩. Uma Hadamard seguida de CX cria um estado de Bell.", "CX=|0⟩⟨0|⊗I+|1⟩⟨1|⊗X; porta de dois qubits que gera entrelaçamento e, com portas de um qubit arbitrárias, é universal."]),
            "SWAP": ("Troca SWAP", ["Troca os estados armazenados em dois qubits.", "SWAP|a,b⟩=|b,a⟩ e costuma ser decomposta em três portas CX.", "SWAP=(I⊗I+X⊗X+Y⊗Y+Z⊗Z)/2; trocas de roteamento podem gerar sobrecarga em dispositivos com conectividade limitada."]),
            "CCX": ("Toffoli / X com controle duplo", ["Inverte o alvo somente quando os dois qubits de controle são 1.", "CCX realiza uma operação reversível semelhante a AND nos estados da base computacional.", "A porta Toffoli é reversível e usa três qubits; suas decomposições incluem várias portas de entrelaçamento e de um qubit."]),
            "CSWAP": ("Fredkin / SWAP controlado", ["Troca dois qubits-alvo somente quando o controle é 1.", "CSWAP troca condicionalmente dois estados de qubit e é usada no teste SWAP.", "Fredkin é uma porta de permutação controlada e preserva o peso de Hamming do par-alvo."]),
            "Measure": ("Medição", ["Lê o qubit como 0 ou 1; em uma superposição, o resultado é probabilístico.", "Para α|0⟩+β|1⟩, a medição resulta em 0 com probabilidade |α|² e em 1 com |β|².", "A medição na base computacional segue a regra de Born; é não unitária e armazena resultados em bits clássicos."]),
            "Reset": ("Reinicialização", ["Retorna um qubit ao estado |0⟩.", "Reset é uma operação não unitária que prepara o qubit em |0⟩.", "Reset é um canal quântico, não uma porta unitária; pode usar medição e correção condicional ou dissipação."]),
            "Barrier": ("Barreira", ["Marca a separação entre partes do circuito e pode limitar a reorganização do compilador.", "Uma barreira é uma diretiva do compilador, não uma operação quântica física.", "Barreiras restringem otimizações do transpiler através de um limite do circuito e ajudam a preservar as camadas planejadas."]),
            "If": ("Condição clássica", ["Escolhe uma operação com base em um resultado de medição anterior.", "O feed-forward clássico aplica portas condicionalmente aos bits clássicos.", "Circuitos dinâmicos combinam fluxo de controle clássico e operações quânticas, permitindo medição adaptativa e correção."]),
            "For": ("Circuito repetido / laço", ["Repete um grupo de operações.", "Um subcircuito repetido pode implementar algoritmos iterativos ou sequências repetidas de portas.", "Laços descrevem famílias de circuitos parametrizados; o suporte e a compilação dependem da interface-alvo."]),
            "Unitary": ("Operação unitária", ["Uma operação personalizada que preserva probabilidades válidas do estado quântico.", "Uma matriz unitária U satisfaz U†U=I e pode representar uma operação quântica reversível.", "Uma unitária de n qubits é uma matriz 2ⁿ×2ⁿ com U†U=I; a síntese a decompõe em portas da base-alvo."]),
        },
    },
}

CIRCUITS = {
    "The Bell State Circuit (Entanglement)": {
        "description": "A two-qubit entangled state. Apply H to qubit 0, then CX with qubit 0 as control and qubit 1 as target. The ideal state is (|00⟩ + |11⟩)/√2.",
        "steps": "1. Start in |00⟩\n2. H on qubit 0\n3. CX(0 → 1)\n4. Measure both qubits (optional for a state-vector illustration).",
    },
    "Three-Qubit GHZ State Circuit": {
        "description": "A three-qubit entangled state. Apply H to qubit 0, then CX from qubit 0 to each of qubits 1 and 2. The ideal state is (|000⟩ + |111⟩)/√2.",
        "steps": "1. Start in |000⟩\n2. H on qubit 0\n3. CX(0 → 1)\n4. CX(0 → 2)\n5. Measure all qubits (optional for a state-vector illustration).",
    },
}



# ─────────────────────────────────────────────
# SELECTED-CIRCUIT TRANSLATIONS
# Localize the circuit name, overview, and steps shown in Window 4.
# The canonical English keys are used internally to identify each circuit.
# ─────────────────────────────────────────────
CIRCUIT_LOCALIZATIONS = {
    "Español": {
        "The Bell State Circuit (Entanglement)": {
            "title": "Circuito del estado de Bell (entrelazamiento)",
            "description": "Un estado entrelazado de dos qubits. Aplica H al qubit 0 y después CX, usando el qubit 0 como control y el qubit 1 como objetivo. El estado ideal es (|00⟩ + |11⟩)/√2.",
            "steps": "1. Comienza en |00⟩\n2. Aplica H al qubit 0\n3. Aplica CX (0 → 1)\n4. Mide ambos qubits (opcional para una ilustración del vector de estado).",
        },
        "Three-Qubit GHZ State Circuit": {
            "title": "Circuito del estado GHZ de tres qubits",
            "description": "Un estado entrelazado de tres qubits. Aplica H al qubit 0 y después CX desde el qubit 0 hacia los qubits 1 y 2. El estado ideal es (|000⟩ + |111⟩)/√2.",
            "steps": "1. Comienza en |000⟩\n2. Aplica H al qubit 0\n3. Aplica CX (0 → 1)\n4. Aplica CX (0 → 2)\n5. Mide todos los qubits (opcional para una ilustración del vector de estado).",
        },
    },
    "Français": {
        "The Bell State Circuit (Entanglement)": {
            "title": "Circuit de l’état de Bell (intrication)",
            "description": "Un état intriqué à deux qubits. Appliquez H au qubit 0, puis CX avec le qubit 0 comme contrôle et le qubit 1 comme cible. L’état idéal est (|00⟩ + |11⟩)/√2.",
            "steps": "1. Commencer dans |00⟩\n2. Appliquer H au qubit 0\n3. Appliquer CX (0 → 1)\n4. Mesurer les deux qubits (facultatif pour une illustration du vecteur d’état).",
        },
        "Three-Qubit GHZ State Circuit": {
            "title": "Circuit de l’état GHZ à trois qubits",
            "description": "Un état intriqué à trois qubits. Appliquez H au qubit 0, puis CX du qubit 0 vers les qubits 1 et 2. L’état idéal est (|000⟩ + |111⟩)/√2.",
            "steps": "1. Commencer dans |000⟩\n2. Appliquer H au qubit 0\n3. Appliquer CX (0 → 1)\n4. Appliquer CX (0 → 2)\n5. Mesurer tous les qubits (facultatif pour une illustration du vecteur d’état).",
        },
    },
    "Deutsch": {
        "The Bell State Circuit (Entanglement)": {
            "title": "Bell-Zustands-Schaltkreis (Verschränkung)",
            "description": "Ein verschränkter Zustand aus zwei Qubits. Wende H auf Qubit 0 an und danach CX, wobei Qubit 0 das Steuer-Qubit und Qubit 1 das Ziel-Qubit ist. Der ideale Zustand ist (|00⟩ + |11⟩)/√2.",
            "steps": "1. Mit |00⟩ beginnen\n2. H auf Qubit 0 anwenden\n3. CX (0 → 1) anwenden\n4. Beide Qubits messen (optional für eine Zustandsvektor-Darstellung).",
        },
        "Three-Qubit GHZ State Circuit": {
            "title": "Drei-Qubit-GHZ-Zustands-Schaltkreis",
            "description": "Ein verschränkter Zustand aus drei Qubits. Wende H auf Qubit 0 an und danach CX von Qubit 0 zu Qubit 1 und Qubit 2. Der ideale Zustand ist (|000⟩ + |111⟩)/√2.",
            "steps": "1. Mit |000⟩ beginnen\n2. H auf Qubit 0 anwenden\n3. CX (0 → 1) anwenden\n4. CX (0 → 2) anwenden\n5. Alle Qubits messen (optional für eine Zustandsvektor-Darstellung).",
        },
    },
    "日本語": {
        "The Bell State Circuit (Entanglement)": {
            "title": "ベル状態回路（量子もつれ）",
            "description": "2量子ビットのもつれ状態です。量子ビット0にHを適用し、次に量子ビット0を制御、量子ビット1を標的としてCXを適用します。理想状態は(|00⟩ + |11⟩)/√2です。",
            "steps": "1. |00⟩から開始\n2. 量子ビット0にHを適用\n3. CX（0 → 1）を適用\n4. 2つの量子ビットを測定（状態ベクトルの説明では省略可能）。",
        },
        "Three-Qubit GHZ State Circuit": {
            "title": "3量子ビットGHZ状態回路",
            "description": "3量子ビットのもつれ状態です。量子ビット0にHを適用し、次に量子ビット0から量子ビット1と2へCXを適用します。理想状態は(|000⟩ + |111⟩)/√2です。",
            "steps": "1. |000⟩から開始\n2. 量子ビット0にHを適用\n3. CX（0 → 1）を適用\n4. CX（0 → 2）を適用\n5. すべての量子ビットを測定（状態ベクトルの説明では省略可能）。",
        },
    },
    "中文": {
        "The Bell State Circuit (Entanglement)": {
            "title": "贝尔态电路（量子纠缠）",
            "description": "这是一个由两个量子比特组成的纠缠态。先对量子比特0应用H门，再应用CX门，其中量子比特0是控制位，量子比特1是目标位。理想状态为(|00⟩ + |11⟩)/√2。",
            "steps": "1. 从|00⟩开始\n2. 对量子比特0应用H门\n3. 应用CX（0 → 1）\n4. 测量两个量子比特（状态向量示意中可选）。",
        },
        "Three-Qubit GHZ State Circuit": {
            "title": "三量子比特GHZ态电路",
            "description": "这是一个由三个量子比特组成的纠缠态。先对量子比特0应用H门，再从量子比特0分别向量子比特1和2应用CX门。理想状态为(|000⟩ + |111⟩)/√2。",
            "steps": "1. 从|000⟩开始\n2. 对量子比特0应用H门\n3. 应用CX（0 → 1）\n4. 应用CX（0 → 2）\n5. 测量所有量子比特（状态向量示意中可选）。",
        },
    },
    "हिन्दी": {
        "The Bell State Circuit (Entanglement)": {
            "title": "बेल स्टेट सर्किट (क्वांटम उलझाव)",
            "description": "दो क्यूबिट की उलझी हुई अवस्था। पहले क्यूबिट 0 पर H लगाएँ, फिर CX लगाएँ जिसमें क्यूबिट 0 नियंत्रण और क्यूबिट 1 लक्ष्य है। आदर्श अवस्था (|00⟩ + |11⟩)/√2 है।",
            "steps": "1. |00⟩ से शुरू करें\n2. क्यूबिट 0 पर H लगाएँ\n3. CX (0 → 1) लगाएँ\n4. दोनों क्यूबिट का मापन करें (state-vector चित्रण के लिए वैकल्पिक)।",
        },
        "Three-Qubit GHZ State Circuit": {
            "title": "तीन-क्यूबिट GHZ स्टेट सर्किट",
            "description": "तीन क्यूबिट की उलझी हुई अवस्था। पहले क्यूबिट 0 पर H लगाएँ, फिर क्यूबिट 0 से क्यूबिट 1 और 2 तक CX लगाएँ। आदर्श अवस्था (|000⟩ + |111⟩)/√2 है।",
            "steps": "1. |000⟩ से शुरू करें\n2. क्यूबिट 0 पर H लगाएँ\n3. CX (0 → 1) लगाएँ\n4. CX (0 → 2) लगाएँ\n5. सभी क्यूबिट का मापन करें (state-vector चित्रण के लिए वैकल्पिक)।",
        },
    },
    "Português": {
        "The Bell State Circuit (Entanglement)": {
            "title": "Circuito do estado de Bell (entrelaçamento)",
            "description": "Um estado entrelaçado de dois qubits. Aplique H ao qubit 0 e depois CX, usando o qubit 0 como controle e o qubit 1 como alvo. O estado ideal é (|00⟩ + |11⟩)/√2.",
            "steps": "1. Comece em |00⟩\n2. Aplique H ao qubit 0\n3. Aplique CX (0 → 1)\n4. Meça os dois qubits (opcional para uma ilustração do vetor de estado).",
        },
        "Three-Qubit GHZ State Circuit": {
            "title": "Circuito do estado GHZ de três qubits",
            "description": "Um estado entrelaçado de três qubits. Aplique H ao qubit 0 e depois CX do qubit 0 para os qubits 1 e 2. O estado ideal é (|000⟩ + |111⟩)/√2.",
            "steps": "1. Comece em |000⟩\n2. Aplique H ao qubit 0\n3. Aplique CX (0 → 1)\n4. Aplique CX (0 → 2)\n5. Meça todos os qubits (opcional para uma ilustração do vetor de estado).",
        },
    },
}


# ─────────────────────────────────────────────
# LATEX EQUATION RENDERING
# Formula snippets are rendered to equation images using Matplotlib MathText.
# Install with: python -m pip install matplotlib
# Install with: python -m pip install matplotlib. If unavailable, text remains readable.
# ─────────────────────────────────────────────
try:
    from matplotlib.mathtext import math_to_image
    LATEX_RENDERING_AVAILABLE = True
except ImportError:
    math_to_image = None
    LATEX_RENDERING_AVAILABLE = False


def extract_equations(text):
    """Find equation-sized snippets embedded in technical prose."""
    patterns = [
        # Gate matrices and gate definitions.
        r'\b(?:H|X|Y|Z|S|T|SX|RX|RY|RZ|P|CX|SWAP|CCX|CSWAP)\s*(?:\([^)]*\))?\s*=\s*(?:1/√2\s*)?\[\[[^\]]+\],\[[^\]]+\]\](?:\s*=\s*σ[xyz])?',
        r'\b(?:H|X|Y|Z|S|T|SX|RX|RY|RZ|P|CX|SWAP|CCX|CSWAP)\s*(?:\([^)]*\))?\s*=\s*(?:diag|exp)\((?:[^()]|\([^()]*\))*\)',
        r'\bSWAP\s*\|[^|]*⟩\s*=\s*\|[^|]*⟩',
        r'\b(?:H|X|Y|Z|S|T|SX|RX|RY|RZ|P|CX|CCX|CSWAP)\s*\|[^|]*⟩\s*=\s*[^.;；。।\n]+',
        # State vectors, transformations, and common identities.
        r'\bCX\s*=\s*\|0⟩⟨0\|⊗I\+\|1⟩⟨1\|⊗X',
        r'\bSWAP\s*=\s*\(I⊗I\+X⊗X\+Y⊗Y\+Z⊗Z\)/2',
        r'\bS=T²=diag\(1,i\)',
        r'\bZ=diag\(1,-1\)=σz',
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
    return [item for item in found if not any(item != other and item in other for other in found)]


def text_without_rendered_equations(text):
    """Keep prose readable while avoiding duplicate raw text for rendered equations."""
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
    """Convert compact Unicode quantum notation to Matplotlib MathText syntax."""
    value = formula.strip().rstrip(".。")
    # Matplotlib MathText does not implement LaTeX matrix environments, so express
    # 2x2 matrices compactly with brackets and a semicolon separating rows.
    matrix_pattern = re.compile(r"\[\[([^\]]+)\],\[([^\]]+)\]\]")
    value = matrix_pattern.sub(lambda m: r"\left[" + m.group(1).replace(",", r"\quad ") + r"\ ;\ " + m.group(2).replace(",", r"\quad ") + r"\right]", value)
    value = re.sub(r"\|([^|⟩]+)⟩", r"|\1\\rangle", value)
    value = re.sub(r"⟨([^⟨|]+)\|", r"\\langle \1|", value)
    value = value.replace("√2", r"\sqrt{2}").replace("√", r"\sqrt{}")
    value = value.replace("θ", r"\theta ").replace("π", r"\pi ")
    value = value.replace("α", r"\alpha ").replace("β", r"\beta ")
    value = value.replace("σx", r"\sigma_x").replace("σy", r"\sigma_y").replace("σz", r"\sigma_z")
    value = value.replace("†", r"^{\dagger}").replace("ⁿ", "^n").replace("²", "^2")
    value = value.replace("×", r"\times ").replace("⊗", r"\otimes ")
    value = value.replace("→", r"\to ").replace("XOR", r"\mathrm{XOR}")
    value = re.sub(r"\s+(?:to|en|vers|in|へ|映射为|में)\s+", lambda m: r" \to ", value, flags=re.IGNORECASE)
    value = re.sub(r"\s+(?:and|y|et|und|e)\s+", lambda m: r",\quad ", value, flags=re.IGNORECASE)
    value = value.replace("、", r",\quad ").replace("且", r",\quad ").replace("और", r",\quad ")
    value = re.sub(r"\bdiag\(", lambda m: r"\mathrm{diag}(", value)
    value = re.sub(r"\bexp\(", lambda m: r"\exp(", value)
    # Normalize compact exponents such as e^(iπ/4) to LaTeX exponent braces.
    value = re.sub(r"e\^\(([^()]*)\)", lambda m: "e^{" + m.group(1) + "}", value)
    value = value.replace("=", r" = ").replace("/", r" / ")
    return value


def render_equation_pixmap(formula):
    """Render a formula as a transparent PNG and return it as a QPixmap."""
    if not LATEX_RENDERING_AVAILABLE:
        return None
    latex = to_mathtext(formula)
    buffer = BytesIO()
    try:
        math_to_image("$" + latex + "$", buffer, dpi=180, format="png", color="black")
        pixmap = QPixmap()
        if pixmap.loadFromData(buffer.getvalue(), "PNG"):
            return pixmap
    except Exception:
        return None
    return None


def add_equation_images(layout, source_text):
    """Add visually typeset equation images for equations found in technical content."""
    for formula in extract_equations(source_text):
        pixmap = render_equation_pixmap(formula)
        if pixmap is not None and not pixmap.isNull():
            equation = QLabel()
            equation.setPixmap(pixmap)
            equation.setAlignment(Qt.AlignmentFlag.AlignLeft)
            equation.setToolTip(formula)
            equation.setStyleSheet("background: #fbfbfb; padding: 5px; border-radius: 4px;")
            layout.addWidget(equation)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def build_circuit(circuit_name):
    """Return a Qiskit circuit when Qiskit is installed; otherwise return None."""
    if QuantumCircuit is None:
        return None
    if "Bell" in circuit_name or "bell" in circuit_name.lower():
        qc = QuantumCircuit(2, name="Bell State")
        qc.h(0)
        qc.cx(0, 1)
    else:
        qc = QuantumCircuit(3, name="GHZ State")
        qc.h(0)
        qc.cx(0, 1)
        qc.cx(0, 2)
    return qc


def render_circuit_pixmap(qc):
    """Render a Qiskit circuit as a PNG-backed QPixmap for display in Qt."""
    if qc is None:
        return None
    buffer = BytesIO()
    figure = None
    try:
        # The mpl drawer creates a real graphical circuit diagram.
        figure = qc.draw(output="mpl", fold=-1, style={"backgroundcolor": "#ffffff"})
        figure.savefig(buffer, format="png", dpi=160, bbox_inches="tight", facecolor="white")
        pixmap = QPixmap()
        if pixmap.loadFromData(buffer.getvalue(), "PNG") and not pixmap.isNull():
            return pixmap
    except Exception:
        # The caller falls back to the text diagram if visualization dependencies
        # such as pylatexenc are missing or the installed Qiskit version differs.
        return None
    finally:
        if figure is not None:
            try:
                import matplotlib.pyplot as plt
                plt.close(figure)
            except Exception:
                pass
    return None


def experience_index(experience_text, t):
    if experience_text == t["novice"]:
        return 0
    if experience_text == t["school"]:
        return 1
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
        self.country = QComboBox()
        self.country.addItems(COUNTRIES.keys())
        self.region = QComboBox()
        self.language = QComboBox()
        self.language.addItems(LANGUAGES)
        self.country.currentTextChanged.connect(self.update_regions)
        self.update_regions(self.country.currentText())

        layout = QVBoxLayout(self)
        title = QLabel("⚛️ Quantum Circuit Builder")
        title.setFont(QFont("Arial", 19, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        form = QFormLayout()
        form.addRow("Country:", self.country)
        form.addRow("State / Province:", self.region)
        form.addRow("Preferred language:", self.language)
        layout.addLayout(form)
        button = QPushButton("✔ Continue")
        button.setStyleSheet(BUTTON_STYLE_GREEN)
        button.clicked.connect(self.accept)
        layout.addWidget(button)

    def update_regions(self, country):
        self.region.clear()
        self.region.addItems(COUNTRIES.get(country, ["Not applicable"]))

    def get_answers(self):
        return {"country": self.country.currentText(), "state": self.region.currentText(), "language": self.language.currentText()}


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
        layout = QVBoxLayout(central); layout.setContentsMargins(35, 30, 35, 30); layout.setSpacing(18)
        title = QLabel(self.t["main"]); title.setAlignment(Qt.AlignmentFlag.AlignCenter); title.setFont(QFont("Arial", 20, QFont.Weight.Bold)); layout.addWidget(title)
        summary = QLabel(f"📍 {answers['state']}, {answers['country']}  |  🌐 {answers['language']}")
        summary.setAlignment(Qt.AlignmentFlag.AlignCenter); summary.setStyleSheet("color: gray;"); layout.addWidget(summary)
        self.experience = QComboBox(); self.experience.addItems([self.t["novice"], self.t["school"], self.t["university"]])
        row = QHBoxLayout(); row.addWidget(QLabel(self.t["experience"])); row.addWidget(self.experience); layout.addLayout(row)
        begin = QPushButton(self.t["begin"]); begin.setStyleSheet(BUTTON_STYLE_GREEN); begin.clicked.connect(self.begin_tutorial); layout.addWidget(begin)
        back = QPushButton(self.t["back"]); back.setStyleSheet(BUTTON_STYLE_BACK); back.clicked.connect(self.go_back); layout.addWidget(back)
        self.status = QLabel(self.t["ready"]); self.status.setAlignment(Qt.AlignmentFlag.AlignCenter); layout.addWidget(self.status)

    def go_back(self):
        self._closing_for_navigation = True; self.close(); self.back_requested.emit()

    def begin_tutorial(self):
        chosen = self.experience.currentText()
        self._closing_for_navigation = True; self.close(); self.next_requested.emit(chosen)

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

    def __init__(self, answers):
        super().__init__(); self.answers = answers; self.t = TRANSLATIONS.get(answers["language"], TRANSLATIONS["English"])
        self._closing_for_navigation = False
        self.setWindowTitle(self.t["title"]); self.setMinimumSize(650, 380)
        central = QWidget(); self.setCentralWidget(central); layout = QVBoxLayout(central); layout.setContentsMargins(35, 30, 35, 30); layout.setSpacing(18)
        title = QLabel("⚛️ Select a Quantum Circuit" if answers["language"] == "English" else self.t["choose_circuit"])
        title.setAlignment(Qt.AlignmentFlag.AlignCenter); title.setFont(QFont("Arial", 20, QFont.Weight.Bold)); layout.addWidget(title)
        summary = QLabel(f"📍 {answers['state']}, {answers['country']}  |  🌐 {answers['language']}  |  🎓 {answers['experience']}")
        summary.setAlignment(Qt.AlignmentFlag.AlignCenter); summary.setStyleSheet("color: gray;"); layout.addWidget(summary)
        layout.addWidget(QLabel(self.t["choose_circuit"]))
        self.circuit = QComboBox()
        if answers["language"] == "Español":
            self.circuit.addItems(["El Circuito de Estado Bell (Entrelazamiento)", "Circuito de Estado GHZ de Tres Qubits"])
        elif answers["language"] == "Français":
            self.circuit.addItems(["Le Circuit d'État de Bell (Intrication)", "Circuit d'État GHZ à Trois Qubits"])
        elif answers["language"] == "Deutsch":
            self.circuit.addItems(["Bell-Zustand-Schaltkreis (Verschränkung)", "Drei-Qubit-GHZ-Zustand-Schaltkreis"])
        elif answers["language"] == "日本語":
            self.circuit.addItems(["ベル状態回路（エンタングルメント）", "3量子ビットGHZ状態回路"])
        elif answers["language"] == "中文":
            self.circuit.addItems(["贝尔态电路（纠缠）", "三量子比特GHZ态电路"])
        elif answers["language"] == "हिन्दी":
            self.circuit.addItems(["बेल स्टेट सर्किट (उलझाव)", "तीन-क्यूबिट GHZ स्टेट सर्किट"])
        elif answers["language"] == "Português":
            self.circuit.addItems(["O Circuito de Estado Bell (Entrelaçamento)", "Circuito de Estado GHZ de Três Qubits"])
        else:
            self.circuit.addItems(list(CIRCUITS.keys()))
        layout.addWidget(self.circuit)
        explore = QPushButton(self.t["explore"]); explore.setStyleSheet(BUTTON_STYLE_GREEN); explore.clicked.connect(self.explore); layout.addWidget(explore)
        back = QPushButton(self.t["back"]); back.setStyleSheet(BUTTON_STYLE_BACK); back.clicked.connect(self.go_back); layout.addWidget(back)
        self.status = QLabel(self.t["ready"]); self.status.setAlignment(Qt.AlignmentFlag.AlignCenter); layout.addWidget(self.status)

    def canonical_circuit_name(self):
        return "Three-Qubit GHZ State Circuit" if self.circuit.currentIndex() == 1 else "The Bell State Circuit (Entanglement)"

    def go_back(self):
        self._closing_for_navigation = True; self.close(); self.back_requested.emit()

    def explore(self):
        self._closing_for_navigation = True; self.close(); self.next_requested.emit(self.canonical_circuit_name())

    def closeEvent(self, event):
        event.accept()
        if not self._closing_for_navigation:
            QApplication.quit()


# ─────────────────────────────────────────────
# WINDOW 4 - QUANTUM OPERATORS GUIDE + SELECTED CIRCUIT
# ─────────────────────────────────────────────
class OperatorsWindow(QMainWindow):
    back_requested = Signal()
    simulation_requested = Signal()

    def __init__(self, answers, circuit_name):
        super().__init__(); self.answers = answers; self.circuit_name = circuit_name
        self.t = TRANSLATIONS.get(answers["language"], TRANSLATIONS["English"])
        self._closing_for_navigation = False
        self.level = experience_index(answers["experience"], self.t)
        self.setWindowTitle(self.t["operators"]); self.setMinimumSize(850, 700); self.resize(1000, 850)
        root = QWidget(); self.setCentralWidget(root); outer = QVBoxLayout(root); outer.setContentsMargins(20, 18, 20, 18); outer.setSpacing(12)
        title = QLabel(self.t["operators"]); title.setFont(QFont("Arial", 20, QFont.Weight.Bold)); title.setAlignment(Qt.AlignmentFlag.AlignCenter); outer.addWidget(title)
        summary = QLabel(f"📍 {answers['state']}, {answers['country']}  |  🌐 {answers['language']}  |  🎓 {answers['experience']}")
        summary.setAlignment(Qt.AlignmentFlag.AlignCenter); summary.setStyleSheet("color: gray;"); outer.addWidget(summary)

        scroll = QScrollArea(); scroll.setWidgetResizable(True); outer.addWidget(scroll, 1)
        content = QWidget(); content_layout = QVBoxLayout(content); content_layout.setSpacing(12); scroll.setWidget(content)
        localized = OPERATOR_LOCALIZATIONS.get(answers["language"])
        for category_index, (category, items) in enumerate(OPERATORS):
            display_category = localized["categories"][category_index] if localized else category
            heading = QLabel(display_category); heading.setFont(QFont("Arial", 12, QFont.Weight.Bold)); heading.setStyleSheet("background: #e8f5e9; padding: 8px; border-radius: 5px;"); content_layout.addWidget(heading)
            for symbol, name, novice, school, university in items:
                card = QFrame(); card.setFrameShape(QFrame.Shape.StyledPanel); card_layout = QVBoxLayout(card)
                if localized and symbol in localized["gates"]:
                    display_name, descriptions = localized["gates"][symbol]
                    description = descriptions[self.level]
                    level_label = localized["levels"][self.level]
                else:
                    display_name = name
                    description = (novice, school, university)[self.level]
                    level_label = ""
                gate_title = QLabel(f"{symbol} — {display_name}"); gate_title.setFont(QFont("Arial", 11, QFont.Weight.Bold)); card_layout.addWidget(gate_title)
                prose = text_without_rendered_equations(description)
                text = QLabel(f"{self.t['description']}: {level_label}{prose}"); text.setWordWrap(True); card_layout.addWidget(text)
                add_equation_images(card_layout, description)
                content_layout.addWidget(card)

        circuit_heading = QLabel(self.t["circuit"]); circuit_heading.setFont(QFont("Arial", 13, QFont.Weight.Bold)); circuit_heading.setStyleSheet("background: #e3f2fd; padding: 9px; border-radius: 5px;"); content_layout.addWidget(circuit_heading)
        circuit_data = CIRCUITS[circuit_name]
        localized_circuits = CIRCUIT_LOCALIZATIONS.get(answers["language"], {})
        display_circuit = localized_circuits.get(circuit_name, circuit_data)
        display_circuit_title = display_circuit.get("title", circuit_name)
        circuit_description = display_circuit["description"]
        circuit_steps = display_circuit["steps"]
        circuit_text = QLabel(
            f"{display_circuit_title}\n\n"
            f"{text_without_rendered_equations(circuit_description)}\n\n"
            f"{text_without_rendered_equations(circuit_steps)}"
        )
        circuit_text.setWordWrap(True); circuit_text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse); content_layout.addWidget(circuit_text)
        add_equation_images(content_layout, f"{circuit_description}\n{circuit_steps}")
        qc = build_circuit(circuit_name)
        if qc is not None:
            circuit_pixmap = render_circuit_pixmap(qc)
            if circuit_pixmap is not None:
                diagram = QLabel()
                diagram.setPixmap(circuit_pixmap)
                diagram.setAlignment(Qt.AlignmentFlag.AlignCenter)
                diagram.setScaledContents(False)
                diagram.setMinimumHeight(circuit_pixmap.height() + 16)
                diagram.setToolTip("Graphical quantum circuit diagram")
            else:
                # Keep the circuit visible even if graphical-drawer dependencies
                # are missing: show the text drawing as a reliable fallback.
                diagram = QLabel(
                    qc.draw(output="text", fold=-1).__str__()
                    + "\n\nFor graphical circuit images, install the visualization dependencies with:\n"
                    + "python -m pip install 'qiskit[visualization]'"
                )
                diagram.setFont(QFont("Menlo", 11))
                diagram.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        else:
            diagram = QLabel(
                "Qiskit is not installed, so a generated circuit diagram is unavailable.\n"
                "Install it with: python -m pip install 'qiskit[visualization]'"
            )
        diagram.setWordWrap(True); diagram.setStyleSheet("background: #f7f7f7; padding: 10px;"); content_layout.addWidget(diagram)

        buttons = QHBoxLayout()
        back = QPushButton(self.t["back"]); back.setStyleSheet(BUTTON_STYLE_BACK); back.clicked.connect(self.go_back); buttons.addWidget(back)
        simulate = QPushButton("▶ Theory & Local Simulation" if answers["language"] == "English" else "▶ Simulation locale"); simulate.setStyleSheet(BUTTON_STYLE_GREEN); simulate.clicked.connect(self.open_simulation); buttons.addWidget(simulate)
        close = QPushButton("✕ Close" if answers["language"] == "English" else self.t["back"]); close.setStyleSheet(BUTTON_STYLE_BACK); close.clicked.connect(self.close_application); buttons.addWidget(close)
        outer.addLayout(buttons)

    def go_back(self):
        self._closing_for_navigation = True; self.close(); self.back_requested.emit()

    def open_simulation(self):
        self._closing_for_navigation = True
        self.close()
        self.simulation_requested.emit()

    def close_application(self):
        self._closing_for_navigation = True; self.close(); QApplication.quit()

    def closeEvent(self, event):
        event.accept()
        if not self._closing_for_navigation:
            QApplication.quit()


# ─────────────────────────────────────────────
# WINDOW 5 - THEORETICAL EXPECTATIONS + LOCAL SIMULATION
# Runs on the user's laptop; no cloud account or quantum hardware is used.
# ─────────────────────────────────────────────
class SimulationWindow(QMainWindow):
    back_requested = Signal()

    def __init__(self, answers, circuit_name):
        super().__init__()
        self.answers = answers
        self.circuit_name = circuit_name
        self.t = TRANSLATIONS.get(answers["language"], TRANSLATIONS["English"])
        self._closing_for_navigation = False
        self.setWindowTitle("Quantum Theory & Local Simulation")
        self.setMinimumSize(850, 650)
        self.resize(1000, 800)

        root = QWidget(); self.setCentralWidget(root)
        outer = QVBoxLayout(root); outer.setContentsMargins(20, 18, 20, 18); outer.setSpacing(10)
        title = QLabel("⚛️ Theoretical Expectations & Local Simulation")
        title.setFont(QFont("Arial", 19, QFont.Weight.Bold)); title.setAlignment(Qt.AlignmentFlag.AlignCenter); outer.addWidget(title)
        intro = QLabel(
            f"Circuit: {CIRCUIT_LOCALIZATIONS.get(answers['language'], {}).get(circuit_name, CIRCUITS[circuit_name]).get('title', circuit_name)}\n"
            "The theory below is the ideal, noiseless prediction. The simulator runs locally on this computer; "
            "it does not submit jobs to a cloud service or quantum device."
        )
        intro.setWordWrap(True); outer.addWidget(intro)

        scroll = QScrollArea(); scroll.setWidgetResizable(True); outer.addWidget(scroll, 1)
        body = QWidget(); body_layout = QVBoxLayout(body); body_layout.setSpacing(12); scroll.setWidget(body)

        theory = QTextBrowser(); theory.setOpenExternalLinks(False); theory.setMinimumHeight(245)
        if "Bell" in circuit_name:
            theory_html = """
            <h3>Gate-by-gate theoretical expectations</h3>
            <p><b>Initial state:</b> both qubits start in |00⟩.</p>
            <p><b>1. Hadamard H on qubit 0</b><br>H creates an equal superposition from |0⟩. The two-qubit state becomes (|00⟩ + |10⟩)/√2 when ket positions are written in qubit-index order (q0, q1). Each branch has probability 1/2.</p>
            <p><b>2. Controlled-X (CNOT), control 0 → target 1</b><br>CNOT flips the target when the control is |1⟩. The final Bell state is |Φ⁺⟩ = (|00⟩ + |11⟩)/√2. Ideal measurement outcomes are 00 and 11, each with probability 50%; 01 and 10 have probability 0.</p>
            <p><b>Expected values:</b> P(00)=1/2, P(11)=1/2, P(01)=P(10)=0. Each qubit individually is 0 or 1 with equal probability, while the two results are perfectly correlated.</p>
            """
            formulas = "H = 1/√2 [[1, 1], [1, -1]]\n|Φ⁺⟩ = (|00⟩ + |11⟩)/√2\nP(00) = P(11) = 1/2; P(01) = P(10) = 0"
        else:
            theory_html = """
            <h3>Gate-by-gate theoretical expectations</h3>
            <p><b>Initial state:</b> all three qubits start in |000⟩.</p>
            <p><b>1. Hadamard H on qubit 0</b><br>Creates an equal superposition: (|000⟩ + |100⟩)/√2 when ket positions are written in qubit-index order (q0, q1, q2). Each branch has probability 1/2.</p>
            <p><b>2. CNOT, control 0 → target 1</b><br>Copies the control's computational-basis value to qubit 1, giving (|000⟩ + |110⟩)/√2 in q0,q1,q2 order.</p>
            <p><b>3. CNOT, control 0 → target 2</b><br>Correlates the third qubit too, producing the GHZ state |GHZ⟩ = (|000⟩ + |111⟩)/√2.</p>
            <p><b>Expected values:</b> P(000)=1/2, P(111)=1/2; all other six outcomes have probability 0. All three qubits are perfectly correlated when measured in the computational basis.</p>
            """
            formulas = "|GHZ⟩ = (|000⟩ + |111⟩)/√2\nP(000) = P(111) = 1/2; all other outcomes have probability 0"
        theory.setHtml(theory_html); body_layout.addWidget(theory)
        add_equation_images(body_layout, formulas)

        control_row = QHBoxLayout()
        control_row.addWidget(QLabel("Number of measurement shots:"))
        self.shots = QComboBox(); self.shots.addItems(["100", "1,000", "10,000"]); self.shots.setCurrentIndex(1)
        control_row.addWidget(self.shots)
        run = QPushButton("▶ Run Local Simulation"); run.setStyleSheet(BUTTON_STYLE_GREEN); run.clicked.connect(self.run_simulation); control_row.addWidget(run)
        body_layout.addLayout(control_row)

        self.result = QTextBrowser(); self.result.setMinimumHeight(190); self.result.setPlaceholderText("Click Run Local Simulation to see sampled measurement counts.")
        body_layout.addWidget(self.result)
        self.status = QLabel("Status: Ready — simulation stays on this laptop."); self.status.setWordWrap(True); outer.addWidget(self.status)

        buttons = QHBoxLayout()
        back = QPushButton(self.t["back"]); back.setStyleSheet(BUTTON_STYLE_BACK); back.clicked.connect(self.go_back); buttons.addWidget(back)
        close = QPushButton("✕ Close Application"); close.setStyleSheet(BUTTON_STYLE_BACK); close.clicked.connect(self.close_application); buttons.addWidget(close)
        outer.addLayout(buttons)

    def run_simulation(self):
        if QuantumCircuit is None or Statevector is None:
            self.result.setPlainText(
                "Qiskit is not installed. In the VS Code terminal, run:\n\n"
                "python -m pip install 'qiskit[visualization]' matplotlib\n\n"
                "Then restart the application and try again."
            )
            self.status.setText("Simulation unavailable: install Qiskit first.")
            return
        import random
        qc = build_circuit(self.circuit_name)
        state = Statevector.from_instruction(qc)
        probabilities = state.probabilities_dict()
        shots = int(self.shots.currentText().replace(",", ""))
        # Sample the exact statevector probabilities locally, without Aer or a network connection.
        outcomes = list(probabilities.keys())
        weights = [float(probabilities[key]) for key in outcomes]
        samples = random.choices(outcomes, weights=weights, k=shots)
        counts = {key: samples.count(key) for key in sorted(set(samples))}
        width = qc.num_qubits
        all_outcomes = [format(i, f"0{width}b") for i in range(2 ** width)]
        rows = []
        for outcome in all_outcomes:
            # Qiskit's displayed bitstrings are ordered c[n-1]...c[0]. Bell/GHZ outcomes are symmetric.
            prob = float(probabilities.get(outcome, 0.0))
            count = counts.get(outcome, 0)
            rows.append(f"{outcome:<10} {prob:>10.1%} {count:>12} {count/shots:>12.1%}")
        state_lines = []
        for label, amplitude in state.to_dict().items():
            if abs(amplitude) > 1e-10:
                state_lines.append(f"|{label}⟩: amplitude {amplitude.real:+.4f}{amplitude.imag:+.4f}i")
        self.result.setPlainText(
            f"LOCAL STATEVECTOR SIMULATION — {shots:,} shots\n\n"
            f"Final state amplitudes (Qiskit bit-string convention):\n  " + "\n  ".join(state_lines) + "\n\n"
            f"{'Outcome':<10} {'Theory':>10} {'Sample count':>12} {'Observed':>12}\n"
            f"{'-'*48}\n" + "\n".join(rows) + "\n\n"
            "Theory = exact ideal probability; Observed = this run's sampled fraction. "
            "Finite-shot counts fluctuate, so observed percentages may differ slightly from theory."
        )
        self.status.setText(f"Simulation complete: {shots:,} shots sampled locally. No cloud or quantum hardware used.")

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
    answers = dialog.get_answers()
    launch_main(answers)


def launch_main(answers):
    window = MainWindow(answers)
    window.back_requested.connect(launch_questionnaire)
    window.next_requested.connect(lambda experience: launch_circuit({**answers, "experience": experience}))
    window.show(); app._main_window = window


def launch_circuit(answers):
    window = CircuitWindow(answers)
    window.back_requested.connect(lambda: launch_main({k: answers[k] for k in ("country", "state", "language")}))
    window.next_requested.connect(lambda circuit_name: launch_operators(answers, circuit_name))
    window.show(); app._circuit_window = window


def launch_operators(answers, circuit_name):
    window = OperatorsWindow(answers, circuit_name)
    window.back_requested.connect(lambda: launch_circuit(answers))
    window.simulation_requested.connect(lambda: launch_simulation(answers, circuit_name))
    window.show(); app._operators_window = window


def launch_simulation(answers, circuit_name):
    window = SimulationWindow(answers, circuit_name)
    window.back_requested.connect(lambda: launch_operators(answers, circuit_name))
    window.show(); app._simulation_window = window


# ─────────────────────────────────────────────
# MAIN - APP ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    launch_questionnaire()
    sys.exit(app.exec())
