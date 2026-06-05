from flask import Flask, render_template, request, jsonify, Response
import pandas as pd
import xgboost as xgb
import datetime
import sqlite3
import os

app = Flask(__name__)

# ==========================================
# DOSYA YOLLARI (DOCKER UYUMU İÇİN MUTLAK YOL)
# ==========================================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'rossmann.db')
MODEL_PATH = os.path.join(BASE_DIR, 'rossmann_model.json')


# 1. Eğittiğimiz Yapay Zeka modelini (beyni) projeye dahil ediyoruz
model = xgb.XGBRegressor()
model.load_model(MODEL_PATH)


# 2. Veritabanı bağlantısı için yardımcı fonksiyon
def get_db_connection():
    # Artık her zaman projenin klasöründeki veritabanına gidecek
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# 3. ANA SAYFA (Tahmin Ekranı)
@app.route('/', methods=['GET', 'POST'])
def home():
    tahmin_sonucu = None
    if request.method == 'POST':
        try:
            store_id = int(request.form.get('store_id', 1))
            tarih_str = request.form.get('predict_date')
            store_type = int(request.form.get('store_type', 0))
            assortment = int(request.form.get('assortment', 0))
            comp_dist = float(request.form.get('comp_dist') or 0.0)
            promo = 1 if request.form.get('promo') else 0
            school_holiday = 1 if request.form.get('school_holiday') else 0

            tarih = datetime.datetime.strptime(tarih_str, '%Y-%m-%d')
            girdi_verisi = pd.DataFrame([{
                'Store': store_id, 'DayOfWeek': tarih.weekday() + 1, 'Promo': promo,
                'StateHoliday': 0, 'SchoolHoliday': school_holiday, 'StoreType': store_type,
                'Assortment': assortment, 'CompetitionDistance': comp_dist,
                'CompetitionOpenSinceMonth': 0, 'CompetitionOpenSinceYear': 0,
                'Promo2': 0, 'Promo2SinceWeek': 0, 'Promo2SinceYear': 0, 'PromoInterval': 0,
                'Yil': tarih.year, 'Ay': tarih.month, 'Gun': tarih.day,
                'HaftaninGunu': tarih.weekday(), 'YilinHaftasi': tarih.isocalendar()[1]
            }])

            tahmin = model.predict(girdi_verisi)[0]
            tahmin_sonucu = f"{int(tahmin):,}".replace(",", ".")
        except Exception as e:
            tahmin_sonucu = "Hata oluştu"

    return render_template('index.html', prediction=tahmin_sonucu)


# 4. MAĞAZALAR SAYFASI (Veritabanı Görüntüleme)
@app.route('/magazalar')
def magazalar():
    conn = get_db_connection()
    magazalar_listesi = conn.execute('SELECT * FROM magazalar').fetchall()
    conn.close()
    return render_template('magazalar.html', magazalar=magazalar_listesi)


# 10. YENİ EKLENEN: DASHBOARD (İŞ ZEKASI) SAYFASI
@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()

    # 1. Toplam Mağaza Sayısı
    toplam_magaza = conn.execute('SELECT COUNT(*) FROM magazalar').fetchone()[0]

    # 2. Aktif Promosyonlu Mağaza Sayısı (Promo2 = 1 olanlar)
    aktif_promo = conn.execute('SELECT COUNT(*) FROM magazalar WHERE Promo2 = 1').fetchone()[0]

    # 3. Mağaza Tipi Dağılımı (A, B, C, D tiplerini gruplayarak sayma)
    tip_dagilimi = conn.execute('SELECT StoreType, COUNT(*) FROM magazalar GROUP BY StoreType').fetchall()
    conn.close()

    # Grafik için verileri (A=1, B=2, C=3, D=4) sözlük yapısında düzenleme
    dagilim_dict = {1: 0, 2: 0, 3: 0, 4: 0}
    for row in tip_dagilimi:
        dagilim_dict[row['StoreType']] = row[1]

    # Arayüze (HTML) gönderilecek paket
    stats = {
        'toplam_magaza': toplam_magaza,
        'aktif_promo': aktif_promo,
        'r2_skoru': '%89.4',  # Eğitimden elde edilen temsili R² başarı skoru
        'ortalama_sapma': '1270 €',
        'dagilim': list(dagilim_dict.values())  # Sadece sayıları listeye çevir [A_sayisi, B_sayisi, ...]
    }

    return render_template('dashboard.html', stats=stats)


# 5. VERİ YÖNETİMİ VE SİSTEM ANALİTİĞİ SAYFASI
@app.route('/veri_yonetimi')
def veri_yonetimi():
    conn = get_db_connection()
    magaza_sayisi = conn.execute('SELECT COUNT(*) FROM magazalar').fetchone()[0]
    conn.close()

    try:
        model_boyutu = round(os.path.getsize(MODEL_PATH) / (1024 * 1024), 2)
    except:
        model_boyutu = 0

    stats = {
        'magaza_sayisi': magaza_sayisi,
        'model_boyutu': model_boyutu,
        'rmse': 1270.94,
        'algoritma': 'XGBoost Regressor'
    }
    return render_template('veri_yonetimi.html', stats=stats)


# ==========================================
# V2.0 YENİ EKLENEN API (CRUD) ENDPOINT'LERİ
# ==========================================

# 6. YENİ MAĞAZA EKLE (CREATE)
@app.route('/api/magaza_ekle', methods=['POST'])
def magaza_ekle():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
                       INSERT INTO magazalar (Store, StoreType, Assortment, CompetitionDistance, Promo2)
                       VALUES (?, ?, ?, ?, ?)
                       ''', (data['Store'], data['StoreType'], data['Assortment'], data['CompetitionDistance'],
                             data['Promo2']))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Mağaza başarıyla eklendi!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


# 7. MAĞAZA GÜNCELLE (UPDATE)
@app.route('/api/magaza_guncelle/<int:store_id>', methods=['PUT'])
def magaza_guncelle(store_id):
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
                       UPDATE magazalar
                       SET StoreType           = ?,
                           Assortment          = ?,
                           CompetitionDistance = ?,
                           Promo2              = ?
                       WHERE Store = ?
                       ''',
                       (data['StoreType'], data['Assortment'], data['CompetitionDistance'], data['Promo2'], store_id))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Mağaza başarıyla güncellendi!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


# 8. MAĞAZA SİL (DELETE)
@app.route('/api/magaza_sil/<int:store_id>', methods=['DELETE'])
def magaza_sil(store_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM magazalar WHERE Store = ?', (store_id,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Mağaza başarıyla silindi!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


# 9. TOPLU VERİ DIŞA AKTARMA (CSV EXPORT)
@app.route('/api/export_csv')
def export_csv():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM magazalar", conn)
        conn.close()

        return Response(
            df.to_csv(index=False),
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=rossmann_magazalar_yedek.csv"}
        )
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    # host='0.0.0.0' ekleyerek dış dünyadan (Docker'dan) gelen istekleri açıyoruz
    app.run(host='0.0.0.0', port=5000)