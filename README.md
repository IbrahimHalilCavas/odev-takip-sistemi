# 📚 Öğrenci Ödev Takip Sistemi

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
*(Geliştirme ilerledikçe güncellenecektir.)*

## 🔗 Bağlantılar
- **Kanban Panosu:** BURAYA_PANO_LINKI
- **Canlı Uygulama:** *(6. haftada eklenecek)*

## 👤 Geliştirici
İbrahim Halil Çavaş – Beykoz Üniversitesi, Yazılım Mühendisliği
