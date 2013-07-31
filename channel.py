import numpy as np

class rayleigh_multipath:
    """ a multipath channel with Rayleigh fading and AWGN """
    def __init__(self, sigma_awgn, sigma_rayleigh, pdp):
        self.sigma_awgn = sigma_awgn
        self.sigma_rayleigh = sigma_rayleigh
        self.pdp = np.array(pdp)
        self.l = self.pdp.size-1
        self.update_cir()

    def update_cir(self):
        """ generate a new CIR from the PDP with Rayleigh fading """
        self.cir = np.sqrt(np.array(self.pdp))
        randray = np.random.rayleigh(self.sigma_rayleigh, self.cir.size)
        self.cir = self.cir*randray

    def awgn(self, symbols):
        """ add white Gaussian noise """
        real_noise = np.random.randn(symbols.size)
        imag_noise = np.random.randn(symbols.size)
        noise = real_noise+1j*imag_noise
        return symbols+self.sigma_awgn*noise

    def apply_cir(self, symbols):
        """ convolve the symbols with the CIR """
        if self.l != 0:
            self.old_symbols = symbols[-self.l:]
        # apply the cir
        symbols = np.convolve(symbols, self.cir)
        return symbols 
