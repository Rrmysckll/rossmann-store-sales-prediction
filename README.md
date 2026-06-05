# 🚀 Retail Store Sales Prediction System (End-to-End ML Microservice)

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-black?logo=flask)
![XGBoost](https://img.shields.io/badge/XGBoost-Machine_Learning-red)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite)

Büyük ölçekli bir perakende zincirinin geçmiş satış dinamiklerini ve mağaza özelliklerini kullanarak, gelecekteki ciro hacmini öngören yapay zeka destekli tam yığın (full-stack) web uygulamasıdır. 

Proje, yalnızca bir veri bilimi modeli olmakla kalmayıp; kendi veritabanına sahip, REST API uç noktaları barındıran ve **Docker** ile kapsayıcı mimarisinde (containerized) çalışmaya hazır kurumsal bir mikroservis olarak tasarlanmıştır.

## 🎯 Temel Özellikler
* **Makine Öğrenmesi Motoru:** Milyonlarca satırlık perakende verisiyle eğitilmiş XGBoost Regressor algoritması.
* **Kapsayıcı Mimarisi (Docker):** Uygulama `Dockerfile` ile izole edilmiş olup, herhangi bir sunucuda bağımlılık sorunu yaşatmadan saniyeler içinde ayağa kalkar.
* **İlişkisel Veritabanı (SQLite):** Mağaza bilgileri ve istatistikler, arka planda çalışan SQLite mimarisiyle yönetilir.
* **REST API Entegrasyonu:** Mağaza ekleme, silme ve güncelleme (CRUD) işlemleri için JSON tabanlı asenkron uç noktalar.
* **Karanlık Tema Destekli UI/UX:** Veri yönetimi, tahminleme ve gösterge paneli (dashboard) için tasarlanmış modern arayüz.

## 🏗️ Sistem Mimarisi

Sistem, istemci ve sunucu olmak üzere birbirine tam entegre katmanlardan oluşur:
1. **Frontend:** HTML5, CSS3, JavaScript (Asenkron Fetch API ile haberleşme)
2. **Backend:** Python (Flask)
3. **Model:** XGBoost (`rossmann_model.json` formatında serileştirilmiş)
4. **Veri Saklama:** SQLite (`rossmann.db`)
5. **Dağıtım:** Docker Image

## ⚙️ Kurulum ve Çalıştırma (Docker ile)

Projeyi kendi ortamınızda test etmek için sisteminizde Docker'ın kurulu olması yeterlidir. Bilgisayarınıza Python kurmanıza gerek yoktur.

**1. Depoyu Klonlayın:**
```bash
git clone [https://github.com/KULLANICI_ADIN/rossmann-store-sales-prediction.git](https://github.com/KULLANICI_ADIN/rossmann-store-sales-prediction.git)
cd rossmann-store-sales-prediction


## 📸 Ekran Görüntüleri

### 1. Satış Tahmin Ekranı
<img width="1919" height="965" alt="Ekran görüntüsü 2026-06-05 212542" src="https://github.com/user-attachments/assets/c0625c8f-5699-47f1-ba2c-0a82c5bc6d08" />
<img width="1915" height="964" alt="Ekran görüntüsü 2026-06-05 212601" src="https://github.com/user-attachments/assets/055261ca-98c7-46f6-84d1-970df186afeb" />

*(Sürükle-Bırak: Ana tahmin formunun olduğu ekran görüntüsünü tam buraya sürükleyip bırak)*

### 2. İş Zekası (Dashboard) Paneli
<img width="1918" height="954" alt="Ekran görüntüsü 2026-06-05 212644" src="https://github.com/user-attachments/assets/86c71b36-2377-44bd-a498-5899fe7802a2" />
<img width="1916" height="955" alt="Ekran görüntüsü 2026-06-05 212623" src="https://github.com/user-attachments/assets/a1cdb20a-e5e4-450e-8945-516791ba788f" />

*(Sürükle-Bırak: İstatistiklerin ve grafiklerin olduğu ekran görüntüsünü tam buraya sürükleyip bırak)*

### 3. Veri Yönetimi
<img width="1917" height="966" alt="Ekran görüntüsü 2026-06-05 212716" src="https://github.com/user-attachments/assets/0a0587a0-43c0-491d-ac89-e11daf1ee44e" />
<img width="1918" height="957" alt="Ekran görüntüsü 2026-06-05 212704" src="https://github.com/user-attachments/assets/987eca8a-b4a8-4b6e-b516-4ff8513549e9" />

*(Sürükle-Bırak: Model durumu ve veri tablolarının olduğu ekran görüntüsünü tam buraya sürükleyip bırak)*

### 3. Mağazalar
<img width="1916" height="963" alt="Ekran görüntüsü 2026-06-05 212745" src="https://github.com/user-attachments/assets/149e2abc-599f-4f1f-9400-22dc576026a6" />
<img width="1919" height="955" alt="Ekran görüntüsü 2026-06-05 212732" src="https://github.com/user-attachments/assets/e92b8347-21b8-427b-affe-32e5b65278ae" />

*(Sürükle-Bırak: Model durumu ve veri tablolarının olduğu ekran görüntüsünü tam buraya sürükleyip bırak)*


## 💡 API Kullanımı (Örnek)

Sistem dışarıya REST API desteği sunmaktadır. Yeni bir mağaza eklemek için örnek JSON isteği:
```json
POST /api/magaza_ekle
{
    "Store": 1116,
    "StoreType": 1,
    "Assortment": 3,
    "CompetitionDistance": 1250,
    "Promo2": 1
}     
