"""
Arquivo para testes de novas funcionalidades
"""
import re
import os
import subprocess

texto_base = 'iscpsociedadeeducacionalltda'
pasta = r'C:\Users\jbrag\PycharmProjects\monday_bot'

if __name__ == "__main__":
    subprocess.run(['explorer', pasta])
    print(re.findall("iscp", texto_base, re.IGNORECASE))
    pass
