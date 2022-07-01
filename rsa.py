import random
import math


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def prime_finder(n):
    test_number = random.randrange(n, n+50)
    for i in range(2, test_number):
        if (test_number % i) == 0:
            return prime_finder(n)
    return test_number


def pub_key1(phi):
    pub_keys = []
    for i in range(2, phi):
        if gcd(i, phi) == 1:
            pub_keys.append(i)
        if len(pub_keys) >= 50:
            break
    e = random.choice(pub_keys)
    del(pub_keys)
    return e


def gcd2(p, q):

    while(q):
        p, q = q, p % q

    return p


def finder2(n):
    test_number = random.randrange(n+1, n+50, 2)
    limit = math.floor((math.sqrt(test_number)))
    for i in range(3, limit+1, 2):
        if (test_number % i) == 0:
            return finder2(n)
    return test_number


def pub_key(phi):
    pub_keys = []
    for i in range(2, phi):
        if gcd2(i, phi) == 1:
            pub_keys.append(i)
        if len(pub_keys) >= 50:
            break
    e = random.choice(pub_keys)
    del(pub_keys)
    return e


def priv_key(e, phi):
    i = 2
    while 1:
        if (i * e) % phi == 1:
            d = i
            break
        i += 1
    return d
