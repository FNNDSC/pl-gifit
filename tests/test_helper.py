from pathlib import PurePath

import pytest

from gifit import helpers


@pytest.mark.parametrize(
    'input_name, expected',
    [
        ('brain.mnc', '*.obj'),
        ('lh.brain.mnc', 'lh.*.obj'),
        ('rh.brain.mnc', 'rh.*.obj'),
    ]
)
def test_sided_glob(input_name, expected):
    input_path = PurePath(input_name)
    assert helpers.sided_glob(input_path, '.obj') == expected
