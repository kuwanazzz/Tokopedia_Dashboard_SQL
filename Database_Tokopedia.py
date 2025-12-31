import pandas as pd
from sqlalchemy import create_engine
import sys

# 1. Alamat file CSV 
file_path = r'C:\Users\yameh\OneDrive\Desktop\dashboards\Dashboard_Tokopedia\tokopedia_products_with_review.csv'

# 2. Detail Koneksi (Sudah menggunakan password)
username = 'postgres'
password = 'NakayamaFesta1112'
host = 'localhost'
port = '5432'
database_name = 'Dashboard_Tokopedia'

try:
    print("--- Memulai Proses Import ---")
    
    # 3. Membaca CSV
    # engine='python' digunakan agar lebih toleran terhadap karakter tanda petik yang berantakan
    print("1. Sedang membaca file CSV...")
    df = pd.read_csv(file_path, engine='python', on_bad_lines='warn')

    # 4. Cleaning Ringan (Menghilangkan N/A agar menjadi NULL di database)
    df = df.replace('N/A', None)

    # 5. Membuat Koneksi ke PostgreSQL
    print("2. Menghubungkan ke PostgreSQL...")
    conn_string = f'postgresql://{username}:{password}@{host}:{port}/{database_name}'
    engine = create_engine(conn_string)

    # 6. Mengirim ke Database
    # Nama tabel di pgAdmin nanti adalah "tokopedia_raw"
    print("3. Mengirim data ke tabel 'tokopedia_raw'...")
    df.to_sql('tokopedia_raw', engine, if_exists='replace', index=False)

    print("\n" + "="*30)
    print("HASIL: BERHASIL TOTAL!")
    print("="*30)
    print("Silakan cek pgAdmin Anda:")
    print(f"Database: {database_name}")
    print("Table: tokopedia_raw")
    print("\nData sekarang sudah siap ditarik ke Tableau.")

except Exception as e:
    print(f"\nTerjadi kesalahan: {e}")

