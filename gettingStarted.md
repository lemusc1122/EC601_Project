# Getting started

## Local prototype

The prototype uses Python 3.11 and the dependencies listed in `install_dependencies.bash`. From the repository root on macOS or Linux:

```bash
./install_dependencies.bash
source .venv/bin/activate
python prototype.py
```

The installer creates a project-local `.venv`; activate it again in each new terminal before launching the app. Audio narration is optional and uses the operating system's installed text-to-speech voices. Voice availability varies by system.

## Optional IBM Quantum hardware example

`firstQiskitScript.py` submits a Bell-state circuit to a real IBM Quantum device. It is separate from the local prototype and requires an IBM Quantum API key, an internet connection, and `qiskit-ibm-runtime`. Hardware use may be subject to account or usage limits.

Activate `.venv`, then install the optional runtime package:

```bash
python -m pip install qiskit-ibm-runtime
```

Set `IBM_QUANTUM_TOKEN` for the current terminal session, then run the script:

- macOS / Linux: `export IBM_QUANTUM_TOKEN="your-api-key"`
- Windows PowerShell: `$env:IBM_QUANTUM_TOKEN = "your-api-key"`

If your IBM Quantum account has multiple service instances, set `IBM_QUANTUM_INSTANCE` to the instance CRN to select one explicitly. This setting is optional when your account can select an instance automatically.

The script reads the token from the environment and does not save it to the local Qiskit account configuration. Never commit or paste an API key into source code. If a key has been shared or committed, revoke it and create a replacement in IBM Quantum before using the example.

## Feedback

Feedback submitted in the application is saved as a local Markdown issue in `Feedback/`. The prototype does not send it to a remote issue tracker.
