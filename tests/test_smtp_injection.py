import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from email.mime.text import MIMEText  # noqa: E402

from routes import auth  # noqa: E402


class SmtpInjectionTests(unittest.TestCase):
    def test_email_helper_attaches_unsanitized_crlf_headers(self):
        """Vuln #161: the SMTP helper stores attacker CRLF headers verbatim.

        The helper assigns the raw recipient string without any sanitization.
        The Python runtime's serializer rejects such a value at send time, so
        this regression asserts the unsanitized attachment step the lab code
        performs before serialization instead of a delivered message.
        """

        injected_to = "victim@example.test\r\nBcc: target@attacker.test"
        captured = {}

        real_mime_text = MIMEText

        class CapturingMimeText(real_mime_text):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                captured["message"] = self

        with mock.patch.object(auth, "MIMEText", CapturingMimeText):
            auth.send_email_smtp(injected_to, "Verify your email", "body")

        self.assertEqual(captured["message"]["To"], injected_to)
        self.assertIn("\r\n", captured["message"]["To"])


if __name__ == "__main__":
    unittest.main()
