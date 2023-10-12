"""
Gyrification index helper functions.
"""
import os
from pathlib import Path
import subprocess as sp
import shlex
from typing import Optional
from tempfile import NamedTemporaryFile

from loguru import logger


def gyrification_index(surface: Path, output_file: Path) -> float:
    with NamedTemporaryFile(suffix=surface.suffix) as tmp:
        _run_adapt_object_mesh(surface, tmp.name)
        return _run_gyrification_index(tmp.name, output_file)


def _run_adapt_object_mesh(surface: str | os.PathLike, output: str | os.PathLike):
    """
    Run ``adapt_object_mesh``. Doing this before ``gyrification_index`` can work around some bugs.

    See https://github.com/FNNDSC/pl-innerspfit/issues/1

    If ``adapt_object_mesh`` fails, as a fallback ``output`` is created as a symlink to ``surface``.
    """
    surface = Path(surface)
    output = Path(output)
    cmd = ['adapt_object_mesh', surface, output, '9999999', '50', '0', '0']
    proc = sp.run(cmd)
    if proc.returncode != 0:
        logger.warning('Failed: {}', shlex.join(map(str, cmd)))
        output.unlink(missing_ok=True)
        output.symlink_to(surface)


def _run_gyrification_index(surface: str | os.PathLike, output_file: str | os.PathLike) -> float:
    cmd = ['gyrification_index', surface, output_file]
    proc = sp.run(cmd)
    if proc.returncode != 0:
        logger.warning('Failed: {}', shlex.join(map(str, cmd)))
        return 1.0
    if (gi := _parse_gi_from_file(output_file)) is not None:
        return gi
    logger.warning('Failed to parse gyrification_index output file: {}', output_file)
    return 1.0


def _parse_gi_from_file(f: str | os.PathLike) -> Optional[float]:
    try:
        last_line = _last_line_of(f)
        left, right = last_line.rsplit(':', maxsplit=1)
        if left != 'gyrification index':
            return None
        return float(right.strip())
    except Exception:  # noqa
        return None


def _last_line_of(f: str | os.PathLike) -> str:
    last_line = ''
    count = 0
    with open(f, 'r', encoding='utf-8') as o:
        nonempty_lines = filter(_not_empty, o)
        for i, line in enumerate(nonempty_lines):
            last_line = line
            count = i

    if count > 1:
        logger.warning('{} contains multiples lines. Maybe it contains error messages?', f)
    if count == 0:
        logger.warning('{} is empty')

    return last_line


def _not_empty(s: str) -> bool:
    return not s.isspace()
