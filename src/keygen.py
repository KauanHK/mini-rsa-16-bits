"""Geração de chaves para o Mini RSA de 16 bits."""

import random

from src.math_utils import gcd, is_prime, mod_inverse

# Valor padrão de e; se muito grande para φ(n) usamos candidatos menores.
_E_CANDIDATES: tuple[int, ...] = (65537, 257, 17, 13, 11, 7, 5, 3)


def _generate_prime_in_range(low: int, high: int) -> int:
    """Gera um primo aleatório no intervalo fechado [low, high].

    Args:
        low: Limite inferior (inclusive).
        high: Limite superior (inclusive).

    Returns:
        Um número primo no intervalo.

    Raises:
        ValueError: Se nenhum primo existir no intervalo.
    """
    if low > high:
        raise ValueError(f"Intervalo inválido: [{low}, {high}]")
    candidates = list(range(low if low % 2 != 0 else low + 1, high + 1, 2))
    random.shuffle(candidates)
    for c in candidates:
        if is_prime(c):
            return c
    raise ValueError(f"Nenhum primo encontrado em [{low}, {high}]")


def _choose_e(phi: int) -> int:
    """Escolhe o expoente público e compatível com φ(n).

    Args:
        phi: Valor de φ(n) = (p-1)(q-1).

    Returns:
        e tal que 1 < e < phi e MDC(e, phi) = 1.

    Raises:
        ValueError: Se nenhum candidato for compatível.
    """
    for e in _E_CANDIDATES:
        if 1 < e < phi and gcd(e, phi) == 1:
            return e
    raise ValueError(f"Não foi possível encontrar e compatível com φ(n) = {phi}")


def generate_keypair(verbose: bool = True) -> dict[str, int | tuple[int, int]]:
    """Gera um par de chaves RSA com n = p*q < 65 536 (16 bits).

    O algoritmo:
        1. Sorteia p primo em [100, 255].
        2. Sorteia q primo em [100, ⌊65535/p⌋], com q ≠ p.
        3. Calcula n = p*q e φ(n) = (p-1)(q-1).
        4. Escolhe e tal que MDC(e, φ(n)) = 1.
        5. Calcula d = e⁻¹ mod φ(n) via Euclides Estendido.

    Args:
        verbose: Se True, imprime o passo a passo matemático.

    Returns:
        Dicionário com as chaves:
            p, q       — primos secretos
            n          — módulo público
            phi        — φ(n) (mantido em segredo)
            e          — expoente público
            d          — expoente privado
            public_key — (e, n)
            private_key — (d, n)
    """
    for attempt in range(1000):
        p = _generate_prime_in_range(100, 255)
        q_max = 65535 // p
        if q_max < 100:
            continue
        try:
            q = _generate_prime_in_range(100, q_max)
        except ValueError:
            continue
        if p == q:
            continue

        n = p * q
        if n >= 65536:
            continue

        phi = (p - 1) * (q - 1)

        try:
            e = _choose_e(phi)
        except ValueError:
            continue

        try:
            d = mod_inverse(e, phi)
        except ValueError:
            continue

        # Sanidade: e * d ≡ 1 (mod phi)
        if (e * d) % phi != 1:
            continue

        if verbose:
            from src.presenter import show_keygen_steps

            show_keygen_steps(p, q, n, phi, e, d)

        return {
            "p": p,
            "q": q,
            "n": n,
            "phi": phi,
            "e": e,
            "d": d,
            "public_key": (e, n),
            "private_key": (d, n),
        }

    raise RuntimeError("Falha na geração de chaves após 1000 tentativas.")
