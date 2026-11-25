# 📚 Öğrenci Ödev Takip Sistemi

![CI](https://github.com/IbrahimHalilCavas/odev-takip-sistemi/actions/workflows/ci.yml/badge.svg)

Öğrencilerin ödevlerini ve teslim tarihlerini yönetebildiği küçük ölçekli bir web uygulaması.
Bu proje, Beykoz Üniversitesi **Modern Yazılım Mühendisliği – Bulut ve DevOps** dersi kapsamında,
yazılım geliştirme, DevOps ve Cloud süreçlerini uygulamalı olarak öğrenmek amacıyla geliştirilmiştir.

🌐 **Canlı uygulama:** https://odev-takip-sistemi.onrender.com

## 🛠️ Teknolojiler
- **Backend:** Python 3.12, Flask
- **Veritabanı:** SQLite
- **Üretim sunucusu:** gunicorn
- **Test:** pytest (22 otomatik test)
- **CI:** GitHub Actions (testler + pip-audit güvenlik taraması)
- **Container:** Docker
- **Cloud / CD:** Render (PaaS) – CI başarılı olduktan sonra otomatik deploy

## ⚙️ Temel Fonksiyonlar
1. **Ödev ekleme** – Başlık, ders adı, açıklama ve teslim tarihi ile yeni ödev oluşturma
2. **Ödevleri listeleme** – Teslim tarihine göre sıralı ödev listesi
3. **Durum güncelleme** – Bekliyor → Devam Ediyor → Teslim Edildi; duruma göre filtreleme
4. **Düzenleme ve silme** – Mevcut ödevi güncelleme veya onay vererek silme
5. **Gecikme uyarısı** – Tarihi geçen ödevleri "Gecikti", 3 gün içindekileri "Yaklaşıyor" olarak işaretleme
6. **Takvim entegrasyonu** – Teslim edilmemiş ödevleri iCalendar (.ics) olarak indirme (teslimden önceki gün 09:00 hatırlatmalı) ve her ödevi tek tıkla Google Takvim'e ekleme

## 📋 Fonksiyonel Gereksinimler
- FR1: Kullanıcı başlık, ders adı, açıklama ve teslim tarihi girerek ödev ekleyebilmelidir.
- FR2: Başlık veya teslim tarihi boş bırakılırsa sistem hata mesajı göstermelidir.
- FR3: Sistem ödevleri teslim tarihine göre sıralı listelemelidir.
- FR4: Kullanıcı ödevin durumunu değiştirebilmeli ve duruma göre filtreleyebilmelidir.
- FR5: Kullanıcı bir ödevi düzenleyebilmeli ve onay vererek silebilmelidir.
- FR6: Sistem teslim tarihi geçmiş ve yaklaşan ödevleri görsel olarak işaretlemelidir.
- FR7: Kullanıcı teslim edilmemiş ödevlerini standart takvim dosyası olarak indirebilmeli ve tek bir ödevi Google Takvim'e ekleyebilmelidir.

## 📐 Mimari
Katmanlı mimari, veri modeli, endpoint listesi ve CI/CD akış diyagramı için: **[docs/architecture.md](docs/architecture.md)**

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

### 🧪 Testleri Çalıştırma
```bash
pytest -v
```
22 test: route/entegrasyon testleri (`test_app.py`), gecikme kuralı (`test_kurallar.py`) ve takvim üretimi (`test_takvim.py`). Testler her seferinde geçici, boş bir veritabanı kullanır.

### 🐳 Docker ile Çalıştırma

```bash
# Image oluştur
docker build -t odev-takip-sistemi .

# Container çalıştır (veriler odev-veri volume'unda kalıcı tutulur)
docker run -d -p 5000:5000 -v odev-veri:/app/data --name odev-app odev-takip-sistemi

# Logları ve kaynak kullanımını izle
docker logs -f odev-app
docker stats odev-app

# Durdur ve sil
docker rm -f odev-app
```

### Ortam Değişkenleri
| Değişken | Açıklama | Varsayılan |
|---|---|---|
| `DB_PATH` | SQLite veritabanı dosyasının yolu | `src/odevler.db` (Docker: `/app/data/odevler.db`) |
| `SECRET_KEY` | Flask oturum anahtarı | Geliştirme anahtarı (canlıda mutlaka ayarlanmalı) |
| `PORT` | Uygulamanın dinlediği port (Docker/gunicorn) | `5000` |
| `TZ` | Saat dilimi | `Europe/Istanbul` |

## 🔄 CI/CD Süreci
1. Her değişiklik bir **feature branch**'te geliştirilir ve **Pull Request** ile `main`'e gönderilir.
2. **GitHub Actions** her push ve PR'da testleri (`pytest`) ve bağımlılık güvenlik taramasını (`pip-audit`) çalıştırır.
3. `main` dalı **korumalıdır**: CI başarılı olmadan merge yapılamaz.
4. **Render**, `main`'e gelen her commit için CI sonucunu bekler; testler geçerse uygulamayı Docker ile yeniden derleyip **otomatik deploy** eder.

## ☁️ Bulut Dağıtımı (Cloud Deployment)

Uygulama **Render** PaaS platformunda Docker container olarak çalışmaktadır.

### Platform Seçimi
| Platform | Ücretsiz Kullanım | Değerlendirme |
|---|---|---|
| **Render** ✅ | Ücretsiz web servisi, kredi kartı gerekmez | Dockerfile desteği, GitHub ile otomatik deploy, panelde log ve metrikler |
| Railway | Yalnızca kısa süreli deneme kredisi | 8 haftalık dönem için sürdürülebilir değil |
| Azure / Google Cloud Run | Ücretsiz katman mevcut | Genellikle kredi kartı gerekir, kurulum daha karmaşık |

**Seçim gerekçesi:** Render; mevcut Dockerfile'ı doğrudan kullanabilmesi, GitHub ile entegre otomatik deploy (CD) sunması ve panelinden log/metrik izlenebilmesi nedeniyle seçilmiştir.

### Yapılandırma
- **Bölge:** Frankfurt (EU Central), Türkiye'ye en yakın bölge
- **Auto-Deploy:** After CI Checks Pass (testler geçmeden yeni sürüm yayına alınmaz)
- **Health Check:** `/health` endpoint'i Render tarafından düzenli olarak kontrol edilir
- **Ortam değişkenleri:** `SECRET_KEY` (Render'da gizli olarak tutulur), `TZ=Europe/Istanbul`
- **Port:** Render'ın verdiği `PORT` ortam değişkeni Dockerfile'da kullanılır

## 📊 İzleme ve Loglama
- Zaman damgalı, seviyeli uygulama logları (INFO / WARNING / ERROR); Render **Logs** panelinden aranıp filtrelenebilir
- `/health` hem uygulamayı hem veritabanı bağlantısını kontrol eder; arızada HTTP 503 döner
- Kaynak kullanımı: Render **Metrics** ve `docker stats`

## 🔒 Güvenlik
- Gizli anahtar koda yazılmaz, ortam değişkeninden okunur; canlıda debug kapalıdır (gunicorn)
- Container root olmayan kullanıcıyla (`appuser`) çalışır
- Güvenlik başlıkları (`X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`) ve 16 KB istek sınırı
- SQL sorgularında parametre kullanımı (SQL Injection koruması)
- CI'da `pip-audit`, GitHub'da Dependabot ve Secret Protection; `main` branch koruması

## ⚠️ Bilinen Sınırlamalar
- **Geçici dosya sistemi:** Render ücretsiz katmanında SQLite verileri yeniden başlatma, deploy veya uyku modunda sıfırlanır. Kalıcı veri için kalıcı disk veya yönetilen bir veritabanı (ör. PostgreSQL) kullanılabilir.
- **Uyku modu:** 15 dakika istek almayan servis uyutulur; ilk istek ~1 dakika sürebilir.
- **Tarih doğrulaması:** Teslim tarihi için makul yıl aralığı kontrolü henüz yoktur.

## 🔗 Bağlantılar
- **GitHub Deposu:** https://github.com/IbrahimHalilCavas/odev-takip-sistemi
- **Kanban Panosu:** https://github.com/users/IbrahimHalilCavas/projects/2
- **CI Çalışmaları (GitHub Actions):** https://github.com/IbrahimHalilCavas/odev-takip-sistemi/actions
- **Canlı Uygulama:** https://odev-takip-sistemi.onrender.com
- **Sağlık Kontrolü:** https://odev-takip-sistemi.onrender.com/health

## 👤 Geliştirici
İbrahim Halil Çavaş – Beykoz Üniversitesi, Yazılım Mühendisliği