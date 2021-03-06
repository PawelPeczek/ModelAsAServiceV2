FROM python:3.9

RUN apt-get update && apt-get install -y build-essential && \
    apt-get install -y python3-dev python3-opencv

RUN mkdir /build
RUN mkdir /project

COPY ./requirements.txt build/requirements.txt
RUN python -m pip install -r build/requirements.txt
RUN rm -r build

RUN mkdir /weights
RUN wget --no-check-certificate 'https://github.com/PawelPeczek/RetinaFaceNet/releases/download/v1.0/weights' \
    -O /weights/weights.pth

COPY ./face_detection_service /project/face_detection_service
WORKDIR project

ENTRYPOINT ["python", "-m", "face_detection_service.app"]