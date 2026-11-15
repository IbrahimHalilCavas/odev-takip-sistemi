from datetime import date

from kurallar import teslim_uyarisi

# Testlerde "bugün" sabit: hangi gün çalıştırılırsa çalıştırılsın sonuç aynı olur.
BUGUN = date(2026, 11, 15)


def test_tarihi_gecmis_odev_gecikti_olarak_isaretlenir():
    assert teslim_uyarisi("2026-11-10", "Bekliyor", bugun=BUGUN) == "Gecikti"


def test_uc_gun_icindeki_odev_yaklasiyor_olarak_isaretlenir():
    assert teslim_uyarisi("2026-11-17", "Bekliyor", bugun=BUGUN) == "Yaklaşıyor"


def test_teslim_gunu_bugun_olan_odev_yaklasiyor_olarak_isaretlenir():
    assert teslim_uyarisi("2026-11-15", "Devam Ediyor", bugun=BUGUN) == "Yaklaşıyor"


def test_uzak_tarihli_odevde_uyari_yoktur():
    assert teslim_uyarisi("2026-12-30", "Bekliyor", bugun=BUGUN) is None


def test_teslim_edilmis_odevde_tarihi_gecse_bile_uyari_yoktur():
    assert teslim_uyarisi("2026-11-01", "Teslim Edildi", bugun=BUGUN) is None