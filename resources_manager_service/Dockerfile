FROM python:3.9

RUN mkdir /build
RUN mkdir /project

COPY ./requirements.txt build/requirements.txt
RUN python -m pip install -r build/requirements.txt
RUN rm -r build

COPY . /project
WORKDIR project

ENTRYPOINT ["python", "-m", "resources_manager_service.app"]