"""
Carter Sifferman 2022

Main program for running a user experiment where gaze data is measured.
Displays a random image when the space bar is pressed, image goes away when
the space bar is pressed again. Duration of image display, image itself, and
gaze data are recorded.

Developed with a tobiipro eye tracker and Ubuntu 22
"""

import os
import sys
import time

import yaml
import matplotlib.pyplot as plt
import matplotlib.image as img
import tobii_research as tr
import webbrowser

SAVE_DIR = "results"
IMG_DIR = "images"
TEXTS, STYLES = ["example", "text_3", "text_2", "text_1"], ["control", "control", "bionic", "random"]
FORM_URLS = {
    "example": "https://forms.gle/a57tyhBs5FDuEXvTA",
    "text_1": "https://forms.gle/xaPmFvsGbrSXu9LL8",
    "text_2": "https://forms.gle/dyAK6pxbSD8n7XSr8",
    "text_3": "https://forms.gle/5sAcm81AzVe8LERb8",
    "end": "https://forms.gle/fvUgpH35AiUYtern9"
}

state = "blank"
start_time = 0
end_time = 0
my_eyetracker = tr.find_all_eyetrackers()[0]
all_gaze_data = []

def save_trial(dir, start_time, end_time, image_path, all_gaze_data):
    curtime = time.strftime("%Y%m%d-%H%M%S")
    results = {
        "time": curtime,
        "start_time": start_time,
        "end_time": end_time,
        "duration": end_time-start_time,
        "image_path": image_path
    }
    os.makedirs(dir)
    with open(os.path.join(dir, "trial.yaml"), 'w+') as file:
        yaml.dump(results, file)

    with open(os.path.join(dir, "gaze.txt"), 'w+') as file:
        for datapoint in all_gaze_data:
            file.write(f"{str(datapoint)}\n")

def display_img(img_path):
    """Display a given image on the screen, and record gaze data, start time, and end time
    """

    fig, ax = plt.subplots()
    image = img.imread(img_path)
    ax.axis('off')
    fig.subplots_adjust(
        top=1.0,
        bottom=0.0,
        left=0.0,
        right=1.0
    )

    # http://stackoverflow.com/questions/32428193/ddg#32428266
    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())

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
                my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA)
                plt.close()
                end_time = time.time()

    fig.canvas.mpl_connect('key_press_event', on_press)

    plt.show()


def main():
    global all_gaze_data
    global start_time
    global end_time
    global state

    timestamp_save_dir = os.path.join(SAVE_DIR, time.strftime("%Y%m%d-%H%M%S"))
    for text, style, i in zip(TEXTS, STYLES, range(len(TEXTS))):
        img_path = os.path.join(IMG_DIR, text, f"{style}.png")

        display_img(img_path)

        trial_save_dir = os.path.join(timestamp_save_dir, f"{i}_{text}_{style}")
        save_trial(trial_save_dir, start_time, end_time, img_path, all_gaze_data)
        
        # reset the globals
        all_gaze_data = []
        start_time = 0
        end_time = 0
        state = "blank"
        
        # open appropriate google form in browser
        print("opening google form")
        webbrowser.open_new(FORM_URLS[text])

        # wait for input in terminal to continue to display next window
        if i != len(TEXTS)-1:
            input("Press enter to continue")
        else:
            webbrowser.open_new(FORM_URLS["end"])


if __name__ == '__main__':
    main()