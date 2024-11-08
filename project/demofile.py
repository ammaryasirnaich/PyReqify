import pandas
import numpy
# import keras
import sklearn
from sklearn import datasets
# from keras.models import Sequential
# from keras.layers import Dense
# from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
# from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt


print(sklearn.__version__)


# if __name__ == "__main__":
#     import pkg_resources

#     # List of modules to check
#     modules = [
#         "pandas",
#         "numpy",
#         "keras",
#         "sklearn",
#         "matplotlib"
#     ]

#     # Get and print versions
#     for module in modules:
#         try:
#             version = pkg_resources.get_distribution(module).version
#             print(f"{module}: {version}")
#         except pkg_resources.DistributionNotFound:
#             print(f"{module}: Not installed")


