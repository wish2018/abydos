# Copyright 2018-2020 by Christopher C. Little.
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

"""abydos.tests.fuzz.test_fingerprint.

This module contains fuzz tests for abydos.fingerprint
"""

import codecs
import unittest
from random import choice, randint, sample

from abydos.fingerprint import (
    BWTF,
    BWTRLEF,
    Consonant,
    Count,
    Extract,
    ExtractPositionFrequency,
    LACSS,
    LCCutter,
    Occurrence,
    OccurrenceHalved,
    OmissionKey,
    Phonetic,
    Position,
    QGram,
    SkeletonKey,
    String,
    SynonameToolcode,
)

from . import EXTREME_TEST, _corpus_file, _fuzz, _random_char


synoname = SynonameToolcode()

algorithms = {
    'bwtf': BWTF().fingerprint,
    'bwtrlef': BWTRLEF().fingerprint,
    'consonant': Consonant().fingerprint,
    'consonant_2': Consonant(variant=2).fingerprint,
    'consonant_3': Consonant(variant=3).fingerprint,
    'consonant_nd': Consonant(doubles=False).fingerprint,
    'count': Count().fingerprint,
    'count_32': Count(n_bits=32).fingerprint,
    'extract': Extract().fingerprint,
    'extract_2': Extract(letter_list=2).fingerprint,
    'extract_3': Extract(letter_list=3).fingerprint,
    'extract_4': Extract(letter_list=4).fingerprint,
    'extract_position_frequency': ExtractPositionFrequency().fingerprint,
    'lacss': LACSS().fingerprint,
    'lc_cutter': LCCutter().fingerprint,
    'occurrence': Occurrence().fingerprint,
    'occurrence_halved': OccurrenceHalved().fingerprint,
    'omission_key': OmissionKey().fingerprint,
    'phonetic': Phonetic().fingerprint,
    'position': Position().fingerprint,
    'position_32_2': Position(n_bits=32, bits_per_letter=2).fingerprint,
    'qgram': QGram().fingerprint,
    'qgram_q3': QGram(qval=3).fingerprint,
    'qgram_ssj': QGram(start_stop='$#', joiner=' ').fingerprint,
    'skeleton_key': SkeletonKey().fingerprint,
    'string': String().fingerprint,
    'synoname_toolcode': synoname.fingerprint,
    'synoname_toolcode_2name': lambda _: synoname.fingerprint(_, _),
}


class BigListOfNaughtyStringsTestCases(unittest.TestCase):
    """Test each fingerprint algorithm against the BLNS set.

    Here, we test each algorithm against each string, but we only care that it
    does not result in an exception.

    While not actually a fuzz test, this does serve the purpose of looking for
    errors resulting from unanticipated input.
    """

    def fuzz_test_blns(self):
        """Test each fingerprint algorithm against the BLNS set."""
        blns = []
        with codecs.open(_corpus_file('blns.txt'), encoding='UTF-8') as nsf:
            for line in nsf:
                line = line[:-1]
                if line and line[0] != '#':
                    blns.append(line)

        for algo in algorithms:
            for ns in blns:
                try:
                    algorithms[algo](ns)
                except Exception as inst:
                    self.fail(
                        'Exception "{}" thrown by {} for BLNS: {}'.format(
                            inst, algo, ns
                        )
                    )


class FuzzedWordsTestCases(unittest.TestCase):
    """Test each fingerprint algorithm against the base words set."""

    reps = 1000 * (10000 if EXTREME_TEST else 1)

    basewords = []
    with codecs.open(
        _corpus_file('basewords.txt'), encoding='UTF-8'
    ) as basewords_file:
        for line in basewords_file:
            line = line[:-1]
            if line:
                basewords.append(line)

    def fuzz_test_base(self):
        """Test each fingerprint algorithm against the unfuzzed base words."""
        for algo in algorithms:
            for word in self.basewords:
                try:
                    algorithms[algo](word)
                except Exception as inst:
                    self.fail(
                        'Exception "{}" thrown by {} for word: {}'.format(
                            inst, algo, word
                        )
                    )

    def fuzz_test_20pct(self):
        """Fuzz test fingerprint algorithms against 20% fuzzed words."""
        for _ in range(self.reps):
            fuzzed = _fuzz(choice(self.basewords), fuzziness=0.2)

            if EXTREME_TEST:
                algs = list(algorithms.keys())
            else:
                algs = sample(list(algorithms.keys()), k=5)

            for algo in algs:
                try:
                    algorithms[algo](fuzzed)
                except Exception as inst:
                    self.fail(
                        'Exception "{}" thrown by {} for word: {}'.format(
                            inst, algo, fuzzed
                        )
                    )

    def fuzz_test_100pct(self):
        """Fuzz test fingerprint algorithms against 100% fuzzed words."""
        for _ in range(self.reps):
            fuzzed = _fuzz(choice(self.basewords), fuzziness=1)

            if EXTREME_TEST:
                algs = list(algorithms.keys())
            else:
                algs = sample(list(algorithms.keys()), k=5)

            for algo in algs:
                try:
                    algorithms[algo](fuzzed)
                except Exception as inst:
                    self.fail(
                        'Exception "{}" thrown by {} for word: {}'.format(
                            inst, algo, fuzzed
                        )
                    )

    def fuzz_test_fuzz_bmp(self):
        """Fuzz test fingerprint algorithms against BMP fuzz."""
        for _ in range(self.reps):
            fuzzed = ''.join(
                _random_char(0xFFFF) for _ in range(0, randint(8, 16))
            )

            if EXTREME_TEST:
                algs = list(algorithms.keys())
            else:
                algs = sample(list(algorithms.keys()), k=5)

            for algo in algs:
                try:
                    algorithms[algo](fuzzed)
                except Exception as inst:
                    self.fail(
                        'Exception "{}" thrown by {} for word: {}'.format(
                            inst, algo, fuzzed
                        )
                    )

    def fuzz_test_fuzz_bmpsmp_letter(self):
        """Fuzz test fingerprint algorithms against alphabetic BMP+SMP fuzz."""
        for _ in range(self.reps):
            fuzzed = ''.join(
                _random_char(0x1FFFF, ' LETTER ')
                for _ in range(0, randint(8, 16))
            )

            if EXTREME_TEST:
                algs = list(algorithms.keys())
            else:
                algs = sample(list(algorithms.keys()), k=5)

            for algo in algs:
                try:
                    algorithms[algo](fuzzed)
                except Exception as inst:
                    self.fail(
                        'Exception "{}" thrown by {} for word: {}'.format(
                            inst, algo, fuzzed
                        )
                    )

    def fuzz_test_fuzz_bmpsmp_latin(self):
        """Fuzz test fingerprint algorithms against Latin BMP+SMP fuzz."""
        for _ in range(self.reps):
            fuzzed = ''.join(
                _random_char(0x1FFFF, 'LATIN ')
                for _ in range(0, randint(8, 16))
            )

            if EXTREME_TEST:
                algs = list(algorithms.keys())
            else:
                algs = sample(list(algorithms.keys()), k=5)

            for algo in algs:
                try:
                    algorithms[algo](fuzzed)
                except Exception as inst:
                    self.fail(
                        'Exception "{}" thrown by {} for word: {}'.format(
                            inst, algo, fuzzed
                        )
                    )

    def fuzz_test_fuzz_unicode(self):
        """Fuzz test fingerprint algorithms against valid Unicode fuzz."""
        for _ in range(self.reps):
            fuzzed = ''.join(_random_char() for _ in range(0, randint(8, 16)))

            if EXTREME_TEST:
                algs = list(algorithms.keys())
            else:
                algs = sample(list(algorithms.keys()), k=5)

            for algo in algs:
                try:
                    algorithms[algo](fuzzed)
                except Exception as inst:
                    self.fail(
                        'Exception "{}" thrown by {} for word: {}'.format(
                            inst, algo, fuzzed
                        )
                    )


if __name__ == '__main__':
    unittest.main()
