import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import xgboost as xgb

print("1. Aşama: Veriler okunuyor...")
satis_verisi = pd.read_csv("train.csv", low_memory=False)
magaza_bilgisi = pd.read_csv("store.csv")

print("2. Aşama: Eksik veriler temizleniyor...")
max_dist = magaza_bilgisi['CompetitionDistance'].max()
magaza_bilgisi['CompetitionDistance'] = magaza_bilgisi['CompetitionDistance'].fillna(max_dist)

magaza_bilgisi['CompetitionOpenSinceMonth'] = magaza_bilgisi['CompetitionOpenSinceMonth'].fillna(0)
magaza_bilgisi['CompetitionOpenSinceYear'] = magaza_bilgisi['CompetitionOpenSinceYear'].fillna(0)
magaza_bilgisi['Promo2SinceWeek'] = magaza_bilgisi['Promo2SinceWeek'].fillna(0)
magaza_bilgisi['Promo2SinceYear'] = magaza_bilgisi['Promo2SinceYear'].fillna(0)
magaza_bilgisi['PromoInterval'] = magaza_bilgisi['PromoInterval'].fillna("None")

print("3. Aşama: Tablolar birleştiriliyor...")
tum_veri = pd.merge(satis_verisi, magaza_bilgisi, on='Store', how='left')

print("4. Aşama: Tarihler parçalanıyor (Özellik Mühendisliği)...")
tum_veri['Date'] = pd.to_datetime(tum_veri['Date'])
tum_veri['Yil'] = tum_veri['Date'].dt.year
tum_veri['Ay'] = tum_veri['Date'].dt.month
tum_veri['Gun'] = tum_veri['Date'].dt.day
tum_veri['HaftaninGunu'] = tum_veri['Date'].dt.dayofweek
tum_veri['YilinHaftasi'] = tum_veri['Date'].dt.isocalendar().week.astype(int)

# Gereksiz sütunları siliyoruz
tum_veri = tum_veri.drop(['Date', 'Customers'], axis=1)

print("5. Aşama: Metinler yapay zeka için sayılara çevriliyor...")
le = LabelEncoder()
metin_sutunlari = ['StateHoliday', 'StoreType', 'Assortment', 'PromoInterval']

for sutun in metin_sutunlari:
    tum_veri[sutun] = le.fit_transform(tum_veri[sutun].astype(str))

# Mağazanın kapalı olduğu (satışın 0 olduğu) günleri eğitimden çıkarıyoruz
tum_veri = tum_veri[tum_veri['Open'] != 0]
tum_veri = tum_veri.drop(['Open'], axis=1)

print("6. Aşama: Yapay Zeka modeli eğitiliyor (Bu işlem 1-2 dakika sürebilir, lütfen bekleyin)...")
# Hedefimizi (Satışlar) ve özelliklerimizi ayırıyoruz
y = tum_veri['Sales']
X = tum_veri.drop(['Sales'], axis=1)

# Veriyi Eğitim (%80) ve Test (%20) olarak bölüyoruz
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# XGBoost Modelini kuruyoruz
model = xgb.XGBRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=8,
    random_state=42
)

# Modeli Eğitiyoruz
model.fit(X_train, y_train)

# Başarıyı ölçüyoruz
tahminler = model.predict(X_test)
hata = np.sqrt(mean_squared_error(y_test, tahminler))
print(f"\n---> Eğitim Tamamlandı! Ortalama Hata (RMSE): {hata:.2f}")

# Modelin beynini kaydediyoruz
model.save_model("rossmann_model.json")
print("---> Harika! Model 'rossmann_model.json' adıyla klasöre başarıyla kaydedildi.")