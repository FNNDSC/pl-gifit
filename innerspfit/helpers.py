import functools
from typing import Iterable

from innerspfit.model import SurfaceFitParams


def to_cliargs(sched: Iterable[SurfaceFitParams]) -> Iterable[str]:
    return functools.reduce(join, sched).to_cliargs()


def join(a: SurfaceFitParams, b: SurfaceFitParams) -> SurfaceFitParams:
    params = (','.join(t) for t in zip(a.astuple(), b.astuple()))
    return SurfaceFitParams(*params)
