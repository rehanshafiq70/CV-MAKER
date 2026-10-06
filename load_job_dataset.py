"""
CareerAI - Dataset Loader Script: Kaggle Job Description Dataset
Helper script to load Kaggle Job Description Dataset for matching experiments.
"""
import os
import pandas as pd
from typing import Optional

JOB_DATASET_PATH = "data/job_descriptions/job_descriptions.csv"

def load_job_dataset(path: str = JOB_DATASET_PATH) -> Optional[pd.DataFrame]:
    """Loads Kaggle Job Description dataset if available."""
    if not os.path.exists(path):
        print(f"Dataset file not found at '{path}'.")
        print("Please download the Kaggle Job Description Dataset from https://www.kaggle.com/datasets/ravindrasinghrana/job-description-dataset")
        print("and place the dataset CSV inside 'data/job_descriptions/'.")
        return None

    try:
        df = pd.read_csv(path)
        print(f"Successfully loaded {len(df)} job descriptions from '{path}'.")
        print("Columns available:", list(df.columns))
        return df
    except Exception as e:
        print(f"Error loading job description dataset: {e}")
        return None

if __name__ == "__main__":
    df = load_job_dataset()
    if df is not None:
        print(df.head(2))
