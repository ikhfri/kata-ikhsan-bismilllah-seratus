import csv, os
from datetime import datetime

FILE = "data.csv"

if not os.path.exists(FILE):
    with open(FILE, "w", newline="") as f:
        csv.writer(f).writerow(["id", "tanggal", "nominal", "keterangan", "rating"])

def clear():
    os.system("cls" if os.name == "nt" else "clear")
def load():
    with open(FILE) as f:
        return [r for r in csv.DictReader(f)]

def save(data):
    with open(FILE, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "tanggal", "nominal", "keterangan", "rating"])
        w.writeheader()
        w.writerows(data)


def rating_status(r):
    r = int(r)
    if r <= 3:
        return "😭 Sangat Kecewa"
    elif r <= 6:
        return "🙂 Biasa Saja"
    elif r <= 8:
        return "😁 Puas"
    else:
        return "🤩 Sangat Puas"

def tabel(data):
    rows = [["🆔 ID","📆 Tanggal","💰 Nominal","📝 Keterangan","⭐ Rating","🎭 Status"]]
    
    for d in data:
        status = rating_status(d["rating"])
        rows.append([
            d["id"],
            d["tanggal"],
            f"Rp{float(d['nominal']):.0f}",
            d["keterangan"],
            d["rating"],
            status
        ])

    w = [max(len(str(r[i])) for r in rows) for i in range(len(rows[0]))]
    return "\n".join(" | ".join(str(r[i]).ljust(w[i]) for i in range(len(r))) for r in rows)

def tambah():
    data = load()

    print("\n💸 Tambah Pengeluaran")

    try:
        nominal = float(input("💰 Nominal: "))
    except:
        return print("❌ Nominal harus angka!")

    ket = input("📝 Keterangan: ")

    print("\n⭐ Beri Rating (1–10)")
    print(" 1–3  : 😭 Sangat Kecewa")
    print(" 4–6  : 🙂 Biasa Saja")
    print(" 7–8  : 😁 Puas")
    print(" 9–10 : 🤩 Sangat Puas")

    try:
        rating = int(input("⭐ Rating: "))
        if not 1 <= rating <= 10:
            return print("⚠️ Rating harus 1–10!")
    except:
        return print("❌ Rating harus angka!")

    data.append({
        "id": str(len(data)+1),
        "tanggal": datetime.now().strftime("%Y-%m-%d"),
        "nominal": nominal,
        "keterangan": ket,
        "rating": rating
    })

    save(data)
    clear()
    print("✅ Data berhasil ditambahkan!\n")

def update_data():
    data = load()
    clear()

    if not data:
        return print("📭 Belum ada data untuk diupdate.")

    print("\n✏️ DATA SAAT INI")
    print(tabel(data))
    print("\n")

    id_edit = input("🆔 Masukkan ID yang ingin diupdate: ")

    # Cek ID valid
    dlist = [d for d in data if d["id"] == id_edit]
    if not dlist:
        return print("❌ ID tidak ditemukan!\n")

    d = dlist[0]

    print("\n➡️ Tekan ENTER jika tidak ingin mengubah field.\n")

    new_nom = input(f"💰 Nominal ({d['nominal']}): ")
    if new_nom.strip() != "":
        try:
            d["nominal"] = float(new_nom)
        except:
            return print("❌ Nominal harus angka!")

    new_ket = input(f"📝 Keterangan ({d['keterangan']}): ")
    if new_ket.strip() != "":
        d["keterangan"] = new_ket

    new_rating = input(f"⭐ Rating ({d['rating']}): ")
    if new_rating.strip() != "":
        try:
            r = int(new_rating)
            if not 1 <= r <= 10:
                return print("⚠️ Rating harus 1–10!")
            d["rating"] = r
        except:
            return print("❌ Rating harus angka!")

    save(data)
    clear()
    print("\n✅ Data berhasil diupdate!\n")

def lihat(data=None):
    clear()
    data = load() if data is None else data
    if not data:
        return print("📭 Belum ada data.")

    print("\n📊 TABEL PENGELUARAN")
    print(tabel(data))

    total = sum(float(d["nominal"]) for d in data)
    avg = sum(int(d["rating"]) for d in data) / len(data)
    status = rating_status(avg)

    print(f"\n📌 Total Pengeluaran: 💰 Rp{total:.0f}")
    print(f"📌 Rata-rata Rating: ⭐ {avg:.1f} — {status}\n")

def lihat_hari():
    t = input("📅 Masukkan tanggal (YYYY-MM-DD): ")
    data = [d for d in load() if d["tanggal"] == t]

    if not data:
        return print("❌ Tidak ada data tanggal tersebut.")

    lihat(data)

def hapus():
    data = load()
    clear()

    if not data:
        return print("📭 Belum ada data untuk dihapus.")

    print("\n📊 DATA SAAT INI")
    print(tabel(data))
    print("\n")

    id_del = input("🆔 Masukkan ID yang ingin dihapus: ")

    if id_del not in [d["id"] for d in data]:
        return print("❌ ID tidak ditemukan!\n")

    data = [d for d in data if d["id"] != id_del]

    for i, d in enumerate(data):
        d["id"] = str(i+1)

    save(data)
    clear()
    print("🗑️ Data berhasil dihapus!\n")

def mood_header_hari_ini():
    data = load()
    today = datetime.now().strftime("%Y-%m-%d")

    # Filter hanya data hari ini
    today_data = [d for d in data if d["tanggal"] == today]

    if not today_data:
        return f"🎭 Mood Hari Ini: - (Belum ada data untuk {today})"

    avg = sum(int(d["rating"]) for d in today_data) / len(today_data)

    if avg <= 4:
        return f"🎭 Mood Hari Ini: 😭 {avg:.1f} — Sangat Kecewa"
    elif avg <= 6:
        return f"🎭 Mood Hari Ini: 🙂 {avg:.1f} — Biasa Saja"
    elif avg <= 8:
        return f"🎭 Mood Hari Ini: 😁 {avg:.1f} — Puas"
    else:
        return f"🎭 Mood Hari Ini: 🤩 {avg:.1f} — Sangat Puas"
    
def ranking_kategori():
    data = load()
    clear()

    if not data:
        print("📭 Belum ada data.")
        return

    kategori_map = {}

    for d in data:
        ket = d["keterangan"].strip().lower()
        rating = int(d["rating"])

        if ket not in kategori_map:
            kategori_map[ket] = []
        kategori_map[ket].append(rating)

    ranking = []
    for ket, ratings in kategori_map.items():
        avg = sum(ratings) / len(ratings)
        ranking.append((ket, avg, len(ratings)))

    # Fungsi sorting 
    def ambil_rata(item):
        return item[1]

    ranking.sort(key=ambil_rata, reverse=True)

    print("\n🏆 RANKING KATEGORI BERDASARKAN MOOD RATA-RATA\n")
    print("Kategori | Rata-rata | Jumlah Data")
    print("-----------------------------------")

    for ket, avg, count in ranking:
        print(f"{ket.capitalize():<15} ⭐ {avg:.2f}   ({count}x)")

    print("\n")


while True:
    print("\n============================")
    print("💵 **MOODSPENDER** 💵")
    print("============================")
    print(mood_header_hari_ini())
    print("============================")
    print("""--------------------------
|                        |
|   (1) Tambah Data      |
|                        |
--------------------------""")
    print("""--------------------------
|                        |
|    (2) Update Data     |
|                        |
--------------------------""")
    print("""--------------------------
|                        |
|    (3) Lihat Semua     |
|                        |
--------------------------""")
    print("""--------------------------
|                        |
|     (4) Hapus Data     |
|                        |
--------------------------""")
    print("""--------------------------
|                        |
|   (5) Ranking Mood     |
|         Kategori       |
|                        |
--------------------------""")
    print("""--------------------------
|                        |
|   (6) Lihat Per Hari   |
|                        |
--------------------------""")
    print("""--------------------------
|                        |
|       (7) Keluar       |
|                        |
--------------------------""")

    print("============================")

    p = input("👉 Pilih menu: ")

    if p == "1":
        clear()
        tambah()

    elif p == "2":
        clear()
        update_data()

    elif p == "3":
        clear()
        lihat()

    elif p == "4":
        clear()
        hapus()

    elif p == "5":
        clear()
        ranking_kategori()

    elif p == "6":
        clear()
        lihat_hari()

    elif p == "7":
       print("👋 Keluar... Sampai jumpa!\n")
       break

    else:
        print("❌ Pilihan tidak dikenal!")

