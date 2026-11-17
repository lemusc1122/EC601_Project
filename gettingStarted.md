# Getting started

## Local prototype

The prototype uses Python 3.11 and the dependencies listed in `install_dependencies.bash`. From the repository root on macOS or Linux:

```bash
./install_dependencies.bash
source .venv/bin/activate
python prototype.py
```

The installer creates a project-local `.venv`; activate it again in each new terminal before launching the app. Audio narration is optional and uses the operating system's installed text-to-speech voices. Voice availability varies by system.

## Build a Windows executable

Build on a Windows machine or Windows virtual machine. The executable is
platform-specific, so a build made on macOS or Linux cannot run on Windows.
Use Python 3.11 or 3.12 for the build (64-bit on Windows).

1. Clone the repository onto Windows.
2. Double-click `packaging\windows\BuildApp.bat`. It selects Python 3.12 if
   installed, otherwise Python 3.11, then creates the matching virtual
   environment and installs the build dependencies. You do not need to create
   or activate the environment yourself. You can also start the builder from
   PowerShell in the repository root:

   ```powershell
   py -3.11 packaging\build_app.py
   ```

3. Run the executable:

   ```powershell
   .\dist\QuantumCircuitBuilder\QuantumCircuitBuilder.exe
   ```

   Distribute the entire `dist\QuantumCircuitBuilder` directory; the executable
   needs the runtime files alongside it.

The bundle includes the Python runtime and dependencies in separate files,
so distribute the full folder rather than only the `.exe`. Qiskit is included
for the optional circuit simulation and diagram features. IBM Quantum hardware
access remains a separate script and is not packaged into this desktop app.

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

Feedback submitted in the application is saved as a local Markdown copy in
`Feedback/`. To also send it to GitHub Issues, deploy `feedback_backend.py`
behind HTTPS, configure its `GITHUB_TOKEN` secret, then set
`QCB_FEEDBACK_API_URL` to the deployed `/feedback` endpoint
or add the URL to `feedback_config.json` alongside the script or executable.
The GitHub token belongs only on the backend. See the Remote feedback section
in `README.md` for details.

## Package on macOS

Double-click `packaging/macos/BuildApp.command`. It selects Python 3.12 if
available, otherwise Python 3.11, then creates the matching virtual environment
and installs the build dependencies. You do not need to create or activate the
environment yourself. Python 3.11 or 3.12 must already be installed. You can
also run the shared builder from the repository root:

```bash
python3.11 packaging/build_app.py
```

The shared builder is `packaging/build_app.py`. The matching platform files are
named `setup.py` and `requirements.txt` in both `packaging/macos/` and
`packaging/windows/`.
