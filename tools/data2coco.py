import json
import os


import cv2


file_train = '/home/Documentos/doutorado/experimentos/drive-download-20200719T020903Z-001/pictor_ppe_crowdsourced_approach-01_train.txt'
file_val = '/home/Documentos/doutorado/experimentos/drive-download-20200719T020903Z-001/pictor_ppe_crowdsourced_approach-01_valid.txt'
file_test = '/home/Documentos/doutorado/experimentos/drive-download-20200719T020903Z-001/pictor_ppe_crowdsourced_approach-01_test.txt'
images_path = '/home/Documentos/doutorado/experimentos/Images'

with open(file_train, 'r') as f_train, open(file_val, 'r') as f_val, open(file_test, 'r') as f_test:

    images = list()
    annotations = list()
    image_id = 0
    annotation_id = 0

    categories = [
        {'id': 1, 'name': 'capacete', 'supercategory': None},
        {'id': 2, 'name': 'colete', 'supercategory': None},
        {'id': 3, 'name': 'trabalhador', 'supercategory': None}
    ]

    line = f_train.readline()
    while line:
        line = line.replace('\n', '').split('	')
        file_name = line[0]
        bboxes = line[1:]

        image = cv2.imread(os.path.join(images_path, file_name))
        height, width, _ = image.shape

        images.append({
            'id': image_id,
            'file_name': file_name,
            'height': height,
            'width': width
        })

        for bbox in bboxes:
            bbox = bbox.split(',')
            xmin = int(bbox[0])
            ymin = int(bbox[1])
            xmax = int(bbox[2])
            ymax = int(bbox[3])
            category_id = int(bbox[4]) + 1
            bbox = [xmin, ymin, abs(xmax-xmin), abs(ymax-ymin)]
            area = abs(xmax-xmin) * abs(ymax-ymin)


            annotations.append({
                'id': annotation_id,
                'image_id': image_id,
                'category_id': category_id,
                'bbox': bbox,
                'area': area,
                'iscrowd': 0,
                'segmentation': []
            })
            annotation_id += 1
        image_id += 1
        line = f_train.readline()

    json_train = {
        'images': images,
        'annotations': annotations,
        'categories': categories
    }
    with open('/home/Documentos/doutorado/experimentos/train.json', 'w') as dump_train:
        json.dump(json_train, dump_train)

    images = list()
    annotations = list()

    line = f_val.readline()
    while line:
        line = line.replace('\n', '').split('	')
        file_name = line[0]
        bboxes = line[1:]

        image = cv2.imread(os.path.join(images_path, file_name))
        height, width, _ = image.shape

        images.append({
            'id': image_id,
            'file_name': file_name,
            'height': height,
            'width': width
        })

        for bbox in bboxes:
            bbox = bbox.split(',')
            xmin = int(bbox[0])
            ymin = int(bbox[1])
            xmax = int(bbox[2])
            ymax = int(bbox[3])
            category_id = int(bbox[4]) + 1
            bbox = [xmin, ymin, abs(xmax-xmin), abs(ymax-ymin)]
            area = abs(xmax-xmin) * abs(ymax-ymin)


            annotations.append({
                'id': annotation_id,
                'image_id': image_id,
                'category_id': category_id,
                'bbox': bbox,
                'area': area,
                'iscrowd': 0,
                'segmentation': []
            })
            annotation_id += 1
        image_id += 1
        line = f_val.readline()

    json_val = {
        'images': images,
        'annotations': annotations,
        'categories': categories
    }
    with open('/home/Documentos/doutorado/experimentos/val.json', 'w') as dump_val:
        json.dump(json_val, dump_val)

    images = list()
    annotations = list()

    line = f_test.readline()
    while line:
        line = line.replace('\n', '').split('	')
        file_name = line[0]
        bboxes = line[1:]

        image = cv2.imread(os.path.join(images_path, file_name))
        height, width, _ = image.shape

        images.append({
            'id': image_id,
            'file_name': file_name,
            'height': height,
            'width': width
        })

        for bbox in bboxes:
            bbox = bbox.split(',')
            xmin = int(bbox[0])
            ymin = int(bbox[1])
            xmax = int(bbox[2])
            ymax = int(bbox[3])
            category_id = int(bbox[4]) + 1
            bbox = [xmin, ymin, abs(xmax-xmin), abs(ymax-ymin)]
            area = abs(xmax-xmin) * abs(ymax-ymin)


            annotations.append({
                'id': annotation_id,
                'image_id': image_id,
                'category_id': category_id,
                'bbox': bbox,
                'area': area,
                'iscrowd': 0,
                'segmentation': []
            })
            annotation_id += 1
        image_id += 1
        line = f_test.readline()

    json_test = {
        'images': images,
        'annotations': annotations,
        'categories': categories
    }
    with open('/home/Documentos/doutorado/experimentos/test.json', 'w') as dump_test:
        json.dump(json_test, dump_test)
