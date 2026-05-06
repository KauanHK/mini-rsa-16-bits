# Mini RSA 16-bits

Este projeto é uma implementação didática e modular do algoritmo de criptografia assimétrica **RSA**, limitada a chaves de **16 bits** ($n < 65.536$). Desenvolvido para fins acadêmicos, o código prioriza a legibilidade e a demonstração passo a passo dos cálculos matemáticos envolvidos.

## 🚀 Como Executar

Este projeto utiliza o [uv](https://docs.astral.sh/uv/), um gerenciador de pacotes e ambientes Python extremamente rápido.

Para executar o fluxo completo (geração de chaves, cifração de texto e números), utilize o comando abaixo na raiz do projeto:

```bash
uv run -m src.main
```

---

## 🛠️ Funcionalidades

- **Geração de Chaves:** Escolha automática de primos $p$ e $q$ para garantir um módulo $n$ de 16 bits.
- **Matemática Transparente:** Exibição detalhada de:
  - Cálculo do Totiente de Euler $\phi(n)$.
  - Verificação do MDC para o expoente público $e$.
  - Cálculo do inverso modular para o expoente privado $d$ via Algoritmo de Euclides Estendido.
- **Criptografia de Texto:** Suporte a strings (convertidas em blocos).
- **Criptografia Numérica:** Suporte direto para valores inteiros.

## 📂 Estrutura do Projeto

A implementação segue um padrão modular para facilitar o estudo de cada etapa do RSA:

```text
src/
├── main.py        # Ponto de entrada e interface CLI
├── rsa_core.py    # Lógica de cifração (c = m^e mod n) e decifração
├── keygen.py      # Lógica de geração de chaves e busca de primos
└── math_utils.py  # Funções base (MDC, Inverso Modular, Miller-Rabin)
```

## 🧠 Conceitos Matemáticos Aplicados

1. **Teste de Primalidade:** Verificação se $p$ e $q$ são primos.
2. **Algoritmo de Euclides Estendido:** Utilizado para encontrar o coeficiente $d$, tal que $e \cdot d \equiv 1 \pmod{\phi(n)}$.
3. **Exponenciação Modular Rápida:** Implementada para garantir eficiência e evitar overflow de memória antes da operação de módulo.

---

## 📋 Exemplo de Saída

Ao rodar o sistema, você verá um log detalhado:

```text
==================================================
  GERAÇÃO DE CHAVES — Mini RSA 16 bits
==================================================
  Passo 1 | Primos: p=233, q=263
  Passo 2 | Módulo: n=61279 (16 bits)
  Passo 3 | φ(n): 60784
  Passo 4 | e: 257 (MDC=1)
  Passo 5 | d: 52033
==================================================
```
