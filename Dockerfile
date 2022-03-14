FROM python:jessie

# Installation of all requirements is done
# by first copying the requirements for pip
# this is done to ensure a better caching.
COPY requirements.txt /tmp/
RUN python3 -m pip install -r /tmp/requirements.txt

# One that we have all the dependencies we
# then copy the entire app into /app/ in the container
COPY . /app/
# this command runs the "__main__.py"
ENTRYPOINT [ "python3", "/app/src/" ]