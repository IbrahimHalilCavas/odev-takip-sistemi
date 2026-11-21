import logging
import os
from datetime import datetime

from flask import Flask, abort, flash, redirect, render_template, request, url_for

import database
from kurallar import teslim_uyarisi

# Loglama: zaman, seviye ve mesaj biçiminde ekrana (stdout) yazılır
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("odev-takip")

app = Flask(__name__)
# Flash mesajları için gizli anahtar. Canlı ortamda ortam değişkeninden okunacak.
app.secret_key = os.environ.get("SECRET_KEY", "gelistirme-anahtari")
# F5: Şablonlarda teslim_uyarisi() fonksiyonu kullanılabilsin
app.jinja_env.globals["teslim_uyarisi"] = teslim_uyarisi

# Uygulama açılırken tablo yoksa oluştur
database.init_db()


@app.template_filter("tarih")
def tarih_formatla(deger):
    """2026-11-20 biçimindeki tarihi 20.11.2026 olarak gösterir."""
    return datetime.strptime(deger, "%Y-%m-%d").strftime("%d.%m.%Y")


@app.route("/")
def index():
    """F2 + F3: Ödevleri listeleme ve duruma göre filtreleme."""
    secili_durum = request.args.get("status", "")
    odevler = database.get_assignments(secili_durum or None)
    return render_template(
        "index.html",
        odevler=odevler,
        durumlar=database.DURUMLAR,
        secili_durum=secili_durum,
    )


@app.route("/status/<int:assignment_id>", methods=["POST"])
def update_status(assignment_id):
    """F3: Ödev durumunu güncelleme."""
    yeni_durum = request.form.get("status", "")
    if database.update_status(assignment_id, yeni_durum):

        flash("Ödev durumu güncellendi.", "basari")
        logger.info("Ödev durumu güncellendi: id=%s -> %s", assignment_id, yeni_durum)
    else:
        flash("Durum güncellenemedi.", "hata")
        logger.warning("Geçersiz durum güncelleme denemesi: id=%s, durum=%r", assignment_id, yeni_durum)


    # Kullanıcı filtreli listedeyse aynı filtreye geri dön
    filtre = request.form.get("filtre", "")
    if filtre in database.DURUMLAR:
        return redirect(url_for("index", status=filtre))
    return redirect(url_for("index"))


@app.route("/add", methods=["GET", "POST"])
def add():
    """F1: Ödev ekleme."""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        course = request.form.get("course", "").strip()
        description = request.form.get("description", "").strip()
        due_date = request.form.get("due_date", "").strip()

        # Doğrulama: başlık ve teslim tarihi zorunlu
        if not title or not due_date:
            logger.warning("Geçersiz ödev ekleme denemesi: başlık veya tarih boş")
            flash("Başlık ve teslim tarihi zorunludur.", "hata")
            return render_template("add.html", form=request.form), 400

        database.add_assignment(title, course, description, due_date)
        logger.info("Ödev eklendi: %s (teslim: %s)", title, due_date)
        flash(
            f"Ödev eklendi! Toplam ödev sayısı: {database.count_assignments()}",
            "basari",
        )
        return redirect(url_for("index"))

    return render_template("add.html", form={})

@app.route("/edit/<int:assignment_id>", methods=["GET", "POST"])
def edit(assignment_id):
    """F4: Ödev düzenleme."""
    odev = database.get_assignment(assignment_id)
    if odev is None:
        abort(404)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        course = request.form.get("course", "").strip()
        description = request.form.get("description", "").strip()
        due_date = request.form.get("due_date", "").strip()

        if not title or not due_date:
            flash("Başlık ve teslim tarihi zorunludur.", "hata")
            return render_template(
                "add.html", form=request.form,
                baslik="Ödevi Düzenle", buton="Güncelle",
            ), 400

        database.update_assignment(assignment_id, title, course, description, due_date)
        flash("Ödev güncellendi.", "basari")
        return redirect(url_for("index"))

    return render_template(
        "add.html", form=dict(odev),
        baslik="Ödevi Düzenle", buton="Güncelle",
    )


@app.route("/delete/<int:assignment_id>", methods=["POST"])
def delete(assignment_id):
    """F4: Ödev silme."""
    if database.delete_assignment(assignment_id):
        flash("Ödev silindi.", "basari")
        logger.info("Ödev silindi: id=%s", assignment_id)
    else:
        flash("Ödev bulunamadı.", "hata")
        logger.warning("Silinmek istenen ödev bulunamadı: id=%s", assignment_id)
    return redirect(url_for("index"))

@app.route("/health")
def health():
    """Sağlık kontrolü: uygulama ve veritabanı bağlantısı."""
    try:
        database.check_connection()
        return {"status": "ok", "database": "ok"}
    except Exception:
        logger.exception("Health check başarısız: veritabanına erişilemiyor")
        return {"status": "error", "database": "unreachable"}, 503


if __name__ == "__main__":
    app.run(debug=True)