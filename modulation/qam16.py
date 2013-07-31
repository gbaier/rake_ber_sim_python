import numpy as np

def modulate(bits):
    """ generates a 16-QAM symbol of unit energy """
    assert bits.size == 4, 'we need exactly 4 bits for a 16-QAM symbol'
    # first two bits determine the quadrant
    # real part quadrant
    rpq = 4*bits[0]-2
    # imaginary part quadrant
    ipq = 4*bits[1]-2
    
    # last two bits determine the position in the quadrant
    rp = 2*bits[2]-1
    # to get gray coding we need to rotate the sub qpsk symbol
    rp = rp*np.sign(rpq)
    ip = 2*bits[3]-1
    ip = ip*np.sign(ipq)

    symbol = np.complex(rpq+rp, ipq+ip)

    # normalize
    symbol = symbol/np.sqrt(10)

    return symbol

def demodulate(symbol):
    """ demodulates a 16-QAM symbol of unit energy """
    # denormalize to 1,3 grid
    symbol = symbol*np.sqrt(10)
    def compute_bit(level):
        if (level>=0):
            return 1
        else:
            return 0
    cb = compute_bit
    rp = symbol.real
    ip = symbol.imag
    # quadrant bits
    rbq = cb(rp)
    ibq = cb(ip)

    # position bits, remove information from the quadrant bits
    rbp = rp-(4*rbq-2)
    # undo the rotation
    rbp = cb(np.sign(rp)*rbp)
    ibp = ip-(4*ibq-2)
    ibp = cb(np.sign(ip)*ibp)

    bits = np.array([rbq, ibq, rbp, ibp])
    return bits

def vec_mod(bits):
    """ vector wrapper for qam16.modulate """
    M = bits.size/4
    # split bits into chunks for symbol generation
    bits = np.array_split(bits, M)
    symbols = [ modulate(x) for x in bits ]
    # reshape symbols
    symbols = np.hstack(symbols)
    return symbols

def vec_demod(symbols):
    """ vector wrapper for qam16.demodulate """
    M = symbols.size
    symbols = np.array_split(symbols, M)
    bits = [ demodulate(x) for x in symbols ]
    bits = np.hstack(bits)
    return bits
