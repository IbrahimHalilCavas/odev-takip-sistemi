"""F6: Takvim entegrasyonu – iCalendar (.ics) dosyası ve Google Takvim bağlantısı."""
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

TAMAMLANDI = "Teslim Edildi"


def _tarih(due_date):
    """'2026-11-27' metnini tarih nesnesine çevirir."""
    return datetime.strptime(due_date, "%Y-%m-%d").date()


def _kacis(metin):
    """iCalendar'da özel anlamı olan karakterleri kaçışla yazar (RFC 5545)."""
    return (
        metin.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\r\n", "\\n")
        .replace("\n", "\\n")
    )


def _katla(satir):
    """75 bayttan uzun satırları RFC 5545'e göre böler.
    Türkçe karakterler (ş, ğ, ü...) 2 bayt tuttuğu için karakter değil bayt sayılır."""
    parcalar, mevcut, uzunluk, sinir = [], "", 0, 75
    for karakter in satir:
        bayt = len(karakter.encode("utf-8"))
        if uzunluk + bayt > sinir:
            parcalar.append(mevcut)
            mevcut, uzunluk, sinir = "", 0, 74  # devam satırı bir boşlukla başlar
        mevcut += karakter
        uzunluk += bayt
    parcalar.append(mevcut)
    return "\r\n ".join(parcalar)


def takvim_olustur(odevler, simdi=None):
    """Teslim edilmemiş ödevlerden iCalendar (.ics) metni üretir.
    Her ödev tüm gün süren bir etkinlik olur ve teslimden önceki gün
    saat 09:00'da hatırlatma içerir."""
    if simdi is None:
        simdi = datetime.now(timezone.utc)
    damga = simdi.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    satirlar = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Odev Takip Sistemi//TR",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:Ödevlerim",
    ]

    for odev in odevler:
        if odev["status"] == TAMAMLANDI:
            continue  # Teslim edilmiş ödev için hatırlatmaya gerek yok

        teslim = _tarih(odev["due_date"])
        baslik = _kacis(odev["title"])
        ders = _kacis(odev["course"] or "")
        ozet = f"Ödev teslimi: {baslik}" + (f" ({ders})" if ders else "")
        aciklama = f"Durum: {odev['status']}"
        if odev["description"]:
            aciklama += "\\n" + _kacis(odev["description"])

        satirlar += [
            "BEGIN:VEVENT",
            f"UID:odev-{odev['id']}@odev-takip-sistemi",
            f"DTSTAMP:{damga}",
            f"DTSTART;VALUE=DATE:{teslim:%Y%m%d}",
            f"DTEND;VALUE=DATE:{teslim + timedelta(days=1):%Y%m%d}",
            f"SUMMARY:{ozet}",
            f"DESCRIPTION:{aciklama}",
            "BEGIN:VALARM",
            "ACTION:DISPLAY",
            f"DESCRIPTION:Yarın teslim: {baslik}",
            "TRIGGER:-PT15H",  # Gün başı (00:00) - 15 saat = önceki gün 09:00
            "END:VALARM",
            "END:VEVENT",
        ]

    satirlar.append("END:VCALENDAR")
    return "\r\n".join(_katla(s) for s in satirlar) + "\r\n"


def google_takvim_linki(odev):
    """Ödevi tek tıkla Google Takvim'e ekleyen bağlantıyı üretir."""
    teslim = _tarih(odev["due_date"])
    parametreler = {
        "action": "TEMPLATE",
        "text": f"Ödev teslimi: {odev['title']}",
        "dates": f"{teslim:%Y%m%d}/{teslim + timedelta(days=1):%Y%m%d}",
        "details": odev["description"] or "Öğrenci Ödev Takip Sistemi",
    }
    return "https://calendar.google.com/calendar/render?" + urlencode(parametreler)