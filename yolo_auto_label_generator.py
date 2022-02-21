import cv2 as cv
import numpy as np
from PIL import Image, ImageOps
import os

def padding(img, expected_size):
    desired_size = expected_size
    delta_width = desired_size - img.size[0]
    delta_height = desired_size - img.size[1]
    pad_width = delta_width // 2
    pad_height = delta_height // 2
    padding = (pad_width, pad_height, delta_width - pad_width, delta_height - pad_height)
    return ImageOps.expand(img, padding)

def resize_with_padding(img, expected_size):
    img.thumbnail((expected_size[0], expected_size[1]))
    delta_width = expected_size[0] - img.size[0]
    delta_height = expected_size[1] - img.size[1]
    pad_width = delta_width // 2
    pad_height = delta_height // 2
    padding = (pad_width, pad_height, delta_width - pad_width, delta_height - pad_height)
    return ImageOps.expand(img, padding)

path = "/home/isuzu/Desktop/berat_asrin/RGBs/test/subject8"
images = os.listdir(path)
images = list(filter(lambda x: '.jpg' in x, images))
counter = 0
for image in images:
    counter = counter + 1
    img_location_and_name = path + "/" + image
    cfg_location = "cfg/yolov4-tiny-object-detection.cfg"
    weight_location = "weights/yolov4_drowsiness_last.weights"

    # Resize image to achieve same aspect ratio
    img = Image.open(img_location_and_name)
    width, height = img.size

    if(width <= 416 or height <= 416):
        img = cv.imread(img_location_and_name)
        img = cv.resize(img, (416,416))
        img = cv.imwrite(img_location_and_name, img)

    else:        
        img = resize_with_padding(img, (800, 800))
        img = img.save(img_location_and_name)

    img = cv.imread(img_location_and_name)

    img_width = img.shape[0]
    img_height = img.shape[1]

    img_blob = cv.dnn.blobFromImage(img, 1/255, (416,416), swapRB=True, crop=False)

    labels = ["closed_eye",
	"open_eye",
	"not_yawning_mouth",
	"yawning_mouth"]

    colors = ["0,255,0", "0,0,255", "0,0,255", "255,0,255", "255,255,0"]
    colors = [np.array(color.split(",")).astype("int") for color in colors]
    colors = np.array(colors)
    colors = np.tile(colors, (18, 1))

    model = cv.dnn.readNetFromDarknet(cfg_location, weight_location)
    layers = model.getLayerNames()
    output_layer = [layers[layer[0]-1] for layer in model.getUnconnectedOutLayers()]

    model.setInput(img_blob)

    detection_layer = model.forward(output_layer)

    ids_list = []
    boxes_list = []
    confidences_list = []

    for detection in detection_layer:
        for object_detection in detection:

            scores = object_detection[5:] 
            predicted_id = np.argmax(scores)
            confidence = scores[predicted_id]

            label = labels[predicted_id]
            bounding_box = object_detection[0:4] * np.array([img_width, img_height, img_width, img_height])
            (box_center_x, box_center_y, box_width, box_height) = bounding_box.astype("int")
        
            start_x = int(box_center_x - (box_width/2))
            start_y = int(box_center_y - (box_height/2))
        
            ids_list.append(predicted_id)
            confidences_list.append(float(confidence))
            boxes_list.append([start_x, start_y, int(box_width), int(box_height)])

    max_ids = cv.dnn.NMSBoxes(boxes_list, confidences_list, 0.5, 0.4)

    for max_id in max_ids:
    	
        max_class_id = max_id[0]
        box = boxes_list[max_class_id]

        start_x = box[0]
        start_y = box[1]
        box_width = box[2]
        box_height = box[3]    

        predicted_id = ids_list[max_class_id]
        label = labels[predicted_id]
        confidence = confidences_list[max_class_id]

        end_x = start_x + box_width
        end_y = start_y + box_height

        #box_color = colors[predicted_id]
        #box_color = [int(each) for each in box_color]

        label = "{} :{:.1f}%".format(label, confidence*100)
    
        center_x_normalized = ((start_x + end_x)/2)/img_width
        center_y_normalized = (start_y + end_y)/2/img_height
        box_width_normalized = box_width/img_width
        box_height_normalized = box_height/img_height

        to_write = str(predicted_id) + " " + str(center_x_normalized) + " " + str(center_y_normalized) + " " + str(box_width_normalized) + " " + str(box_height_normalized) + "\n"
        file = open(path + "/" + image.split(".")[0] + ".txt", "a")
        file.write(to_write)
        file.close()
        print(str(counter) + "/" + str(len(images)))
        #cv.rectangle(img, (start_x, start_y), (end_x, end_y), box_color, 1)
        #cv.putText(img, label, (start_x, start_y-10), cv.FONT_HERSHEY_PLAIN, 1, box_color, 1)
"""
    cv.imshow("Detection Frame", img)

    cv.waitKey(0)
    cv.destroyAllWindows()
"""
