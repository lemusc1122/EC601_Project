# Spanish-to-English static string comparison

Reviewed Spanish static strings against their English static counterparts. This is not an automated provider round trip; the prototype has no translation provider.

- Fields reviewed: 74
- Exact text matches (Yes): 43
- Non-exact English renderings (No): 31
- Match rate: 58.1%
- Wording items flagged: 3

Exact comparison ignores only outer whitespace; wording differences can remain semantically equivalent.

## Items flagged for review

### TRANSLATIONS / `novice`

- Spanish: Desde cero
- English static: Brand new
- English rendering: Starting from scratch
- Note: Close in context, but “from scratch” is less direct than “brand new”; consider “Principiante total.”

### TRANSLATIONS / `playground`

- Spanish: 🧩 Zona de dos qubits
- English static: 🧩 Two-Qubit Playground
- English rendering: 🧩 Two-qubit area
- Note: “Area” is less playful and less specific than “playground.”

### TRANSLATIONS / `shots`

- Spanish: Número de mediciones:
- English static: Number of circuit runs:
- English rendering: Number of measurements:
- Note: Meaning differs: measurements are outcomes; circuit runs are repetitions. Consider “Número de ejecuciones del circuito.”
