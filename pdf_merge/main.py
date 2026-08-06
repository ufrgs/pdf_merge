""" módulo principal """

from pdf_merge.classes import Aplicativo


def main() -> None:
    """ ponto de entrada do aplicativo """
    app: Aplicativo = Aplicativo()
    app.mainloop()


if __name__ == "__main__":
    main()
