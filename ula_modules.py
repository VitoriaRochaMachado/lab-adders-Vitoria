#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blocos combinacionais de somadores em MyHDL.

Este modulo declara implementacoes de:
- meio somador (half adder),
- somador completo (full adder),
- somador de 2 bits,
- somador generico por encadeamento,
- somador vetorial comportamental.
"""

from myhdl import *


@block
def halfAdder(a, b, soma, carry):
    """Meio somador de 1 bit.

    Args:
        a: Entrada de 1 bit.
        b: Entrada de 1 bit.
        soma: Saida de soma.
        carry: Saida de carry.
    """
    @always_comb
    def comb():
        soma.next = a ^ b   # XOR
        carry.next = a & b  # AND

    return instances()


@block
def fullAdder(a, b, c, soma, carry):
    """Somador completo de 1 bit.

    Args:
        a: Primeira entrada de 1 bit.
        b: Segunda entrada de 1 bit.
        c: Carry de entrada.
        soma: Saida de soma.
        carry: Carry de saida.
    """
    @always_comb
    def comb():
        soma.next = a ^ b ^ c
        carry.next = (a & b) | (b & c) | (a & c)

    return instances()


@block
def adder2bits(x, y, soma, carry):
    """Somador de 2 bits.

    Implementacao esperada com dois full adders, gerando
    uma soma de 2 bits e carry final.

    Args:
        x: Vetor de entrada de 2 bits.
        y: Vetor de entrada de 2 bits.
        soma: Vetor de saida de 2 bits.
        carry: Carry de saida.
    """
    """Somador de 2 bits usando dois full adders."""
    c0 = Signal(bool(0))

    fa0 = fullAdder(x[0], y[0], 0, soma[0], c0)
    fa1 = fullAdder(x[1], y[1], c0, soma[1], carry)

    return instances()


@block
def adder(x, y, soma, carry):
    """Somador generico para vetores de mesmo tamanho.

    Implementacao esperada por ripple-carry (encadeamento de carries)
    usando celulas de full adder.

    Args:
        x: Vetor de entrada.
        y: Vetor de entrada.
        soma: Vetor de saida com mesma largura de x/y.
        carry: Carry de saida mais significativo.
    """
    n = len(x)
    c = [Signal(bool(0)) for _ in range(n+1)]

    fa_list = []
    for i in range(n):
        fa_list.append(fullAdder(x[i], y[i], c[i], soma[i], c[i+1]))

    @always_comb
    def logic():
        carry.next = c[n]

    return instances()

@block
def addervb(x, y, soma, carry):
    """Somador vetorial em estilo comportamental.

    Versao combinacional que pode usar operacoes aritmeticas diretas
    sobre os vetores para gerar soma e carry.

    Args:
        x: Vetor de entrada.
        y: Vetor de entrada.
        soma: Vetor de saida.
        carry: Carry de saida.
    """
    @always_comb
    def comb():
        total = int(x) + int(y)
        soma.next = total & ((1 << len(x)) - 1)  # pega apenas os bits da largura
        carry.next = total >> len(x)             # pega o carry

    return instances()

