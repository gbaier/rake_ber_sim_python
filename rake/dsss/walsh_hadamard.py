import numpy as np

def gen_walsh_hadamard(N):
    """ generates the Walsh Hadamard code matrix of dimension N X N """
    nat_numbers = np.arange(1, 100)
    N_ld = np.log2(np.array([N]))
    assert (np.any(N_ld == nat_numbers)), 'N must be a power of 2'
    if (N == 2):
        H = np.array( [[1, 1], [1, -1]] )
    else:
        H_sub = gen_walsh_hadamard(N/2)
        H = np.hstack( (H_sub, H_sub) )
        H_temp = np.hstack( (H_sub, -H_sub) )
        H = np.vstack( (H, H_temp) )
    return H

