import os
import scipy.io
import pandas as pd
import json

def convert_mat_to_csv(input_directory, output_directory):
    """Converts .mat files from a directory to CSV and JSON formats."""
    
    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    # Loop through all .mat files in the directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".mat"):
            mat_path = os.path.join(input_directory, filename)
            mat_data = scipy.io.loadmat(mat_path)
            
            # Remove MATLAB metadata keys (start with '__')
            mat_data = {key: value for key, value in mat_data.items() if not key.startswith("__")}
            
            # Save JSON version
            json_path = os.path.join(output_directory, filename.replace(".mat", ".json"))
            with open(json_path, "w") as json_file:
                json.dump(mat_data, json_file, indent=4, default=lambda x: x.tolist() if hasattr(x, "tolist") else str(x))
            
            # Save CSV version for numerical arrays
            for key, value in mat_data.items():
                if isinstance(value, (list, tuple)) or hasattr(value, "shape"):
                    csv_path = os.path.join(output_directory, f"{filename.replace('.mat', '')}_{key}.csv")
                    df = pd.DataFrame(value)
                    df.to_csv(csv_path, index=False)
                    
            print(f"Converted {filename} -> JSON and CSV files saved in {output_directory}")

if __name__ == "__main__":
    input_dir = "Data/"
    output_dir = "ConvertedData/"
    convert_mat_to_csv(input_dir, output_dir)
