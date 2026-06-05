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
<img width="1917" height="972" alt="image" src="https://github.com/user-attachments/assets/bf7e254f-59bd-4c74-a563-b4ce31ceba4d" />
<img width="1919" height="967" alt="image" src="https://github.com/user-attachments/assets/a21d18ee-096e-49d3-be9e-4db95127fc45" />

### 2. İş Zekası (Dashboard) Paneli
<img width="1919" height="969" alt="image" src="https://github.com/user-attachments/assets/1a269dd1-75d1-48b4-8528-47eb56fc4017" />
<img width="1899" height="969" alt="image" src="https://github.com/user-attachments/assets/69e41623-c7de-4c73-bfe0-917c9227fb8a" />

### 3. Veri Yönetimi
<img width="1919" height="915" alt="image" src="https://github.com/user-attachments/assets/4396ea5f-fce2-4b03-b502-cf6e9fe0afe4" />
<img width="1919" height="941" alt="image" src="https://github.com/user-attachments/assets/9bf64eff-0f12-4a34-bd98-187184fac101" />

### 3. Mağazalar


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
