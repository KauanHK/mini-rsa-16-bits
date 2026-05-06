"""Operações de cifração e decifração do Mini RSA."""


def fast_mod_exp(base: int, exp: int, mod: int) -> int:
    """Exponenciação modular rápida pelo método de quadração repetida.

    Calcula base^exp mod mod em O(log exp) multiplicações.

    Args:
        base: Base da exponenciação.
        exp: Expoente (inteiro não-negativo).
        mod: Módulo (inteiro positivo).

    Returns:
        (base ** exp) % mod.

    Examples:
        >>> fast_mod_exp(2, 10, 1000)
        24
    """
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:  # bit menos significativo é 1
            result = result * base % mod
        base = base * base % mod
        exp >>= 1
    return result


def encrypt(message: int, e: int, n: int) -> int:
    """Cifra um bloco inteiro com a chave pública (e, n).

    Calcula c = m^e mod n.

    Args:
        message: Mensagem em claro como inteiro (deve ser 0 ≤ m < n).
        e: Expoente público.
        n: Módulo público.

    Returns:
        Texto cifrado c.

    Raises:
        ValueError: Se message ≥ n.

    Examples:
        >>> encrypt(65, 17, 3233)  # m='A', chaves de exemplo
        2790
    """
    if message >= n:
        raise ValueError(f"Mensagem ({message}) deve ser menor que n ({n}).")
    return fast_mod_exp(message, e, n)


def decrypt(ciphertext: int, d: int, n: int) -> int:
    """Decifra um bloco com a chave privada (d, n).

    Calcula m = c^d mod n.

    Args:
        ciphertext: Texto cifrado c.
        d: Expoente privado.
        n: Módulo público.

    Returns:
        Mensagem em claro m.

    Examples:
        >>> decrypt(2790, 2753, 3233)
        65
    """
    return fast_mod_exp(ciphertext, d, n)


def encrypt_string(text: str, e: int, n: int) -> list[int]:
    """Cifra uma string caractere por caractere.

    Cada caractere é convertido para seu valor ASCII e cifrado
    individualmente com encrypt().

    Args:
        text: Texto em claro.
        e: Expoente público.
        n: Módulo público.

    Returns:
        Lista de blocos cifrados, um por caractere.

    Raises:
        ValueError: Se algum caractere tiver valor ASCII ≥ n.
    """
    result: list[int] = []
    for ch in text:
        m = ord(ch)
        if m >= n:
            raise ValueError(
                f"Caractere '{ch}' (ASCII {m}) ≥ n ({n}). "
                "Use um módulo maior ou restrinja o alfabeto."
            )
        result.append(encrypt(m, e, n))
    return result


def decrypt_string(ciphertext_blocks: list[int], d: int, n: int) -> str:
    """Decifra uma lista de blocos e reconstrói a string original.

    Args:
        ciphertext_blocks: Lista de blocos cifrados.
        d: Expoente privado.
        n: Módulo público.

    Returns:
        Texto em claro recuperado.
    """
    return "".join(chr(decrypt(c, d, n)) for c in ciphertext_blocks)
