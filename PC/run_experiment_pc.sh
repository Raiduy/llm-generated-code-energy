!#/bin/bash

# USE run_experiment_pc.sh <experiment> <pc_id>

cd ./experiment/llm-generated-code-energy

git checkout main
git restore .
git fetch
git pull

source ../experiment-runner/.venv/bin/activate
cd PC

git branch results-$1-$2 && git checkout results-$1-$2

python3 ../../experiment-runner/experiment-runner/ ./RunnerConfig.py

cd ../
git add .
git commit -m "Experiment finished."

git push

