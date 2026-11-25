"""Kanban kartlarını (GitHub Issues) HTML ve CSV olarak dışa aktarır.

Kullanım (proje ana klasöründe):
    python scripts/kanban_export.py

Çıktılar:
    kanban_export/Kanban_Kartlari.html  -> Tarayıcıda açıp Ctrl+P ile PDF olarak kaydedin
    kanban_export/Kanban_Kartlari.csv   -> Excel ile açılabilir

Depo herkese açık olduğu için GitHub hesabı veya şifre gerekmez.
Sadece Python'un kendi kütüphaneleri kullanılır.
"""
import csv
import html
import json
import re
import urllib.request
from datetime import datetime
from pathlib import Path

DEPO = "IbrahimHalilCavas/odev-takip-sistemi"
PANO = "https://github.com/users/IbrahimHalilCavas/projects/2"
API = (
    f"https://api.github.com/repos/{DEPO}/issues"
    "?state=all&per_page=100&sort=created&direction=asc"
)
CIKTI = Path("kanban_export")


def kartlari_getir():
    """GitHub'dan tüm issue'ları (Kanban kartlarını) çeker."""
    istek = urllib.request.Request(
        API,
        headers={
            # full+json: Markdown metnin yanında GitHub'ın hazırladığı HTML'i de getirir
            "Accept": "application/vnd.github.full+json",
            "User-Agent": "kanban-export-script",
        },
    )
    with urllib.request.urlopen(istek, timeout=30) as yanit:
        veriler = json.load(yanit)
    # Issues API'si pull request'leri de döndürür; sadece kartları al
    return [v for v in veriler if "pull_request" not in v]


def hafta(kart):
    """Başlıktaki 'W3' gibi hafta bilgisini sayı olarak döndürür."""
    eslesme = re.match(r"\s*W(\d+)", kart["title"])
    return int(eslesme.group(1)) if eslesme else 99


def durum(kart):
    return "Done" if kart["state"] == "closed" else "Açık"


def tarih(deger):
    if not deger:
        return "-"
    return datetime.strptime(deger, "%Y-%m-%dT%H:%M:%SZ").strftime("%d.%m.%Y")


def etiketler(kart):
    return ", ".join(e["name"] for e in kart.get("labels", [])) or "-"


def csv_yaz(kartlar, yol):
    with open(yol, "w", newline="", encoding="utf-8-sig") as dosya:
        yazici = csv.writer(dosya)
        yazici.writerow([
            "Numara", "Hafta", "Başlık", "Durum", "Etiketler",
            "Açılış", "Kapanış", "Bağlantı", "İçerik (Description / Acceptance Criteria / Evidence)",
        ])
        for k in kartlar:
            yazici.writerow([
                f"#{k['number']}",
                f"W{hafta(k)}" if hafta(k) != 99 else "-",
                k["title"],
                durum(k),
                etiketler(k),
                tarih(k.get("created_at")),
                tarih(k.get("closed_at")),
                k["html_url"],
                k.get("body") or "",
            ])


STIL = """
body { font-family: Arial, sans-serif; color: #222; max-width: 900px; margin: 24px auto; padding: 0 16px; font-size: 13px; }
h1 { margin-bottom: 4px; }
.alt { color: #555; margin-top: 0; }
table { border-collapse: collapse; width: 100%; margin: 12px 0; }
th, td { border: 1px solid #ccc; padding: 5px 7px; text-align: left; vertical-align: top; }
th { background: #f2f4f8; }
.kart { border: 1px solid #bbb; border-radius: 8px; padding: 10px 14px; margin: 16px 0; page-break-inside: avoid; }
.kart h2 { font-size: 16px; margin: 0 0 4px 0; }
.meta { color: #555; font-size: 12px; margin-bottom: 8px; }
.done { color: #1a7f37; font-weight: bold; }
.acik { color: #9a6700; font-weight: bold; }
.icerik h2 { font-size: 14px; border-bottom: 1px solid #ddd; padding-bottom: 2px; }
.icerik img { max-width: 100%; max-height: 260px; border: 1px solid #ddd; }
.icerik ul { padding-left: 20px; }
.icerik .task-list-item { list-style: none; margin-left: -18px; }
.ozet td:first-child { width: 220px; font-weight: bold; }
@media print { .kart { page-break-inside: avoid; } a { color: #222; } }
"""


def html_yaz(kartlar, yol):
    done = sum(1 for k in kartlar if durum(k) == "Done")
    satirlar = []
    for k in kartlar:
        sinif = "done" if durum(k) == "Done" else "acik"
        satirlar.append(
            f"<tr><td>#{k['number']}</td><td>{html.escape(k['title'])}</td>"
            f"<td>{html.escape(etiketler(k))}</td><td class='{sinif}'>{durum(k)}</td></tr>"
        )

    kart_bloklari = []
    for k in kartlar:
        sinif = "done" if durum(k) == "Done" else "acik"
        icerik = k.get("body_html") or f"<pre>{html.escape(k.get('body') or '')}</pre>"
        kart_bloklari.append(f"""
<div class="kart">
  <h2>#{k['number']} – {html.escape(k['title'])}</h2>
  <div class="meta">
    Durum: <span class="{sinif}">{durum(k)}</span> ·
    Etiketler: {html.escape(etiketler(k))} ·
    Açılış: {tarih(k.get('created_at'))} · Kapanış: {tarih(k.get('closed_at'))} ·
    <a href="{k['html_url']}">{k['html_url']}</a>
  </div>
  <div class="icerik">{icerik}</div>
</div>""")

    sayfa = f"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="UTF-8">
<title>Kanban Kartları – Öğrenci Ödev Takip Sistemi</title>
<style>{STIL}</style></head>
<body>
<h1>Kanban Görev Kartları</h1>
<p class="alt">Öğrenci Ödev Takip Sistemi – Modern Yazılım Mühendisliği: Bulut ve DevOps</p>

<table class="ozet">
  <tr><td>Geliştirici</td><td>İbrahim Halil Çavaş</td></tr>
  <tr><td>Kanban Panosu</td><td><a href="{PANO}">{PANO}</a></td></tr>
  <tr><td>GitHub Deposu</td><td><a href="https://github.com/{DEPO}">https://github.com/{DEPO}</a></td></tr>
  <tr><td>Toplam kart</td><td>{len(kartlar)} (Done: {done}, Açık: {len(kartlar) - done})</td></tr>
  <tr><td>Dışa aktarma tarihi</td><td>{datetime.now():%d.%m.%Y %H:%M}</td></tr>
</table>

<h2>Kart Listesi</h2>
<table>
  <tr><th>No</th><th>Başlık</th><th>Etiketler</th><th>Durum</th></tr>
  {''.join(satirlar)}
</table>

<h2>Kart Detayları (Description · Acceptance Criteria · Evidence)</h2>
{''.join(kart_bloklari)}
</body></html>"""
    yol.write_text(sayfa, encoding="utf-8")


def main():
    print("GitHub'dan Kanban kartları alınıyor...")
    kartlar = sorted(kartlari_getir(), key=lambda k: (hafta(k), k["number"]))
    CIKTI.mkdir(exist_ok=True)
    html_yaz(kartlar, CIKTI / "Kanban_Kartlari.html")
    csv_yaz(kartlar, CIKTI / "Kanban_Kartlari.csv")
    done = sum(1 for k in kartlar if durum(k) == "Done")
    print(f"{len(kartlar)} kart dışa aktarıldı (Done: {done}).")
    print(f"-> {CIKTI / 'Kanban_Kartlari.html'}  (tarayıcıda açıp Ctrl+P ile PDF kaydedin)")
    print(f"-> {CIKTI / 'Kanban_Kartlari.csv'}")


if __name__ == "__main__":
    main()
