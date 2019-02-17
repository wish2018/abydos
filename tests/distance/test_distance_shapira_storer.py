# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
# This file is part of Abydos.
#
# Abydos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Abydos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Abydos. If not, see <http://www.gnu.org/licenses/>.

"""abydos.tests.distance.test_distance_shapira_storer.

This module contains unit tests for abydos.distance.ShapiraStorer
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import ShapiraStorer


class ShapiraStorerTestCases(unittest.TestCase):
    """Test ShapiraStorer functions.

    abydos.distance.ShapiraStorer
    """

    cmp = ShapiraStorer()

    def test_shapira_storer_dist(self):
        """Test abydos.distance.ShapiraStorer.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0)
        self.assertEqual(self.cmp.dist('a', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'a'), 1.0)
        self.assertEqual(self.cmp.dist('abc', ''), 1.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 1.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 2.0)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), float('nan'))
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), float('nan'))
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), float('nan'))
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), float('nan'))
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), float('nan')
        )

    def test_shapira_storer_dist_abs(self):
        """Test abydos.distance.ShapiraStorer.dist_abs."""
        # Base cases
        self.assertEqual(self.cmp.dist_abs('', ''), 0)
        self.assertEqual(self.cmp.dist_abs('a', ''), 1)
        self.assertEqual(self.cmp.dist_abs('', 'a'), 1)
        self.assertEqual(self.cmp.dist_abs('abc', ''), 3)
        self.assertEqual(self.cmp.dist_abs('', 'abc'), 3)
        self.assertEqual(self.cmp.dist_abs('abc', 'abc'), float('nan'))
        self.assertEqual(self.cmp.dist_abs('abcd', 'efgh'), 8)

        self.assertAlmostEqual(
            self.cmp.dist_abs('Nigel', 'Niall'), float('nan')
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Niall', 'Nigel'), float('nan')
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Colin', 'Coiln'), float('nan')
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('Coiln', 'Colin'), float('nan')
        )
        self.assertAlmostEqual(
            self.cmp.dist_abs('ATCAACGAGT', 'AACGATTAG'), float('nan')
        )


if __name__ == '__main__':
    unittest.main()
