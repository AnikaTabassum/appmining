# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors

# import data
data = pd.read_csv("D:\\8th_semester\\my_8th_semester\\SPL3\\appmining\\final\\topic_2_IDF.csv")
# input data
df = data[["Serial", "Scores"]]
# scatterplot of inputs data
plt.scatter(df["Serial"], df["Scores"])
plt.show()
# new_df=df["Contribution"].copy()
# create arrays
X = df.values
# instantiate model
nbrs = NearestNeighbors(n_neighbors = 5)
# fit model
nbrs.fit(X)
# distances and indexes of k-neaighbors from model outputs
distances, indexes = nbrs.kneighbors(X)
print("distances" , distances)
# plot mean of k-distances of each observation
plt.plot(distances.mean(axis =1))
plt.show()
nintythPerc=np.percentile(distances, 90)
print(nintythPerc)
# visually determine cutoff values > 0.9
outlier_index = np.where(distances.mean(axis = 1) > nintythPerc)
print("outlier_index",outlier_index)
# filter outlier values
outlier_values = df.iloc[outlier_index]
print("outlier_values",outlier_values)


new_df= df.sort_values(by=['Serial'], ascending=False)
print("new_df", new_df)
plt.scatter(new_df["Serial"], new_df["Scores"])
plt.gca().invert_xaxis()
plt.show()
# new_new_df=new_df["Contribution"].copy()
# create arrays
X = new_df.values
# instantiate model
nbrs = NearestNeighbors(n_neighbors = 5)
# fit model
nbrs.fit(X)
# distances and indexes of k-neaighbors from model outputs
distances, indexes = nbrs.kneighbors(X)
print("distances" , distances)
# plot mean of k-distances of each observation
plt.plot(distances.mean(axis =1))
plt.show()
tenthPerc=np.percentile(distances, 10)
print("tenthPerc",tenthPerc)
# visually determine cutoff values > 0.9
outlier_index = np.where(distances.mean(axis = 1) < tenthPerc)
print("outlier_index",outlier_index)
# filter outlier values
outlier_values = new_df.iloc[outlier_index]
print("outlier_values",outlier_values)