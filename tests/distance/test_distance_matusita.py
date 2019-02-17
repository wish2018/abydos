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

"""abydos.tests.distance.test_distance_matusita.

This module contains unit tests for abydos.distance.Matusita
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest

from abydos.distance import Matusita


class MatusitaTestCases(unittest.TestCase):
    """Test Matusita functions.

    abydos.distance.Matusita
    """

    cmp = Matusita()

    def test_matusita_dist(self):
        """Test abydos.distance.Matusita.dist."""
        # Base cases
        self.assertEqual(self.cmp.dist('', ''), 0.0)
        self.assertEqual(self.cmp.dist('a', ''), 0.0)
        self.assertEqual(self.cmp.dist('', 'a'), 0.0)
        self.assertEqual(self.cmp.dist('abc', ''), 2.0)
        self.assertEqual(self.cmp.dist('', 'abc'), 2.0)
        self.assertEqual(self.cmp.dist('abc', 'abc'), 0.0)
        self.assertEqual(self.cmp.dist('abcd', 'efgh'), 3.1622776601683795)

        self.assertAlmostEqual(self.cmp.dist('Nigel', 'Niall'), 2.4494897428)
        self.assertAlmostEqual(self.cmp.dist('Niall', 'Nigel'), 2.4494897428)
        self.assertAlmostEqual(self.cmp.dist('Colin', 'Coiln'), 2.4494897428)
        self.assertAlmostEqual(self.cmp.dist('Coiln', 'Colin'), 2.4494897428)
        self.assertAlmostEqual(
            self.cmp.dist('ATCAACGAGT', 'AACGATTAG'), 2.6457513111
        )


if __name__ == '__main__':
    unittest.main()
