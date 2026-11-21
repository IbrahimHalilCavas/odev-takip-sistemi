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

### 🐳 Docker ile Çalıştırma

```bash
# Image oluştur
docker build -t odev-takip-sistemi .

# Container çalıştır (veriler odev-veri volume'unda kalıcı tutulur)
docker run -d -p 5000:5000 -v odev-veri:/app/data --name odev-app odev-takip-sistemi

# Logları izle
docker logs -f odev-app

# Durdur ve sil
docker rm -f odev-app
```

### Ortam Değişkenleri
| Değişken | Açıklama | Varsayılan |
|---|---|---|
| `DB_PATH` | SQLite veritabanı dosyasının yolu | `src/odevler.db` |
| `SECRET_KEY` | Flask oturum anahtarı | Geliştirme anahtarı |

## ☁️ Bulut Dağıtımı (Cloud Deployment)

Uygulama **Render** PaaS platformunda Docker container olarak çalışmaktadır.

### Platform Seçimi
| Platform | Ücretsiz Kullanım | Değerlendirme |
|---|---|---|
| **Render** ✅ | Ücretsiz web servisi, kredi kartı gerekmez | Dockerfile desteği, GitHub ile otomatik deploy, panelde log ve metrikler |
| Railway | Yalnızca kısa süreli deneme kredisi | 8 haftalık dönem için sürdürülebilir değil |
| Azure / Google Cloud Run | Ücretsiz katman mevcut | Genellikle kredi kartı gerekir, kurulum daha karmaşık |

**Seçim gerekçesi:** Render; mevcut Dockerfile'ı doğrudan kullanabilmesi, GitHub `main` dalına yapılan her merge'de otomatik yeniden dağıtım (CD) yapması ve panelinden log/metrik izlenebilmesi nedeniyle seçilmiştir.

### Yapılandırma
- **Bölge:** Frankfurt (EU Central), Türkiye'ye en yakın bölge
- **Health Check:** `/health` endpoint'i Render tarafından düzenli olarak kontrol edilir
- **Ortam değişkenleri:** `SECRET_KEY` (Render'da gizli olarak tutulur), `TZ=Europe/Istanbul`
- **Port:** Render'ın verdiği `PORT` ortam değişkeni Dockerfile'da kullanılır

### Bilinen Sınırlamalar (Ücretsiz Katman)
- **Uyku modu:** 15 dakika istek almayan servis uyutulur; ilk istek ~1 dakika sürebilir.
- **Geçici dosya sistemi:** SQLite veritabanı kalıcı değildir; servis yeniden başladığında veya yeniden dağıtıldığında veriler sıfırlanır. Kalıcı veri için ücretli plandaki kalıcı disk veya yönetilen bir veritabanı (ör. PostgreSQL) kullanılabilir.

## 🔗 Bağlantılar
- **Kanban Panosu:** https://github.com/users/IbrahimHalilCavas/projects/2
- **Canlı Uygulama:** https://odev-takip-sistemi.onrender.com
- **Sağlık Kontrolü:** https://odev-takip-sistemi.onrender.com/health

## 👤 Geliştirici
İbrahim Halil Çavaş – Beykoz Üniversitesi, Yazılım Mühendisliği
