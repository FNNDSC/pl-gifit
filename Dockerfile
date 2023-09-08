# Python version can be changed, e.g.
# FROM python:3.8
# FROM docker.io/fnndsc/conda:python3.10.2-cuda11.6.0
FROM docker.io/python:3.11.3-slim-bullseye

LABEL org.opencontainers.image.authors="FNNDSC <Jennings.Zhang@childrens.harvard.edu>" \
      org.opencontainers.image.title="Inner Subplate Surface Fit" \
      org.opencontainers.image.description="Outer to inner surface mesh deformation using a radial distance map for human fetal MRI"

ARG SRCDIR=/usr/local/src/pl-inner-subplate-surface-fit
WORKDIR ${SRCDIR}

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ARG extras_require=none
RUN pip install ".[${extras_require}]" \
    && cd / && rm -rf ${SRCDIR}
WORKDIR /

CMD ["innerspfit"]
