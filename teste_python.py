import whisper
import os

#modelo = whisper.load_model("base")
#resposta = modelo.transcribe(".\minha_voz.mp3")
#print(os.listdir())
#print(resposta['text'])


def funcao(funcao):
    def funcao_interna(*args, **kwargs):
        print("vai")
        funcao(*args, **kwargs)
    return funcao_interna


def funcao1(fun):
    def funcao_interna1(*args, **kwargs):
        print("vai1")
        fun(*args, **kwargs)
    return funcao_interna1

@funcao
@funcao1
def funcao2(nome, sobrenome):
    print(f"vai2 {nome} {sobrenome}")


funcao2("J", "M")
lista1 = [1, 2, 3]
lista2 = [4, 5, 6]
lista3 = [7, 8, 9, 0]

zip1 = zip(lista1, lista2, lista3)
print(tuple(zip1))
zip2 = zip(lista3, lista2, lista1)
print(tuple(zip2))


