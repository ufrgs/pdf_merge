""" fixtures compartilhadas pelos testes """

import tkinter
from pathlib import Path

import pytest

from pdf_merge.classes import Aplicativo

PASTA_PDFS: Path = Path(__file__).resolve().parent.parent / "pdfs"


def cria_app() -> Aplicativo:
    """ cria o aplicativo real ou pula o teste em ambientes sem display
    (servidores, por exemplo) """
    try:
        return Aplicativo()
    except tkinter.TclError:
        pytest.skip("sem display disponível para o tkinter")


@pytest.fixture
def config_isolada(monkeypatch, tmp_path) -> Path:
    """ redireciona o arquivo de preferências para uma pasta temporária,
    para os testes não lerem nem alterarem as preferências reais """
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("APPDATA", str(tmp_path))
    return tmp_path


@pytest.fixture
def app(config_isolada):
    """ instância real do aplicativo com as preferências isoladas """
    aplicativo: Aplicativo = cria_app()
    yield aplicativo
    aplicativo.destroy()
