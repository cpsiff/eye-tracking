# Eye Tracking

Code for running a user study for CS770 HCI Fall 2022.

`python run_trial.py` to run a user study. You'll want to change the `TEXTS` and `STYLES` global variables at the top of the script between each run, in order to change the matching of texts to styles, and the order of presentation

## Installation
Here is how I installed everything:

1. Install [Tobii Pro Eye Tracker Manager](https://connect.tobii.com/s/etm-downloads?language=en_US)
2. Create a new conda environment: `conda create -n eye-tracking python=3.8.13`
3. Install TobiiPro SDK for Python: `pip install tobii_research` ([official guide](https://developer.tobiipro.com/python/python-getting-started.html))
4. `pip install pyyaml matplotlib`
5. Before running `run_trial.py`, plug in the eye tracker, run the Tobii Pro Eye Tracker Manager, install the eye tracker if needed, an perform calibration

## Documentation
[Official getting started guide for SDK](https://developer.tobiipro.com/python/python-getting-started.html)
