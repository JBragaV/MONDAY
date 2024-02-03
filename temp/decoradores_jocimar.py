def imprimeNome(fun):
    def whraper():
        print(f"Estou na {fun.__name__}")
        return fun()
    return whraper
