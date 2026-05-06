"""Toda a lógica de apresentação/display do Mini RSA."""

import sys

from src.use_cases.encrypt_number import EncryptNumberResult
from src.use_cases.encrypt_text import EncryptTextResult

_SEP_THIN = "-" * 50
_SEP_THICK = "=" * 50


def show_keygen_steps(p: int, q: int, n: int, phi: int, e: int, d: int) -> None:
    print(_SEP_THICK)
    print("  GERAÇÃO DE CHAVES — Mini RSA 16 bits")
    print(_SEP_THICK)
    print(f"  Passo 1 │ Primos escolhidos")
    print(f"          │   p = {p}")
    print(f"          │   q = {q}")
    print(f"  Passo 2 │ Módulo público")
    print(f"          │   n = p × q = {p} × {q} = {n}")
    print(f"          │   Bits de n: {n.bit_length()}  (deve ser ≤ 16)")
    print(f"  Passo 3 │ Função totiente de Euler")
    print(f"          │   φ(n) = (p-1)(q-1) = {p - 1} × {q - 1} = {phi}")
    print(f"  Passo 4 │ Expoente público")
    print(f"          │   e = {e}  [MDC(e, φ(n)) = 1 ✓]")
    print(f"  Passo 5 │ Expoente privado  (Euclides Estendido)")
    print(f"          │   d = e⁻¹ mod φ(n) = {e}⁻¹ mod {phi} = {d}")
    print(f"          │   Verificação: (e × d) mod φ(n) = {(e * d) % phi} ✓")
    print(f"  Chave pública  → (e={e}, n={n})")
    print(f"  Chave privada  → (d={d}, n={n})")
    print(_SEP_THICK)


def show_text_result(result: EncryptTextResult) -> None:
    print(_SEP_THIN)
    print("  CIFRAÇÃO DE TEXTO")
    print(_SEP_THIN)
    print(f"  Texto original  : {result.original!r}")

    if result.error:
        print(f"  [ERRO] {result.error}", file=sys.stderr)
        print(_SEP_THIN)
        return

    print(f"  Blocos cifrados : {result.ciphertext}")
    print(f"  Texto recuperado: {result.recovered!r}")
    print(f"  Resultado       : {'✓  SUCESSO' if result.success else '✗  FALHA'}")
    print(_SEP_THIN)


def show_number_result(result: EncryptNumberResult) -> None:
    print(_SEP_THIN)
    print("  CIFRAÇÃO DE NÚMERO")
    print(_SEP_THIN)
    print(f"  Número original : {result.original}")

    if result.error:
        print(f"  [ERRO] {result.error}", file=sys.stderr)
        print(_SEP_THIN)
        return

    print(f"  Cifrado         : {result.encrypted}")
    print(f"  Decifrado       : {result.decrypted}")
    print(f"  Resultado       : {'✓  SUCESSO' if result.success else '✗  FALHA'}")
    print(_SEP_THIN)
