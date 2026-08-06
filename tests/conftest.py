""" fixtures compartilhadas pelos testes """

import tkinter
from pathlib import Path

import pytest

from pdf_merge.classes import Aplicativo

PASTA_PDFS: Path = Path(__file__).resolve().parent.parent / "pdfs"


@pytest.fixture
def app():
    """ instância real do aplicativo. os testes que a usam são pulados
    automaticamente em ambientes sem display (servidores, por exemplo) """
    try:
        aplicativo: Aplicativo = Aplicativo()
    except tkinter.TclError:
        pytest.skip("sem display disponível para o tkinter")
    yield aplicativo
    aplicativo.destroy()
