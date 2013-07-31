import unittest
import numpy as np
import walsh_hadamard

class test_walsh_hadamard(unittest.TestCase):

    def setUp(self):
        pass

    def test_orthogonality(self):
        length = 8
        H = walsh_hadamard.gen_walsh_hadamard(length)
        # check that the matrix product of H with the transpose of H is a diagonal matrix
        np.testing.assert_equal( np.dot(H, H), length*np.eye(length))

if __name__ == '__main__':
    unittest.main()
