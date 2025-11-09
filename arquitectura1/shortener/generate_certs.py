from pathlib import Path
from datetime import datetime, timedelta, timezone

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID


CERTS_DIR = Path(__file__).resolve().parent / "certs"
KEY_PATH = CERTS_DIR / "server.key"
CRT_PATH = CERTS_DIR / "server.crt"


def generate():
    CERTS_DIR.mkdir(exist_ok=True)

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    subject = issuer = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, "CL"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Valparaiso"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Valparaiso"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "ShortenerV1"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ]
    )

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(timezone.utc) - timedelta(days=1))
        .not_valid_after(datetime.now(timezone.utc) + timedelta(days=3650))
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName("localhost")]),
            critical=False,
        )
        .sign(key, hashes.SHA256())
    )

    with KEY_PATH.open("wb") as key_file:
        key_file.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    with CRT_PATH.open("wb") as crt_file:
        crt_file.write(cert.public_bytes(serialization.Encoding.PEM))

    print(f"Generated {KEY_PATH} and {CRT_PATH}")


if __name__ == "__main__":
    generate()
