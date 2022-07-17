FROM python:alpine

ENV FLASK_APP blog.py
ENV FLASK_CONFIG docker
ENV PRODUCTION 1

RUN adduser -D blog
USER blog

WORKDIR /home/blog

COPY requirements.txt requirements
# RUN python -m venv venv
RUN pip install -r requirements

COPY app app
COPY blog.py blog.py
COPY boot.sh boot.sh


EXPOSE 5000 
ENTRYPOINT [ "./boot.sh" ]