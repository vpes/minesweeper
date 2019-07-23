FROM ubuntu:19.04
ENV PYTHONUNBUFFERED 1

MAINTAINER "Victor Pesquin <vpesquin@acm.org>"

# Create workdir
RUN mkdir -p /app
WORKDIR /app

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
	git \
	python3 \
	python3-dev \
	python3-setuptools \
	python3-pip \
	nginx \
	supervisor \
	sqlite3 && \
	pip3 install -U pip setuptools && \
    rm -rf /var/lib/apt/lists/*

# Copy app files
COPY requirements.txt /

# Install dependencies
RUN pip install -r requirements.txt

# Copy project code
COPY . /app

# Open ports and run command
EXPOSE 80
CMD ["gunicorn", "--chdir", "/app", "config.wsgi:application", "--bind", ":80", "--workers", "3"]