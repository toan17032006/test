import sys
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from routes import auth  # noqa: E402


class PasswordResetExpiryTests(unittest.TestCase):
    def test_reset_accepts_a_token_created_ten_years_ago(self):
        email = "expired-reset-marker@example.test"
        token = "LAB_ONLY_EXPIRED_RESET_TOKEN"
        auth.users_db[email] = {
            "id": 99999,
            "email": email,
            "password_hash": "old-hash",
            "password_plain": "old-password",
        }
        auth.reset_tokens_db[token] = {
            "email": email,
            "created_at": time.time() - 10 * 365 * 24 * 60 * 60,
        }
        try:
            coroutine = auth.reset_password(
                auth.ResetPasswordRequest(
                    token=token,
                    new_password="Synthetic-New-Password-Only",
                )
            )
            with self.assertRaises(StopIteration) as completed:
                coroutine.send(None)
            result = completed.exception.value
            self.assertEqual(result["message"], "Password reset successful")
            self.assertEqual(
                auth.users_db[email]["password_plain"],
                "Synthetic-New-Password-Only",
            )
        finally:
            auth.reset_tokens_db.pop(token, None)
            auth.users_db.pop(email, None)


if __name__ == "__main__":
    unittest.main()
