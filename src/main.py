"""Interface CLI para demonstração do Mini RSA de 16 bits.

Uso:
    python main.py                        # demonstração com string padrão
    python main.py --text "Olá Mundo"     # cifra texto fornecido
    python main.py --number 42            # cifra número inteiro
    python main.py --no-verbose           # suprime logs matemáticos
"""

import argparse

from src.keygen import generate_keypair
from src.presenter import show_number_result, show_text_result
from src.use_cases.encrypt_number import encrypt_number
from src.use_cases.encrypt_text import encrypt_text


def main() -> None:
    """Ponto de entrada da CLI."""
    parser = argparse.ArgumentParser(description="Demonstração do Mini RSA de 16 bits.")
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

    keys = generate_keypair(verbose=not args.no_verbose)
    e, n = keys["public_key"]   # type: ignore[misc]
    d, _ = keys["private_key"]  # type: ignore[misc]

    if args.text is not None:
        show_text_result(encrypt_text(args.text, e, d, n))  # type: ignore[arg-type]
    elif args.number is not None:
        show_number_result(encrypt_number(args.number, e, d, n))  # type: ignore[arg-type]
    else:
        show_text_result(encrypt_text("RSA", e, d, n))       # type: ignore[arg-type]
        show_number_result(encrypt_number(42, e, d, n))      # type: ignore[arg-type]


if __name__ == "__main__":
    main()
