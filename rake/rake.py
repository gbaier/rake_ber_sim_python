import numpy as np
import dsss

class rake_receiver():
    """ a rake receiver that employs maximum ratio combining and uses every
    multipath component """
    def __init__(self, cir, spread_seq):
        self.cir = cir
        self.length = self.cir.size-1
        self.spread_seq = spread_seq
        # for every multipath component we need a complete spreaded
        # code word. As a result of the channel impulse response
        # we need to store some old chips.
        self.taps = self.compute_taps()

    def update_cir(self, cir):
        """ update the channel impulse response """
        self.cir = cir
        self.taps = self.compute_taps()

    def compute_taps(self):
        """ computes the taps and respective delay of each finger """
        # return taps and delays where the channel impulse response is nonzero
        taps = self.cir[self.cir != 0]
        delays = np.arange(0, self.cir.size)[self.cir != 0]
        return zip(taps, delays)

    def process_signal(self, chips):
        """ process the received chips """
        # preallocate storage space for processed symbols
        tot_symbols = np.zeros(chips.size/self.spread_seq.size)
        # for each finger of the rake receiver despread the chips
        for (t, d) in self.taps:
            # despread
            temp_symbols = dsss.vec_despread(chips[d:chips.size-self.length+d], self.spread_seq)
            # maximum ratio combining
            tot_symbols = tot_symbols+np.conj(t)*temp_symbols
        # normalize the output signal
        tot_symbols = tot_symbols/np.sum(np.abs(self.cir)**2)
        return tot_symbols
