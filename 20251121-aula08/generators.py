
def teste():
    yield 1
    yield 2
    yield 3

if __name__ == "__main__":

    for valor in teste():
        print(valor)

    print(next(teste()))
    print(next(teste()))
    print(next(teste()))
    print(next(teste()))