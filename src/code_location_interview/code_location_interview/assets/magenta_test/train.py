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

from dagstermill import define_dagstermill_asset

log_fmt = "[%(asctime)s] %(message)s"
log_datefmt = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(stream=sys.stdout, format=log_fmt, datefmt=log_datefmt, level=logging.INFO)
logger = get_dagster_logger(__name__)

group_name = "churn_smartphone_training"


@multi_asset(
    group_name=group_name,
    outs={
        "train_data": AssetOut(
            io_manager_key="bigquery_io_manager",
        ),
        "test_data": AssetOut(
            io_manager_key="bigquery_io_manager",
        ),
    },
)
def split_train_test(df_input_preprocessed):
    X = df_input_preprocessed.copy()
    train_data, test_data = train_test_split(X, test_size=0.2, random_state=42, stratify=X["has_churned"])

    return train_data, test_data


@asset(group_name=group_name, io_manager_key="gcs_pickle_io_manager")
def classifier(train_data):
    # Dynamically select columns to impute
    columns_to_impute = [col for col in train_data.columns if col.startswith("n_case") or col.startswith("days_since_last_case")]

    # Define imputation for numeric columns
    imputer = SimpleImputer(strategy="constant", fill_value=0)

    # One-hot encoding for categorical columns
    categorical_transformer = OneHotEncoder(handle_unknown="ignore")

    # ColumnTransformer: numeric imputation + categorical processing
    preprocessor = ColumnTransformer(
        transformers=[
            ("num_imputer", imputer, columns_to_impute),
            (
                "one_hot_encoder",
                categorical_transformer,
                ["smartphone_brand"],
            ),
        ],
        remainder="passthrough",
        verbose_feature_names_out=False,
    )

    # Model parameters
    quick_param_space = {
        "max_depth": 5,
        "scale_pos_weight": 10,
        "eval_metric": "auc",
    }

    # Define the complete pipeline
    pipeline = Pipeline(
        [
            ("preprocessing", preprocessor),
            ("classifier", XGBClassifier(**quick_param_space)),
        ]
    )

    # Separate target variable
    y_train = train_data.pop("has_churned")
    train_data = train_data.set_index("rating_account_id")

    # Train the pipeline
    pipeline.fit(train_data, y_train)

    return pipeline


@asset(
    group_name=group_name,
    io_manager_key="bigquery_io_manager",
)
def evaluation_metrics(classifier, test_data):
    y_test = test_data.pop("has_churned")
    test_data = test_data.set_index("rating_account_id")

    # Predicted labels
    y_pred = classifier.predict(test_data)
    # Predicted probabilities
    y_prob = classifier.predict_proba(test_data)[:, 1]

    # Metrics calculation
    metrics = {
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "F1-Score": f1_score(y_test, y_pred),
        "ROC-AUC": roc_auc_score(y_test, y_prob),
    }

    metrics_df = pd.DataFrame([metrics])

    # TODO: assign a run_id to the metrics

    return metrics_df


exploration_notebook = define_dagstermill_asset(
    name="exploration_nb",
    notebook_path=file_relative_path(__file__, "../../../notebooks/explore.ipynb"),
    group_name=group_name,
    ins={
        "df": AssetIn("df_input_preprocessed", input_manager_key="bigquery_io_manager")
    },  # the first is the name of the object in the jupyther nb
)
