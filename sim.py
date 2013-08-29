#!/usr/bin/python

import numpy as np

import matplotlib as mp
mp.use('PDF')
mp.rc('text', usetex=True)
mp.rc('font', family='serif', size=13)
import matplotlib.pyplot as plt

import channel
import modulation
from rake import dsss
from rake import rake_receiver
# theoretical curves
import theory

# maximum number of packages after which the simulation stops
max_packets = 1e7
# maximum number of errors after which the simulation stops
max_errors = 5e4
# number of symbols per package
M = 50
#energy per symbol
Es = 1
# bits per symbol
bps = 4
# spreading sequence
spread_seq = dsss.mls.gen_mls([1,1,1,1])
# Eb/N0
EbN0 = np.logspace(-1, 2, 31)
sigmas = np.sqrt(Es*spread_seq.size/(2*bps*EbN0))
# power delay profiles used for the simulation
pdps = [{'pdp': np.array([1]),       'plotstyle':'b', 'legend':'1 finger'},
        {'pdp': np.array([1, 1]),    'plotstyle':'g', 'legend':'2 fingers'},
        {'pdp': np.array([1, 1, 1]), 'plotstyle':'r', 'legend':'3 fingers'}]
# total number of bit errors
tot_bit_errors = np.zeros((len(pdps), EbN0.size))
# bit error ratios
ber_sim = np.zeros(tot_bit_errors.shape)
ber_theo = np.zeros(tot_bit_errors.shape)
# sigma of the rayleigh distribution
sigma_rayleigh = np.sqrt(2/np.pi)

# compute the theoretical curves for every power delay profile
for idx_pdp, pdp_el in enumerate(pdps):
    ber_theo[idx_pdp,:] = np.array([theory.qam_mrc_ber(bps**2, len(pdp_el['pdp']), x) for x in EbN0])

# simulation of the rake receivers
for idx_pdp, pdp_el in enumerate(pdps):
    print "Computing the BER for the following pdp: ", pdp_el['pdp']
    for idx, sigma in enumerate(sigmas):
        print "sigma=%f,"% (sigma),
        # number of transmitted packages
        n = 0;
        # a Rayleigh distributed multipath channel with AWGN
        ch = channel.rayleigh_multipath(sigma, sigma_rayleigh, pdp_el['pdp'])
        # rake receiver the normalized spreading sequence
        rake_rec = rake_receiver(ch.cir, spread_seq/np.sum(spread_seq**2))
        while 1:
            n = n+1
            # update the channel impulse response to simulate fading
            ch.update_cir()
            # update the CIR of the rake for the MRC
            rake_rec.update_cir(ch.cir)
            # generate random bits
            bits_tx = np.random.randint(low = 0, high = 2, size = bps*M)
            # map from bits to symbols
            symbols = modulation.qam16.vec_mod(bits_tx)
            # spread symbols
            symbols = dsss.vec_spread(symbols, spread_seq)
            # convolute with channel impulse response
            symbols = ch.apply_cir(symbols)
            # add white Gaussian noise
            symbols = ch.awgn(symbols)
            # feed symbols into rake receiver
            symbols = rake_rec.process_signal(symbols)
            # map from symbols to bits
            bits_rx = modulation.qam16.vec_demod(symbols)
            # compare received bits with transmitted bits
            bits_errors = bits_rx[(bits_rx != bits_tx)]
            # compute number of bit errors
            nbit_errors = bits_errors.size
            tot_bit_errors[idx_pdp, idx] = tot_bit_errors[idx_pdp, idx] + nbit_errors
            # if enough bit errors are available for a thourough statistic quit
            # the simulation for this Eb/N0
            if ((tot_bit_errors[idx_pdp, idx] > max_errors) or (n > max_packets)):
                    print n, "packets were processed:",
                    ber_sim[idx_pdp, idx] = tot_bit_errors[idx_pdp, idx]/(n*M*bps)
                    break
        print "BER=%f" % (ber_sim[idx_pdp, idx])

# save the data
data = { 'sim': ber_theo,
         'theo': ber_theo,
         'EbN0': EbN0}

import pickle
outfile = open('rake_vs_mrc.pkl', 'wb')
pickle.dump(data, outfile)
outfile.close

# plot the data
#ax = plt.subplot(111)
ax = plt.subplot(111)
for idx_pdp, pdp_el in enumerate(pdps):
    plt.semilogy(10*np.log10(EbN0), ber_sim[idx_pdp,:], pdp_el['plotstyle'],
            label='Rake: ' + pdp_el['legend'] + ' (sim)')
    plt.semilogy(10*np.log10(EbN0), ber_theo[idx_pdp,:], pdp_el['plotstyle']+'-o',
            label='MRC: '+pdp_el['legend']+' (theory)')

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, loc=3)

plt.title("16-QAM Rake Receiver")
plt.ylabel(r'BER')
plt.xlabel(r'$E_b/N_0$ in dB')
plt.grid(True)
plt.savefig("rake_vs_mrc.pdf", bbox_inches='tight', dpi=300)
