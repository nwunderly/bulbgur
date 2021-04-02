FROM python:3.8-slim

# give it it's own fancy directory
RUN mkdir /bulbgur
WORKDIR /bulbgur

# install requirements first because cache
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# data/ directory is ignored
COPY . .

# use "main" or "static" as argument when running
ENTRYPOINT ["/bin/bash", "./run_server.sh"]
