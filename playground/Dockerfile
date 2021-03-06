FROM continuumio/miniconda

RUN apt-get update && apt-get install -y build-essential && \
    apt install -y python3 python3-dev python3-opencv
RUN python -m pip install jupyter
RUN mkdir /build
COPY ./requirements* build
RUN conda create -n KerasRetinaNet python=3.7 -y && \
    . ~/.bashrc && \
    conda activate KerasRetinaNet && \
    python -m pip install -r build/requirements-retinanet.txt && \
    python -m ipykernel install --name "KerasRetinaNet" --user &&\
    conda deactivate

