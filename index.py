import csv
import os

FILE = "data.csv"

if not os.path.exists(FILE):
    with open(FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "nominal", "keterangan", "rating"])

def load_data():
    data = []
    with open(FILE, "r") as f:
        reader = csv.DictReader(f)
        for r in reader:
            data.append({
                "id": int(r["id"]),
                "nominal": float(r["nominal"]),
                "keterangan": r["keterangan"],
                "rating": int(r["rating"])
            })
    return data


def save_data(data):
    with open(FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "nominal", "keterangan", "rating"])
        writer.writeheader()
        writer.writerows(data)


def status_item(r):
    if r <= 4: return "😞 Kecewa"
    if r <= 7: return "🙂 Biasa"
    return "😍 Senang"


def status_total(avg):
    if avg <= 4: return "😢 Sangat Kecewa"
    if avg <= 7: return "🙂 Cukup Puas"
    return "😍 Sangat Senang"


def buat_tabel(data):
    rows = [
        ["ID", "Nominal", "Keterangan", "Rating", "Status"]
    ]

    for d in data:
        rows.append([
            d["id"],
            f"Rp{d['nominal']:.0f}",
            d["keterangan"],
            d["rating"],
            status_item(d["rating"])
        ])

    col_widths = [max(len(str(row[i])) for row in rows) for i in range(len(rows[0]))]

    tabel = ""
    for row in rows:
        line = " | ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(row)))
        tabel += line + "\n"
    return tabel


def tambah():
    data = load_data()

    try:
        nominal = float(input("Nominal: "))
    except:
        print("Nominal harus angka!")
        return

    ket = input("Keterangan: ")

    try:
        rating = int(input("Rating (1-10): "))
        if not 1 <= rating <= 10:
            print("Rating harus 1-10!")
            return
    except:
        print("Rating harus angka!")
        return

    data.append({
        "id": len(data) + 1,
        "nominal": nominal,
        "keterangan": ket,
        "rating": rating
    })

    save_data(data)
    print("✓ Pengeluaran ditambahkan.")


def lihat():
    data = load_data()

    if not data:
        print("Belum ada pengeluaran.")
        return

    print("\n===== DAFTAR PENGELUARAN =====\n")
    print(buat_tabel(data))

    total_nominal = sum(d["nominal"] for d in data)
    total_rating = sum(d["rating"] for d in data)
    avg = total_rating / len(data)

    print(f"Total Pengeluaran : Rp{total_nominal:.0f}")
    print(f"Rata-rata Rating  : {avg:.1f}   {status_total(avg)}\n")


def hapus():
    data = load_data()

    try:
        id_del = int(input("ID yang dihapus: "))
    except:
        print("ID harus angka!")
        return

    baru = [d for d in data if d["id"] != id_del]

    if len(baru) == len(data):
        print("ID tidak ditemukan.")
        return

    for i, d in enumerate(baru):
        d["id"] = i + 1

    save_data(baru)
    print("✓ Pengeluaran dihapus.")



while True:
    print("\n=== Tracker Pengeluaran Anak Kost ===")
    print("1. Tambah Pengeluaran")
    print("2. Lihat Pengeluaran")
    print("3. Hapus Pengeluaran")
    print("4. Keluar")

    pilih = input("Pilih (1-4): ")

    if pilih == "1":
        tambah()
    elif pilih == "2":
        lihat()
    elif pilih == "3":
        hapus()
    elif pilih == "4":
        print("Sampai jumpa!")
        break
    else:
        print("Pilihan tidak valid!")
