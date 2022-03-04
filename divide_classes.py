import os

source_path = "/home/isuzu/Desktop/berat_asrin/RGBs"
data = "/subject3/"
data_path = source_path + data

closed_eye_yawning_path = data_path + "/closed_eye_yawning/"
closed_eye_no_yawning_path = data_path + "/closed_eye_no_yawning/"

open_eye_yawning_path = data_path + "/open_eye_yawning/"
open_eye_no_yawning_path = data_path + "/open_eye_no_yawning/"

only_yawn_path = data_path + "/only_yawn/"
only_no_yawn_path = data_path + "/only_no_yawn_path/"

only_open_eye_path = data_path + "/only_open_eye_path/"
only_closed_eye_path = data_path + "/only_closed_eye_path/"

new_folders = [closed_eye_no_yawning_path,closed_eye_yawning_path,open_eye_no_yawning_path,open_eye_yawning_path, only_yawn_path,
only_no_yawn_path, only_open_eye_path, only_closed_eye_path]

for folder in new_folders:
    if not os.path.exists(folder):
            os.makedirs(folder)

files =  os.listdir(data_path)
files = list(filter(lambda x: '.txt' in x, files))

for file in files:
    open_eye = None
    yawn = None
    file_to_read = open(data_path + file)
    file_content = file_to_read.readlines()
    file_to_read.close()

    for label_class in file_content:
        label_class = int(label_class.split()[0])
        if label_class == 0:
            open_eye = False
        elif label_class == 1:
            open_eye = True
        elif label_class == 2:
            yawn = False
        elif label_class == 3:
            yawn = True

    for file_type in [".txt", ".jpg"]:
        if not open_eye == None and not yawn == None: 
            if open_eye and yawn:
                os.rename(data_path + file.split(".")[0] + file_type, open_eye_yawning_path + file.split(".")[0] + file_type)

            elif not open_eye and yawn:
                os.rename(data_path + file.split(".")[0] + file_type, closed_eye_yawning_path + file.split(".")[0] + file_type)

            elif open_eye and not yawn:
                os.rename(data_path + file.split(".")[0] + file_type, open_eye_no_yawning_path + file.split(".")[0] + file_type)

            elif not open_eye and not yawn:
                os.rename(data_path + file.split(".")[0] + file_type, closed_eye_no_yawning_path + file.split(".")[0] + file_type)
        elif open_eye == None and yawn:
            os.rename(data_path + file.split(".")[0] + file_type, only_yawn_path + file.split(".")[0] + file_type)
        elif open_eye == None and not yawn:
            os.rename(data_path + file.split(".")[0] + file_type, only_no_yawn_path + file.split(".")[0] + file_type)
        elif open_eye and yawn == None:
            os.rename(data_path + file.split(".")[0] + file_type, only_open_eye_path + file.split(".")[0] + file_type)
        elif not open_eye and yawn == None:
            os.rename(data_path + file.split(".")[0] + file_type, only_closed_eye_path + file.split(".")[0] + file_type) 