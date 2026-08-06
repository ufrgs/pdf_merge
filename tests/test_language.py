""" testes do módulo de idiomas """

from pdf_merge.language import IdiomaAplicativo


def test_todos_os_idiomas_tem_as_mesmas_chaves():
    """ uma chave faltando em um idioma vira texto vazio na interface """
    referencia: set = set(IdiomaAplicativo.textos["pt"])
    for idioma, textos in IdiomaAplicativo.textos.items():
        assert set(textos) == referencia, \
            f"chaves divergentes no idioma {idioma}"


def test_nenhum_texto_vazio():
    for idioma, textos in IdiomaAplicativo.textos.items():
        for chave, texto in textos.items():
            assert texto.strip(), f"texto vazio em {idioma}/{chave}"


def test_pega_texto_no_idioma_definido():
    tradutor: IdiomaAplicativo = IdiomaAplicativo()
    assert tradutor.pega_texto("merge") == "Juntar"

    tradutor.define_texto("en")
    assert tradutor.pega_texto("merge") == "Merge"


def test_chave_inexistente_retorna_texto_vazio():
    assert IdiomaAplicativo().pega_texto("chave-que-nao-existe") == ""
