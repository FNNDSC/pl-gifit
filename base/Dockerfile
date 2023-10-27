FROM docker.io/fnndsc/microminc-builder:latest as builder

COPY surface_fit_script.pl /usr/local/bin/surface_fit_script.pl

RUN microminc.sh -p '&run' \
    gyrification_index \
    convex_hull \
    xfminvert \
    transform_objects \
    measure_surface_area \
    depth_potential \
    surface_fit_script.pl \
    surface_fit \
    volume_object_evaluate \
    vertstats_math \
        /microminc

# MNI data needs to be copied manually
RUN mkdir -vp /microminc/share/surface-extraction
RUN cp -v "$MNI_DATAPATH/surface-extraction/white_model_320.obj" /microminc/share/surface-extraction/white_model_320.obj

FROM ghcr.io/mamba-org/micromamba:1.5.1-bookworm-slim

USER root
RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean \
    && apt-get update \
    && apt-get -y --no-install-recommends install perl

COPY --from=builder /microminc /opt/microminc
ENV PATH=/opt/conda/bin:/opt/microminc/bin:$PATH \
    LD_LIBRARY_PATH=/opt/microminc/lib:$LD_LIBRARY_PATH \
    MINC_FORCE_V2=1 MINC_COMPRESS=4 VOLUME_CACHE_THRESHOLD=-1 \
    MNI_DATAPATH=/opt/microminc/share \
    PERL5LIB=/opt/microminc/perl

USER mambauser
