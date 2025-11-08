from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta


KEY_PATH = "certs/server.key"
CRT_PATH = "certs/server.crt"


def generate():
    from pathlib import Path
    Path("certs").mkdir(exist_ok=True)


    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)


    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"CL"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Santiago"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Santiago"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"MiURLShortener"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
    ])


    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow() - timedelta(days=1))
        .not_valid_after(datetime.utcnow() + timedelta(days=3650))
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
            critical=False,
        )
        .sign(key, hashes.SHA256())
    )


    with open(KEY_PATH, "wb") as f:
        f.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )


    with open(CRT_PATH, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))


    print(f"Generated {KEY_PATH} and {CRT_PATH}")


if __name__ == "__main__":
    generate()