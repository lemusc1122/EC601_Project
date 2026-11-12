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

## Repository contents

- `prototype.py` — desktop application and local demonstrations.
- `firstQiskitScript.py` — optional Bell-state job submitted to IBM Quantum hardware.
- `install_dependencies.bash` — creates `.venv` and installs dependencies for the local prototype.
- `Feedback/` — local Markdown copies of feedback submissions.
- `feedback_backend.py` — optional HTTPS-proxyable service that files feedback as GitHub issues.

## Remote feedback

To send feedback to GitHub Issues, deploy `feedback_backend.py` behind an HTTPS
reverse proxy. Configure `GITHUB_TOKEN` with a fine-grained token that has
**Issues: write** access to this repository. The backend defaults to
`lemusc1122/EC601_Project`; set `GITHUB_REPOSITORY` to `owner/name` only if
using a different repository. Set `QCB_FEEDBACK_API_URL` to the deployed endpoint URL ending in
`/feedback`, or update `feedback_config.json` in the project before packaging.
`setup.py` includes this file in the macOS app bundle; a config beside the app
executable can override it. Keep the GitHub token on the server; never include
it in the desktop app.

The app continues to save a local Markdown copy and sends the same feedback to
the endpoint in the background. If no endpoint URL is configured, submissions
remain local. The backend uses a small per-process rate limit; put additional
rate limiting at the hosting proxy before exposing it publicly. Configure the
proxy to overwrite `X-Forwarded-For` if using that header for per-student limits.
- `docs/` — project documentation and references.
- `SPRINT1.md`, `TEAM.md`, and `brainstormingPart*.md` — project planning and notes.
