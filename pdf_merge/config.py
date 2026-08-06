""" módulo responsável por guardar as preferências do usuário (tema e
idioma) entre as execuções do aplicativo """

import json
import os
import platform


def caminho_config() -> str:
    """ retorna o caminho do arquivo de preferências no local padrão de
    configurações de cada sistema """
    if platform.system() == "Windows":
        base: str = os.environ.get("APPDATA", os.path.expanduser("~"))
    else:
        base: str = os.environ.get(
            "XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    return os.path.join(base, "juntador-pdfs", "config.json")


def carrega_config() -> dict:
    """ lê as preferências salvas; arquivo inexistente ou inválido resulta
    nas preferências padrão """
    try:
        with open(caminho_config(), encoding="utf-8") as arq:
            config: dict = json.load(arq)
    except (OSError, json.JSONDecodeError):
        return {}
    return config if isinstance(config, dict) else {}


def salva_config(config: dict) -> None:
    """ grava as preferências. uma falha aqui não pode impedir o uso do
    aplicativo, então erros de escrita são ignorados """
    caminho: str = caminho_config()
    try:
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as arq:
            json.dump(config, arq, indent=4)
    except OSError:
        pass
