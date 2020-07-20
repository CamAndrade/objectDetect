import argparse
import json
import pickle
import os


def parse_args():
    parser = argparse.ArgumentParser(
        description='Transform pkl file results in txt')
    parser.add_argument('pkl_results', help='pkl results')
    parser.add_argument('pkl_filenames', help='pkl filenames')
    parser.add_argument('json_file', help='json test file')
    parser.add_argument('out', help='path to save txt file')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    if not os.path.exists(args.out):
        os.makedirs(args.out)

    with open(args.pkl_results, 'rb') as r, \
            open(args.pkl_filenames, 'rb') as f, \
            open(args.json_file, 'r') as j:

        results = pickle.load(r)
        filenames = pickle.load(f)
        json_file = json.load(j)

        # create labels dict
        labels = list()
        for label in json_file['categories']:
            labels.append(label['name'])
        labels = dict(enumerate(sorted(labels)))

        # create txt file to each test image
        assert len(results) == len(filenames)

        for i in range(len(results)):
            image_name = filenames[i][:-3]
            txt_path = os.path.join(args.out, image_name + 'txt')

            classes = results[i][:len(labels)]  # only used labels

            with open(txt_path, 'w') as txt:
                for res in range(len(classes)):
                    for det in classes[res]:
                        label = labels[res]
                        xmin = str(det[0])
                        ymin = str(det[1])
                        xmax = str(det[2])
                        ymax = str(det[3])
                        score = str(det[4])

                        line = label + ' ' + xmin + ' ' + ymin + ' ' + xmax + ' ' + ymax + ' ' + score + '\n'
                        txt.write(line)


if __name__ == '__main__':
    main()
