#!/bin/bash

CONDA_PATH=/opt/conda/

source ${CONDA_PATH}/etc/profile.d/conda.sh

conda activate /home/george/.conda/envs/timeregister    

python3 /home/george/git/TimeRegister/gui.py