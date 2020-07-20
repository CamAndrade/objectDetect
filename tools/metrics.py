import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams.update({'font.size': 22})

file_path = 'camila.txt'
names = ['AP',
         'AP IoU=.50',
         'AP IoU=.75',
         'AP small',
         'AP medium',
         'AP large',
         'AR max=1',
         'AR max=10',
         'AR max=100',
         'AR small',
         'AR medium',
         'AR large'
         ]

data = list()
with open(file_path, 'r') as w:
    lines = w.readlines()
    for line in lines:
        data.append(
            list(map(float, line.replace('\n', '').split()))
        )

treino1 = pd.DataFrame(data[:50], columns=names)
treino2 = pd.DataFrame(data[50:100], columns=names)
treino3 = pd.DataFrame(data[100:150], columns=names)
treino4 = pd.DataFrame(data[150:], columns=names)

fig, axes = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True)
linestyles_tuple = ['-', '-', '-', '-', '-', '-',
                    '--', '--', '--', '--', '--', '--']


treino1.plot(ax=axes[0, 0], legend=None, style=linestyles_tuple)
axes[0, 0].set_title('Resnet50 - Pretrained')
axes[0, 0].set_ylabel("Metric")
treino2.plot(ax=axes[0, 1], legend=None, style=linestyles_tuple)
axes[0, 1].set_title('Resnet101 - Pretrained')
treino3.plot(ax=axes[1, 0], legend=None, style=linestyles_tuple)
axes[1, 0].set_title('Resnet50 - No Pretrained')
axes[1, 0].set_ylabel("Metric")
axes[1, 0].set_xlabel("Epoch")
treino4.plot(ax=axes[1, 1], legend=None, style=linestyles_tuple)
axes[1, 1].set_title('Resnet101 - No Pretrained')
axes[1, 1].set_xlabel("Epoch")

fig.legend(names, loc='center right')
plt.xlabel("Epoch")
plt.ylabel("Coco Metric")

plt.show()
