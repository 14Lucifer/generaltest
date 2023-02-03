# syntax=docker/dockerfile:1
FROM python:3

# work dir
WORKDIR /app

# install app dependencies
RUN cd /app
RUN pip install flask==2.2.2;pip install psutil

# install app
COPY . /app

# port export
EXPOSE 5000

# process config
CMD flask --app general-testing.py run --host 0.0.0.0 --port 5000
