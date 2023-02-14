import os


def convert_ui_to_py():
    """
    Essa função converte todos os arquivos .ui para .py e os salva na pasta screens do projeto client.

            Parameters:
                    None

            Returns:
                    None
    """
    arqs = os.listdir("./ui")
    arqs = [arq for arq in arqs if arq.endswith(".ui")]
    for i in arqs:
        os.system("pyuic5 ./ui/%s -o ./screens/%s.py" % (i, i[2:-3]))


if __name__ == "__main__":
    convert_ui_to_py()
