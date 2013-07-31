import numpy as np

def spread(symbol, codeword):
    """ spreads the symbols with the given codeword """
    return symbol*codeword
    
def despread(spreaded_sybmol, codeword):
    """ despreads the chip sequence with the given codeword """
    return np.sum(spreaded_sybmol*codeword)

def vec_spread(symbols, codeword):
    """ vector wrapper for dsss.spread """
    symbols = [ spread(x, codeword) for x in symbols ]
    symbols = np.hstack(symbols)
    return symbols

def vec_despread(symbols, codeword):
    """ vector wrapper for dsss.despread """
    M = symbols.size/codeword.size
    symbols = np.array_split(symbols, M)
    symbols = [ despread(x, codeword) for x in symbols ]
    symbols = np.hstack(symbols)
    return symbols
