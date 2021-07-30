FROM python:3.9.5-slim-buster

WORKDIR .
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN pip install virtualenv \
    flask[async] \
    matplotlib \
    pandas

EXPOSE 5000
COPY . .
CMD ["flask", "run"]

