
# The given code extracts all the frames for the entire dataset and saves these frames in the folder of the video clips.
# Kindly have ffmpeg (https://www.ffmpeg.org/) (all credits) in order to successfully execute this script.
# The script must in the a same directory as the Dataset Folder.
import os
import subprocess
import yaml


def split_video(video_file, image_name_prefix, destination_path):
    return subprocess.check_output('ffmpeg -i "' + destination_path + video_file + '" ' +
                                   image_name_prefix + '%d.jpg -hide_banner', shell=True, cwd=destination_path)


if __name__ == "__main__":
    data_root = yaml.safe_load(open("data/config.yml"))["data_root"]
    data_path = os.path.join(data_root, 'DataSet/')
    dataset = os.listdir(data_path)

    for ttv in dataset:
        users = os.listdir(data_path + ttv + '/')
        for user in users:
            currUser = os.listdir(data_path + ttv + '/' + user + '/')
            for extract in currUser:
                if len(os.listdir(data_path + ttv + '/' + user + '/' + extract + '/')) != 1:
                    continue
                clip = os.listdir(data_path + ttv + '/' + user + '/' + extract + '/')[0]
                path = data_path + ttv + '/' + user + '/' + extract + '/'
                if not os.path.isfile(path):
                    split_video(clip, clip[:-4], path)

    print("================================================================================\n")
    print("Frame Extraction Successful")
