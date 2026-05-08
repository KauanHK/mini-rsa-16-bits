"""Quebra de chave do Mini RSA 16 bits por fatoração trivial.

Ataque possível porque n < 65 536: basta testar divisores até √n ≈ 256.
Etapas:
    1. Fatorar n em p e q por divisão tentativa.
    2. Recalcular φ(n) = (p-1)(q-1).
    3. Inverter e módulo φ(n) para obter d.
"""

from src.math_utils import mod_inverse


def factor_n(n: int) -> tuple[int, int]:
    """Fatora n = p*q por divisão tentativa até √n.

    Args:
        n: Módulo público.

    Returns:
        Par (p, q) com p ≤ q.

    Raises:
        ValueError: Se n não for produto de dois primos distintos.
    """
    if n < 4:
        raise ValueError(f"n={n} é muito pequeno para ser produto de dois primos.")

    i = 2
    while i * i <= n:
        if n % i == 0:
            p, q = i, n // i
            if p != q:
                return (p, q)
            raise ValueError(f"n={n} é quadrado perfeito ({i}²); RSA exige p ≠ q.")
        i += 1

    raise ValueError(f"n={n} é primo; não é um módulo RSA válido.")


def crack_private_key(e: int, n: int) -> tuple[int, int, int, int, int]:
    """Recupera a chave privada a partir apenas da chave pública (e, n).

    Args:
        e: Expoente público.
        n: Módulo público.

    Returns:
        Tupla (p, q, phi, d, n) com os valores recuperados.

    Raises:
        ValueError: Se a fatoração ou o inverso modular falharem.
    """
    p, q = factor_n(n)
    phi = (p - 1) * (q - 1)
    d = mod_inverse(e, phi)
    return p, q, phi, d, n
