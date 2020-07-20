import argparse
import json
import os

import cv2


def arg_parse():
    parser = argparse.ArgumentParser()

    parser.add_argument('path', help='path to search images')
    parser.add_argument('gt', help='path to json gts')
    parser.add_argument('dts', help='path to txt file with detections')
    parser.add_argument('out', help='path to save results')
    parser.add_argument('threshold', help='Default 0.7', type=float, default=0.7)
    args = parser.parse_args()
    return args


def load_img_ids(json_file):
    images = dict()
    for image in json_file['images']:
        image_name = image['file_name']
        image_id = image['id']
        images[image_name] = image_id
    return images


def load_dts(path):
    detections = dict()
    images = os.listdir(path)

    for img in images:
        img_path = os.path.join(path, img)
        dets = list()
        with open(img_path, 'r') as f:
            line = f.readline()
            while line:
                line = line.replace('\n', '').split()
                label = line[0]
                xmin = float(line[1])
                ymin = float(line[2])
                xmax = float(line[3])
                ymax = float(line[4])
                score = round(float(line[5]), 2)
                dets.append((label, xmin, ymin, xmax, ymax, score))

                line = f.readline()

        detections[img] = dets
    return detections


def load_gts(json_file):
    ground_truths = dict()  # {image_id: [annotations]}
    for ann in json_file['annotations']:
        image_id = ann['image_id']
        if image_id not in ground_truths.keys():
            ground_truths[image_id] = list()
        ground_truths[image_id].append({
            'label': ann['category_id'],
            'bbox': ann['bbox']
        })

    return ground_truths


def load_labels(json_file):
    labels = dict()
    for label in json_file['categories']:
        label_id = label['id']
        label_name = label['name']
        labels[label_id] = label_name
    return labels


def draw_gts_dts(path, img_ids, ground_truths, detections, labels, out, threshold):
    for key in img_ids.keys():

        img_path = os.path.join(path, key)
        print(img_path)
        img_gts = cv2.imread(img_path, cv2.IMREAD_COLOR)
        img_dts = cv2.imread(img_path, cv2.IMREAD_COLOR)

        color = {
            1: (255, 0, 0),
            2: (0, 255, 0),
            3: (0, 0, 255)
        }

        # draw ground truths
        img_id = img_ids[key]
        gts = ground_truths[img_id]
        for gt in gts:
            label = gt['label']
            bbox = gt['bbox']
            p1 = (bbox[0], bbox[1])
            p2 = (bbox[0] + bbox[2], bbox[1] + bbox[3])
            text = labels[label]
            #color = (255, 0, 0)

            cv2.rectangle(img_gts, p1, p2, color[label], thickness=2)
            cv2.putText(img_gts, text, p1, cv2.FONT_HERSHEY_PLAIN, 2, color[label], thickness=2)

        # draw detections
        color_label = {
            'capacete': (255, 0, 0),
            'colete': (0, 255, 0),
            'trabalhador': (0, 0, 255)
        }
        txt_key = key[:-3] + 'txt'
        dts = detections[txt_key]
        for dt in dts:
            label = dt[0]
            p1 = (int(dt[1]), int(dt[2]))
            p2 = (int(dt[3]), int(dt[4]))
            score = float(dt[5])
            if score >= threshold:
                text = label + ' ' + str(score)
                #color = (0, 0, 255)

                cv2.rectangle(img_dts, p1, p2, color_label[label], thickness=2)
                cv2.putText(img_dts, text, p1, cv2.FONT_HERSHEY_PLAIN, 2, color_label[label], thickness=2)

        # cv2.imshow(img_path, img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        filename = os.path.join(out, 'gts ' + key)
        cv2.imwrite(filename, img_gts)
        filename = os.path.join(out, 'dts ' + key)
        cv2.imwrite(filename, img_dts)


def draw_gts(path, img_ids, ground_truths, labels, out):
    for key in img_ids.keys():

        img_path = os.path.join(path, key)
        print(img_path)
        img_gts = cv2.imread(img_path, cv2.IMREAD_COLOR)

        color = {
            1: (255, 0, 0),
            2: (0, 255, 0),
            3: (0, 0, 255)
        }

        # draw ground truths
        img_id = img_ids[key]
        gts = ground_truths[img_id]
        for gt in gts:
            label = gt['label']
            bbox = gt['bbox']
            p1 = (bbox[0], bbox[1])
            p2 = (bbox[0] + bbox[2], bbox[1] + bbox[3])
            text = labels[label]
            #color = (255, 0, 0)

            cv2.rectangle(img_gts, p1, p2, color[label], thickness=2)
            cv2.putText(img_gts, text, p1, cv2.FONT_HERSHEY_PLAIN, 2, color[label], thickness=2)

        filename = os.path.join(out, 'gts ' + key)
        cv2.imwrite(filename, img_gts)


def draw_dts(path, img_ids, detections, labels, out, threshold):
    for key in img_ids.keys():

        img_path = os.path.join(path, key)
        print(img_path)
        img_dts = cv2.imread(img_path, cv2.IMREAD_COLOR)

        # draw detections
        color_label = {
            'capacete': (255, 0, 0),
            'colete': (0, 255, 0),
            'trabalhador': (0, 0, 255)
        }
        txt_key = key[:-3] + 'txt'
        dts = detections[txt_key]
        for dt in dts:
            label = dt[0]
            p1 = (int(dt[1]), int(dt[2]))
            p2 = (int(dt[3]), int(dt[4]))
            score = float(dt[5])
            if score >= threshold:
                text = label + ' ' + str(score)
                #color = (0, 0, 255)

                cv2.rectangle(img_dts, p1, p2, color_label[label], thickness=2)
                cv2.putText(img_dts, text, p1, cv2.FONT_HERSHEY_PLAIN, 2, color_label[label], thickness=2)

        # cv2.imshow(img_path, img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        filename = os.path.join(out, 'dts ' + key)
        cv2.imwrite(filename, img_dts)


def load_json(path):
    with open(path, 'r') as j:
        json_file = json.load(j)
        return json_file


def main():
    args = arg_parse()

    if not os.path.exists(args.out):
        os.makedirs(args.out)

    json_file = load_json(args.gt)
    img_ids = load_img_ids(json_file)
    ground_truths = load_gts(json_file)
    labels = load_labels(json_file)
    detections = load_dts(args.dts)

    #draw_gts(args.path, img_ids, ground_truths, labels, args.out)
    draw_dts(args.path, img_ids, detections, labels, args.out, args.threshold)


if __name__ == '__main__':
    main()
