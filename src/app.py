import os
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for

import database

app = Flask(__name__)
# Flash mesajları için gizli anahtar. Canlı ortamda ortam değişkeninden okunacak.
app.secret_key = os.environ.get("SECRET_KEY", "gelistirme-anahtari")

# Uygulama açılırken tablo yoksa oluştur
database.init_db()


@app.template_filter("tarih")
def tarih_formatla(deger):
    """2026-11-20 biçimindeki tarihi 20.11.2026 olarak gösterir."""
    return datetime.strptime(deger, "%Y-%m-%d").strftime("%d.%m.%Y")


@app.route("/")
def index():
    """F2: Ödevleri listeleme."""
    odevler = database.get_assignments()
    return render_template("index.html", odevler=odevler)


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
            flash("Başlık ve teslim tarihi zorunludur.", "hata")
            return render_template("add.html", form=request.form), 400

        database.add_assignment(title, course, description, due_date)
        flash(
            f"Ödev eklendi! Toplam ödev sayısı: {database.count_assignments()}",
            "basari",
        )
        return redirect(url_for("index"))

    return render_template("add.html", form={})


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True)