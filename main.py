from monday import bot
from random import randint


def numeros_mega_sena():
    conjunto = set()
    while len(conjunto) <= 5:
        numero = randint(1, 60)
        conjunto.add(numero)
    print(conjunto)


if __name__ == "__main__":
    numeros_mega_sena()
    bot.infinity_polling()
