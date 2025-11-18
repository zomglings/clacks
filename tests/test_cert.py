import tempfile
import unittest
from pathlib import Path

from cryptography import x509

from slack_clacks.auth.cert import (
    ensure_cert_exists,
    generate_self_signed_cert,
    get_cert_info,
    get_cert_paths,
)


class TestCertificatePaths(unittest.TestCase):
    def test_get_cert_paths(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cert_path, key_path = get_cert_paths(tmpdir)
            self.assertEqual(cert_path, Path(tmpdir) / "localhost.crt")
            self.assertEqual(key_path, Path(tmpdir) / "localhost.key")


class TestCertificateGeneration(unittest.TestCase):
    def test_generate_self_signed_cert(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cert_path, key_path = generate_self_signed_cert(tmpdir)

            self.assertTrue(cert_path.exists())
            self.assertTrue(key_path.exists())

            with open(cert_path, "rb") as f:
                cert = x509.load_pem_x509_certificate(f.read())
                self.assertEqual(
                    cert.subject.get_attributes_for_oid(x509.oid.NameOID.COMMON_NAME)[
                        0
                    ].value,
                    "localhost",
                )

    def test_ensure_cert_exists_creates_if_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cert_path, key_path = ensure_cert_exists(tmpdir)

            self.assertTrue(cert_path.exists())
            self.assertTrue(key_path.exists())

    def test_ensure_cert_exists_reuses_existing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cert_path_1, key_path_1 = ensure_cert_exists(tmpdir)
            mtime_1 = cert_path_1.stat().st_mtime

            cert_path_2, key_path_2 = ensure_cert_exists(tmpdir)
            mtime_2 = cert_path_2.stat().st_mtime

            self.assertEqual(cert_path_1, cert_path_2)
            self.assertEqual(mtime_1, mtime_2)


class TestCertificateInfo(unittest.TestCase):
    def test_get_cert_info(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            generate_self_signed_cert(tmpdir)
            info = get_cert_info(tmpdir)

            self.assertIsNotNone(info)
            self.assertIn("CN=localhost", info["subject"])
            self.assertIsNotNone(info["not_valid_before"])
            self.assertIsNotNone(info["not_valid_after"])
            self.assertIsNotNone(info["serial_number"])

    def test_get_cert_info_no_cert(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            info = get_cert_info(tmpdir)
            self.assertIsNone(info)


if __name__ == "__main__":
    unittest.main()
