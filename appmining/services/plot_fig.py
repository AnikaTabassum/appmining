# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
class plot_fig(object):
	def __init__(self, *args, **kwargs):
		print("initiating service plot")
	def plot(self,topicNo, newScore):
		# import data
		# topicNo=str(9)
		filename="D:\\8th_semester\\my_8th_semester\\SPL3\\appmining\\final\\final_topic_"+str(topicNo)+"_IDF_healthy.csv"
		data = pd.read_csv(filename)
		# input data
		df = data[["Serial", "Scores"]]
		# scatterplot of inputs data
		plt.scatter(df["Serial"], df["Scores"])
		plt.scatter(len(df["Serial"])+1,[newScore])
		plt.xlabel('App no.')
		plt.ylabel('Anomaly Score')
		plt.title('Anomaly score of topic '+str(topicNo))

		plt.savefig('appmining/static/images/my_plot.png')
		# plt.show()