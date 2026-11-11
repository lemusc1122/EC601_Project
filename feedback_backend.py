"""Small HTTPS-proxyable endpoint that turns prototype feedback into GitHub issues.

Configure GITHUB_TOKEN, then run this behind an HTTPS reverse proxy. The
repository defaults to lemusc1122/EC601_Project and can be overridden with
GITHUB_REPOSITORY. Never put the GitHub token in the desktop application.
"""

import json
import os
import time
from collections import defaultdict, deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

MAX_BODY_BYTES = 16_000
RATE_WINDOW_SECONDS = 60
RATE_LIMIT = 5
_requests_by_ip = defaultdict(deque)


class FeedbackHandler(BaseHTTPRequestHandler):
    def _reply(self, status, body):
        encoded = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(encoded)

    def do_POST(self):
        if self.path != "/feedback":
            self._reply(404, {"error": "not found"})
            return

        try:
            size = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._reply(400, {"error": "invalid content length"})
            return
        if size <= 0 or size > MAX_BODY_BYTES:
            self._reply(413, {"error": "feedback is empty or too large"})
            return

        now = time.monotonic()
        # Only trust this header when the HTTPS proxy overwrites it on ingress.
        client_ip = self.headers.get("X-Forwarded-For", self.client_address[0]).split(",", 1)[0].strip()
        recent = _requests_by_ip[client_ip]
        while recent and now - recent[0] > RATE_WINDOW_SECONDS:
            recent.popleft()
        if len(recent) >= RATE_LIMIT:
            self._reply(429, {"error": "rate limit exceeded"})
            return
        recent.append(now)

        try:
            payload = json.loads(self.rfile.read(size).decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("object required")
            feedback = payload.get("feedback", "").strip()
            source = payload.get("source", "Unknown screen").strip()
            language = payload.get("language", "Unknown").strip()
            submitted = payload.get("submitted", "Unknown").strip()
            if not all(isinstance(v, str) for v in (feedback, source, language, submitted)):
                raise ValueError("string fields required")
            if not feedback or len(feedback) > 12_000:
                raise ValueError("feedback length out of range")
        except (UnicodeDecodeError, json.JSONDecodeError, AttributeError, ValueError):
            self._reply(400, {"error": "invalid feedback payload"})
            return

        token = os.environ.get("GITHUB_TOKEN", "")
        repository = os.environ.get("GITHUB_REPOSITORY", "lemusc1122/EC601_Project")
        if not token or "/" not in repository or repository.count("/") != 1:
            self._reply(503, {"error": "feedback service is not configured"})
            return

        owner, repo = repository.split("/", 1)
        title = f"Student feedback: {source[:100]} ({language[:40]})"
        body = (
            f"**Screen:** {source}\n\n"
            f"**Interface language:** {language}\n\n"
            f"**Submitted:** {submitted}\n\n"
            f"### Feedback\n\n{feedback}\n"
        )
        request = Request(
            f"https://api.github.com/repos/{owner}/{repo}/issues",
            data=json.dumps({"title": title, "body": body}).encode("utf-8"),
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "Quantum-Circuit-Builder-Feedback",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urlopen(request, timeout=12) as response:
                issue = json.loads(response.read(65536).decode("utf-8"))
            self._reply(201, {"url": issue.get("html_url", "")})
        except HTTPError as exc:
            # Do not send GitHub's response body or credentials to desktop clients.
            self._reply(502, {"error": f"GitHub returned HTTP {exc.code}"})
        except (URLError, TimeoutError, OSError, ValueError):
            self._reply(502, {"error": "GitHub could not be reached"})
    
    def do_GET(self):
        if self.path == "/health":
            self._reply(200, {"status": "ok"})
        else:
            self._reply(404, {"error": "not found"})
    
    def log_message(self, format, *args):
        # Avoid logging submitted feedback or other request data.
        return


if __name__ == "__main__":
    host = os.environ.get("FEEDBACK_HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", os.environ.get("FEEDBACK_PORT", "10000")))
    server = ThreadingHTTPServer((host, port), FeedbackHandler)
    print(f"Feedback API listening on {host}:{port}; expose it only through HTTPS.")
    server.serve_forever()
