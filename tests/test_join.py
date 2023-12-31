from typing import Iterable

from gifit import helpers
from gifit.model import SurfaceFitParams
import pytest

PARAMS1 = SurfaceFitParams(
    '20480',
    '100',
    '1e-5',
    '200',
    '100',
    '10',
    '0.2',
    '0',
    '0.005',
    '0.5',
    '10',
)
PARAMS2 = SurfaceFitParams(
    '20480',
    '200',
    '2e-5',
    '300',
    '100',
    '10',
    '0.2',
    '0',
    '0.005',
    '0.5',
    '10',
)
PARAMS3 = SurfaceFitParams(
    '20480',
    '300',
    '3e-5',
    '400',
    '100',
    '10',
    '0.2',
    '0',
    '0.005',
    '0.5',
    '10',
)


@pytest.mark.parametrize(
    'sched, expected',
    [
        (
            [PARAMS1],
            [
                '-size',
                '20480',
                '-sw',
                '100',
                '-lw',
                '1e-5',
                '-iter-outer',
                '200',
                '-iter-inner',
                '100',
                '-iso-value',
                '10',
                '-step-size',
                '0.2',
                '-oversample',
                '0',
                '-self-dist',
                '0.005',
                '-self-weight',
                '0.5',
                '-taubin',
                '10',
            ],
        ),
        (
            [PARAMS1, PARAMS2],
            [
                '-size',
                '20480,20480',
                '-sw',
                '100,200',
                '-lw',
                '1e-5,2e-5',
                '-iter-outer',
                '200,300',
                '-iter-inner',
                '100,100',
                '-iso-value',
                '10,10',
                '-step-size',
                '0.2,0.2',
                '-oversample',
                '0,0',
                '-self-dist',
                '0.005,0.005',
                '-self-weight',
                '0.5,0.5',
                '-taubin',
                '10,10',
            ],
        ),
        (
            [PARAMS1, PARAMS2, PARAMS3],
            [
                '-size',
                '20480,20480,20480',
                '-sw',
                '100,200,300',
                '-lw',
                '1e-5,2e-5,3e-5',
                '-iter-outer',
                '200,300,400',
                '-iter-inner',
                '100,100,100',
                '-iso-value',
                '10,10,10',
                '-step-size',
                '0.2,0.2,0.2',
                '-oversample',
                '0,0,0',
                '-self-dist',
                '0.005,0.005,0.005',
                '-self-weight',
                '0.5,0.5,0.5',
                '-taubin',
                '10,10,10',
            ],
        ),
    ],
)
def test_join_cliargs(sched: Iterable[SurfaceFitParams], expected: list[str]):
    assert list(helpers.to_cliargs(sched)) == expected
