FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    libgl1 \
    libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY /app /app

RUN groupadd -r noroot && \
    useradd -r -s /bin/false -g noroot -d /home/noroot noroot && \
    mkdir -p /home/noroot && \
    chown -R noroot:noroot /home/noroot /app
USER noroot

CMD ["gunicorn", "--config", "/app/gunicorn.conf.py", "rest_server:app"]
