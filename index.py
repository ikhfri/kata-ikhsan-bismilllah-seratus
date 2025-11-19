import csv
from datetime import datetime
import os

FILE = "data.csv"
HEADER = ["tanggal", "jumlah", "kategori", "mood", "deskripsi"]

if not os.path.exists(FILE):
    f = open(FILE, "w", newline="", encoding="utf-8")
    writer = csv.writer(f)
    writer.writerow(HEADER)
    f.close()

def tambah_data():
    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M")
    jumlah = input("Nominal (Rp): ")
    kategori = input("Kategori: ")
    mood = input("Mood: ")
    deskripsi = input("Deskripsi: ")

    f = open(FILE, "a", newline="", encoding="utf-8")
    writer = csv.writer(f)
    writer.writerow([tanggal, jumlah, kategori, mood, deskripsi])
    f.close()
    print("✅ Data berhasil ditambahkan!\n")

def lihat_data():
    f = open(FILE, "r", encoding="utf-8")
    reader = csv.reader(f)
    next(reader)
    data = list(reader)
    f.close()

    if not data:
        print("Belum ada data.\n")
        return

    total = 0
    for i, row in enumerate(data, 1):
        tanggal, jumlah, kategori, mood, deskripsi = row
        total += float(jumlah)
        print(f"{i}. [{tanggal}] Rp{jumlah} - {kategori} - {mood} - {deskripsi}")

    print(f"\n💰 Total pengeluaran: Rp{total:,.0f}\n")

def ubah_data():
    lihat_data()
    nomor = int(input("Pilih nomor data yang ingin diubah: ")) - 1

    f = open(FILE, "r", encoding="utf-8")
    reader = list(csv.reader(f))
    f.close()

    if nomor + 1 >= len(reader):
        print("❌ Nomor tidak valid!\n")
        return

    new_mood = input("Mood baru: ")
    new_harga= input("ganti harga: ")
    new_desc = input("Deskripsi baru: ")

    reader[nomor + 1][1] = new_harga or reader[nomor + 1][1]
    reader[nomor + 1][3] = new_mood or reader[nomor + 1][3]
    reader[nomor + 1][4] = new_desc or reader[nomor + 1][4]

    f = open(FILE, "w", newline="", encoding="utf-8")
    writer = csv.writer(f)
    writer.writerows(reader)
    f.close()
    print("✅ Data berhasil diubah!\n")

def hapus_data():
    lihat_data()
    nomor = int(input("Pilih nomor data yang ingin dihapus: ")) - 1

    f = open(FILE, "r", encoding="utf-8")
    reader = list(csv.reader(f))
    f.close()

    if nomor + 1 >= len(reader):
        print("❌ Nomor tidak valid!\n")
        return

    del reader[nomor + 1]

    f = open(FILE, "w", newline="", encoding="utf-8")
    writer = csv.writer(f)
    writer.writerows(reader)
    f.close()
    print("🗑 Data berhasil dihapus!\n")

while True:
    print("=== Budget x Emotion Tracker ===")
    print("1. Tambah Data")
    print("2. Lihat Data")
    print("3. Ubah Data")
    print("4. Hapus Data")
    print("5. Keluar")
    pilih = input("Pilih menu (1-5): ")

    if pilih == "1":
        tambah_data()
    elif pilih == "2":
        lihat_data()
    elif pilih == "3":
        ubah_data()
    elif pilih == "4":
        hapus_data()
    elif pilih == "5":
        print("Sampai jumpa! 💚")
        break
    else:
        print("Pilihan tidak valid!\n")