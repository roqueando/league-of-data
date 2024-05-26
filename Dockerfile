FROM python:3.12-slim

WORKDIR /pipe

COPY ./pipe /pipe
COPY ./requirements.txt /pipe/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "-m"]
