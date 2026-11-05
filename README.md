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
- `feedback_backend.py` — optional HTTPS service that saves submissions in the GitHub `Feedback/` directory.

## Remote feedback

To enable the prototype's Submit button to save feedback into GitHub, deploy the
included `render.yaml` blueprint from this repository. In the hosting service,
set `GITHUB_TOKEN` to a fine-grained token that has
**Contents: write** access to the `lemusc1122/EC601_Project` repository. The
backend defaults to that repository and writes each submission as a Markdown
file under `Feedback/`; set `GITHUB_REPOSITORY` to `owner/name` only if
using a different repository. After deployment, set `QCB_FEEDBACK_API_URL` to
the service URL ending in `/feedback`, or copy
`feedback_config.example.json` to `feedback_config.json` and replace the
placeholder with that URL. Put the config beside the script or packaged
executable. Keep the GitHub token on the server; never include it in the
desktop app. The service health check is available at `/health`.

The app saves a local Markdown copy and sends the same feedback to the endpoint
in the background. The backend creates a uniquely named Markdown file in the
`Feedback/` directory in the GitHub repository. If no endpoint URL is configured, submissions
remain local. The backend uses a small per-process rate limit; put additional
rate limiting at the hosting proxy before exposing it publicly. Configure the
proxy to overwrite `X-Forwarded-For` if using that header for per-student limits.
- `docs/` — project documentation and references.
- `SPRINT1.md`, `TEAM.md`, and `brainstormingPart*.md` — project planning and notes.
