"""
Moduł ECDH (Elliptic Curve Diffie-Hellman) odpowiedzialny za generowanie par kluczy
i obliczanie wspólnych sekretów na krzywych eliptycznych.
"""

from dataclasses import dataclass
from typing import Dict, Optional

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend

from utils.logger import app_logger


@dataclass
class ECDHKeyPair:
    """Struktura przechowująca wygenerowaną parę kluczy."""
    curve_name: str
    private_key_pem: str
    public_key_pem: str


@dataclass
class ECDHSharedSecret:
    """Struktura z wynikami uzgodnienia klucza."""
    curve_name: str
    shared_secret_hex: str
    derived_key_hex: str


class ECDH:
    """
    Wysokopoziomowa obsługa ECDH bazująca na bibliotece cryptography.
    Zapewnia generowanie par kluczy oraz obliczanie wspólnego sekretu
    z dodatkową derivacją klucza poprzez HKDF.
    """

    CURVE_MAP: Dict[str, ec.EllipticCurve] = {
        "SECP256R1": ec.SECP256R1(),
        "SECP384R1": ec.SECP384R1(),
        "SECP521R1": ec.SECP521R1(),
        "SECP256K1": ec.SECP256K1(),
    }

    def __init__(self, curve_name: str = "SECP256R1"):
        normalized = curve_name.upper().replace("-", "")
        if normalized not in self.CURVE_MAP:
            raise ValueError(
                f"Nieobsługiwana krzywa: {curve_name}. Dostępne: {', '.join(self.CURVE_MAP)}"
            )
        self.curve_name = normalized
        self.curve = self.CURVE_MAP[normalized]
        app_logger.info(f"ECDH initialized on {self.curve_name}")

    def generate_key_pair(self) -> ECDHKeyPair:
        """Generuje nową parę kluczy ECDH."""
        app_logger.start_operation(
            f"ECDH Generowanie Kluczy ({self.curve_name})",
            "ECDH",
            "generate",
        )
        try:
            private_key = ec.generate_private_key(self.curve, default_backend())
            app_logger.add_step(
                "STEP",
                "Wygenerowano klucz prywatny",
                {"krzywa": self.curve_name},
                explanation="Klucz prywatny to losowa liczba w zakresie porządku krzywej.",
            )

            public_key = private_key.public_key()
            app_logger.add_step(
                "STEP",
                "Obliczono klucz publiczny",
                explanation="Klucz publiczny to punkt na krzywej: PK = priv * G.",
            )

            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            ).decode("utf-8")

            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            ).decode("utf-8")

            app_logger.add_step(
                "SUCCESS",
                "Para kluczy gotowa",
                {"długość_klucza": self.curve.key_size},
            )
            app_logger.finish_operation(True, "Klucze ECDH wygenerowane")

            return ECDHKeyPair(
                curve_name=self.curve_name,
                private_key_pem=private_pem,
                public_key_pem=public_pem,
            )
        except Exception as exc:
            app_logger.add_step("ERROR", f"Błąd generowania kluczy: {exc}")
            app_logger.finish_operation(False, str(exc))
            raise

    def compute_shared_secret(
        self,
        private_key_pem: str,
        peer_public_key_pem: str,
        hkdf_length: int = 32,
        hkdf_info: Optional[bytes] = None,
        hkdf_salt: Optional[bytes] = None,
    ) -> ECDHSharedSecret:
        """
        Oblicza wspólny sekret i dodatkowo wyprowadza klucz HKDF.

        Args:
            private_key_pem: Klucz prywatny w formacie PEM.
            peer_public_key_pem: Klucz publiczny partnera w formacie PEM.
            hkdf_length: Długość klucza wynikowego w bajtach.
            hkdf_info: Dodatkowy kontekst HKDF.
            hkdf_salt: Opcjonalna sól HKDF.
        """
        app_logger.start_operation(
            f"ECDH Wspólny Sekret ({self.curve_name})",
            "ECDH",
            "exchange",
        )
        try:
            private_key = serialization.load_pem_private_key(
                private_key_pem.encode("utf-8"),
                password=None,
                backend=default_backend(),
            )
            peer_public_key = serialization.load_pem_public_key(
                peer_public_key_pem.encode("utf-8"),
                backend=default_backend(),
            )

            shared_secret = private_key.exchange(ec.ECDH(), peer_public_key)
            shared_hex = shared_secret.hex()
            app_logger.add_step(
                "STEP",
                "Obliczono wspólny sekret",
                {"długość_bajtów": len(shared_secret)},
                explanation="Sekret jest wynikiem mnożenia punktu publicznego przez klucz prywatny.",
            )

            info = hkdf_info or f"ECDH-{self.curve_name}".encode("utf-8")
            hkdf = HKDF(
                algorithm=hashes.SHA256(),
                length=hkdf_length,
                salt=hkdf_salt,
                info=info,
                backend=default_backend(),
            )
            derived_key = hkdf.derive(shared_secret)
            derived_hex = derived_key.hex()
            app_logger.add_step(
                "STEP",
                "HKDF wyprowadził klucz symetryczny",
                {"długość_klucza": hkdf_length},
                explanation="HKDF zapewnia jednolity rozkład bitów i odporność na przeciek sekretu.",
            )

            app_logger.add_step(
                "SUCCESS",
                "Sekret ECDH i klucz HKDF gotowe",
            )
            app_logger.finish_operation(
                True, f"Wspólny sekret wyprowadzony ({hkdf_length} bajtów)"
            )

            return ECDHSharedSecret(
                curve_name=self.curve_name,
                shared_secret_hex=shared_hex,
                derived_key_hex=derived_hex,
            )
        except Exception as exc:
            app_logger.add_step("ERROR", f"Błąd ECDH: {exc}")
            app_logger.finish_operation(False, str(exc))
            raise


def ecdh_generate_key_pair(curve_name: str = "SECP256R1") -> ECDHKeyPair:
    """Funkcja pomocnicza dla interfejsu."""
    return ECDH(curve_name).generate_key_pair()


def ecdh_compute_shared_secret(
    private_key_pem: str,
    peer_public_key_pem: str,
    curve_name: str = "SECP256R1",
    hkdf_length: int = 32,
) -> ECDHSharedSecret:
    """Funkcja pomocnicza dla interfejsu."""
    return ECDH(curve_name).compute_shared_secret(
        private_key_pem=private_key_pem,
        peer_public_key_pem=peer_public_key_pem,
        hkdf_length=hkdf_length,
    )

