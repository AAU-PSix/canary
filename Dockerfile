FROM python:jessie

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends cmake manpages-dev gcc g++ && \
    rm -rf /var/lib/apt/lists/*

#RUN wget https://github.com/Kitware/CMake/releases/download/v3.21.0/cmake-3.21.0-Linux-x86_64.sh \
#      -q -O /tmp/cmake-install.sh \
#      && chmod u+x /tmp/cmake-install.sh \
#      && mkdir /usr/bin/cmake \
#      && /tmp/cmake-install.sh --skip-license --prefix=/usr/bin/cmake \
#      && rm /tmp/cmake-install.sh

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