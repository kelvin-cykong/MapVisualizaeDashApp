FROM python:3.11.5

## Install base utilities
#RUN apt-get update \
#    && apt-get install -y build-essential \
#    && apt-get install -y wget \
#    && apt-get clean \
#    && rm -rf /var/lib/apt/lists/*

## Install miniconda
#ENV CONDA_DIR /opt/conda
#RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
#    /bin/bash ~/miniconda.sh -b -p /opt/conda

## Put conda in path so we can use conda activate
#ENV PATH=$CONDA_DIR/bin:$PATH
WORKDIR /dash_app

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /dash_app/package_requirement.txt

CMD ["python","apps/index.py"]