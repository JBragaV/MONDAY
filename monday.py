# coding: utf8
import time
from datetime import datetime
import re
import os
import magic
import whisper

import telebot
from telebot import types, custom_filters


from SECRETS import TOKEN_API
import agendamento_funcoes as manipulador
from registro_pagamentos import atualiza_pagamentos, dizer_contas_a_pagar


def gerador_hora():
    dia_hora = datetime.now()
    dia_hora = dia_hora.strftime("%H:%M")
    return dia_hora


dia_hora = gerador_hora()

bot = telebot.TeleBot(TOKEN_API)


print(f"Monday começou!\n{dia_hora}")


LISTA_PAGAMENTOS_MENSAIS = ["faculdade", "mei", "net", "claro",
                            "vivo", "conta_luz", "aluguel",
                            "caixinha", "cartao_nu_bank", "unimed"]

bot.add_custom_filter(custom_filters.TextMatchFilter())


# Função finalizada
def enviar_escala(chat_id):
    bot.send_chat_action(chat_id, "upload_document")
    time.sleep(5)
    doc = open('servicos_jo_nov.xlsx', 'rb')
    bot.send_document(chat_id, doc)
    bot.send_document(chat_id, "FILEID")


@bot.message_handler(regexp="http[s]?://")
def links_guardar(mensagem):
    texto = mensagem.text
    id = mensagem.from_user.id
    padrao_link = r"http[s]?:\D\D[a-zA-z0-9._/-]*"
    link_texto = re.search(padrao_link, texto)
    inicio = link_texto.start()
    texto = texto[inicio:]
    try:
        with open("links.txt", "a") as f:
            f.write(f"{id}: {texto}\n")
        bot.send_chat_action(id, "typing", 5)
        bot.send_message(id, "Link gravado com sucesso!!!!")
    except Exception:
        bot.send_message(id, "Erro ao gravar atividade!!!")
        bot.send_chat_action(id, "typing", 5)


# Função finalizada, para sair do sistema.
def vencimento_contas(id_):
    try:
        CONTAS = {
            "Aluguel": "dia 06",
            "Cartão nú": "primeiro útil após dia 09",
            "Luz": "dia 08",
            "Net": "dia 08",
            "Vivo": "dia 08",
            "Faculdade": "dia 18",
            "Caixinha": "não tem vencimento",
            "Mei": "dia 22",
            "Unimed": "Dia 05",
        }
        for chave, valor in CONTAS.items():
            bot.send_message(id_, f"{chave} vence {valor}")
        bot.send_message(id_, "Essa é a listagem das contas!!!")
    except Exception:
        bot.send_chat_action(id_, "typing", 5)
        bot.send_message(id_, "Erro!!! Me enrolei aqui")
        bot.send_chat_action(id_, "typing", 5)
        bot.send_message(id_, "Me conserta, meu mestre")


# @bot.message_handler(content_types=['photo'])
# def funcao_teste_foto_notafiscal(mensagem):
#     print("Cheguei até aqui e agora o que vou fazer?!?!")


@bot.message_handler(content_types=['photo'])
def recibos_imagem(mensagem, tipo=""):
    print(mensagem)
    id_user = mensagem.from_user.id
    nome_temporario = "temp_img.jpg"
    if not tipo:
        id_photo = mensagem.photo[-1].file_id
    else:
        id_photo = mensagem.json['document']['file_id']
    photo_info = bot.get_file(id_photo)
    download_foto = bot.download_file(photo_info.file_path)
    with open(nome_temporario, 'wb') as nova_foto:
        nova_foto.write(download_foto)
    mes, nome_foto = manipulador.tratar_imagem()
    caminho_imagem = manipulador.cria_pastas(mes, nome_foto, 'jpg')
    with open(caminho_imagem, 'wb') as recibo:
        recibo.write(download_foto)
    os.remove(nome_temporario)
    bot.send_message(id_user, "Recibo recebido e salvo!!!!")
    if nome_foto in LISTA_PAGAMENTOS_MENSAIS:
        try:
            atualiza_pagamentos(nome_foto)
            bot.send_message(id_user, "Tabela de pagamentos atualizado com sucesso!!!")
        except Exception as e:
            print(e)
            bot.send_message(id_user, "Ops!!! Alguma coisa deu errado!!!")


#@bot.message_handler(content_types=['document'])
def recibos_pdf(mensagem, tipo=""):
    print(mensagem)
    id_user = mensagem.from_user.id
    arquivo = bot.get_file(mensagem.document.file_id)
    nome_arquivo = arquivo.file_path.split("/")
    if "pdf" in nome_arquivo[-1]:
        arquivo_dowloaded = bot.download_file(arquivo.file_path)
        with open("recibo.pdf", "wb") as recibo:
            recibo.write(arquivo_dowloaded)
        mes, nome_arquivo = manipulador.extrair_texto_pdf("recibo.pdf")
        caminho_recibo = manipulador.cria_pastas(mes, nome_arquivo, 'pdf')
        with open(caminho_recibo, 'wb') as recibo:
            recibo.write(arquivo_dowloaded)
        os.remove("recibo.pdf")
        bot.send_message(id_user, "Documento recebido e salvo!!!!")
        try:
            if nome_arquivo in LISTA_PAGAMENTOS_MENSAIS:
                atualiza_pagamentos(nome_arquivo)
                bot.send_message(id_user, "Tabela de pagamentos atualizado com sucesso!!!")
        except Exception as e:
            print(e)
            bot.send_message(id_user, "Ops!!! Alguma coisa deu errado!!!")
    elif "png" in nome_arquivo[-1]:
        print(mensagem.json['document']['file_id'])
        recibos_imagem(mensagem, 'png')
    elif "xlsx" in nome_arquivo[-1]:
        print("AINDA FALTA SER FEITA A IMPLEMENTAÇÃO")
        pass
    else:
        bot.send_message(id_user, "Formato do arquivo não suportado!!!")


def servico(mensagem):
    id_user = mensagem.from_user.id
    servicos = manipulador.exibircao_servico_dia()
    hora_atual = gerador_hora()
    hora = hora_atual.split(":")[0]
    if len(servicos) > 1:
        inicio = servicos[0]
        final = servicos[1]
        if hora < inicio:
            bot.send_message(id_user, "Jocimar está trabalhando hoje")
            bot.send_message(id_user, f"Entra as {inicio} e sai as {final}")
        elif hora < final:
            bot.send_message(id_user, "Jocimar está no trabalho agora!!")
            bot.send_message(id_user, f"Vai sair as {final}")
        else:
            bot.send_message(id_user, "Jocimar trabalhou hoje")
            bot.send_message(id_user, f"Mas já saiu.")
    else:
        bot.send_message(id_user, f"Jocimar está de {servicos[0]}")


@bot.message_handler(content_types=['contact'])
def responder1(mensagem):
    print(mensagem)


@bot.message_handler(content_types=['document'])
def responder1(mensagem):
    ### Enviando e recebendo os arquivos para reentender como funciona o recebimento, download e salvamento dos arquivos
    if mensagem.document.mime_type != "image/jpeg":
        print(mensagem)
        # Observar MimiType em documents
        if mensagem.caption:
            print(mensagem.caption)
            file_id = mensagem.document.file_id
            nome_arquivo = mensagem.document.file_name.split(".")[0]
            print(file_id)
            arquivo = bot.get_file(mensagem.document.file_id)
            print(arquivo)
            print(arquivo.file_path)
            arquivo_dowloaded = bot.download_file(arquivo.file_path)
            extensao_arquivo = arquivo.file_path.split('/')[-1].split(".")[-1]
            print(extensao_arquivo)
            with open(f"{nome_arquivo}_{mensagem.caption}.{extensao_arquivo}", "wb") as recibo:
                recibo.write(arquivo_dowloaded)
            # print(magic.from_file(f"recibo.{extensao_arquivo}"))
    else:
        funcao_teste_foto_notafiscal(mensagem, "essa função veio daqui")


@bot.message_handler(content_types=['photo'])
def funcao_teste_foto_notafiscal(mensagem, teste=""):
    print(mensagem)
    print(teste)
    if mensagem.caption:
        print(mensagem.caption)
        print(mensagem.photo[-1])


@bot.message_handler(content_types=['audio'])
def responder2(mensagem):
    print(mensagem)


@bot.message_handler(content_types=['location'])
def responder3(mensagem):
    print(mensagem)


@bot.message_handler(content_types=['voice'])
def responder4(mensagem):
    # https://www.hashtagtreinamentos.com/como-transcrever-audio-com-python
    print(mensagem)
    audio = bot.get_file(mensagem.voice.file_id)
    audio_baixado = bot.download_file(audio.file_path)
    print(audio)
    with open(f"minha_voz.m4a", "wb") as recibo:
        recibo.write(audio_baixado)
    with open(f"minha_voz.mp3", "wb") as recibo:
        recibo.write(audio_baixado)
    modelo = whisper.load_model("base")
    bot.send_audio(1189527779, mensagem.voice.file_id)
    resposta = modelo.transcribe('minha_voz.mp3')
    bot.send_message(1189527779, resposta["text"])


@bot.message_handler(func=lambda m: True)
def responder(mensagem):
    print(mensagem)
    id_user = mensagem.from_user.id
    texto = mensagem.text
    if texto.lower() == "serviço":
        servico(mensagem)
    elif texto.lower() == "enviar escala":
        enviar_escala(id_user)
    elif texto.lower() == "listar links":
        listar_links(id_user)
    elif texto.lower() == "vencimento contas":
        vencimento_contas(id_user)
    elif texto.lower() == "opção":
        teste_funcao_repeteco(id_user)
    elif texto.lower() == "contas em aberto":
        contas_em_aberto(id_user)
    else:
        menu = f"""O que você quer saber de mim, {mensagem.from_user.first_name}"""
        bot.send_message(mensagem.chat.id, menu)


def contas_em_aberto(id):
    lista_contas_em_aberto = dizer_contas_a_pagar()
    if len(lista_contas_em_aberto) > 0:
        bot.send_message(id, "Essas são as contas em aberto desse mês")
        for conta in lista_contas_em_aberto:
            bot.send_message(id, conta)
    else:
        bot.send_message(id, "Todas as contas do mês já foram pagas!!!")


def listar_links(id):
    try:
        with open("links.txt", "r") as f:
            lista_conteusdos = []
            for linha in f:
                conteudo_arquivo = linha.split(": ")
                if int(conteudo_arquivo[0]) == id:
                    lista_conteusdos.append(conteudo_arquivo[1][0:-1])
        if len(lista_conteusdos) > 0:
            if id == 1189527779:
                bot.send_message(id, "Meu mestre e senhor supremo!!!")
                bot.send_chat_action(id, "typing", 3)
                time.sleep(3)
                bot.send_message(id, "Aqui estão os links que o senhor me enviou!!!")
                bot.send_chat_action(id, "typing", 3)
                time.sleep(3)
            else:
                bot.send_message(id, "Aqui estão os links que me enviou!!!")
            for conteudo in lista_conteusdos:
                bot.send_message(id, conteudo)
        else:
            bot.send_message(id, "Não tem nenhum link guardado!!!")
    except Exception:
        bot.send_message(id, "Ops!!! Deu algum erro na hora de abrir o arquivos com os links")


def teste_funcao_repeteco(chat_id):
    markup = types.ReplyKeyboardMarkup()
    itembtna = types.KeyboardButton('Enviar Escala')
    itembtnv = types.KeyboardButton('Contas em aberto')
    itembtnb = types.KeyboardButton('vencimento contas')
    itembtnc = types.KeyboardButton('Serviço')
    itembtnd = types.KeyboardButton('Listar Links')
    itembtne = types.KeyboardButton('Ajuda')
    markup.row(itembtna, itembtnv, itembtnb)
    markup.row(itembtnc, itembtnd, itembtne)
    bot.send_message(chat_id, "Escolha uma das opções:", reply_markup=markup)


# Função finalizada, para sair do sistema.
def inicio_de_tudo():
    print("Vamnos começar a festa")
    bot.send_message(1189527779, "Teste de mensagem")


bot.send_message(1189527779, "As suas ordens, Meu Senhor Supremo")

if __name__ == "__main__":
    # bot.send_message(1189527779, "Teste de mensagem")
    inicio_de_tudo()
    bot.infinity_polling()
