FROM docker.io/fnndsc/pl-innerspfit:base-1

LABEL org.opencontainers.image.authors="FNNDSC <Jennings.Zhang@childrens.harvard.edu>" \
      org.opencontainers.image.title="Inner Subplate Surface Fit" \
      org.opencontainers.image.description="Outer to inner surface mesh deformation using a radial distance map for human fetal MRI"

RUN \
    --mount=type=cache,target=/home/mambauser/.mamba/pkgs,uid=57439,gid=57439 \
    --mount=type=cache,target=/opt/conda/pkgs,uid=57439,gid=57439 \
    micromamba install -y -n base -c conda-forge python=3.11.5 pandas=2.1.1

ARG SRCDIR=/home/mambauser/pl-innerspfit
ARG MAMBA_DOCKERFILE_ACTIVATE=1
WORKDIR ${SRCDIR}

COPY --chown=57439:57439 requirements.txt .
RUN --mount=type=cache,uid=57439,gid=57439,target=/home/mambauser/.cache/pip \
    pip install -r requirements.txt

COPY --chown=mambauser:mambauser . .
ARG extras_require=none
RUN pip install ".[${extras_require}]" \
    && cd / && rm -rf ${SRCDIR}
WORKDIR /

CMD ["innerspfit"]
