CACHE_FACT = [
    1,
    1,
    2,
    6,
    24,
    120,
    720,
    5040,
    40320,
    362880,
    3628800,
    39916800,
    479001600,
    6227020800,
    87178291200,
    1307674368000,
    20922789888000,
    355687428096000,
    6402373705728000,
    121645100408832000,
]


def puissancerecursif(a, b):
    if b == 0:
        return 1
    else:
        return a * puissancerecursif(a, b - 1)


def puissancerapide(a, b):
    if b == 0:
        return 1
    elif b % 2 == 2:
        val = puissancerapide(a, b // 2)
        return val * val
    else:
        return a * puissancerapide(a, b - 1)


def factrecursif(n):
    if n == 0:
        return 1
    else:
        return n * factrecursif(n - 1)


def coeffbin(k, n):
    if k > n:
        return 0
    else:
        return (CACHE_FACT[n]) / ((CACHE_FACT[k] * CACHE_FACT[n - k]))


def tobernstein(b):
    l = len(b)
    pol = [0] * l
    for k in range(l):
        for i in range(l):
            pol[k] = pol[k] + b[i] * (coeffbin(i, k) / coeffbin(i, l - 1))
    return pol


if __name__ == "__main__":
    # s assurer qu'on a pas de pol de deg > 20
    print([factrecursif(i) for i in range(20)])
