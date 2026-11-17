# Quantum Circuit Builder

A desktop learning prototype for exploring quantum gates, example circuits, local simulations, and a BB84 plus one-time-pad teaching demonstration. The interface currently supports English, Spanish, and Arabic.

## Run the prototype

From macOS or Linux, in the repository root:

```bash
./install_dependencies.bash
source .venv/bin/activate
python prototype.py
```

See [gettingStarted.md](gettingStarted.md) for setup notes and the optional IBM Quantum hardware example.

## Build an app or executable

Clone this repository on the target machine and install Python 3.11 or 3.12
(64-bit on Windows). Double-click the platform launcher; it selects an installed
Python version, creates a version-specific virtual environment, installs the
build dependencies there, and builds the app. You do not need to create or
activate the environment yourself:

- Windows: `packaging/windows/BuildApp.bat`
- macOS: `packaging/macos/BuildApp.command`

The launchers keep the terminal window open so you can read build errors. You
can also run the shared builder from the repository root:

Windows PowerShell:

```powershell
py -3.11 packaging\build_app.py
```

macOS Terminal:

```bash
python3.11 packaging/build_app.py
```

The environment is named `.venv-windows-py311` or `.venv-windows-py312` on
Windows, and `.venv-macos-py311` or `.venv-macos-py312` on macOS. The builder
uses `packaging/windows/requirements.txt` or `packaging/macos/requirements.txt`.
Both platform folders use the same names for their `requirements.txt` and
`setup.py` files. Windows output is in
`dist/QuantumCircuitBuilder/QuantumCircuitBuilder.exe`; macOS output is
`dist/PrototypeApp.app`. Build on the same operating system and architecture
where the app will be used.

## Repository contents

- `prototype.py` — desktop application and local demonstrations.
- `firstQiskitScript.py` — optional Bell-state job submitted to IBM Quantum hardware.
- `install_dependencies.bash` — creates `.venv` and installs dependencies for the local prototype.
- `packaging/macos/` and `packaging/windows/` — platform-specific packaging configuration and build dependencies.
- `Feedback/` — local Markdown copies of feedback submissions.
- `feedback_backend.py` — optional HTTPS-proxyable service that files feedback as GitHub issues.

## Remote feedback

To send feedback to GitHub Issues, deploy `feedback_backend.py` behind an HTTPS
reverse proxy. Configure `GITHUB_TOKEN` with a fine-grained token that has
**Issues: write** access to this repository. The backend defaults to
`lemusc1122/EC601_Project`; set `GITHUB_REPOSITORY` to `owner/name` only if
using a different repository. Set `QCB_FEEDBACK_API_URL` to the deployed endpoint URL ending in
`/feedback`, or update `feedback_config.json` in the project before packaging.
`packaging/macos/setup.py` includes this file in the macOS app bundle; a config beside the app
executable can override it. Keep the GitHub token on the server; never include
it in the desktop app.

The app continues to save a local Markdown copy and sends the same feedback to
the endpoint in the background. If no endpoint URL is configured, submissions
remain local. The backend uses a small per-process rate limit; put additional
rate limiting at the hosting proxy before exposing it publicly. Configure the
proxy to overwrite `X-Forwarded-For` if using that header for per-student limits.
- `docs/` — project documentation and references.
- `SPRINT1.md`, `TEAM.md`, and `brainstormingPart*.md` — project planning and notes.
