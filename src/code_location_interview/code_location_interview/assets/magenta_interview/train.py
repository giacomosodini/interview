import logging
import sys

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score

from dagster import AssetOut, AssetIn, asset, get_dagster_logger, multi_asset, file_relative_path

# from dagstermill import define_dagstermill_asset

log_fmt = "[%(asctime)s] %(message)s"
log_datefmt = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(stream=sys.stdout, format=log_fmt, datefmt=log_datefmt, level=logging.INFO)
logger = get_dagster_logger(__name__)

# group_name = "training"


# @multi_asset(
#     group_name=group_name,
#     outs={
#         "train_data": AssetOut(
#             
#         ),
#         "test_data": AssetOut(
#             
#         ),
#     },
# )
# def split_train_test(df_input_preprocessed):
#
#     return train_data, test_data
# 
# 
# @asset(group_name=group_name)
# def classifier(train_data):
# 
#     return pipeline