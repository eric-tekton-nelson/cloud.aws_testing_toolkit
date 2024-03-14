#!/bin/bash

git clone https://github.com/pyenv/pyenv.git ~/.pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
. ~/.bashrc
sudo apt install zlib1g zlib1g-dev
sudo apt-get install liblzma-dev
sudo apt-get install libbz2-dev
sudo apt-get install mysql-client
pyenv install 3.12.2
pyenv global 3.12.2
pip install boto3
