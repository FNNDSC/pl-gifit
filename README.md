# Inner Subplate Surface Fit

[![Version](https://img.shields.io/docker/v/fnndsc/pl-inner-subplate-surface-fit?sort=semver)](https://hub.docker.com/r/fnndsc/pl-inner-subplate-surface-fit)
[![MIT License](https://img.shields.io/github/license/fnndsc/pl-inner-subplate-surface-fit)](https://github.com/FNNDSC/pl-inner-subplate-surface-fit/blob/main/LICENSE)
[![ci](https://github.com/FNNDSC/pl-inner-subplate-surface-fit/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/pl-inner-subplate-surface-fit/actions/workflows/ci.yml)

`pl-inner-subplate-surface-fit` is a [_ChRIS_](https://chrisproject.org/)
_ds_ plugin which takes in ...  as input files and
creates ... as output files.

## Abstract

...

## Installation

`pl-inner-subplate-surface-fit` is a _[ChRIS](https://chrisproject.org/) plugin_, meaning it can
run from either within _ChRIS_ or the command-line.

[![Get it from chrisstore.co](https://raw.githubusercontent.com/FNNDSC/ChRIS_store_ui/963938c241636e4c3dc4753ee1327f56cb82d8b5/src/assets/public/badges/light.svg)](https://chrisstore.co/plugin/pl-inner-subplate-surface-fit)

## Local Usage

To get started with local command-line usage, use [Apptainer](https://apptainer.org/)
(a.k.a. Singularity) to run `pl-inner-subplate-surface-fit` as a container:

```shell
apptainer exec docker://fnndsc/pl-inner-subplate-surface-fit innerspfit [--args values...] input/ output/
```

To print its available options, run:

```shell
apptainer exec docker://fnndsc/pl-inner-subplate-surface-fit innerspfit --help
```

## Examples

`innerspfit` requires two positional arguments: a directory containing
input data, and a directory where to create output data.
First, create the input directory and move input data into it.

```shell
mkdir incoming/ outgoing/
mv some.dat other.dat incoming/
apptainer exec docker://fnndsc/pl-inner-subplate-surface-fit:latest innerspfit [--args] incoming/ outgoing/
```

## Development

Instructions for developers.

### Building

Build a local container image:

```shell
docker build -t localhost/fnndsc/pl-inner-subplate-surface-fit .
```

### Running

Mount the source code `innerspfit.py` into a container to try out changes without rebuild.

```shell
docker run --rm -it --userns=host -u $(id -u):$(id -g) \
    -v $PWD/__main__.py:/usr/local/lib/python3.11/site-packages/__main__.py:ro \
    -v $PWD/in:/incoming:ro -v $PWD/out:/outgoing:rw -w /outgoing \
    localhost/fnndsc/pl-inner-subplate-surface-fit innerspfit /incoming /outgoing
```

### Testing

Run unit tests using `pytest`.
It's recommended to rebuild the image to ensure that sources are up-to-date.
Use the option `--build-arg extras_require=dev` to install extra dependencies for testing.

```shell
docker build -t localhost/fnndsc/pl-inner-subplate-surface-fit:dev --build-arg extras_require=dev .
docker run --rm -it localhost/fnndsc/pl-inner-subplate-surface-fit:dev pytest
```

## Release

Steps for release can be automated by [Github Actions](.github/workflows/ci.yml).
This section is about how to do those steps manually.

### Increase Version Number

Increase the version number in `setup.py` and commit this file.

### Push Container Image

Build and push an image tagged by the version. For example, for version `1.2.3`:

```
docker build -t docker.io/fnndsc/pl-inner-subplate-surface-fit:1.2.3 .
docker push docker.io/fnndsc/pl-inner-subplate-surface-fit:1.2.3
```

### Get JSON Representation

Run [`chris_plugin_info`](https://github.com/FNNDSC/chris_plugin#usage)
to produce a JSON description of this plugin, which can be uploaded to a _ChRIS Store_.

```shell
docker run --rm localhost/fnndsc/pl-inner-subplate-surface-fit:dev chris_plugin_info > chris_plugin_info.json
```

