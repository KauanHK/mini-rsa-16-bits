"""
╔══════════════════════════════════════════════════════════════╗
║              Mini RSA de 16 bits — Implementação             ║
║                                                              ║
║  n = p * q  onde n < 2^16 = 65.536                          ║
║  Cada byte da mensagem é cifrado individualmente             ║
╚══════════════════════════════════════════════════════════════╝

Conceitos:
  - p, q   → primos escolhidos tal que n = p*q caiba em 16 bits
  - n      → módulo público
  - φ(n)   → (p-1)(q-1) — função totiente de Euler
  - e      → expoente público (coprimo com φ(n))
  - d      → expoente privado (inverso modular de e mod φ(n))

  Cifrar:    c = m^e mod n
  Decifrar:  m = c^d mod n
"""

import math
import random


# ─────────────────────────────────────────────
#  Utilitários matemáticos
# ─────────────────────────────────────────────

def is_prime(n: int) -> bool:
    """Teste de primalidade determinístico simples."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def primes_in_range(low: int, high: int) -> list[int]:
    """Retorna todos os primos no intervalo [low, high]."""
    return [p for p in range(low, high + 1) if is_prime(p)]


def mod_inverse(e: int, phi: int) -> int:
    """
    Calcula o inverso modular de e mod phi usando
    o Algoritmo de Euclides Estendido.
    Retorna d tal que (e * d) % phi == 1.
    """
    def extended_gcd(a, b):
        if b == 0:
            return a, 1, 0
        g, x, y = extended_gcd(b, a % b)
        return g, y, x - (a // b) * y

    g, x, _ = extended_gcd(e % phi, phi)
    if g != 1:
        raise ValueError(f"Inverso modular não existe: mdc({e}, {phi}) = {g}")
    return x % phi


def mod_pow(base: int, exp: int, mod: int) -> int:
    """
    Exponenciação modular rápida: base^exp mod mod
    (equivalente ao pow(base, exp, mod) nativo do Python).
    """
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:          # bit menos significativo é 1
            result = (result * base) % mod
        exp >>= 1                  # desloca 1 bit à direita
        base = (base * base) % mod
    return result


# ─────────────────────────────────────────────
#  Geração de chaves RSA de 16 bits
# ─────────────────────────────────────────────

def generate_keys(verbose: bool = True) -> tuple[tuple, tuple]:
    """
    Gera um par de chaves RSA de 16 bits.

    Estratégia:
      - Escolhe p e q aleatoriamente da lista de primos entre
        50 e 255, garantindo que n = p*q <= 65535 (16 bits)
        e que p != q.
      - Escolhe e coprimo com φ(n).
      - Calcula d = inverso modular de e.

    Retorna:
      chave_publica  = (e, n)
      chave_privada  = (d, n)
    """
    candidate_primes = primes_in_range(50, 255)

    while True:
        p, q = random.sample(candidate_primes, 2)
        n = p * q
        if n <= 65535:            # cabe em 16 bits
            break

    phi_n = (p - 1) * (q - 1)

    # Escolhe e: pequeno, coprimo com φ(n) e 1 < e < φ(n)
    common_e_candidates = [3, 5, 17, 257, 65537]
    e = None
    for candidate in common_e_candidates:
        if candidate < phi_n and math.gcd(candidate, phi_n) == 1:
            e = candidate
            break

    if e is None:                 # fallback: busca aleatória
        while True:
            e = random.randrange(2, phi_n)
            if math.gcd(e, phi_n) == 1:
                break

    d = mod_inverse(e, phi_n)

    if verbose:
        print("╔══════════════════════════════════════════╗")
        print("║         GERAÇÃO DE CHAVES RSA 16-bit     ║")
        print("╠══════════════════════════════════════════╣")
        print(f"║  Primo p          = {p:<22}║")
        print(f"║  Primo q          = {q:<22}║")
        print(f"║  n  = p × q       = {n:<22}║")
        print(f"║  bits de n        = {n.bit_length():<22}║")
        print(f"║  φ(n) = (p-1)(q-1)= {phi_n:<22}║")
        print(f"║  e (pub. exp.)    = {e:<22}║")
        print(f"║  d (priv. exp.)   = {d:<22}║")
        print("╠══════════════════════════════════════════╣")
        print(f"║  Chave Pública    = (e={e}, n={n})")
        print(f"║  Chave Privada    = (d={d}, n={n})")
        print("╚══════════════════════════════════════════╝")

    public_key  = (e, n)
    private_key = (d, n)
    return public_key, private_key


# ─────────────────────────────────────────────
#  Cifrar e Decifrar
# ─────────────────────────────────────────────

def encrypt_message(message: str, public_key: tuple) -> list[int]:
    """
    Cifra uma string byte a byte.

    Cada caractere vira um inteiro m (0–255) e é cifrado como:
        c = m^e mod n

    Retorna lista de inteiros cifrados.
    """
    e, n = public_key
    ciphertext = []
    for char in message:
        m = ord(char)
        if m >= n:
            raise ValueError(
                f"Caractere '{char}' (ASCII {m}) >= n ({n}). "
                "Use primos maiores ou restrinja a mensagem a ASCII básico."
            )
        c = mod_pow(m, e, n)
        ciphertext.append(c)
    return ciphertext


def decrypt_message(ciphertext: list[int], private_key: tuple) -> str:
    """
    Decifra uma lista de inteiros de volta para string.

        m = c^d mod n
    """
    d, n = private_key
    plaintext = ""
    for c in ciphertext:
        m = mod_pow(c, d, n)
        plaintext += chr(m)
    return plaintext


# ─────────────────────────────────────────────
#  Demonstração interativa
# ─────────────────────────────────────────────

def demo():
    print()
    print("═" * 44)
    print("   MINI RSA 16-BIT — DEMO COMPLETA")
    print("═" * 44)

    # 1. Gerar chaves
    print()
    public_key, private_key = generate_keys(verbose=True)
    e, n = public_key
    d, _  = private_key

    # 2. Mensagem original
    print()
    mensagem = "RSA 16bit"
    print(f"  Mensagem original : \"{mensagem}\"")
    print(f"  Bytes (ASCII)     : {[ord(c) for c in mensagem]}")

    # 3. Cifrar
    cifrado = encrypt_message(mensagem, public_key)
    print()
    print("─" * 44)
    print("  CIFRAGEM  (c = m^e mod n)")
    print("─" * 44)
    print(f"  Texto cifrado     : {cifrado}")

    # 4. Decifrar
    decifrado = decrypt_message(cifrado, private_key)
    print()
    print("─" * 44)
    print("  DECIFRAGEM  (m = c^d mod n)")
    print("─" * 44)
    print(f"  Texto decifrado   : \"{decifrado}\"")

    # 5. Verificação
    print()
    ok = "✓  CORRETO" if decifrado == mensagem else "✗  ERRO"
    print(f"  Verificação       : {ok}")
    print("═" * 44)

    # 6. Tabela char a char
    print()
    print("  Detalhes por caractere:")
    print(f"  {'Char':<6} {'ASCII':>6} {'Cifrado':>10} {'Decifrado':>10}")
    print("  " + "─" * 36)
    for char, c in zip(mensagem, cifrado):
        m_orig = ord(char)
        m_dec  = mod_pow(c, d, n)
        print(f"  {repr(char):<6} {m_orig:>6} {c:>10} {m_dec:>10}")

    # 7. Ataque por força-bruta (mostra vulnerabilidade de n pequeno)
    print()
    print("─" * 44)
    print("  AVISO DE SEGURANÇA")
    print("─" * 44)
    print(f"  n = {n} é pequeno demais para uso real.")
    print(f"  Um atacante pode fatorar n facilmente:")
    for p_try in range(2, int(n**0.5) + 1):
        if n % p_try == 0:
            q_try = n // p_try
            print(f"  → Fatoração: {n} = {p_try} × {q_try}")
            phi_try = (p_try - 1) * (q_try - 1)
            d_try   = mod_inverse(e, phi_try)
            print(f"  → d recuperado por atacante: {d_try}")
            print(f"  → Chave privada real:         {d}")
            print(f"  → {'Iguais ✓' if d_try == d else 'Diferentes ✗'}")
            break
    print("═" * 44)
    print()


if __name__ == "__main__":
    demo()
