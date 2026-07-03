import pandas as pd
from pathlib import Path

def load_file(data_file): 
    file_type = Path(data_file.name).suffix

    if file_type == ".xlsx":
        filetype = "Excel"
    elif file_type == ".csv":
        filetype = "CSV"
    else:
        filetype = "Unknown"

    file_name = data_file.name

    if file_type == ".xlsx":
            df=pd.read_excel(data_file)
            return df,filetype,file_name
    elif file_type ==".csv":
            df=pd.read_csv(data_file)
            return df,filetype,file_name
    else :
          raise ValueError("Unsupported file type")
