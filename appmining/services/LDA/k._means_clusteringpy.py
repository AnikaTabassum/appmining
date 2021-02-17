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

datafile = "output_file_with_topics_without_doc.csv"
# labels_file = "TCGA-PANCAN-HiSeq-801x20531/labels.csv"
# data=pd.read_csv(datafile)
data = np.genfromtxt(
    datafile,
    delimiter=",",
    usecols=range(0,6),
    skip_header=1
)

other_file="names.csv"
true_label_names = np.genfromtxt(
    other_file,
    delimiter=",",
    usecols=(0,),
    skip_header=1,
    dtype="str"
)

# print(data)
# true_label_names=["topic_0","topic_1","topic_2","topic_3","topic_4","topic_5"]
print(len(true_label_names))
# for names in true_label_names:
#   print("names ", true_label_names)

label_encoder = LabelEncoder()
true_labels = label_encoder.fit_transform(true_label_names)

# print(len(true_labels))
# print(true_labels)
# print(label_encoder.classes_)
n_clusters = len(label_encoder.classes_)


# n_cluster koyta nibo bujhtesina.... N-cluster should be number of unique classes
# n_clusters=6
#Principal Component Analysis (PCA)
print("n_clusters ", n_clusters)
preprocessor = Pipeline(
    [
        ("scaler", MinMaxScaler()),
        ("pca", PCA(n_components=5, random_state=42)),
    ]
)
# #Build the k-means clustering pipeline with user-defined arguments in the KMeans constructor:
clusterer = Pipeline(
   [
       (
           "kmeans",
           KMeans(
               n_clusters=6,
               init="k-means++",
               n_init=50,
               max_iter=5000,
               random_state=42,
           ),
       ),
   ]
)

print("clusterer ", (clusterer))

# #The Pipeline class can be chained to form a larger pipeline. Build an end-to-end k-means clustering pipeline by passing the "preprocessor" and "clusterer" pipelines to Pipeline:
pipe = Pipeline(
    [
        ("preprocessor", preprocessor),
        ("clusterer", clusterer)
    ]
)
# #Calling .fit() with data as the argument performs all the pipeline steps on the data:


print(pipe.fit(data))


# #Evaluate the performance by calculating the silhouette coefficient:
preprocessed_data = pipe["preprocessor"].transform(data)
predicted_labels = pipe["clusterer"]["kmeans"].labels_
print("Resulting App Clusters", predicted_labels, pipe["clusterer"]["kmeans"])
print("silhouette_score",silhouette_score(preprocessed_data, predicted_labels))

# #Calculate ARI, too, since the ground truth cluster labels are available:

# print(adjusted_rand_score(true_labels, predicted_labels))

# #Plot the results using a pandas DataFrame and the seaborn plotting library:

pcadf = pd.DataFrame(
    pipe["preprocessor"].transform(data),
    columns=["component_1", "component_2","component_3", "component_4","component_5"],
)

pcadf["predicted_cluster"] = pipe["clusterer"]["kmeans"].labels_
# pcadf["true_label"] = label_encoder.inverse_transform(
#   )

plt.style.use("fivethirtyeight")
plt.figure(figsize=(8, 8))

scat = sns.scatterplot(
    "component_1",
    "component_2",
    "component_3",
    "component_4",
    "component_5",
    s=50,
    data=pcadf,
    hue="predicted_cluster",
    style="true_label",
    palette="Set2",
)

scat.set_title(
    "APPMINING"
)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)

plt.show()


# #Iterate over a range of n_components and record evaluation metrics for each iteration:

# # Empty lists to hold evaluation metrics
silhouette_scores = []
# ari_scores = []
for n in range(2, 6):
    # This set the number of components for pca,
    # but leaves other steps unchanged
    pipe["preprocessor"]["pca"].n_components = n
    pipe.fit(data)

    silhouette_coef = silhouette_score(
        pipe["preprocessor"].transform(data),
        pipe["clusterer"]["kmeans"].labels_,
    )
    # ari = adjusted_rand_score(
    #     true_labels,
    #     pipe["clusterer"]["kmeans"].labels_,
    # )

#     # Add metrics to their lists
    silhouette_scores.append(silhouette_coef)
    # ari_scores.append(ari)

# #Plot the evaluation metrics as a function of n_components to visualize the relationship between adding components and the performance of the k-means clustering results:
plt.style.use("fivethirtyeight")
plt.figure(figsize=(6, 6))
plt.plot(
    range(2, 6),
    silhouette_scores,
    c="#008fd5",
    label="Silhouette Coefficient",
)
# plt.plot(range(2, n_clusters), ari_scores, c="#fc4f30", label="ARI")

plt.xlabel("n_components")
plt.legend()
plt.title("Clustering Performance as a Function of n_components")
plt.tight_layout()
plt.show()