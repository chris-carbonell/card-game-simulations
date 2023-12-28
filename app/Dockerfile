# Overview
# build image for card game simulations

FROM quay.io/jupyter/base-notebook:latest

# install dependencies
USER root
RUN apt-get update \
    && apt-get install -y libpq-dev gcc

# set up working dir
USER jovyan
WORKDIR /home/jovyan/work

# install requirements
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# run app
COPY ./game .
COPY ./constants.py .
COPY ./simulations.py .
CMD ["python", "simulations.py"]