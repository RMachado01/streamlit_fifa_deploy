import pandas as pd
import glob
import os

folder = "Data"
csv_files = glob.glob(os.path.join(folder, "*.csv"))

# Ler e juntar todos
df_final = pd.concat((pd.read_csv(f) for f in csv_files), ignore_index=True)

# Salvar em um novo arquivo
df_final.to_csv("CLEAN_FIFA2023_offcial_data.csv", index=False)

print("CSV unificado salvo como dataset_final.csv")
