FROM python:alpine

ENV FLASK_APP blog.py
ENV FLASK_CONFIG docker
ENV PRODUCTION 1

# RUN adduser -D blog
# USER blog

WORKDIR /home/blog

COPY requirements.txt requirements
# RUN python -m venv venv
RUN pip install SQLAlchemy
RUN pip install -r requirements

COPY app app
COPY blog.py blog.py
COPY boot.sh boot.sh
COPY Devlog.md Devlog.md 

EXPOSE 5000 
# ENTRYPOINT [ "./boot.sh" ]
CMD [ "gunicorn", "-b", "0.0.0.0:5000", "blog:blog" ]