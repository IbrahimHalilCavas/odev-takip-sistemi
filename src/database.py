import os
import sqlite3

# Veritabanı dosyasının yolu.
# Ortam değişkeniyle değiştirilebilir (testler, Docker ve Cloud için).
DB_PATH = os.environ.get(
    "DB_PATH", os.path.join(os.path.dirname(__file__), "odevler.db")
)

# Ödevin alabileceği durumlar
DURUMLAR = ["Bekliyor", "Devam Ediyor", "Teslim Edildi"]


def get_connection():
    """SQLite bağlantısı açar. Satırlara sütun adıyla erişilebilir."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """assignments tablosu yoksa oluşturur."""
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            course TEXT,
            description TEXT,
            due_date DATE NOT NULL,
            status TEXT NOT NULL DEFAULT 'Bekliyor',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def add_assignment(title, course, description, due_date):
    """F1: Yeni ödev ekler."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO assignments (title, course, description, due_date) "
        "VALUES (?, ?, ?, ?)",
        (title, course, description, due_date),
    )
    conn.commit()
    conn.close()


def count_assignments():
    """Kayıtlı ödev sayısını döndürür."""
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) FROM assignments").fetchone()[0]
    conn.close()
    return count




def get_assignments(status=None):
    """F2 + F3: Ödevleri teslim tarihine göre sıralı döndürür.
    status verilirse sadece o durumdaki ödevleri getirir."""
    conn = get_connection()
    if status:
        rows = conn.execute(
            "SELECT * FROM assignments WHERE status = ? ORDER BY due_date ASC",
            (status,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM assignments ORDER BY due_date ASC"
        ).fetchall()
    conn.close()
    return rows


def update_status(assignment_id, status):
    """F3: Ödevin durumunu günceller. Geçersiz durumda False döndürür."""
    if status not in DURUMLAR:
        return False
    conn = get_connection()
    cursor = conn.execute(
        "UPDATE assignments SET status = ? WHERE id = ?",
        (status, assignment_id),
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0