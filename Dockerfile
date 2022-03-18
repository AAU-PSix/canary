FROM python:jessie

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends cmake manpages-dev gcc g++ && \
    rm -rf /var/lib/apt/lists/*

# Installation of all requirements is done
# by first copying the requirements for pip
# this is done to ensure a better caching.
COPY requirements.txt /src/
RUN python3 -m pip install -r /src/requirements.txt

# One that we have all the dependencies we
# then copy the entire app into /app/ in the container
COPY . .
# this command runs the "__main__.py"
ENTRYPOINT [ "python3", "/src/" ]