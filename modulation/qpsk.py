import numpy as np

def modulate(bits):
    # real part
    rp = 2*bits[0]-1
    # imaginary part
    ip = 2*bits[1]-1
    symbol = np.complex(rp, ip)
    # normalize
    symbol = symbol/np.sqrt(2)
    return symbol

def demodulate(symbol):
    def compute_bit(level):
        if (level>=0):
            return 1
        else:
            return 0
    rb = compute_bit(symbol.real)
    ib = compute_bit(symbol.imag)

    bits = np.array([rb, ib])
    return bits

def vec_mod(bits):
    M = bits.size/2
    # split bits into chunks for symbol generation
    bits = np.array_split(bits, M)
    symbols = [ modulate(x) for x in bits ]
    # reshape symbols
    symbols = np.hstack(symbols)
    return symbols

def vec_demod(symbols):
    M = symbols.size
    symbols = np.array_split(symbols, M)
    bits = [ demodulate(x) for x in symbols ]
    bits = np.hstack(bits)
    return bits
