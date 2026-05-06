"""Interface CLI para demonstração do Mini RSA de 16 bits.

Uso:
    python main.py                        # demonstração com string padrão
    python main.py --text "Olá Mundo"     # cifra texto fornecido
    python main.py --number 42            # cifra número inteiro
    python main.py --no-verbose           # suprime logs matemáticos
"""

from __future__ import annotations

import argparse
import sys

from src.keygen import generate_keypair
from src.rsa_core import decrypt, decrypt_string, encrypt, encrypt_string


def _demo_string(text: str, e: int, d: int, n: int) -> None:
    """Executa o fluxo completo de cifração/decifração de uma string."""
    sep = "-" * 50
    print(sep)
    print(f"  CIFRAÇÃO DE TEXTO")
    print(sep)
    print(f"  Texto original  : {text!r}")

    try:
        ciphertext = encrypt_string(text, e, n)
    except ValueError as err:
        print(f"  [ERRO] {err}", file=sys.stderr)
        return

    print(f"  Blocos cifrados : {ciphertext}")
    recovered = decrypt_string(ciphertext, d, n)
    print(f"  Texto recuperado: {recovered!r}")
    ok = "✓  SUCESSO" if recovered == text else "✗  FALHA"
    print(f"  Resultado       : {ok}")
    print(sep)


def _demo_number(number: int, e: int, d: int, n: int) -> None:
    """Executa o fluxo completo de cifração/decifração de um inteiro."""
    sep = "-" * 50
    print(sep)
    print(f"  CIFRAÇÃO DE NÚMERO")
    print(sep)
    print(f"  Número original : {number}")

    if number >= n:
        print(
            f"  [ERRO] O número {number} deve ser menor que n = {n}.",
            file=sys.stderr,
        )
        return

    c = encrypt(number, e, n)
    print(f"  Cifrado         : {c}")
    m = decrypt(c, d, n)
    print(f"  Decifrado       : {m}")
    ok = "✓  SUCESSO" if m == number else "✗  FALHA"
    print(f"  Resultado       : {ok}")
    print(sep)


def main() -> None:
    """Ponto de entrada da CLI."""
    parser = argparse.ArgumentParser(
        description="Demonstração do Mini RSA de 16 bits."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--text", metavar="TEXTO", help="Texto a cifrar.")
    group.add_argument(
        "--number", metavar="N", type=int, help="Número inteiro a cifrar."
    )
    parser.add_argument(
        "--no-verbose",
        action="store_true",
        help="Suprime o log matemático da geração de chaves.",
    )
    args = parser.parse_args()

    verbose = not args.no_verbose
    keys = generate_keypair(verbose=verbose)
    e, n = keys["public_key"]   # type: ignore[misc]
    d, _ = keys["private_key"]  # type: ignore[misc]

    if args.text is not None:
        _demo_string(args.text, e, d, n)  # type: ignore[arg-type]
    elif args.number is not None:
        _demo_number(args.number, e, d, n)  # type: ignore[arg-type]
    else:
        # Demonstração padrão
        _demo_string("RSA", e, d, n)   # type: ignore[arg-type]
        _demo_number(42, e, d, n)      # type: ignore[arg-type]


if __name__ == "__main__":
    main()
