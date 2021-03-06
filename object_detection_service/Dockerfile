FROM python:3.9

RUN apt-get update && apt-get install -y build-essential && \
    apt-get install -y python3-dev python3-opencv

RUN mkdir /build

COPY ./requirements.txt build/requirements.txt
COPY ./cache_weights.py build/cache_weights.py
RUN python -m pip install -r build/requirements.txt
RUN python build/cache_weights.py
RUN rm -r build

RUN mkdir /project
COPY . /project
WORKDIR project

ENTRYPOINT ["python", "-m", "object_detection_service.app"]
