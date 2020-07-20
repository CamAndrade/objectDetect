import argparse
import json
import numpy as np
import os


import matplotlib.pyplot as plt
from sklearn.metrics import plot_confusion_matrix


def arg_parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('ground_truth', help='ground_truth file')
    parser.add_argument('detections', help='detection path')
    parser.add_argument('threshold', type=float, default=0.7)
    args = parser.parse_args()
    return args

def nms(boxes, threshold):
    # https://www.pyimagesearch.com/2015/02/16/faster-non-maximum-suppression-python/

    classes = dict()
    for box in boxes:
        if box[0] not in classes.keys():
            classes[box[0]] = []
        classes[box[0]].append(box)

    for classe in classes.keys():

        if len(boxes) == 0:
            return []

        pick = []
        boxes2 = np.array([b[1:5] for b in classes[classe]])

        x1 = boxes2[:, 0]
        y1 = boxes2[:, 1]
        x2 = boxes2[:, 2]
        y2 = boxes2[:, 3]

        area = (x2 - x1 + 1) * (y2 - y1 + 1)
        idxs = np.argsort(y2)

        while len(idxs) > 0:
            last = len(idxs) - 1
            i = idxs[last]
            pick.append(i)

            xx1 = np.maximum(x1[i], x1[idxs[:last]])
            yy1 = np.maximum(y1[i], y1[idxs[:last]])
            xx2 = np.maximum(x2[i], x2[idxs[:last]])
            yy2 = np.maximum(y2[i], y2[idxs[:last]])

            w = np.maximum(0, xx2 - xx1 + 1)
            h = np.maximum(0, yy2 - yy1 + 1)

            overlap = (w * h) / area[idxs[:last]]

            idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > threshold)[0])))
        classes[classe] = [classes[classe][pick[p]] for p in range(len(pick))]

    last_bboxes = list()
    for key, value in classes.items():
        last_bboxes.append(value)

    return [l[0] for l in last_bboxes]


def calculateIoU(bbox1, bbox2):
    # https://www.pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/#:~:text=The%20Intersection%20over%20Union%20can,area%20would%20be%20doubly%20counted).

    # print(len(bbox1), len(bbox2))
    if len(bbox1) != 0 and len(bbox2) != 0:
        # get x, y coordinates
        x_bbox1 = max(bbox1[0], bbox2[0])
        y_bbox1 = max(bbox1[1], bbox2[1])
        x_bbox2 = min(bbox1[2], bbox2[2])
        y_bbox2 = min(bbox1[3], bbox2[3])

        # compute intersection area
        intersection = max(0, x_bbox2 - x_bbox1 + 1) * max(0, y_bbox2 - y_bbox1 + 1)

        # compute bbox areas
        area_bbox1 = (bbox1[2] - bbox1[0] + 1) * (bbox1[3] - bbox1[1] + 1)
        area_bbox2 = (bbox2[2] - bbox2[0] + 1) * (bbox2[3] - bbox2[1] + 1)

        # compute intersection over union
        iou = intersection / float(area_bbox1 + area_bbox2 - intersection)
        return iou


def load_gts(json_file):
    ground_truths = dict()
    for ann in json_file['annotations']:
        image_id = ann['image_id']
        if image_id not in ground_truths.keys():
            ground_truths[image_id] = list()

        x, y, w, h = ann['bbox']
        bbox = [x, y, x + w, y + h]

        ground_truths[image_id].append({
            'label': ann['category_id'],
            'bbox': bbox
        })
    return ground_truths


def load_dts(path):
    detections = dict()
    images = os.listdir(path)

    for image in images:
        image_path = os.path.join(path, image)
        dets = list()
        with open(image_path, 'r') as f:
            line = f.readline()
            while line:
                line = line.replace('\n', '').split()
                label = line[0]
                xmin = float(line[1])
                ymin = float(line[2])
                xmax = float(line[3])
                ymax = float(line[4])
                score = float(line[5])
                dets.append((label, xmin, ymin, xmax, ymax, score))
                line = f.readline()
        detections[image] = dets
    return detections


def load_img_ids(json_file):
    images = dict()
    for image in json_file['images']:
        image_name = image['file_name']
        image_id = image['id']
        # images[image_name] = image_id
        images[image_id] = image_name
    return images


def load_labels(json_file):
    labels = dict()
    for label in json_file['categories']:
        label_id = label['id']
        label_name = label['name']
        # labels[label_id] = label_name
        labels[label_name] = label_id - 1
    return labels


def create_confusion_matrix(ground_truths, detections, image_ids, labels, threshold):
    n_labels = len(labels)
    confusion_matrix = np.zeros((n_labels, n_labels))

    ids_dts = []
    ids_gts = []

    for image in ground_truths.keys():
        image_name = image_ids[image][:-3] + 'txt'
        # dets = nms(detections[image_name], threshold)
        dets = detections[image_name]
        for ground_truth in ground_truths[image]:
            label_id_ground_truth = ground_truth['label'] - 1
            for det in dets:
                iou = calculateIoU(ground_truth['bbox'], det[1:5])
                # print(iou)
                if iou:
                    if iou >= threshold:
                        label_id_detection = labels[det[0]]
                        ids_dts.append(label_id_detection)
                        ids_gts.append(label_id_ground_truth)
                        confusion_matrix[label_id_ground_truth][label_id_detection] += 1
    print(confusion_matrix)

def load_json(path):
    with open(path, 'r') as j:
        json_file = json.load(j)
        return json_file


def main():
    args = arg_parse()

    json_file = load_json(args.ground_truth)
    ground_truths = load_gts(json_file)
    detections = load_dts(args.detections)
    image_ids = load_img_ids(json_file)
    labels = load_labels(json_file)
    create_confusion_matrix(ground_truths, detections, image_ids, labels, args.threshold)

if __name__ == '__main__':
    main()
