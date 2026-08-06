""" testes do fluxo principal usando a interface real. as caixas de diálogo
são substituídas por versões que apenas registram as chamadas. """

import pytest
from pypdf import PdfReader

from pdf_merge import classes
from pdf_merge.classes import FramePdf
from tests.conftest import PASTA_PDFS


def carrega(app, *arqs_path) -> None:
    """ adiciona PDFs à lista como se tivessem sido carregados pelo botão """
    for arq_path in arqs_path:
        frame_pdf: FramePdf = FramePdf(app.frm_lista, app, str(arq_path))
        app.pdfs.append(frame_pdf)
        frame_pdf.pack()
    app.update()


def nomes_carregados(app) -> list[str]:
    return [frame_pdf.entry.get() for frame_pdf in app.pdfs]


@pytest.fixture
def dialogos(monkeypatch) -> dict[str, list[str]]:
    """ captura as mensagens exibidas em vez de abrir as caixas de diálogo """
    capturadas: dict[str, list[str]] = {"avisos": [], "infos": []}
    monkeypatch.setattr(
        classes, "showwarning",
        lambda titulo, corpo: capturadas["avisos"].append(corpo))
    monkeypatch.setattr(
        classes, "showinfo",
        lambda titulo, corpo: capturadas["infos"].append(corpo))
    return capturadas


def test_merge_com_menos_de_dois_pdfs(app, dialogos):
    carrega(app, PASTA_PDFS / "arq1.pdf")
    app.merge_pdfs()
    assert dialogos["avisos"] == [app.pega_texto("two-or-more")]


def test_merge_com_sucesso(app, dialogos, monkeypatch, tmp_path):
    origens: list = [PASTA_PDFS / f"arq{i}.pdf" for i in (1, 2, 3)]
    carrega(app, *origens)

    saida = tmp_path / "resultado.pdf"
    monkeypatch.setattr(
        classes, "asksaveasfilename", lambda **opcoes: str(saida))
    app.merge_pdfs()

    assert dialogos["avisos"] == []
    assert dialogos["infos"] == [
        app.pega_texto("success-msg") + "resultado.pdf"]

    paginas_esperadas: int = sum(
        len(PdfReader(origem).pages) for origem in origens)
    assert len(PdfReader(saida).pages) == paginas_esperadas


def test_merge_cancelado_na_janela_de_salvar(
        app, dialogos, monkeypatch, tmp_path):
    carrega(app, PASTA_PDFS / "arq1.pdf", PASTA_PDFS / "arq2.pdf")

    # asksaveasfilename retorna string vazia com Cancel ou no X
    monkeypatch.setattr(classes, "asksaveasfilename", lambda **opcoes: "")
    app.merge_pdfs()

    assert dialogos["avisos"] == [app.pega_texto("no-name")]
    assert list(tmp_path.iterdir()) == []


def test_merge_com_pdf_removido_apos_carregar(
        app, dialogos, monkeypatch, tmp_path):
    sumido = tmp_path / "sumido.pdf"
    sumido.write_bytes((PASTA_PDFS / "arq2.pdf").read_bytes())
    carrega(app, PASTA_PDFS / "arq1.pdf", sumido)

    sumido.unlink()
    monkeypatch.setattr(
        classes, "asksaveasfilename",
        lambda **opcoes: pytest.fail("não deveria chegar na janela de salvar"))
    app.merge_pdfs()

    assert dialogos["avisos"] == [
        app.pega_texto("read-error") + "sumido.pdf"]


def test_merge_com_destino_sem_escrita(app, dialogos, monkeypatch, tmp_path):
    carrega(app, PASTA_PDFS / "arq1.pdf", PASTA_PDFS / "arq2.pdf")

    # o diretório pai não existe, então a escrita falha
    saida = tmp_path / "nao-existe" / "resultado.pdf"
    monkeypatch.setattr(
        classes, "asksaveasfilename", lambda **opcoes: str(saida))
    app.merge_pdfs()

    assert dialogos["avisos"] == [
        app.pega_texto("write-error") + "resultado.pdf"]


def test_mover_e_remover_pdfs(app):
    carrega(app, *[PASTA_PDFS / f"arq{i}.pdf" for i in (1, 2, 3)])

    app.pdfs[2].move_cima()
    assert nomes_carregados(app) == ["arq1.pdf", "arq3.pdf", "arq2.pdf"]

    app.pdfs[0].move_baixo()
    assert nomes_carregados(app) == ["arq3.pdf", "arq1.pdf", "arq2.pdf"]

    # mover além das bordas não altera nada
    app.pdfs[0].move_cima()
    app.pdfs[-1].move_baixo()
    assert nomes_carregados(app) == ["arq3.pdf", "arq1.pdf", "arq2.pdf"]

    app.pdfs[1].remove()
    assert nomes_carregados(app) == ["arq3.pdf", "arq2.pdf"]


def test_limpar_pdfs_zera_lista_e_rolagem(app):
    carrega(app, *[PASTA_PDFS / f"arq{(i % 4) + 1}.pdf" for i in range(10)])
    assert len(app.pdfs) == 10

    app.limpar_pdfs()
    app.update()

    assert app.pdfs == []
    assert app.canvas_lista.cget("scrollregion") == "0 0 0 0"
