# deepracer-rc
Repository for remote controlling your Deep Racer with a PS4 controller. Created by [ARCC](arcc.ai).

## Dependencies
1. This repo has been developed on and tested on Ubuntu 18.04 with python 3.7
2. Ensure you have python downloaded and the AWS DeepRacer running on your network

## Setup 
1. Start by installing and setting up conda
2. Create a conda env with the command `conda env create -f environmrent.yaml`. That should load all of the proper dependencies for running league core.
3. Activate conda env with with `conda activate league_env` 

## Getting Started
In order to run to use the joystick, plug the USB into the computer and run `python joystick_mode.py`

## Controls
PS4 Button Map: 
L2 = reverse
R2 = accelearate
L = steering
Triangle = stop program
