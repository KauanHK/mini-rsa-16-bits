"""Use case: quebrar a chave privada RSA a partir da chave pública."""

from dataclasses import dataclass, field

from src.cracker import crack_private_key
from src.rsa_core import decrypt_string


@dataclass
class CrackResult:
    e: int
    n: int
    p: int = 0
    q: int = 0
    phi: int = 0
    d_recovered: int = 0
    ciphertext: list[int] = field(default_factory=list)
    plaintext_recovered: str = ""
    success: bool = False
    error: str | None = None


def crack_key(
    e: int,
    n: int,
    ciphertext: list[int] | None = None,
) -> CrackResult:
    """Tenta recuperar a chave privada e, opcionalmente, decifrar o texto.

    Args:
        e: Expoente público conhecido.
        n: Módulo público conhecido.
        ciphertext: Blocos cifrados a decifrar (opcional).

    Returns:
        CrackResult com os valores recuperados.
    """
    try:
        p, q, phi, d, _ = crack_private_key(e, n)
    except ValueError as err:
        return CrackResult(e=e, n=n, error=str(err))

    plaintext = ""
    if ciphertext:
        plaintext = decrypt_string(ciphertext, d, n)

    return CrackResult(
        e=e,
        n=n,
        p=p,
        q=q,
        phi=phi,
        d_recovered=d,
        ciphertext=ciphertext or [],
        plaintext_recovered=plaintext,
        success=True,
    )
