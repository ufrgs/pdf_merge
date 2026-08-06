""" módulo responsável pela GUI do projeto """

import os
import platform
import sys
import webbrowser

import sv_ttk
from PIL import Image
from PIL.ImageTk import PhotoImage
from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError
from tkinter import Tk, Toplevel, BOTTOM, LEFT, RIGHT, X
from tkinter.filedialog import askopenfilenames, asksaveasfile
from tkinter.messagebox import showinfo, showwarning
from tkinter.ttk import Button, Entry, Frame, Label, Separator

from . import __url__, __version__
from .language import IdiomaAplicativo


class FramePdf:
    def __init__(self, master, app, path: str):
        """
        master -> container onde o frame será inserido
        app -> referência ao Aplicativo (para acessar self.pdfs, update, etc.)
        path -> caminho do PDF
        """
        self.app = app
        self.path = path

        self.frame = Frame(master)

        nome_pdf = os.path.basename(path)
        self.entry = Entry(
            self.frame, font=("Arial", 12, "italic"), justify="center")
        self.entry.insert(0, nome_pdf)
        self.entry["state"] = "disabled"
        self.entry.grid(row=0, column=2, padx=2)

        # botões de controle
        self.btn_remover = Button(self.frame, text="X", command=self.remove)
        self.btn_remover.grid(row=0, column=3, padx=2)

        self.btn_up = Button(self.frame, text="∧", command=self.move_cima)
        self.btn_up.grid(row=0, column=0, padx=2)

        self.btn_down = Button(self.frame, text="∨", command=self.move_baixo)
        self.btn_down.grid(row=0, column=1, padx=2)

    def pack(self):
        self.frame.pack(pady=5)

    def remove(self):
        self.frame.destroy()
        self.app.pdfs.remove(self)

    def move_cima(self):
        idx = self.app.pdfs.index(self)
        if idx > 0:
            self.app.pdfs[idx], self.app.pdfs[idx - 1] = \
                    self.app.pdfs[idx - 1], self.app.pdfs[idx]
            self.app.reordena_frames()

    def move_baixo(self):
        idx = self.app.pdfs.index(self)
        if idx < len(self.app.pdfs) - 1:
            self.app.pdfs[idx], self.app.pdfs[idx + 1] = \
                    self.app.pdfs[idx + 1], self.app.pdfs[idx]
            self.app.reordena_frames()


class Aplicativo(Tk, IdiomaAplicativo):
    """ classe do aplicativo principal """

    url_univ: str = "https://www.ufrgs.br"

    def __init__(self, idioma: str = "pt"):
        Tk.__init__(self)
        IdiomaAplicativo.__init__(self, idioma)

        self.pdfs: list = []
        self.tipo_arq: list = [(self.pega_texto("pdf-files"), "*.pdf")]
        self.sistema: str = platform.system()

        # cria a interface
        self.configura_aplicativo()
        self.cria_frame_menu()
        self.cria_frame_principal()
        sv_ttk.set_theme("light")  # interface clara padrão

        self.atualiza_idioma_main()  # idioma padrão pt-br

    def configura_aplicativo(self) -> None:
        """ método com as configurações da janela """
        self.geometry("480x360")
        # linux não lidam bem com ícones no aplicativo
        if self.sistema == "Windows":
            icone_path: str = self.caminho_arquivo("assets", "ufrgs.ico")
            self.iconbitmap(icone_path)
        self.maxsize(480, 900)
        self.minsize(480, 360)

    def caminho_arquivo(self, pasta: str, nome_arquivo: str) -> str:
        """ busca o caminho do arquivo, compatível com o PyInstaller """
        # verifica se está em modo executável
        if getattr(sys, "frozen", False):
            base_path: str = sys._MEIPASS
        else:
            base_path: str = os.path.abspath(".")
        return os.path.join(base_path, "pdf_merge", pasta, nome_arquivo)

    def cria_frame_menu(self) -> None:
        """ cria os widgets para o menu do aplicativo """
        self.frm_menu: Frame = Frame(self)
        self.frm_menu.pack(fill=X)

        self.btn_opcoes: Button = Button(
            self.frm_menu, command=self.abre_janela_opcoes)
        self.btn_opcoes.pack(side=LEFT, padx=5, pady=(5, 0))

        self.btn_sobre: Button = Button(
            self.frm_menu, command=self.abre_janela_sobre)
        self.btn_sobre.pack(side=LEFT, padx=5, pady=(5, 0))

        self.btn_sair: Button = Button(
            self.frm_menu, command=self.quit)
        self.btn_sair.pack(side=RIGHT, padx=5, pady=(5, 0))

    def cria_frame_principal(self) -> None:
        """ cria os widgets envolvidos no merge dos PDFs """
        self.frm_main: Frame = Frame(self)
        self.frm_main.pack(expand=True, fill="both")

        Separator(
            self.frm_main, orient="horizontal").pack(fill=X, pady=(5, 10))

        self.lbl_titulo: Label = Label(self.frm_main, font=("Arial", 16))
        self.lbl_titulo.pack(pady=(0, 10))

        self.btn_juntar: Button = Button(
            self.frm_main, command=self.merge_pdfs)
        self.btn_juntar.pack(side=BOTTOM, pady=10)

        frm_botoes: Frame = Frame(self.frm_main)
        frm_botoes.pack()

        self.btn_novo_pdf: Button = Button(
            frm_botoes, command=self.cria_frame)
        self.btn_novo_pdf.pack(side=LEFT, padx=10)
        self.btn_limpar: Button = Button(
            frm_botoes, command=self.limpar_pdfs)
        self.btn_limpar.pack(side=LEFT, padx=10)

    def atualiza_interface(self) -> None:
        """ método usado para criar e atualizar os textos da aplicação. essa
        separação dos métodos de atualização é necessária porque não é possível
        atualizar o idioma dos widgets da janela de opções antes de ter sido
        criada. """
        self.atualiza_idioma_main()
        self.atualiza_idioma_janela_menu()

    def atualiza_idioma_janela_menu(self) -> None:
        """ método usado para criar e atualizar os textos da janela aberta pelo
        menu com base no idioma escolhido """
        self.janela_opcoes.title(self.pega_texto("options"))

        # botões e label do tema
        self.lbl_temas["text"] = self.pega_texto("themes")
        self.btn_claro["text"] = self.pega_texto("light")
        self.btn_escuro["text"] = self.pega_texto("dark")
        self.btn_fechar["text"] = self.pega_texto("close")

        # botões e label dos idiomas
        self.lbl_idioma["text"] = self.pega_texto("language")
        self.btn_pt ["text"] = self.pega_texto("lang_pt")
        self.btn_en ["text"] = self.pega_texto("lang_en")
        self.btn_es ["text"] = self.pega_texto("lang_es")
        self.btn_de ["text"] = self.pega_texto("lang_de")
        self.btn_it ["text"] = self.pega_texto("lang_it")

    def atualiza_idioma_main(self) -> None:
        """ método usado para criar e atualizar os textos da janela principal
        com base no idioma escolhido """
        self.title(self.pega_texto("title-window"))

        # botões de menu
        self.btn_opcoes["text"] = self.pega_texto("options")
        self.btn_sobre["text"] = self.pega_texto("about")
        self.btn_sair["text"] = self.pega_texto("exit")

        # botões e label do frame principal
        self.lbl_titulo["text"] = self.pega_texto("title")
        self.btn_juntar["text"] = self.pega_texto("merge")
        self.btn_novo_pdf["text"] = self.pega_texto("load")
        self.btn_limpar["text"] = self.pega_texto("clear")

        # variáveis
        self.tipo_arq: list = [(self.pega_texto("pdf-files"), "*.pdf")]

    def aplicar_tema(self, tema: str) -> None:
        """ aplica o tema escolhido pelo usuário """
        if tema == "claro":
            sv_ttk.use_light_theme()
        else:
            sv_ttk.use_dark_theme()

        if self.sistema == "Windows":
            self.aplica_tema_barra_titulo()

    def aplica_tema_barra_titulo(self) -> None:
        """ devido a uma limitação do Windows, é necessário usar essa função
        para ser possível alterar também a barra de título no Windows
        https://github.com/rdbende/Sun-Valley-ttk-theme#dark-mode-title-bar-on-windows """
        import pywinstyles

        versao = sys.getwindowsversion()

        if versao.major == 10 and versao.build >= 22000:
            # define a cor da barra de título para a cor de fundo no Windows 11
            # para melhor aparência
            pywinstyles.change_header_color(
                self, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
        elif versao.major == 10:
            pywinstyles.apply_style(
                self, "dark" if sv_ttk.get_theme() == "dark" else "normal")

            # gambiara para atualizar a cor da barra de título no Windows 10
            # (não atualiza instantaneamente como no Windows 11)
            self.wm_attributes("-alpha", 0.99)
            self.wm_attributes("-alpha", 1)

    def abre_janela_opcoes(self) -> None:
        """ abre um toplevel com as opções disponíveis """
        self.janela_opcoes:Toplevel = Toplevel(self)
        self.janela_opcoes.minsize(200, 275)
        self.janela_opcoes.transient(self)
        self.janela_opcoes.grab_set()

        self.lbl_temas: Label = Label(self.janela_opcoes)
        self.lbl_temas.pack(pady=(10, 5))
        self.btn_claro: Button = Button(
            self.janela_opcoes, command=lambda: self.aplicar_tema("claro"))
        self.btn_claro.pack(pady=5)
        self.btn_escuro: Button = Button(
            self.janela_opcoes, command=lambda: self.aplicar_tema("escuro"))
        self.btn_escuro.pack(pady=5)

        Separator(
            self.janela_opcoes,
            orient="horizontal").pack(fill=X, padx=10, pady=15)

        self.lbl_idioma: Label = Label(self.janela_opcoes)
        self.lbl_idioma.pack(pady=5)
        self.btn_pt: Button = Button(
            self.janela_opcoes,command=lambda: self.define_texto("pt"))
        self.btn_pt.pack(pady=5)
        self.btn_en: Button = Button(
            self.janela_opcoes, command=lambda: self.define_texto("en"))
        self.btn_en.pack(pady=5)
        self.btn_es: Button = Button(
            self.janela_opcoes, command=lambda: self.define_texto("es"))
        self.btn_es.pack(pady=5)
        self.btn_de: Button = Button(
            self.janela_opcoes, command=lambda: self.define_texto("de"))
        self.btn_de.pack(pady=5)
        self.btn_it: Button = Button(
            self.janela_opcoes, command=lambda: self.define_texto("it"))
        self.btn_it.pack(pady=5)

        Separator(
            self.janela_opcoes,
            orient="horizontal").pack(fill=X, padx=10, pady=15)

        self.btn_fechar: Button = Button(
            self.janela_opcoes, command=self.janela_opcoes.destroy)
        self.btn_fechar.pack(pady=(5, 10))

        self.atualiza_interface()

    def abre_janela_sobre(self) -> None:
        """ cria uma nova janela para mostrar os dados do aplicativo. tornando
        a janela grab_set, evita que se tenha a janela aberta quando for tentar
        alterar o texto e também evita que várias instâncias sejam criadas de
        qualquer janela. """

        janela_sobre: Toplevel = Toplevel(self)
        janela_sobre.title(self.pega_texto("about-title-window"))
        janela_sobre.geometry("400x300")
        janela_sobre.resizable(False, False)
        janela_sobre.transient(self)
        janela_sobre.grab_set()

        try:
            img_caminho: str = self.caminho_arquivo("assets", "cpd-logo.jpg")
            img_logo: Image = Image.open(img_caminho)
            img_largura: int = img_logo.size[0]
            img_altura: int = img_logo.size[1]
            img_logo: Image = img_logo.resize(
                (img_largura//6, img_altura//6), Image.LANCZOS)
            logo: PhotoImage = PhotoImage(img_logo)
            lbl_logo: Label = Label(janela_sobre, image=logo, cursor="hand2")
            lbl_logo.image = logo
            lbl_logo.pack(pady=10)
            # evento de clique para abrir o link da UFRGS
            lbl_logo.bind(
                "<Button-1>", lambda e: webbrowser.open(Aplicativo.url_univ))
        except Exception as e:
            print(f"Não foi possível carregar o logo: {e}")

        texto_info: str = (
            self.pega_texto("contributor") + "\n\n" +
            self.pega_texto("project") +
            f" ({__version__})\n\nUFRGS\n\n{__url__}"
        )
        lbl_info: Label = Label(
            janela_sobre, text=texto_info, justify="center", cursor="hand2")
        lbl_info.pack(pady=10)

        # evento de clique para abrir o link do repositório no navegador
        lbl_info.bind(
            "<Button-1>",
            lambda e: webbrowser.open(__url__))

        btn_fechar: Button = Button(
            janela_sobre,
            text=self.pega_texto("close"),
            command=janela_sobre.destroy)
        btn_fechar.pack(pady=10)

        # necessário para mostrar as imagens
        janela_sobre.wait_window(janela_sobre)

    def limpar_pdfs(self) -> None:
        """ remove todos os PDFs adicionados """
        for pdf in self.pdfs[::-1]:
            pdf.remove()

    def msg_corrompidos(self, invalidos: list[str]):
        """ mostra a janela de aviso para os arquivos inválidos """
        titulo: str = self.pega_texto("warning")
        if len(invalidos) == 1:
            corpo: str = self.pega_texto("corrupted-file")
        else:
            corpo: str = self.pega_texto("corrupted-files")

        for invalido in invalidos:
            corpo += f"\n  - {os.path.basename(invalido)}"

        showwarning(titulo, corpo)

    def reordena_frames(self):
        """ remove todos os frames e depois os readiciona na nova ordem """
        for f in self.pdfs:
            f.frame.pack_forget()
        for f in self.pdfs:
            f.pack()

    def cria_frame(self) -> None:
        """ abre a janela para carregar novo PDF e adcionar um novo frame """
        arqs_path: tuple[str] = askopenfilenames(
                title=self.pega_texto("select"),
                filetypes=self.tipo_arq)

        if not arqs_path:
            return

        arqs_validos: list[str] = []
        arqs_invalidos: list[str] = []
        for arq_path in arqs_path:
            if self.valida_pdf(arq_path):
                arqs_validos.append(arq_path)
            else:
                arqs_invalidos.append(arq_path)

        if arqs_invalidos:
            self.msg_corrompidos(arqs_invalidos)

        for arq_valido in arqs_validos:
            frame_pdf = FramePdf(self.frm_main, self, arq_valido)
            self.pdfs.append(frame_pdf)
            frame_pdf.pack()

    def valida_pdf(self, arq_path: str) -> bool:
        """ testa se é um PDF válido """
        try:
            with open(arq_path, "rb") as arq:
                leitor: PdfReader = PdfReader(arq)
                if len(leitor.pages) == 0:
                    return False
            return True
        except (PdfReadError, ValueError):
            return False

    def merge_pdfs(self) -> None:
        """
         <(-_-<)            (>-_-)>   FUU
           ^(-_-)^        ^(-_-)^     UUU
              (>-_-)>  <(-_-<)        UUU
             <(-_-<)    (>-_-)>       SÃO
               (>-_-)><(-_-<)         HA!
                    (Ò-Ó)
        """
        if len(self.pdfs) < 2:
            showwarning(
                self.pega_texto("warning"), self.pega_texto("two-or-more"))
            return

        pdf_escritor: PdfWriter = PdfWriter()
        for frame_pdf in self.pdfs:
            with open(frame_pdf.path, "rb") as arq:
                pdf_leitor: PdfReader = PdfReader(arq)
                for pagina in pdf_leitor.pages:
                    pdf_escritor.add_page(pagina)

        novo_pdf: str = asksaveasfile(
            filetypes=self.tipo_arq, defaultextension=".pdf")

        # nenhum nome foi escolhido para salvar
        # (janela fechada com Cancel ou no X)
        if not novo_pdf:
            showwarning(self.pega_texto("warning"), self.pega_texto("no-name"))
            return

        with open(novo_pdf.name, "wb") as arq:
            pdf_escritor.write(arq)

        showinfo(
            self.pega_texto("success"),
            self.pega_texto("success-msg") + os.path.basename(novo_pdf.name))

