import unittest
import numpy as np
import qam16

class TestQAM16(unittest.TestCase):

    def setUp(self):
        bits = [0,1]
        self.bits_comb = [ np.array([w,x,y,z]) for w in bits for x in bits for y in bits for z in bits ]

    def test_moddemod(self):
        for bc in self.bits_comb:
            np.testing.assert_equal( qam16.demodulate(qam16.modulate(bc)), bc)

    def test_energy(self):
        tot_energy = 0
        for bc in self.bits_comb:
            tot_energy = tot_energy + np.abs(qam16.modulate(bc))**2
        # take the average
        tot_energy = tot_energy/16.
        self.assertAlmostEqual(1, tot_energy)

if __name__ == '__main__':
    unittest.main()
