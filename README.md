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