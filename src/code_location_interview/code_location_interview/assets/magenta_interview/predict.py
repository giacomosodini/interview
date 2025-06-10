import logging
import sys
from datetime import datetime
import pandas as pd

from dagster import asset, get_dagster_logger


log_fmt = "[%(asctime)s] %(message)s"
log_datefmt = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(stream=sys.stdout, format=log_fmt, datefmt=log_datefmt, level=logging.INFO)
logger = get_dagster_logger(__name__)

group_name = "churn_smartphone_predict"


@asset(
    group_name=group_name,
    
)
def predictions(classifier, df_input_preprocessed):
    # Not really convenient to reset index every time
    # df_input_preprocessed = df_input_preprocessed.set_index("rating_account_id")
    y_pred = classifier.predict_proba(df_input_preprocessed)[:, 1]

    predictions_df = pd.DataFrame()
    predictions_df["rating_account_id"] = df_input_preprocessed.index
    predictions_df["churn_risk"] = y_pred
    predictions_df["run_dt"] = datetime.now()

    return predictions_df
