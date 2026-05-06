"""Funções matemáticas auxiliares para o Mini RSA."""


def gcd(a: int, b: int) -> int:
    """Calcula o MDC de dois inteiros pelo Algoritmo de Euclides.

    Args:
        a: Primeiro inteiro.
        b: Segundo inteiro.

    Returns:
        MDC(a, b).

    Examples:
        >>> gcd(48, 18)
        6
    """
    while b:
        a, b = b, a % b
    return a


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Algoritmo de Euclides Estendido.

    Encontra (g, x, y) tal que a*x + b*y = g = MDC(a, b).

    Args:
        a: Primeiro inteiro.
        b: Segundo inteiro.

    Returns:
        Tupla (g, x, y) onde g = MDC(a, b) e a*x + b*y = g.

    Examples:
        >>> extended_gcd(3, 11)
        (1, 4, -1)
    """
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    return g, y1 - (b // a) * x1, x1


def mod_inverse(e: int, phi: int) -> int:
    """Calcula o inverso modular de e módulo phi pelo Algoritmo de Euclides Estendido.

    Encontra d tal que (e * d) ≡ 1 (mod phi).

    Args:
        e: Inteiro cujo inverso se deseja.
        phi: Módulo (valor de φ(n)).

    Returns:
        d tal que (e * d) mod phi == 1.

    Raises:
        ValueError: Se o inverso não existe (MDC(e, phi) ≠ 1).

    Examples:
        >>> mod_inverse(3, 40)
        27
    """
    g, x, _ = extended_gcd(e % phi, phi)
    if g != 1:
        raise ValueError(f"Inverso modular não existe: MDC({e}, {phi}) = {g} ≠ 1")
    return x % phi


def miller_rabin(n: int) -> bool:
    """Teste de primalidade determinístico de Miller-Rabin para n < 3 215 031 751.

    Para inteiros nesse intervalo, as testemunhas {2, 3, 5, 7} são suficientes
    para um resultado determinístico (sem falsos positivos).

    Args:
        n: Inteiro a testar.

    Returns:
        True se n é primo, False caso contrário.

    Examples:
        >>> miller_rabin(97)
        True
        >>> miller_rabin(100)
        False
    """
    if n < 2:
        return False
    if n in (2, 3, 5, 7):
        return True
    if n % 2 == 0:
        return False

    # Escreve n-1 como 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for a in (2, 3, 5, 7):
        if a >= n:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def is_prime(n: int) -> bool:
    """Verifica se n é primo usando Miller-Rabin.

    Args:
        n: Inteiro a testar.

    Returns:
        True se n é primo.

    Examples:
        >>> is_prime(251)
        True
    """
    return miller_rabin(n)
