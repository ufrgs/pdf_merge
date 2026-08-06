""" testes das preferências persistidas entre execuções """

from pathlib import Path

from pdf_merge import config
from tests.conftest import cria_app


def test_carrega_config_sem_arquivo(config_isolada):
    assert config.carrega_config() == {}


def test_salva_e_carrega_config(config_isolada):
    config.salva_config({"tema": "escuro", "idioma": "en"})
    assert config.carrega_config() == {"tema": "escuro", "idioma": "en"}


def test_config_corrompida_volta_ao_padrao(config_isolada):
    caminho: Path = Path(config.caminho_config())
    caminho.parent.mkdir(parents=True)
    caminho.write_text("isso não é um json", encoding="utf-8")
    assert config.carrega_config() == {}


def test_tema_e_idioma_persistem_entre_execucoes(config_isolada):
    app = cria_app()
    app.abre_janela_opcoes()
    app.aplicar_tema("escuro")
    app.define_texto("en")
    app.destroy()

    # segunda "execução" deve restaurar as escolhas anteriores
    outro = cria_app()
    assert outro.idioma == "en"
    assert outro.title() == "PDFs Merger"
    assert outro.canvas_lista.cget("background") == "#1c1c1c"
    outro.destroy()


def test_config_invalida_usa_os_padroes(config_isolada):
    config.salva_config({"tema": "azul", "idioma": "fr"})

    app = cria_app()
    assert app.idioma == "pt"
    assert app.canvas_lista.cget("background") == "#fafafa"
    app.destroy()
