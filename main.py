from random import randint
from datetime import timedelta
from monday import bot, gerador_hora_certa


def numeros_mega_sena():
    conjunto = set()
    while len(conjunto) <= 5:
        numero = randint(1, 60)
        conjunto.add(numero)
    print(conjunto)


def meu_looping():
    hora_inicio = gerador_hora_certa()


if __name__ == "__main__":
    numeros_mega_sena()
    meu_looping()
    bot.infinity_polling()
