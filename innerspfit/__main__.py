#!/usr/bin/env python
import itertools
import os
import subprocess as sp
import sys
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional

from chris_plugin import chris_plugin, PathMapper
from loguru import logger

from innerspfit import __version__, DISPLAY_TITLE
from innerspfit.model import Model


parser = ArgumentParser(description='surface_fit wrapper',
                        formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('--no-fail', dest='no_fail', action='store_true',
                    help='Produce exit code 0 even if any subprocesses do not.')
parser.add_argument('-V', '--version', action='version',
                    version=f'%(prog)s {__version__}')
parser.add_argument('-t', '--threads', type=int, default=0,
                    help='Number of threads to use for parallel jobs. '
                         'Pass 0 to use number of visible CPUs.')


@chris_plugin(
    parser=parser,
    title='Inner subplate surface mesh deformation',
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

    model = Model()
    mapper = PathMapper.file_mapper(inputdir, outputdir, glob='**/*.mnc', suffix='.obj')
    with ThreadPoolExecutor(max_workers=nproc) as pool:
        results = pool.map(lambda t, p: run_surface_fit(*t, p), mapper, itertools.repeat(model))

    if not options.no_fail and not all(results):
        sys.exit(1)


def run_surface_fit(grid: Path, output_surf: Path, model: Model) -> bool:
    """
    :return: True if successful
    """
    starting_surface = locate_surface_for(grid)
    if starting_surface is None:
        logger.error('No starting surface found for {}', grid)
        return False

    # TODO measure GI here
    gi = ...

    params = (p.to_cliargs() for p in model.get_params_for(gi))
    cli_args = [arg for row in params for arg in row]

    extra_args = [
        '-disterr', output_surf.with_suffix('.disterr.txt'),
        '-disterr-abs', output_surf.with_suffix('.disterr.abs.txt')
    ]

    cmd = ['surface_fit_script.pl', *cli_args, *extra_args, grid, starting_surface, output_surf]
    log_file = output_surf.with_name(output_surf.name + '.log')
    logger.info('Starting: {}', ' '.join(map(str, cmd)))
    # with log_file.open('wb') as log_handle:
    #     job = sp.run(cmd, stdout=log_handle, stderr=log_handle)
    # rc_file = log_file.with_suffix('.rc')
    # rc_file.write_text(str(job.returncode))
    #
    # if job.returncode == 0:
    #     logger.info('Finished: {} -> {}', starting_surface, output_surf)
    #     return True
    #
    # logger.error('FAILED -- check log file for details: {}', log_file)
    # return False


def locate_surface_for(mask: Path) -> Optional[Path]:
    glob = mask.parent.glob('*.obj')
    first = next(glob, None)
    second = next(glob, None)
    if second is not None:
        return None
    return first


if __name__ == '__main__':
    main()
