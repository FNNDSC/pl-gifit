#!/usr/bin/env python
import importlib.resources
import itertools
import os
import subprocess as sp
import sys
import shlex
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional, Sequence

from chris_plugin import chris_plugin, PathMapper
from loguru import logger

from gifit import __version__, DISPLAY_TITLE, helpers
from gifit.gi import gyrification_index
from gifit.model import Model, SurfaceFitParams

parser = ArgumentParser(description='surface_fit wrapper',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('--no-fail', dest='no_fail', action='store_true',
                    help='Produce exit code 0 even if any subprocesses do not.')
parser.add_argument('-m', '--model', dest='model', type=str, default='d',
                    help='Name of built-in model to use, or a path to a custom CSV model.')
parser.add_argument('-s', '--size', dest='size', type=int, default=81920,
                    help='Output mesh size')
parser.add_argument('-t', '--thickness-fwhm', dest='thickness_fwhm', type=str, default='0,5,10',
                    help='List of fwhm values in mm to use for calculating thickness between surfaces')
parser.add_argument('-V', '--version', action='version',
                    version=f'%(prog)s {__version__}')
parser.add_argument('-J', '--threads', type=int, default=0,
                    help='Number of threads to use for parallel jobs. '
                         'Pass 0 to use number of visible CPUs.')


@chris_plugin(
    parser=parser,
    title='Surface mesh deformation',
    category='Surfaces',
    min_memory_limit='1Gi',
    min_cpu_limit='1000m',
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    print(DISPLAY_TITLE, file=sys.stderr, flush=True)

    if options.threads > 0:
        nproc = options.threads
    else:
        nproc = len(os.sched_getaffinity(0))
    logger.info('Using {} threads.', nproc)

    model_file = options.model if os.path.isfile(options.model) else get_builtin_model(options.model)
    model = Model(model_file)

    thickness_fwhm = __parse_thickness_fwhm(options.thickness_fwhm)

    mapper = PathMapper.file_mapper(inputdir, outputdir, glob='**/*.mnc', suffix='.obj')
    with ThreadPoolExecutor(max_workers=nproc) as pool:
        results = pool.map(lambda t, p, s, b: run_surface_fit(*t, p, s, b), mapper,
                           itertools.repeat(model),
                           itertools.repeat(str(options.size)),
                           itertools.repeat(thickness_fwhm))

    if not options.no_fail and not all(results):
        sys.exit(1)


def run_surface_fit(grid: Path, output_surf: Path, model: Model, size: str, thickness_fwhm: Sequence[int]) -> bool:
    """
    :return: True if successful
    """
    starting_surface = locate_surface_for(grid)
    if starting_surface is None:
        logger.error('No starting surface found for {}', grid)
        return False

    gi_file = output_surf.with_suffix('.gi.txt')
    gi = gyrification_index(starting_surface, gi_file)
    logger.info('{} gyrification_index={}', starting_surface, gi)

    sched = list(model.get_schedule_for(gi))
    # If last stage does not match target size, do one more stage with zero iterations just to resize the mesh
    if sched[-1].size != size:
        sched.append(SurfaceFitParams.empty_with_size(size))
    cli_args = helpers.to_cliargs(sched)

    extra_args = [
        '-disterr', output_surf.with_suffix('.disterr.txt'),
        '-disterr-abs', output_surf.with_suffix('.disterr.abs.txt')
    ]

    cmd = ['surface_fit_script.pl', *cli_args, *extra_args, grid, starting_surface, output_surf]
    log_file = output_surf.with_name(output_surf.name + '.log')
    logger.info('Starting: {}', shlex.join(map(str, cmd)))
    with log_file.open('wb') as log_handle:
        job = sp.run(cmd, stdout=log_handle, stderr=log_handle)
    rc_file = log_file.with_suffix('.rc')
    rc_file.write_text(str(job.returncode))

    if job.returncode != 0:
        logger.error('FAILED -- check log file for details: {}', log_file)
        return False

    thickness_commands_worked = True
    for f in thickness_fwhm:
        output_file = output_surf.with_suffix(f'.tlink_{f}mm.txt')
        log_file = output_file.with_suffix('.log')
        cmd = ['cortical_thickness', '-tlink', '-fwhm', str(f), output_surf, starting_surface, output_file]
        with log_file.open('wb') as log_handle:
            proc = sp.run(cmd, stdout=log_handle, stderr=log_handle)
        if proc.returncode != 0:
            logger.error('Command failed: {}', shlex.join(map(str, cmd)))
            thickness_commands_worked = False

    logger.info('Finished: {} -> {}', starting_surface, output_surf)
    return thickness_commands_worked


def locate_surface_for(mask: Path) -> Optional[Path]:
    glob = mask.parent.glob(helpers.sided_glob(mask, '.obj'))
    first = next(glob, None)
    second = next(glob, None)
    if second is not None:
        return None
    return first


def get_builtin_model(name: str) -> str:
    builtin_model_dir = importlib.resources.files(__package__).joinpath('models')
    model_file = builtin_model_dir.joinpath(name + '.csv')
    return str(model_file)


def __parse_thickness_fwhm(value) -> Sequence[int]:
    try:
        return [int(x) for x in value.split(',')]
    except ValueError:
        logger.error(f'"{value}" is not a comma-separated list of numbers')
        sys.exit(1)


if __name__ == '__main__':
    main()
