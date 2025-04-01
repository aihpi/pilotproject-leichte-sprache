import logging, os
import pandas as pd
import json
from typing import List, Dict
from leichtesprache.prompts import PROMPT_TEMPLATE_FOR_DATASET
import argparse

logging.basicConfig(format=os.getenv("LOG_FORMAT", "%(asctime)s [%(levelname)s] %(message)s"))
logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("LOG_LEVEL", logging.INFO))


def parse_arguments():
    parser = argparse.ArgumentParser(description="Process a dataset for training and testing.")
    parser.add_argument('--file-name', type=str, default='dataset.csv', help='Dataset CSV file.')
    parser.add_argument('--data-path', type=str, default='data', help='Base directory for data files.')
    parser.add_argument('--train-fraction', type=float, default=0.8, help='Fraction of data to be used for training.')
    parser.add_argument('--random-seed', type=int, default=42, help='Random seed for reproducibility.')
    parser.add_argument('--input-header', type=str, default='input', help='Header name for input column.')
    parser.add_argument('--target-header', type=str, default='output', help='Header name for target (output) column.')
    parser.add_argument('--format', choices=['chatml', 'alpaca'], default='chatml', help="Output format: chatml or alpaca.")
    parser.add_argument('--verbose', action='store_true', help='Increase output verbosity.')
    return parser.parse_args()


def load_and_split_data(
    file_path: str,
    train_fraction: float,
    random_seed: int,
    input_header: str,
    target_header: str,
    verbose: bool = False,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load cleaned and analysed dataset from file path."""

    logger.info(f"Loading dataset from {file_path}")
    df = pd.read_csv(file_path, usecols=[0, 1], names=[input_header, target_header], header=0)
    if verbose:
        print(df.info(verbose=False))
    print(f"Number of samples: {len(df)}")
    train_df = df.sample(frac=train_fraction, random_state=random_seed)
    test_df = df.drop(train_df.index)
    # Show the sizes of the datasets
    print(f"Train set size: {len(train_df)}")
    print(f"Test set size: {len(test_df)}")
    if verbose:
        # Show head of each dataset
        print(f"\nTrain set:\n{train_df.head()}")
        print(f"\nTest set:\n{test_df.head()}")
    return train_df, test_df


def format_dataframe_to_chatml_dataset(
    df: pd.DataFrame, input_header: str, target_header: str
) -> List[Dict]:
    """
    Format a DataFrame to the ChatML dataset format.

    Args:
    - df (pd.DataFrame): DataFrame containing input and output columns.

    Returns:
    - List[Dict]: A list of dictionaries in the format required by ChatML.
    """
    return [
        {
            "messages": [
                {
                    "content": PROMPT_TEMPLATE_FOR_DATASET.format(text=row_dict[input_header]),
                    "role": "user",
                },
                {"content": row_dict[target_header], "role": "assistant"},
            ]
        }
        for row_dict in df.to_dict(orient="records")
    ]


def format_dataframe_to_alpaca_dataset(
    df: pd.DataFrame, input_header: str, target_header: str
) -> List[Dict]:
    """
    Format a DataFrame to the Alpaca dataset format.

    Args:
    - df (pd.DataFrame): DataFrame containing input and output columns.

    Returns:
    - List[Dict]: A list of dictionaries in the format required by Alpaca.
    """
    return [
        {
            "instruction": PROMPT_TEMPLATE_FOR_DATASET.format(text=row[input_header]),
            input_header: "",
            target_header: row[target_header],
        }
        for _, row in df.iterrows()
    ]


def save_to_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


def save_to_jsonl(data: List[Dict], file_path: str):
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in data:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')


def main(
    file_name: str,
    data_path: str,
    train_fraction: float,
    random_seed: int,
    input_header: str,
    target_header: str,
    output_format: str,
    verbose: bool = False,
):

    file_path = os.path.join(data_path, file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at {file_path}")

    train_df, test_df = load_and_split_data(
        file_path, train_fraction, random_seed, input_header, target_header, verbose=verbose
    )

    logger.info("Saving train and test datasets to CSV files...")
    train_df.to_csv(os.path.join(data_path, "train.csv"), index=False, encoding='utf-8')
    test_df.to_csv(os.path.join(data_path, "test.csv"), index=False, encoding='utf-8')

    if output_format == 'chatml':
        train_data = format_dataframe_to_chatml_dataset(train_df, input_header, target_header)
        test_data = format_dataframe_to_chatml_dataset(test_df, input_header, target_header)
        if verbose:
            print("\nChatML format sample:")
            print(json.dumps(train_data[:2], indent=4))
        save_to_jsonl(train_data, os.path.join(data_path, "train.jsonl"))
        save_to_jsonl(test_data, os.path.join(data_path, "test.jsonl"))
        logger.info("Data has been converted to ChatML format and saved to JSONL files.")
    elif output_format == 'alpaca':
        train_data = format_dataframe_to_alpaca_dataset(train_df, input_header, target_header)
        test_data = format_dataframe_to_alpaca_dataset(test_df, input_header, target_header)
        if verbose:
            print("\nAlpaca format sample:")
            print(json.dumps(train_data[:2], indent=4))
        save_to_json(train_data, os.path.join(data_path, "train.json"))
        save_to_json(test_data, os.path.join(data_path, "test.json"))
        logger.info("Data has been converted to Alpaca format and saved to JSON files.")
    else:
        raise ValueError("Invalid output format. Choose 'chatml' or 'alpaca'.")

    logger.info("Data preprocessing completed.")


if __name__ == "__main__":
    args = parse_arguments()
    main(
        args.file_name,
        args.data_path,
        args.train_fraction,
        args.random_seed,
        args.input_header,
        args.target_header,
        args.format,
        args.verbose,
    )
