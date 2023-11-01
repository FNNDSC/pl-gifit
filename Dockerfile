FROM docker.io/fnndsc/pl-gifit:base-2

LABEL org.opencontainers.image.authors="FNNDSC <Jennings.Zhang@childrens.harvard.edu>" \
      org.opencontainers.image.title="pl-gifit" \
      org.opencontainers.image.description="A ChRIS plugin for surface mesh deformation using different parameters depending on gyrification index"

RUN \
    --mount=type=cache,sharing=private,target=/home/mambauser/.mamba/pkgs,uid=57439,gid=57439 \
    --mount=type=cache,sharing=private,target=/opt/conda/pkgs,uid=57439,gid=57439 \
    micromamba install -y -n base -c conda-forge python=3.11.5 pandas=2.1.1

ARG SRCDIR=/home/mambauser/pl-gifit
ARG MAMBA_DOCKERFILE_ACTIVATE=1
WORKDIR ${SRCDIR}

COPY --chown=57439:57439 requirements.txt .
RUN --mount=type=cache,sharing=private,target=/home/mambauser/.cache/pip,uid=57439,gid=57439 \
    pip install -r requirements.txt

COPY --chown=mambauser:mambauser . .
ARG extras_require=none
RUN pip install ".[${extras_require}]" \
    && cd / && rm -rf ${SRCDIR}
WORKDIR /

CMD ["innerspfit"]
