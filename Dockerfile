# 1. Temel image: Python 3.12'nin küçük (slim) sürümü (CI ile aynı sürüm)
FROM python:3.12-slim

# 2. Python ayarları: .pyc dosyası oluşturma, logları beklemeden yaz
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Container içindeki çalışma klasörü
WORKDIR /app

# 4. Önce sadece bağımlılık listesini kopyala ve kur (katman önbelleği için)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Uygulama kodunu kopyala
COPY src/ ./src/

# 6. Güvenlik: uygulamayı root (yönetici) yerine sıradan bir kullanıcıyla çalıştır
RUN useradd --create-home appuser && mkdir -p /app/data && chown -R appuser /app
USER appuser

# 7. Ayarlar: veritabanı yolu ve port (ortam değişkenleri)
 ENV DB_PATH=/app/data/odevler.db \
    PORT=5000 \
    TZ=Europe/Istanbul

EXPOSE 5000

# 8. Uygulamayı üretim sunucusu gunicorn ile başlat (erişim logları ekrana yazılır)
CMD ["sh", "-c", "exec gunicorn --chdir src --bind 0.0.0.0:${PORT} --access-logfile - app:app"]