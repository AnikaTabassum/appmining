import tarfile
import urllib

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# uci_tcga_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00401/"
# archive_name = "TCGA-PANCAN-HiSeq-801x20531.tar.gz"

# # Build the url
# full_download_url = urllib.parse.urljoin(uci_tcga_url, archive_name)

# # Download the file
# r = urllib.request.urlretrieve (full_download_url, archive_name)

# # Extract the data from the archive
# tar = tarfile.open(archive_name, "r:gz")
# tar.extractall()
# tar.close()

datafile = "TCGA-PANCAN-HiSeq-801x20531/data.csv"
labels_file = "TCGA-PANCAN-HiSeq-801x20531/labels.csv"

data = np.genfromtxt(
    datafile,
    delimiter=",",
    usecols=range(1, 20532),
    skip_header=1
)

true_label_names = np.genfromtxt(
    labels_file,
    delimiter=",",
    usecols=(1,),
    skip_header=1,
    dtype="str"
)

print(data[:5, :3])

print(true_label_names[:5])

label_encoder = LabelEncoder()
true_labels = label_encoder.fit_transform(true_label_names)

print(true_labels[:5])
print(label_encoder.classes_)
n_clusters = len(label_encoder.classes_)