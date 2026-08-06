""" testes da validação de arquivos PDF """

import os
import sys

import pytest
from pypdf import PdfWriter

from pdf_merge.classes import Aplicativo
from tests.conftest import PASTA_PDFS


def valida(arq_path) -> bool:
    # valida_pdf não depende do estado do aplicativo, então pode ser testado
    # sem criar uma janela
    return Aplicativo.valida_pdf(None, str(arq_path))


@pytest.mark.parametrize(
    "nome", ["arq1.pdf", "arq2.pdf", "arq3.pdf", "arq4.pdf"])
def test_pdf_valido(nome):
    assert valida(PASTA_PDFS / nome) is True


@pytest.mark.parametrize(
    "nome", ["arq-ruim1.pdf", "arq-ruim2.pdf", "arq-ruim3.pdf"])
def test_pdf_corrompido(nome):
    assert valida(PASTA_PDFS / nome) is False


def test_pdf_inexistente(tmp_path):
    assert valida(tmp_path / "nao-existe.pdf") is False


def test_pdf_sem_paginas(tmp_path):
    arq_path = tmp_path / "vazio.pdf"
    with open(arq_path, "wb") as arq:
        PdfWriter().write(arq)
    assert valida(arq_path) is False


@pytest.mark.skipif(
    sys.platform == "win32" or os.geteuid() == 0,
    reason="permissões de leitura não bloqueiam no Windows nem para o root")
def test_pdf_sem_permissao_de_leitura(tmp_path):
    arq_path = tmp_path / "sem-permissao.pdf"
    arq_path.write_bytes((PASTA_PDFS / "arq1.pdf").read_bytes())
    arq_path.chmod(0o000)
    assert valida(arq_path) is False
