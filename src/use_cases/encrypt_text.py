"""Use case: cifrar e decifrar uma string com RSA."""

from dataclasses import dataclass

from src.rsa_core import decrypt_string, encrypt_string


@dataclass
class EncryptTextResult:
    original: str
    ciphertext: list[int]
    recovered: str
    success: bool
    error: str | None = None


def encrypt_text(text: str, e: int, d: int, n: int) -> EncryptTextResult:
    """Cifra e decifra *text* com a chave pública (e, n) e privada (d, n).

    Returns:
        EncryptTextResult com os dados do fluxo completo.
    """
    try:
        ciphertext = encrypt_string(text, e, n)
    except ValueError as err:
        return EncryptTextResult(
            original=text,
            ciphertext=[],
            recovered="",
            success=False,
            error=str(err),
        )

    recovered = decrypt_string(ciphertext, d, n)
    return EncryptTextResult(
        original=text,
        ciphertext=ciphertext,
        recovered=recovered,
        success=recovered == text,
    )
