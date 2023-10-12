import functools
from pathlib import PurePath
from typing import Iterable

from innerspfit.model import SurfaceFitParams


def to_cliargs(sched: Iterable[SurfaceFitParams]) -> Iterable[str]:
    return functools.reduce(join, sched).to_cliargs()


def join(a: SurfaceFitParams, b: SurfaceFitParams) -> SurfaceFitParams:
    params = (','.join(t) for t in zip(a.astuple(), b.astuple()))
    return SurfaceFitParams(*params)


def sided_glob(input_path: PurePath, suffix: str) -> str:
    for prefix in ('lh.', 'rh.'):
        if input_path.name.startswith(prefix):
            return f'{prefix}*{suffix}'
    return f'*{suffix}'
