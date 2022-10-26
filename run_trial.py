"""
Carter Sifferman 2022

Main program for running a user experiment where gaze data is measured.
Displays a random image when the space bar is pressed, image goes away when
the space bar is pressed again. Duration of image display, image itself, and
gaze data are recorded.

Developed with a tobiipro eye tracker and Ubuntu 22
"""

import os
import random
import sys
import time
import datetime

import yaml
import matplotlib.pyplot as plt
import matplotlib.image as img
import tobii_research as tr

IMG_DIR = "images"
SAVE_DIR = "results"

state = "blank"
start_time = 0
end_time = 0
my_eyetracker = tr.find_all_eyetrackers()[0]
all_gaze_data = []

def save_trial(start_time, end_time, image_path, all_gaze_data):
    curtime = datetime.datetime.now().isoformat()
    results = {
        "time": curtime,
        "start_time": start_time,
        "end_time": end_time,
        "duration": end_time-start_time,
        "image_path": image_path
    }
    savedir = os.path.join(SAVE_DIR, curtime)
    os.mkdir(savedir)
    with open(os.path.join(savedir, "trial.yaml"), 'w+') as file:
        yaml.dump(results, file)

    with open(os.path.join(savedir, "gaze.txt"), 'w+') as file:
        for datapoint in all_gaze_data:
            file.write(f"{str(datapoint)}\n")

def main():
    fig, ax = plt.subplots()
    image_path = os.path.join(IMG_DIR, random.choice(os.listdir(IMG_DIR)))
    image = img.imread(image_path)
    ax.axis('off')
    fig.subplots_adjust(
        top=1.0,
        bottom=0.0,
        left=0.0,
        right=1.0
    )

    # http://stackoverflow.com/questions/32428193/ddg#32428266
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()

    def gaze_data_callback(gaze_data):
        global all_gaze_data
        all_gaze_data.append(gaze_data)

    def on_press(event):
        global state
        global start_time
        global end_time
        global my_eyetracker
        sys.stdout.flush()
        if event.key == " ":
            if state == "blank":
                ax.imshow(image)
                fig.canvas.draw()
                state = "shown"
                start_time = time.time()
                my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
            elif state == "shown":
                plt.close()
                end_time = time.time()

    fig.canvas.mpl_connect('key_press_event', on_press)

    plt.show()

    save_trial(start_time, end_time, image_path, all_gaze_data)


if __name__ == '__main__':
    main()