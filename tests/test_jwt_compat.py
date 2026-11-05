import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from utils import jwt_compat  # noqa: E402


class JwtCompatTests(unittest.TestCase):
    def test_signed_token_round_trips_and_rejects_tampering(self):
        token = jwt_compat.encode({"sub": "lab-user", "role": "user"}, "lab-secret")
        self.assertEqual(jwt_compat.decode(token, "lab-secret", ["HS256"])["sub"], "lab-user")
        pieces = token.split(".")
        pieces[1] = jwt_compat._b64encode(b'{"sub":"other-user"}')
        with self.assertRaises(jwt_compat.InvalidTokenError):
            jwt_compat.decode(".".join(pieces), "lab-secret", ["HS256"])

    def test_signature_skip_option_accepts_unsigned_training_token(self):
        token = jwt_compat.encode({"sub": "lab-user"}, "", algorithm="none")
        self.assertEqual(jwt_compat.decode(token, options={"verify_signature": False})["sub"], "lab-user")


if __name__ == "__main__":
    unittest.main()
