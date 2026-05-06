"""Use case: cifrar e decifrar um inteiro com RSA."""

from dataclasses import dataclass

from src.rsa_core import decrypt, encrypt


@dataclass
class EncryptNumberResult:
    original: int
    encrypted: int
    decrypted: int
    success: bool
    error: str | None = None


def encrypt_number(number: int, e: int, d: int, n: int) -> EncryptNumberResult:
    """Cifra e decifra *number* com a chave pública (e, n) e privada (d, n).

    Returns:
        EncryptNumberResult com os dados do fluxo completo.
    """
    if number >= n:
        return EncryptNumberResult(
            original=number,
            encrypted=0,
            decrypted=0,
            success=False,
            error=f"O número {number} deve ser menor que n = {n}.",
        )

    encrypted = encrypt(number, e, n)
    decrypted = decrypt(encrypted, d, n)
    return EncryptNumberResult(
        original=number,
        encrypted=encrypted,
        decrypted=decrypted,
        success=decrypted == number,
    )
