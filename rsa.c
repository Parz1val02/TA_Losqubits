#include <math.h>
#include <stdio.h>
#include <time.h>
#include <stdlib.h>

int gcd2(int a, int b)
{
    int nuevo_a = 0;
    while (b)
    {
        nuevo_a = a;
        a = b;
        b = nuevo_a % b;
    }
    return a;
}

void inicia()
{
    srand(time(NULL));
}

int prime_finder2(int n)
{
    int test_number = rand() % (51) + (n);
    int i;
    if (test_number % 2 == 0)
    {
        return prime_finder2(n);
    }
    else
    {
        int a = (int)sqrt(test_number);
        for (i = 3; i < a + 1; i += 2)
        {
            if (test_number % i == 0)
            {
                return prime_finder2(n);
            }
        }
        return test_number;
    }
}

int pubkeys(int phi)
{
    int i;
    int j = 0;
    int N = 50;
    int pub_keys[N];
    for (i = 0; i < (sizeof(pub_keys) / sizeof(pub_keys[0])); i++)
    {
        pub_keys[i] = 0;
    }
    for (i = 2; i < phi; i++)
    {
        if (gcd2(i, phi) == 1)
        {
            pub_keys[j] = i;
            j++;
        }
        if (j > (N - 1))
        {
            break;
        }
    }
    int e;
    while (1)
    {
        e = pub_keys[rand() % (sizeof(pub_keys) / sizeof(pub_keys[0]))];
        if (e == 0)
        {
            continue;
        }
        else
        {
            break;
        }
    }
    for (i = 0; i < (sizeof(pub_keys) / sizeof(pub_keys[0])); i++)
    {
        pub_keys[i] = 0;
    }
    return e;
}

int privkeys(int e, int phi)
{
    int i = 2;
    int d = 0;
    while (1)
    {
        if ((i * e) % phi == 1)
        {
            d = i;
            break;
        }
        i += 1;
    }
    return d;
}
