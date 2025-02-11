import os
import pandas as pd
from pathlib import Path

def process_jtl_file(file_path, output_dir):
    """
    Processes a .jtl file to extract performance metrics and saves the results as a CSV.
    
    Parameters:
        file_path (str): Path to the .jtl file.
        output_dir (str): Directory to save the processed results.
    """
    # Load data from the .jtl file
    data = pd.read_csv(file_path)

    # Calculate metrics
    throughput = len(data) / ((data['timeStamp'].iloc[-1] - data['timeStamp'].iloc[0]) / 1000)  # requests/second
    avg_response_time = data['elapsed'].mean()  # Average response time in ms
    error_rate = 100 * (len(data[data['success'] == False]) / len(data))  # Error rate in percentage
    avg_latency = data['Latency'].mean()  # Average latency in ms
    total_bytes_received = data['bytes'].sum()  # Total data received in bytes
    total_bytes_sent = data['sentBytes'].sum()  # Total data sent in bytes
    response_code_distribution = data['responseCode'].value_counts().to_dict()  # Response code distribution

    # Create a DataFrame for the results
    metrics = {
        "Metric": ["Throughput", "Average Response Time", "Error Rate", "Average Latency", "Total Data Received", "Total Data Sent"],
        "Value": [throughput, avg_response_time, error_rate, avg_latency, total_bytes_received, total_bytes_sent],
        "Unit": ["Requests/Second", "ms", "%", "ms", "Bytes", "Bytes"]
    }
    results_df = pd.DataFrame(metrics)

    # Add response code distribution to the DataFrame
    for code, count in response_code_distribution.items():
        new_row = pd.DataFrame([{"Metric": f"Response Code {code}", "Value": count, "Unit": "Count"}])
        results_df = pd.concat([results_df, new_row], ignore_index=True)


    # Save results to the output directory
    output_file = os.path.join(output_dir, f"{Path(file_path).stem}_results.csv")
    results_df.to_csv(output_file, index=False)
    print(f"Results saved to: {output_file}")

def main(input_dir):
    """
    Processes all .jtl files in the given directory and saves the results.
    
    Parameters:
        input_dir (str): Path to the directory containing .jtl files.
    """
    # Check if the directory exists
    if not os.path.exists(input_dir):
        print(f"The directory {input_dir} does not exist.")
        return

    # Create output folder
    output_dir = os.path.join(input_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    # Process all .jtl files
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".jtl"):
            file_path = os.path.join(input_dir, file_name)
            print(f"Processing {file_path}...")
            process_jtl_file(file_path, output_dir)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Processes .jtl files and generates results in an 'output' folder.")
    parser.add_argument("input_dir", type=str, help="Path to the directory containing .jtl files.")
    args = parser.parse_args()

    main(args.input_dir)
