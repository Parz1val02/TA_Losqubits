import ctypes
import time
import random
import statistics
import math
import matplotlib.pyplot as plt
import rsa

if __name__ == '__main__':
    so_file = './rsa_c.so'
    lib = ctypes.CDLL(so_file)
    lib.inicia.argtypes = []
    lib.gcd2.argtypes = [ctypes.c_int, ctypes.c_int]
    lib.gcd2.restype = ctypes.c_int
    lib.prime_finder2.argtypes = [ctypes.c_int]
    lib.prime_finder2.restype = ctypes.c_int
    lib.pubkeys.argtypes = [ctypes.c_int]
    lib.pubkeys.restype = ctypes.c_int
    lib.privkeys.argtypes = [ctypes.c_int, ctypes.c_int]
    lib.privkeys.restype = ctypes.c_int

    tc_total = []
    tp_total = []
    tp_no_total = []
    L = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
    #L = [550, 650, 750, 850, 950, 1050, 1150, 1250]
    M = 100
    for i in L:
        tp = []
        for j in range(M):
            s1 = time.perf_counter()
            p = None
            q = None
            while (p == q):
                p = rsa.finder2(i)
                q = rsa.finder2(i)
            n = p*q
            phi = (p-1)*(q-1)
            e = rsa.pub_key(phi)
            d = rsa.priv_key(e, phi)
            e1 = time.perf_counter()
            elap1 = e1-s1
            tp.append(elap1)
        tp_total.append(statistics.median(tp))
        tp_no = []
        for j in range(M):
            s3 = time.perf_counter()
            p = None
            q = None
            while (p == q):
                p = rsa.prime_finder(i)
                q = rsa.prime_finder(i)
            n = p*q
            phi = (p-1)*(q-1)
            e = rsa.pub_key1(phi)
            d = rsa.priv_key(e, phi)
            e3 = time.perf_counter()
            elap3 = e3-s3
            tp_no.append(elap3)
        tp_no_total.append(statistics.median(tp_no))
        tc = []
        for j in range(M):
            s2 = time.perf_counter()
            lib.inicia()
            p = None
            q = None
            while (p == q):
                q = lib.prime_finder2(i)
                p = lib.prime_finder2(i)
            n = p*q
            phi = (p-1)*(q-1)
            e = lib.pubkeys(phi)
            d = lib.privkeys(e, phi)
            e2 = time.perf_counter()
            elap2 = e2-s2
            tc.append(elap2)
        tc_total.append(statistics.median(tc))
    # mediana_p/mediana_c
    SpeedUp1 = [i/j for i, j in zip(tp_total, tc_total)]
    # mediana_p_no/mediana_p
    SpeedUp2 = [i/j for i, j in zip(tp_no_total, tp_total)]
    # mediana_p_no/mediana_c
    SpeedUp3 = [i/j for i, j in zip(tp_no_total, tc_total)]

    plt.plot(L, tc_total, 'r')
    plt.plot(L, tp_total, 'b')
    plt.plot(L, tp_no_total, 'g')
    plt.legend(["C", "Python optimizada", "Python no optimizada"], loc="best")
    plt.grid()
    plt.xlabel("Límite rango primos")
    plt.ylabel("Tiempo de ejecución [s]")
    plt.savefig("tiempos_medianas.png", dpi=500)
    plt.close()

    plt.plot(L, SpeedUp1, 'r')
    plt.plot(L, SpeedUp2, 'b')
    plt.plot(L, SpeedUp3, 'g')
    plt.legend(["Py_op/C", "Py_no_op/Py_op", "Py_no_op/C"], loc="best")
    plt.grid()
    plt.xlabel("Límite rango primos")
    plt.ylabel("SpeedUp")
    plt.savefig("speedup_medianas.png", dpi=500)
    plt.close()
