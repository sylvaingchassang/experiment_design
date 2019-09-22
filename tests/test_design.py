from numpy.testing import TestCase, assert_array_almost_equal
from os import path
from parameterized import parameterized

from design import RCT, KRerandomizedRCT
from balance import MahalanobisBalance, pvalues_report
from assignment import get_assignments_by_positions


class TestRCT(TestCase):
    def setUp(self) -> None:
        self.file = path.join(path.dirname(__file__), 'example_covariates.csv')
        self.rct = RCT(self.file, [.5, .5], 1)

    def test_hash_int(self):
        assert (self.rct.file_hash_int ==
                151671729980354795404869707092356732292)

    def test_seed(self):
        assert (self.rct.seed == 2705298821)

    def test_sample_size(self):
        assert (self.rct.sample_size == 100)

    def test_draw_iid(self):
        assert_array_almost_equal(self.rct.assignment_from_iid.mean(), 0.57)
        assert_array_almost_equal(self.rct.assignment_from_iid[:10].T,
                                  [[1, 1, 0, 0, 0, 1, 0, 1, 0, 1]])
        assert_array_almost_equal(self.rct.assignment_from_iid.mean(), 0.57)

    def test_draw_shuffle(self):
        assert_array_almost_equal(
            self.rct.assignment_from_shuffled.mean(), [.5])
        assert_array_almost_equal(self.rct.assignment_from_shuffled[:10].T,
                                  [[0, 1, 1, 1, 0, 1, 0, 0, 0, 0]])
        assert_array_almost_equal(self.rct.assignment_from_shuffled[:10].T,
                                  [[0, 1, 1, 1, 0, 1, 0, 0, 0, 0]])

    def test_iid_balance(self):
        assert_array_almost_equal(
            pvalues_report(self.rct.df, get_assignments_by_positions(
                self.rct.assignment_from_iid)), [[0.898257, 0.7013, 0.177232]])

    def test_shuffled_balance(self):
        assert_array_almost_equal(
            pvalues_report(self.rct.df, get_assignments_by_positions(
                self.rct.assignment_from_shuffled)),
            [[0.518609, 0.34273, 0.551186]])


class TestKRerandomized(TestCase):
    def setUp(self):
        self.file = path.join(path.dirname(__file__), 'example_covariates.csv')
        self.maha = MahalanobisBalance()
        self.krerand = KRerandomizedRCT(self.maha, self.file, [.5, .5])

    def test_hash_int(self):
        assert (self.krerand.file_hash_int ==
                151671729980354795404869707092356732292)

    def test_seed(self):
        assert (self.krerand.seed == 2705298820)

    def test_k(self):
        assert self.krerand.k == 100

    def test_iid_krerand(self):
        assert_array_almost_equal(
            self.krerand.assignment_from_iid[:10].T,
            [[1, 1, 1, 1, 0, 0, 0, 1, 0, 0]])

    def test_iid_balance(self):
        assert_array_almost_equal(
            pvalues_report(
                self.krerand.df,
                get_assignments_by_positions(
                    self.krerand.assignment_from_iid)),
            [[0.973345, 0.906685, 0.952433]])

    def test_shuffled_balance(self):
        assert_array_almost_equal(
            pvalues_report(
                self.krerand.df,
                get_assignments_by_positions(
                    self.krerand.assignment_from_shuffled)),
            [[0.719567, 0.895064, 0.842654]])
