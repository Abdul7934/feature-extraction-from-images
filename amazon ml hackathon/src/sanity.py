import pandas as pd
import argparse
import os
from utils import parse_string

def check_file(filename):
    """Check if the file exists and is a CSV file."""
    if not filename.lower().endswith('.csv'):
        raise ValueError("Only CSV files are allowed.")
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"File not found: {filename}")

def sanity_check(test_filename, output_filename):
    """Perform sanity check on test and output CSV files."""
    # Check file validity
    check_file(test_filename)
    check_file(output_filename)
    
    # Load the dataframes
    try:
        test_df = pd.read_csv(test_filename)
        output_df = pd.read_csv(output_filename)
    except Exception as e:
        raise ValueError(f"Error reading the CSV files: {e}")
    
    # Ensure required columns exist
    if 'index' not in test_df.columns:
        raise ValueError("Test CSV file must contain the 'index' column.")
    if 'index' not in output_df.columns or 'prediction' not in output_df.columns:
        raise ValueError("Output CSV file must contain 'index' and 'prediction' columns.")
    
    # Check for missing or extra indices
    test_indices = set(test_df['index'])
    output_indices = set(output_df['index'])
    
    missing_index = test_indices - output_indices
    if missing_index:
        print(f"Missing indices in output file: {missing_index}")
        
    extra_index = output_indices - test_indices
    if extra_index:
        print(f"Extra indices in output file: {extra_index}")
    
    # Validate predictions
    invalid_predictions = []
    for _, row in output_df.iterrows():
        try:
            parse_string(row['prediction'])
        except ValueError as e:
            invalid_predictions.append((row['index'], row['prediction'], str(e)))
    
    if invalid_predictions:
        print("Invalid predictions:")
        for idx, pred, err in invalid_predictions:
            print(f"Index: {idx}, Prediction: {pred}, Error: {err}")
    else:
        print(f"Parsing successful for file: {output_filename}")
    
    # Merge dataframes for accuracy calculation
    test_df = test_df.rename(columns={'entity_name': 'true_label'})
    output_df = output_df.rename(columns={'prediction': 'predicted_label'})
    
    merged_data = pd.merge(test_df, output_df, on='index', how='inner')
    
    # Print merged data details
    print("Merged Data (First 10 rows):")
    print(merged_data.head(10))
    
    print("Unique true labels:", merged_data['true_label'].unique())
    print("Unique predicted labels:", merged_data['predicted_label'].unique())
    
    # Check for missing values
    print("Missing values in merged data:")
    print(merged_data.isna().sum())
    
    # Compute accuracy
    if 'true_label' in merged_data.columns and 'predicted_label' in merged_data.columns:
        correct_predictions = (merged_data['true_label'] == merged_data['predicted_label']).sum()
        total_predictions = len(merged_data)
        
        if total_predictions > 0:
            accuracy = correct_predictions / total_predictions
            print(f"Accuracy: {accuracy * 100:.2f}%")
        else:
            print("Error: No predictions to evaluate.")
    else:
        print("Error: Required columns for accuracy calculation are missing in merged data.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run sanity check on a CSV file.")
    parser.add_argument("--test_filename", type=str, required=True, help="The test CSV file name.")
    parser.add_argument("--output_filename", type=str, required=True, help="The output CSV file name to check.")
    args = parser.parse_args()
    
    try:
        sanity_check(args.test_filename, args.output_filename)
    except Exception as e:
        print(f"Error: {e}")
