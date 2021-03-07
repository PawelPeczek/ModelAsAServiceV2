FROM continuumio/miniconda

RUN apt-get update && apt-get install -y build-essential && \
    apt install -y python3 python3-dev python3-opencv
RUN python -m pip install jupyter
RUN mkdir /build
COPY ./requirements.txt build/requirements.txt
RUN conda create -n Playground python=3.9 -y && \
    . ~/.bashrc && \
    conda activate Playground && \
    python -m pip install -r build/requirements.txt && \
    python -m ipykernel install --name "Playground" --user &&\
    conda deactivate
RUN rm -r build
RUN mkdir /project
COPY . /project
WORKDIR project

RUN . ~/.bashrc && \
    conda activate Playground && \
    python -m playground.cache_weights

RUN mkdir /weights
RUN wget --no-check-certificate 'https://github.com/PawelPeczek/RetinaFaceNet/releases/download/v1.0/FaceNet_resnet_50.pth' \
    -O /weights/weights.pth

ENTRYPOINT ["jupyter", "notebook", "--allow-root"]