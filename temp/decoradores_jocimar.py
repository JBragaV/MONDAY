def imprimeNome(fun):
    def whraper(escala="", *args, **kwargs):
        print(f"Estou na {fun.__name__}")
        return fun(escala, *args, **kwargs)
    return whraper
