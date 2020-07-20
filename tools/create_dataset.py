import argparse
import json
import os
import random


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path',
                        help='path to json and images files')
    parser.add_argument('output_path',
                        help='path to save dataset files')
    parser.add_argument('--split_type', choices=['image, class'],
                        help='stratified dataset split. Opts: '
                             'image: split annotations per image. '
                             'class: split annotations per class. '
                             'Default: image', default='image')
    parser.add_argument('--train', type=float,
                        help='percentage of images to train. '
                             'Default=0.7', default=0.7)
    parser.add_argument('--val', type=float, help='percentage of images to val. '
                                      'Default=0.15', default=0.15)
    parser.add_argument('--test', type=float, help='percentage of images to test. '
                                       'Default=0.15', default=0.15)

    args = parser.parse_args()
    return args


def set_categories(categories):
    categories = sorted(list(categories))
    cats = dict()
    for c in range(len(categories)):
        cats[categories[c]] = c + 1
    return cats


def get_dataset(input_path, json_files):
    images = list()
    annotations = list()
    categories = set()
    image_id = 0
    annotation_id = 0

    for json_file in json_files:
        file_path = os.path.join(input_path, json_file)
        with open(file_path, 'r') as jsn:
            data = json.load(jsn)

            shapes = data['shapes']
            for shape in shapes:
                points = shape['points']
                x = int(min(points[0][0], points[1][0]))
                y = int(min(points[0][1], points[1][1]))
                w = int(abs(points[1][0] - points[0][0]))
                h = int(abs(points[1][1] - points[0][1]))

                annotations.append({
                    'iscrowd': 0,
                    'image_id': image_id,
                    'bbox': [x, y, w, h],
                    'segmentation': [],
                    'category_id': shape['label'],
                    'id': annotation_id,
                    'area': w * h
                })
                annotation_id += 1
                categories.add(shape['label'])

            images.append({
                'height': data['imageHeight'],
                'width': data['imageWidth'],
                'id': image_id,
                'file_name': data['imagePath']
            })
            image_id += 1

    categories = set_categories(categories)
    for ann in annotations:
        ann['category_id'] = categories[ann['category_id']]

    cats = list()
    for cat in categories:
        cats.append({
            'supercategory': None,
            'id': categories[cat],
            'name': cat
        })

    dataset = {
        'images': images,
        'annotations': annotations,
        'categories': cats
    }
    return dataset


def get_valid_files(input_path):
    json_files = [f for f in os.listdir(input_path) if f.endswith('.json')]
    return json_files


def image_split(dataset, p_train, p_val):
    images = dataset['images']
    annotations = dataset['annotations']
    categories = dataset['categories']

    images = random.shuffle(images)
    n_images = len(images)
    n_train = int(n_images * p_train)
    n_val = int(n_images * p_val)

    train_images = images[:n_train]
    val_images = images[n_train:n_train+n_val]
    test_images = images[n_train+n_val:]

    train_dataset = list()
    val_dataset = list()
    test_dataset = list()

    for image in train_images:
        for annotation in annotations:
            if image['id'] == annotation['image_id']:
                train_annotations.append()



def class_split(dataset, p_train, p_val, p_test):
    pass


def show_infos():
    pass


def create_dataset(
        input_path,
        output_path,
        split_type,
        p_train=0.7,
        p_val=0.15,
        p_test=0.15
):
    json_files = get_valid_files(input_path)
    dataset = get_dataset(input_path, json_files)
    print(dataset)

    if split_type == 'image':
        image_split(dataset, p_train, p_val)
    else:
        class_split(dataset, p_train, p_val)

    show_infos()


def main():
    args = parse_args()

    create_dataset(
        args.input_path,
        args.output_path,
        args.split_type,
        args.train,
        args.val,
        args.test
    )


if __name__ == '__main__':
    main()
