import pytest

import database
from app import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Her test için geçici, boş bir veritabanı ve test istemcisi hazırlar."""
    monkeypatch.setattr(database, "DB_PATH", str(tmp_path / "test.db"))
    database.init_db()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint_ok_doner(client):
    yanit = client.get("/health")
    assert yanit.status_code == 200
    assert yanit.get_json() == {"status": "ok", "database": "ok"}


def test_bos_basliklu_odev_eklenemez(client):
    yanit = client.post("/add", data={"title": "", "due_date": "2026-12-01"})
    assert yanit.status_code == 400
    assert database.count_assignments() == 0


def test_gecerli_odev_eklenir_ve_listede_gorunur(client):
    client.post(
        "/add",
        data={"title": "DevOps Raporu", "course": "Bulut", "due_date": "2026-12-01"},
    )
    assert database.count_assignments() == 1

    yanit = client.get("/")
    assert "DevOps Raporu" in yanit.get_data(as_text=True)


def test_gecersiz_durum_reddedilir(client):
    database.add_assignment("Test Ödevi", "", "", "2026-12-01")
    odev = database.get_assignments()[0]

    client.post(f"/status/{odev['id']}", data={"status": "Hacklendi"})

    assert database.get_assignment(odev["id"])["status"] == "Bekliyor"


def test_odev_silinir(client):
    database.add_assignment("Silinecek Ödev", "", "", "2026-12-01")
    odev = database.get_assignments()[0]

    client.post(f"/delete/{odev['id']}")

    assert database.count_assignments() == 0

    

def test_durum_guncellemesinden_sonra_filtre_korunur(client):
    database.add_assignment("Filtre Testi", "", "", "2026-12-01")
    odev = database.get_assignments()[0]

    yanit = client.post(
        f"/status/{odev['id']}",
        data={"status": "Teslim Edildi", "filtre": "Bekliyor"},
    )

    assert yanit.status_code == 302
    assert "status=Bekliyor" in yanit.headers["Location"]

    

def test_veritabani_erisilemezse_health_503_doner(client, monkeypatch):
    def hata_ver():
        raise RuntimeError("veritabanına erişilemiyor")

    monkeypatch.setattr(database, "check_connection", hata_ver)

    yanit = client.get("/health")

    assert yanit.status_code == 503
    assert yanit.get_json()["status"] == "error"
    

def test_yanitlarda_guvenlik_basliklari_vardir(client):
    yanit = client.get("/health")

    assert yanit.headers["X-Content-Type-Options"] == "nosniff"
    assert yanit.headers["X-Frame-Options"] == "DENY"
    assert "Referrer-Policy" in yanit.headers


def test_cok_buyuk_istek_reddedilir(client):
    yanit = client.post(
        "/add",
        data={"title": "Büyük", "due_date": "2026-12-01", "description": "a" * 20000},
    )

    assert yanit.status_code == 413

    

def test_takvim_dosyasi_indirilir(client):
    database.add_assignment("Takvim Testi", "Bulut", "", "2026-12-01")

    yanit = client.get("/takvim.ics")

    assert yanit.status_code == 200
    assert yanit.mimetype == "text/calendar"
    assert "attachment" in yanit.headers["Content-Disposition"]
    assert "Takvim Testi" in yanit.get_data(as_text=True)

    

def test_takvim_sayfasi_sadece_teslim_edilmemis_odevleri_listeler(client):
    database.add_assignment("Listelenecek Ödev", "", "", "2026-12-01")
    database.add_assignment("Bitmiş Ödev", "", "", "2026-12-02")
    bitmis = [o for o in database.get_assignments() if o["title"] == "Bitmiş Ödev"][0]
    database.update_status(bitmis["id"], "Teslim Edildi")

    yanit = client.get("/takvim")
    sayfa = yanit.get_data(as_text=True)

    assert yanit.status_code == 200
    assert "Listelenecek Ödev" in sayfa
    assert "Bitmiş Ödev" not in sayfa
    assert "/takvim.ics" in sayfa