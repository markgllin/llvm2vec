# llvm2vec

This is an extension of the `asm2vec` model (official paper [here](https://ieeexplore.ieee.org/document/8835340)) and builds upon the unofficial `asm2vec` Python implementation by [Lancern](https://github.com/Lancern/asm2vec) to add support for LLVM IR.

# Requirements
## Docker
Installation with Docker is preferred + easiest:
```
# build the docker image
docker build . -t llvm2vec

# start docker image with interactive shell
docker run -it -v $PWD:/home llvm2vec /bin/bash
```
*assumes you are currently in the root directory of the repo.

## Without Docker
Install the following
- Python3
- libgraphviz-dev

afterwards, install the following Python dependencies:
```
# --install-option(s) may differ depending on system
pip3 install pygraphviz --install-option="--include-path=/usr/include/graphviz" --install-option="--library-path=/usr/lib/x86_64-linux-gnu/graphviz" 
pip3 install llvmlite networkx numpy sklearn seaborn matplotlib

# dl code + required submodules
git clone https://github.com/markgllin/llvm2vec.git
cd llvm2vec
git submodule init

# add asm2vec to python path
export PYTHONPATH=$PWD/asm2vec:$PYTHONPATH

# run the code
python3 main.py
```

# Usage
```
python3 main.py
python3 -m tensorboard.main --logdir=/home/projections/ --bind_all
```

# To Do
Lots of things:
- ~~improve TSNE plotting (i.e. add labels/colors etc.)~~
- database to persist vectorized functions
- ~~determining function similarity via cosine similarity~~
- proper pipeline for disassembling in LLVM IR w/ retdec and passing into llvm2vec (probably in a new repo)

Nice to haves:
- install python dependencies the proper way
- use venv(?)
- gui