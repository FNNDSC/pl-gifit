# Inner Subplate Surface Fit

[![Version](https://img.shields.io/docker/v/fnndsc/pl-gifit?sort=semver)](https://hub.docker.com/r/fnndsc/pl-gifit)
[![MIT License](https://img.shields.io/github/license/fnndsc/pl-gifit)](https://github.com/FNNDSC/pl-gifit/blob/main/LICENSE)
[![ci](https://github.com/FNNDSC/pl-gifit/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/pl-gifit/actions/workflows/ci.yml)

`pl-gifit` is a [_ChRIS_](https://chrisproject.org/) _ds_ plugin which
performs mesh deformation. Different deformation parameters are used depending
on the gyrification index of the input surface. Similar to the CIVET function
`expand_from_white`, `pl-gifit` is a wrapper around `surface_fit`.

## Models

The primary goal of `pl-gifit` is to deform inwards mesh deformation from the outer
subplate surface to the inner subplate surface for _in-vivo_ human brain MRI.

A "model" for `pl-gifit` refers to a CSV file containing parameters for `surface_fit`.
A model CSV file optimized for inner subplate fitting is provided as the default.

One "schedule" of parameters is run per brain hemisphere. A "schedule" is one or more
runs of `surface_fit`. Sometimes, it is ideal to run `surface_fit` multiple times with
different paremeters. Each run with different parameters is called a "stage."
One row of a model CSV file corresponds to one "stage" of a "schedule."

## Usage

`pl-gifit` is a _[ChRIS](https://chrisproject.org/) plugin_, meaning it can
run from either within _ChRIS_ or the command-line.
