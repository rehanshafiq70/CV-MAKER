"""
CareerAI - Dataset Loader Script: Kaggle Resume Dataset
Helper script to load and parse Kaggle Resume Dataset (Resume.csv) for benchmarking.
"""
import os
import pandas as pd
from typing import Optional

RESUME_DATASET_PATH = "data/resumes/Resume.csv"

def load_resume_dataset(path: str = RESUME_DATASET_PATH) -> Optional[pd.DataFrame]:
    """Loads Kaggle Resume dataset if available."""
    if not os.path.exists(path):
        print(f"Dataset file not found at '{path}'.")
        print("Please download the Kaggle Resume Dataset from https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset")
        print("and place 'Resume.csv' in the 'data/resumes/' directory.")
        return None

    try:
        df = pd.read_csv(path)
        print(f"Successfully loaded {len(df)} resumes from '{path}'.")
        print("Columns available:", list(df.columns))
        return df
    except Exception as e:
        print(f"Error loading resume dataset: {e}")
        return None

if __name__ == "__main__":
    df = load_resume_dataset()
    if df is not None:
        print(df.head(2))
