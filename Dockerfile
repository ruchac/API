FROM python:3.7
#EXPOSE 8000
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install -U celery[redis]
ADD . /code/
#ENTRYPOINT ["/bin/bash", "entrypoint.sh" ]
