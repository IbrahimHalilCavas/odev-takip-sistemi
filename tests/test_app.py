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
    assert yanit.get_json() == {"status": "ok"}


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