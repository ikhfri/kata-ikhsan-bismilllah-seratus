import json
import os

# === Fungsi bantu untuk membaca & menyimpan data ===
def load_data():
    if os.path.exists("data_ktp.json"):
        with open("data_ktp.json", "r") as file:
            return json.load(file)
    else:
        return {"penduduk": []}

def save_data(data):
    with open("data_ktp.json", "w") as file:
        json.dump(data, file, indent=4)

# === Fungsi CRUD ===
def tambah_penduduk():
    data = load_data()
    nik = input("Masukkan NIK: ")

    # Cek apakah NIK sudah ada
    if any(p["nik"] == nik for p in data["penduduk"]):
        print("❌ NIK sudah terdaftar! Gunakan NIK lain.")
        return

    nama = input("Masukkan nama lengkap: ")
    asal = input("Masukkan asal daerah: ")
    umur = input("Masukkan umur: ")

    data["penduduk"].append({
        "nik": nik,
        "nama": nama,
        "asal": asal,
        "umur": umur
    })

    save_data(data)
    print(f"✅ Data penduduk {nama} berhasil ditambahkan!")

def lihat_penduduk():
    data = load_data()
    if not data["penduduk"]:
        print("⚠ Belum ada data penduduk.")
        return

    print("=== DAFTAR DATA PENDUDUK ===")
    for i, p in enumerate(data["penduduk"], start=1):
        print(f"{i}. NIK: {p['nik']} | Nama: {p['nama']} | Asal: {p['asal']} | Umur: {p['umur']}")
    print()

def ubah_data_penduduk():
    data = load_data()
    nik = input("Masukkan NIK penduduk yang ingin diubah datanya: ")

    for p in data["penduduk"]:
        if p["nik"] == nik:
            print("=== Data Ditemukan ===")
            print(f"NIK  : {p['nik']}")
            print(f"Nama : {p['nama']}")
            print(f"Asal : {p['asal']}")
            print(f"Umur : {p['umur']}")
            print("======================")

            print("Pilih data yang ingin diubah:")
            print("1. NIK")
            print("2. Nama")
            print("3. Asal Daerah")
            print("4. Umur")
            print("5. Batalkan")

            pilihan = input("Masukkan pilihan (1-5): ")

            if pilihan == "1":
                nik_baru = input("Masukkan NIK baru: ")

                # Cek agar tidak ada NIK yang duplikat
                if any(x["nik"] == nik_baru for x in data["penduduk"]):
                    print("❌ Gagal! NIK baru sudah terdaftar di sistem.")
                    return
                p["nik"] = nik_baru
                print("✅ NIK berhasil diubah!")

            elif pilihan == "2":
                p["nama"] = input("Masukkan nama baru: ")
                print("✅ Nama berhasil diubah!")

            elif pilihan == "3":
                p["asal"] = input("Masukkan asal daerah baru: ")
                print("✅ Asal daerah berhasil diubah!")

            elif pilihan == "4":
                p["umur"] = input("Masukkan umur baru: ")
                print("✅ Umur berhasil diubah!")

            elif pilihan == "5":
                print("❌ Perubahan dibatalkan.")
                return
            else:
                print("Pilihan tidak valid.")
                return

            save_data(data)
            print("✅ Semua perubahan telah disimpan ke database!\n")
            return

    print("❌ NIK tidak ditemukan!\n")


def hapus_penduduk():
    data = load_data()
    nik = input("Masukkan NIK penduduk yang ingin dihapus: ")
    for p in data["penduduk"]:
        if p["nik"] == nik:
            data["penduduk"].remove(p)
            save_data(data)
            print(f"🗑 Data penduduk {p['nama']} berhasil dihapus!")
            return
    print("❌ NIK tidak ditemukan!")

# === Menu Utama ===
while True:
    print("===== SISTEM DATA KTP (CRUD) =====")
    print("1. Tambah Penduduk (Create)")
    print("2. Lihat Semua Penduduk (Read)")
    print("3. Ubah Data KTP (Update)")
    print("4. Hapus Data Penduduk (Delete)")
    print("5. Keluar")

    pilihan = input("Pilih menu (1/2/3/4/5): ")

    if pilihan == "1":
        tambah_penduduk()
    elif pilihan == "2":
        lihat_penduduk()
    elif pilihan == "3":
        ubah_data_penduduk()
    elif pilihan == "4":
        hapus_penduduk()
    elif pilihan == "5":
        print("Program selesai. Data tersimpan di file data_ktp.json ✅")
        break
    else:
        print("Pilihan tidak valid!")