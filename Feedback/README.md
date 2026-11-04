# Local feedback issues

Feedback submitted from the prototype is saved here as a Markdown file with an
open status, submission time, screen context, and the text entered by the user.
When `QCB_FEEDBACK_API_URL` is configured, the app also sends the feedback to
the HTTPS backend, which creates a GitHub issue. The local file remains as a
copy. Without a configured endpoint, the submission stays local.
