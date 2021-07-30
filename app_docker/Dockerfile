FROM frolvlad/alpine-miniconda3

# Python packages from conda
RUN conda install --yes --freeze-installed \
     nomkl \
     pip \
     aiohttp \
     simplejson \
     numpy \
     pandas \
     bokeh \
     netCDF4 \
     psycopg2

RUN conda install -c conda-forge pycrypto\
    scikit-learn \
    scikit-image \
    matplotlib \
    gunicorn \
    aioredis

ADD ./python /code/python
WORKDIR /code/python


RUN apk add bash

RUN conda install scipy