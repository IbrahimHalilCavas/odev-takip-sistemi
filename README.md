# 📚 Öğrenci Ödev Takip Sistemi

![CI](https://github.com/IbrahimHalilCavas/odev-takip-sistemi/actions/workflows/ci.yml/badge.svg)

Öğrencilerin ödevlerini ve teslim tarihlerini yönetebildiği küçük ölçekli bir web uygulaması.
Bu proje, Beykoz Üniversitesi **Modern Yazılım Mühendisliği – Bulut ve DevOps** dersi kapsamında,
yazılım geliştirme, DevOps ve Cloud süreçlerini uygulamalı olarak öğrenmek amacıyla geliştirilmektedir.

## 🛠️ Teknolojiler
- **Backend:** Python, Flask
- **Veritabanı:** SQLite
- **Test:** pytest
- **CI/CD:** GitHub Actions
- **Container:** Docker
- **Cloud:** PaaS (Render / Railway – seçilecek)

## ⚙️ Temel Fonksiyonlar
1. **Ödev ekleme** – Başlık, ders adı, açıklama ve teslim tarihi ile yeni ödev oluşturma
2. **Ödevleri listeleme** – Teslim tarihine göre sıralı ödev listesi
3. **Durum güncelleme** – Bekliyor → Devam Ediyor → Teslim Edildi
4. **Düzenleme ve silme** – Mevcut ödevi güncelleme veya silme
5. **Gecikme uyarısı** – Tarihi geçen ödevleri "Gecikti", 3 gün içindekileri "Yaklaşıyor" olarak işaretleme

## 📋 Fonksiyonel Gereksinimler
- FR1: Kullanıcı başlık, ders adı, açıklama ve teslim tarihi girerek ödev ekleyebilmelidir.
- FR2: Başlık veya teslim tarihi boş bırakılırsa sistem hata mesajı göstermelidir.
- FR3: Sistem ödevleri teslim tarihine göre sıralı listelemelidir.
- FR4: Kullanıcı ödevin durumunu değiştirebilmeli ve duruma göre filtreleyebilmelidir.
- FR5: Kullanıcı bir ödevi düzenleyebilmeli ve onay vererek silebilmelidir.
- FR6: Sistem teslim tarihi geçmiş ve yaklaşan ödevleri görsel olarak işaretlemelidir.

## 🚀 Kurulum ve Çalıştırma

**Gereksinimler:** Python 3.10+ ve Git

```bash
# 1. Depoyu indir
git clone https://github.com/IbrahimHalilCavas/odev-takip-sistemi.git
cd odev-takip-sistemi

# 2. Sanal ortamı oluştur ve etkinleştir
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Bağımlılıkları kur
pip install -r requirements.txt

# 4. Uygulamayı çalıştır
python src/app.py
```

Uygulama `http://127.0.0.1:5000` adresinde açılır.
Sağlık kontrolü: `http://127.0.0.1:5000/health`

### Ortam Değişkenleri
| Değişken | Açıklama | Varsayılan |
|---|---|---|
| `DB_PATH` | SQLite veritabanı dosyasının yolu | `src/odevler.db` |
| `SECRET_KEY` | Flask oturum anahtarı | Geliştirme anahtarı |

## 🔗 Bağlantılar
- **Kanban Panosu:** https://github.com/users/IbrahimHalilCavas/projects/2
- **Canlı Uygulama:** *(6. haftada eklenecek)*

## 👤 Geliştirici
İbrahim Halil Çavaş – Beykoz Üniversitesi, Yazılım Mühendisliği
