from datetime import datetime, timezone
from urllib.parse import parse_qs, urlparse

from takvim import google_takvim_linki, takvim_olustur

# Testlerde "şimdi" sabit: sonuçlar her gün aynı olsun
SIMDI = datetime(2026, 11, 25, 8, 0, tzinfo=timezone.utc)


def ornek_odev(**degisiklikler):
    """Testler için örnek bir ödev üretir; istenen alanlar değiştirilebilir."""
    odev = {
        "id": 1,
        "title": "Final Sunumu",
        "course": "Bulut ve DevOps",
        "description": "",
        "due_date": "2026-11-27",
        "status": "Bekliyor",
    }
    odev.update(degisiklikler)
    return odev


def test_takvim_dosyasi_gecerli_yapidadir():
    ics = takvim_olustur([ornek_odev()], simdi=SIMDI)

    assert ics.startswith("BEGIN:VCALENDAR\r\n")
    assert ics.endswith("END:VCALENDAR\r\n")
    assert ics.count("BEGIN:VEVENT") == 1


def test_etkinlik_tarihi_ve_hatirlatma_dogrudur():
    ics = takvim_olustur([ornek_odev()], simdi=SIMDI)

    assert "DTSTART;VALUE=DATE:20261127" in ics
    assert "DTEND;VALUE=DATE:20261128" in ics
    assert "TRIGGER:-PT15H" in ics


def test_teslim_edilmis_odev_takvime_eklenmez():
    ics = takvim_olustur(
        [ornek_odev(id=1), ornek_odev(id=2, status="Teslim Edildi")],
        simdi=SIMDI,
    )

    assert ics.count("BEGIN:VEVENT") == 1
    assert "UID:odev-2@" not in ics


def test_ozel_karakterler_kacisla_yazilir():
    ics = takvim_olustur([ornek_odev(title="Rapor; bölüm 1, 2")], simdi=SIMDI)

    assert "Rapor\\; bölüm 1\\, 2" in ics


def test_uzun_satirlar_75_bayti_gecmez():
    ics = takvim_olustur([ornek_odev(title="Ş" * 100)], simdi=SIMDI)

    for satir in ics.split("\r\n"):
        assert len(satir.encode("utf-8")) <= 75


def test_google_takvim_linki_dogru_bilgileri_icerir():
    link = google_takvim_linki(ornek_odev())
    parametreler = parse_qs(urlparse(link).query)

    assert link.startswith("https://calendar.google.com/")
    assert parametreler["text"] == ["Ödev teslimi: Final Sunumu"]
    assert parametreler["dates"] == ["20261127/20261128"]