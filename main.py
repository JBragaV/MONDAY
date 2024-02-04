from random import randint
from datetime import timedelta
#from monday import bot, gerador_hora_certa
from arquivos import criador_de_pastas


def numeros_mega_sena():
    conjunto = set()
    while len(conjunto) <= 5:
        numero = randint(1, 60)
        conjunto.add(numero)
    print(conjunto)


if __name__ == "__main__":
    path = criador_de_pastas("Manusinha")
    print(path)
    #numeros_mega_sena()
    #meu_looping()
    #bot.infinity_polling()
