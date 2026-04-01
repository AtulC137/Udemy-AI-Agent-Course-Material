def fun():
    yield 1
    yield 2
    yield 3

c = fun()
print(c)