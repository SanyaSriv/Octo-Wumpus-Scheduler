def xorshift(s, a, b):
    """
    Returns a random number in given range
    """
    s1 = s[0]
    s0 = s[1]

    # xorshift algorithm
    result = (s0 + s1) & ((1 << 64) - 1) 
    s[0] = s0
    s1 ^= (s1 << 23) & ((1 << 64) - 1) 
    s[1] = (s1 ^ s0 ^ (s1 >> 17) ^ (s0 >> 26)) & ((1 << 64) - 1) 

    # Adjust the result random number to fit a given range
    rng_within_range = a + result % (b - a + 1)

    return rng_within_range, s
