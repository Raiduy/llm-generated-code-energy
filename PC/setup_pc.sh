!#/bin/bash

sudo apt-get install -y python3-venv
sudo apt-get install -y python3-pip
mkdir experiments
cd ./experiments/

git clone git@github.com:Raiduy/experiment-runner.git

python3 -m venv ./experiment-runner/.venv
source ./experiment-runner/.venv/bin/activate
pip install -r ./experiment-runner/requirements.txt


git clone git@github.com:Raiduy/llm-generated-code-energy.git

deactivate

git clone git@github.com:tdurieux/EnergiBridge.git
cd EnergiBridge

sudo apt-get install -y curl
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

source ~/.bashrc

cargo build -r

sudo cp ./target/release/energibridge /usr/bin/
sudo setcap cap_sys_rawio=ep /usr/bin/energibridge

sudo addgroup msr
sudo chgrp -R msr /dev/cpu/*/msr
sudo chmod g+r /dev/cpu/*/msr

energibridge -h

