FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt install python3.8 python3-pip libgraphviz-dev -y
RUN pip3 install llvmlite networkx numpy
RUN pip3 install pygraphviz --install-option="--include-path=/usr/include/graphviz" --install-option="--library-path=/usr/lib/x86_64-linux-gnu/graphviz" 
