FROM python:3.13

RUN apt-get update
RUN apt-get install -y --no-install-recommends apt-utils curl
RUN pip install -U pip
RUN pip install --no-cache-dir autopep8 flake8 pytest

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf ./aws/
