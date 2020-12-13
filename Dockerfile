#docker run -it -v $PWD:/home <img_name> /bin/bash

FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH=/home/asm2vec
RUN apt-get update && \
    apt install python3.8 python3-pip libgraphviz-dev -y
RUN pip3 install pygraphviz --install-option="--include-path=/usr/include/graphviz" --install-option="--library-path=/usr/lib/x86_64-linux-gnu/graphviz" 
RUN pip3 install llvmlite networkx numpy sklearn seaborn matplotlib
