import numpy as np

def gen_mls(state):
    # initial state of the linear feedback shift register
    state = np.array(state)
    # length of the register
    length = state.size
    # length of the maximum length sequence
    N = 2**length-1
    # generator polynoms
    generator_polynoms = [
        [1, 1],
        [1, 1, 0],
        [1, 1, 0, 0],
        [1, 0, 1, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 0, 0, 0],
        [1, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        ]
    # pick the generator polynom which matches the length of the LFSR
    g = np.array(generator_polynoms[length-2])
    # array which stores the maximum length sequence
    mls = np.zeros(N)
    for i in xrange(N):
        mls[i] = state[0]
        feedback = np.mod(np.sum(state*g), 2)
        state[0:-1] = state[1:]
        state[-1] = feedback
    # switch from bits to +1, -1
    mls = 2*mls-1
    return mls

