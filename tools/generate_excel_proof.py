import os
import pandas as pd
import numpy as np

# 1. Create Raw Data Sample
raw_data = {
    'InvoiceNo': ['536365', '536365', '536366', '536367', '536368', '536369', '536370', '536371', '536372', '536372'],
    'StockCode': ['85123A', '71053', '22633', '84879', '22727', '22726', '21724', '21883', '22114', '22115'],
    'Quantity': [6, 1, 2, 32, 1, 1, 5, 10, 1, 1],
    'UnitPrice': [2.55, 3.39, 1.85, 1.69, 4.15, 4.15, 0.85, 1.06, 4.95, 4.95],
    'CustomerID': [1001, 1001, 1001, 1002, 1003, 1003, 1003, 1004, 1005, 1005]
}
df_raw = pd.DataFrame(raw_data)
df_raw['TotalAmount'] = df_raw['Quantity'] * df_raw['UnitPrice']

# 2. Aggregate Data (Pivot Table logic)
df_agg = df_raw.groupby('CustomerID').agg(
    Total_Belanja=('TotalAmount', 'sum'),
    Jumlah_Transaksi=('InvoiceNo', 'nunique'),
    Jumlah_Produk=('StockCode', 'nunique')
).reset_index()

# 3. Labeling (Median logic)
median_val = df_agg['Jumlah_Transaksi'].median()
df_agg['Label_Loyal'] = (df_agg['Jumlah_Transaksi'] > median_val).astype(int)

# 4. Entropy Data (Summary for validation)
entropy_summary = pd.DataFrame({
    'Metric': ['Total Data (S)', 'Loyal (1)', 'Tidak Loyal (0)', 'Entropy Total', 'Gain (Total Belanja > 11)'],
    'Value': [5, 2, 3, 0.971, 0.420],
    'Formula/Note': ['N', 'count(1)', 'count(0)', '-sum(p*log2(p))', 'Entropy(S) - Weighted Entropy']
})

# Save to Excel in root project directory
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_file = os.path.join(base_dir, 'BUKTI-PERHITUNGAN-EXCEL.xlsx')
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df_raw.to_excel(writer, sheet_name='1_Data_Mentah', index=False)
    df_agg.to_excel(writer, sheet_name='2_Agregasi_dan_Label', index=False)
    entropy_summary.to_excel(writer, sheet_name='3_Perhitungan_Entropy', index=False)

print(f"Successfully generated {output_file}")
