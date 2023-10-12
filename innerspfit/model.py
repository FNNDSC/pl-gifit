import dataclasses
import importlib.resources
import pandas as pd
from pathlib import Path
import os
from collections import defaultdict
from typing import NewType, Self, Iterator

_MODEL_PATH = Path(str(importlib.resources.files(__package__).joinpath('model.csv')))
_MODEL_PARAM_TYPES: defaultdict[str, type] = defaultdict(lambda: str)
_MODEL_PARAM_TYPES['approximate_age'] = int
_MODEL_PARAM_TYPES['stage'] = int
_MODEL_PARAM_TYPES['gyrification_index'] = float

KnownGi = NewType('KnownGi', float)
"""A specific value for gyrification index which is found in the column in the CSV."""


@dataclasses.dataclass(frozen=True)
class SurfaceFitParams:
    size: str
    stretch_weight: str
    laplacian_weight: str
    iter_outer: str
    iter_inner: str
    iso_value: str
    step_size: str
    oversample: str
    self_dist: str
    self_weight: str
    taubin: str

    @classmethod
    def from_namedtuple(cls, t) -> Self:
        """Deserialize row"""
        return cls(
            size=t.size,
            stretch_weight=t.stretch_weight,
            laplacian_weight=t.laplacian_weight,
            iter_outer=t.iter_outer,
            iter_inner=t.iter_inner,
            iso_value=t.iso_value,
            step_size=t.step_size,
            oversample=t.oversample,
            self_dist=t.self_dist,
            self_weight=t.self_weight,
            taubin=t.taubin
        )

    @classmethod
    def field_names(cls):
        return frozenset(f.name for f in dataclasses.fields(cls))

    def to_cliargs(self) -> list[str]:
        return [
            '-size',
            self.size,
            '-sw',
            self.stretch_weight,
            '-lw',
            self.laplacian_weight,
            '-iter-outer',
            self.iter_outer,
            '-iter-inner',
            self.iter_inner,
            '-iso-value',
            self.iso_value,
            '-step-size',
            self.step_size,
            '-oversample',
            self.oversample,
            '-self-dist',
            self.self_dist,
            '-self-weight',
            self.self_weight,
            '-taubin',
            self.taubin
        ]

    def astuple(self) -> tuple[str, ...]:
        return dataclasses.astuple(self)


class Model:
    def __init__(self, path: str | os.PathLike = _MODEL_PATH):
        self._df = pd.read_csv(path, dtype=_MODEL_PARAM_TYPES)
        missing_fields = SurfaceFitParams.field_names() - set(self._df.columns)
        if missing_fields:
            raise ValueError(f'{path} is missing the following columns: {missing_fields}')

    def get_schedule_for(self, gi: float) -> Iterator[SurfaceFitParams]:
        matched_gi = self._match_gi(gi)
        sliced_df = self._select_schedule_for(matched_gi)
        return map(SurfaceFitParams.from_namedtuple, sliced_df.itertuples())

    def _match_gi(self, gi: float) -> KnownGi:
        """
        Round the given value up to a known value from ``self._df['gyrification_index']``.
        """
        max_gi = self._df['gyrification_index'].max()
        if gi > max_gi:
            return max_gi
        known_gis = iter(self._df['gyrification_index'])
        while gi > (matched := next(known_gis)):
            pass
        return KnownGi(matched)

    def _select_schedule_for(self, gi: KnownGi) -> pd.DataFrame:
        return self._df[self._df['gyrification_index'] == gi]
