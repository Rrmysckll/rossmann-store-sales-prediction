import sqlite3
import pandas as pd

print("1. Veritabanı bağlantısı kuruluyor...")
baglanti = sqlite3.connect('rossmann.db')

print("2. Mağaza verileri (store.csv) okunuyor...")
magazalar_df = pd.read_csv('store.csv')

# Boş verileri temizleyelim (Pandas tip hatalarını önlemek için)
# Sayısal alanları 0 ile, metinsel alanları 'None' ile dolduruyoruz
for col in magazalar_df.columns:
    if magazalar_df[col].dtype == 'object':
        magazalar_df[col] = magazalar_df[col].fillna("None")
    else:
        magazalar_df[col] = magazalar_df[col].fillna(0)

print("3. Veriler SQL tablosuna aktarılıyor...")
magazalar_df.to_sql('magazalar', baglanti, if_exists='replace', index=False)

baglanti.close()
print("BAŞARILI! 'rossmann.db' veritabanı dosyası oluşturuldu ve 'magazalar' tablosu içine kaydedildi.")