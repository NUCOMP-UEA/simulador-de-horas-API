FROM python:3.10

ENV PYTHONPATH=/app

COPY . /app

WORKDIR /app

RUN pip install .

CMD [ "python3", "-m", "add_hours.main" ]