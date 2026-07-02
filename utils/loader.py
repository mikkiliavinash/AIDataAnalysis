import pandas as pd
from pathlib import Path

def load_file(data_file): 
    file_type = Path(data_file.name).suffix

    if file_type == ".xlsx":
        display_file_type = "Excel"
    elif file_type == ".csv":
        display_file_type = "CSV"
    else:
        display_file_type = "Unknown"

    file_name = data_file.name

    if file_type == ".xlsx":
            df=pd.read_excel(data_file)
            return df,display_file_type,file_name
    elif file_type ==".csv":
            df=pd.read_csv(data_file)
            return df,display_file_type,file_name
    else :
          raise ValueError("Unsupported file type")
