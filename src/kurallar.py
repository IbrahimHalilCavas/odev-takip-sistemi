from datetime import date, datetime

# Teslime kaç gün ve daha az kaldığında "Yaklaşıyor" uyarısı verilsin
YAKLASMA_GUN = 3


def teslim_uyarisi(due_date, status, bugun=None):
    """F5: Ödevin teslim durumuna göre uyarı döndürür.

    - Teslim edilmişse: None (uyarı yok)
    - Tarihi geçmişse: "Gecikti"
    - 3 gün veya daha az kaldıysa: "Yaklaşıyor"
    - Aksi halde: None
    """
    if status == "Teslim Edildi":
        return None

    if bugun is None:
        bugun = date.today()

    teslim_tarihi = datetime.strptime(due_date, "%Y-%m-%d").date()
    kalan_gun = (teslim_tarihi - bugun).days

    if kalan_gun < 0:
        return "Gecikti"
    if kalan_gun <= YAKLASMA_GUN:
        return "Yaklaşıyor"
    return None