#!/usr/bin/python3

from subprocess import run


def install_requirements():
    """Installs the requirements to run the main code

    :return:
    :rtype:
    """
    run("py -m venv venv")
    run(
        r".\venv\Scripts\activate && py -m pip install -r requirements.txt",
        shell=True,
    )


if __name__ == "__main__":
    install_requirements()
