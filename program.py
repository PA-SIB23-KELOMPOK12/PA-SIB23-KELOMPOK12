import mysql.connector
from prettytable import PrettyTable
import pwinput
from datetime import datetime


# Fungsi untuk membuat koneksi ke database
def connect_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            # password="password",
            database="climate_care"
        )
        return conn
    except mysql.connector.Error as err:
        print("Error:", err)
        return None
    
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    def display(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next

# Kelas untuk entitas tren_iklim
class TrenIklim:
    def __init__(self, conn):
        self.conn = conn
        self.data = LinkedList()

    # Method untuk menampilkan semua data tren_iklim
    def show_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tren_iklim")
        result = cursor.fetchall()

        if result:
            table = PrettyTable()
            table.field_names = ["ID tren iklim", "Tanggal", "Curah Hujan", "Suhu", "Kelembaban"]
            for row in result:
                table.add_row(row)
            print(table)
        else:
            print("Tidak ada data tren_iklim yang ditemukan.")      

    # # Method untuk menambahkan data tren_iklim baru
    def tambah_data(self, id_tren_iklim, tanggal, curah_hujan, suhu, kelembaban):
        cursor = self.conn.cursor()
        # Periksa apakah data dengan nilai yang sama sudah ada dalam database
        cursor.execute("SELECT * FROM tren_iklim WHERE tanggal = %s AND curah_hujan = %s AND suhu = %s AND kelembaban = %s", (tanggal, curah_hujan, suhu, kelembaban))
        result = cursor.fetchone()
        if result:
            print("Data tren iklim dengan nilai yang sama sudah ada dalam database.")
            return

        # Jika data belum ada, lakukan penambahan
        sql = "INSERT INTO tren_iklim (id_tren_iklim, tanggal, curah_hujan, suhu, kelembaban) VALUES (%s, %s, %s, %s, %s)"
        val = (id_tren_iklim, tanggal, curah_hujan, suhu, kelembaban)
        cursor.execute(sql, val)
        self.conn.commit()
        print("Data tren iklim berhasil ditambahkan.")  

    # Method untuk menghapus data tren iklim berdasarkan ID
    def hapus_data(self, id_tren_iklim):
        cursor = self.conn.cursor()
        sql = "DELETE FROM tren_iklim WHERE id_tren_iklim = %s"
        cursor.execute(sql, (id_tren_iklim,))
        self.conn.commit()
        print("Data tren iklim berhasil dihapus.")
        cursor.close()

    def search_by_date(self, tanggal):
        cursor = self.conn.cursor()
        sql = "SELECT * FROM tren_iklim WHERE tanggal = %s"
        cursor.execute(sql, (tanggal,))
        result = cursor.fetchall()

        if result:
            table = PrettyTable()
            table.field_names = ["ID tren iklim", "Tanggal", "Curah Hujan", "Suhu", "Kelembaban"]
            for row in result:
                table.add_row(row)
            print(table)
        else:
            print("Tren iklim dengan tanggal tersebut tidak ditemukan.")

    def update_data(self, id_tren_iklim, tanggal, curah_hujan, suhu, kelembaban):
        cursor = self.conn.cursor()
        # Periksa apakah data dengan ID yang dimasukkan sudah ada dalam database
        cursor.execute("SELECT * FROM tren_iklim WHERE id_tren_iklim = %s", (id_tren_iklim,))
        result = cursor.fetchone()
        if not result:
            print("Data tren iklim dengan ID yang dimasukkan tidak ditemukan.")
            return

        # Periksa apakah data baru akan menyebabkan duplikasi dengan data lain
        cursor.execute("SELECT * FROM tren_iklim WHERE id_tren_iklim != %s AND tanggal = %s AND curah_hujan = %s AND suhu = %s AND kelembaban = %s",
                       (id_tren_iklim, tanggal, curah_hujan, suhu, kelembaban))
        duplicate_result = cursor.fetchone()
        if duplicate_result:
            print("Data tren iklim yang ingin Anda perbarui memiliki nilai yang sama dengan nilai yang sudah ada dalam database\nHal itu akan menyebabkan duplikasi data.")
            return

        # Lakukan pembaruan data
        sql = "UPDATE tren_iklim SET tanggal = %s, curah_hujan = %s, suhu = %s, kelembaban = %s WHERE id_tren_iklim = %s"
        val = (tanggal, curah_hujan, suhu, kelembaban, id_tren_iklim)
        cursor.execute(sql, val)
        self.conn.commit()
        print("Data tren iklim berhasil diperbarui.")

    def sort_by_date(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tren_iklim")
        result = cursor.fetchall()
        data_list = list(result)
        self.quicksort_by_date(data_list, 0, len(data_list) - 1)  # Memanggil metode quicksort
        sorted_table = PrettyTable()
        sorted_table.field_names = ["ID tren iklim", "Tanggal", "Curah Hujan", "Suhu", "Kelembaban"]
        for row in data_list:  # Tidak perlu menggunakan reversed() karena quicksort sudah mengurutkan secara ascending
            sorted_table.add_row(row)
        print(sorted_table)

    def partition_by_date(self, array, low, high):
        pivot_date = datetime.strptime(array[high][1], "%d/%m/%Y")  # Mengonversi string tanggal menjadi objek datetime
        i = low - 1
        for j in range(low, high):
            current_date = datetime.strptime(array[j][1], "%d/%m/%Y")
            if current_date >= pivot_date:  # Mengubah tanda perbandingan untuk mengurutkan secara descending
                i += 1
                array[i], array[j] = array[j], array[i]
        array[i + 1], array[high] = array[high], array[i + 1]
        return i + 1

    def quicksort_by_date(self, array, low, high):
        if low < high:
            pi = self.partition_by_date(array, low, high)
            self.quicksort_by_date(array, low, pi - 1)
            self.quicksort_by_date(array, pi + 1, high)

class User:
    def __init__(self, conn):
        self.conn = conn
        self.data = LinkedList()

    def show_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user")
        result = cursor.fetchall()

        if result:
            table = PrettyTable()
            table.field_names = ["Nama", "ID User", "Alamat", "E-mail", "No Telepon"]
            for row in result:
                table.add_row(row)
            print(table)
        else:
            print("Tidak ada data tentang user yang ditemukan.")

    def add_data(self, nama_user, alamat_user, email_user, no_hp):
        cursor = self.conn.cursor()
        
        # Cek apakah email atau nomor telepon sudah ada dalam database
        cursor.execute("SELECT * FROM user WHERE email_user = %s OR no_hp = %s", (email_user, no_hp))
        result = cursor.fetchone()
        if result:
            existing_email = result[3]  # Ambil email yang sudah terdaftar
            existing_no_hp = result[4]   # Ambil nomor telepon yang sudah terdaftar
            if existing_email == email_user:
                print("Email sudah terdaftar. Silakan gunakan email lain.")
            if existing_no_hp == no_hp:
                print("Nomor telepon sudah terdaftar. Silakan gunakan nomor telepon lain.")
            return None  # Kembalikan None untuk menandakan bahwa penambahan data gagal
        
        # Jika email dan nomor telepon belum terdaftar, tambahkan data baru
        sql = "INSERT INTO user (nama_user, alamat_user, email_user, no_hp) VALUES (%s, %s, %s, %s)"
        val = (nama_user, alamat_user, email_user, no_hp)
        cursor.execute(sql, val)
        self.conn.commit()
        id_user = cursor.lastrowid 
        print("Data user berhasil ditambahkan.")
        print("Password Anda adalah:", id_user)
        return id_user

    def delete_data(self, id_user):
        cursor = self.conn.cursor()
        sql = "DELETE FROM user WHERE id_user = %s"
        val = (id_user,)
        cursor.execute(sql, val)
        self.conn.commit()
        print("Data user berhasil dihapus.")

class Admin:
    def __init__(self, conn):
        self.conn = conn
        self.data = LinkedList()

    def show_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM admin")
        result = cursor.fetchall()

        if result:
            for row in result:
                self.data.append(row)
            self.data.display()
        else:
            print("Tidak ada data tentang admin yang ditemukan.")

    def ubah_status_pengaduan(self, id_pengaduan, new_status, id_admin):
        cursor = self.conn.cursor()

        # Memeriksa apakah ID pengaduan yang diberikan valid
        cursor.execute("SELECT * FROM pengaduan WHERE id_pengaduan = %s", (id_pengaduan,))
        pengaduan = cursor.fetchone()

        if pengaduan:
            # Memeriksa apakah status baru sama dengan status pengaduan saat ini
            if pengaduan[4] == new_status:
                print("Status baru sama dengan status saat ini. Tidak ada perubahan yang dilakukan.")
                return

            # Memperbarui status pengaduan
            sql = "UPDATE pengaduan SET status = %s, id_admin = %s WHERE id_pengaduan = %s"
            val = (new_status, id_admin, id_pengaduan)
            cursor.execute(sql, val)
            self.conn.commit()
            print("Status pengaduan berhasil dikelola.")
        else:
            print("Status pengaduan tidak valid.\nPengelolaan dibatalkan")

class Pengaduan:
    def __init__(self, conn):
        self.conn = conn
        self.data = LinkedList()

    def lihat_pengaduan(self):
        conn = connect_database()
        if not conn:
            print("Gagal terkoneksi dengan database. Program berhenti.")
            return
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM pengaduan")
        result = cursor.fetchall()

        if result:
            table = PrettyTable()
            table.field_names = ["ID Pengaduan", "Tanggal", "Status", "Judul Pengaduan", "ID User", "ID Admin"]
            for row in result:
                table.add_row(row)
            print(table)
        else:
            print("Tidak ada pengaduan yang ditemukan.")

    def tambah_pengaduan(self, id_user, tanggal, judul_pengaduan, id_admin=None):
        if not judul_pengaduan.strip():  # Validasi untuk memastikan judul pengaduan tidak kosong atau hanya berisi spasi
            print("Judul pengaduan tidak boleh kosong.")
            return

        cursor = self.conn.cursor()
        status_pengaduan = "Menunggu"
        
        # Periksa apakah judul pengaduan sudah ada dalam database
        cursor.execute("SELECT * FROM pengaduan WHERE judul_pengaduan = %s", (judul_pengaduan,))
        result = cursor.fetchone()
        if result:
            print("Judul pengaduan sudah ada dalam database. Mohon gunakan judul yang berbeda.")
            return

        sql = "INSERT INTO pengaduan (tanggal, status, judul_pengaduan, id_user, id_admin) VALUES (%s, %s, %s, %s, %s)"
        val = (tanggal, status_pengaduan, judul_pengaduan, id_user, id_admin)
        cursor.execute(sql, val)
        self.conn.commit()
        print("Pengaduan berhasil diajukan.")

class Layanan:
    def __init__(self, conn):
        self.conn = conn
        self.data = []

    # Method to fetch data from database and populate the list
    def fetch_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM layanan")
        result = cursor.fetchall()

        if result:
            for row in result:
                self.data.append(row)

    # Method to display data
    def display_data(self):
        if self.data:
            for row in self.data:
                print(row)
        else:
            print("Tidak ada data tentang Layanan yang ditemukan.")

def create_iklim():
    # Membuat koneksi ke database
    conn = connect_database()
    if not conn:
        print("Gagal terkoneksi dengan database. Program berhenti.")
        return
    
    # Membuat objek TrenIklim
    tren_iklim = TrenIklim(conn)
    
    # Input data tren iklim
    while True:
        tanggal_input = input("Masukkan tanggal (format: DD/MM/YYYY): ")
        try:
            tanggal = datetime.strptime(tanggal_input, "%d/%m/%Y").strftime("%d/%m/%Y")
            break
        except ValueError:
            print("Format tanggal yang Anda masukkan tidak valid. Silakan masukkan dengan format DD/MM/YYYY.")

    curah_hujan = input("Masukkan curah hujan: ").strip()
    suhu = input("Masukkan suhu: ").strip()
    kelembaban = input("Masukkan kelembaban: ").strip()

    if not (curah_hujan and suhu and kelembaban):
        print("Semua kolom harus diisi. Silakan coba lagi.")
        return

    try:
        # Mengonversi input menjadi tipe data yang diharapkan
        curah_hujan = float(curah_hujan)
        suhu = float(suhu)
        kelembaban = int(kelembaban)
        
        # Memanggil metode tambah_data() dari objek TrenIklim untuk menambahkan data tren iklim baru
        tren_iklim.tambah_data(None, tanggal, f"{curah_hujan} mm", f"{suhu} derajat celcius", f"{kelembaban}%")
    except ValueError:
        print("Input yang Anda masukkan harus berupa bilangan bulat untuk curah kelembaban.")

def delete_iklim():
    # Membuat koneksi ke database
    conn = connect_database()
    if not conn:
        print("Gagal terkoneksi dengan database. Program berhenti.")
        return
    
    # Membuat objek TrenIklim
    tren_iklim = TrenIklim(conn)

    # Menampilkan data tren iklim untuk referensi pengguna
    tren_iklim.show_data()

    # Input ID tren iklim yang akan dihapus
    while True:
        id_tren_iklim = input("Masukkan ID tren iklim yang akan dihapus: ")
        try:
            id_tren_iklim = int(id_tren_iklim)
            break
        except ValueError:
            print("ID tren iklim harus berupa bilangan bulat.")

    # Mengecek apakah ID tren iklim yang akan dihapus ada dalam database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tren_iklim WHERE id_tren_iklim = %s", (id_tren_iklim,))
    result = cursor.fetchone()
    if not result:
        print(f"Tidak ada data tren iklim dengan ID {id_tren_iklim}. Penghapusan dibatalkan.")
        return
    else:
        # Konfirmasi pengguna untuk menghapus data
        confirm = input(f"Apakah Anda yakin ingin menghapus data tren iklim dengan ID {id_tren_iklim}? (y/n): ")
        if confirm.lower() != 'y':
            print("Penghapusan data dibatalkan.")
            return
    # Memanggil metode hapus_data() dari objek TrenIklim untuk menghapus data tren iklim
        tren_iklim.hapus_data(id_tren_iklim)

def update_iklim():
    # Membuat koneksi ke database
    conn = connect_database()
    if not conn:
        print("Gagal terkoneksi dengan database. Program berhenti.")
        return

    # Membuat objek TrenIklim
    tren_iklim = TrenIklim(conn)
    
    # Menampilkan data tren iklim untuk referensi pengguna
    tren_iklim.show_data()

    # Input ID tren iklim yang ingin diupdate
    id_tren_iklim = input("Masukkan ID tren iklim yang ingin diupdate: ")

    # Memeriksa apakah ID yang dimasukkan ada dalam database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tren_iklim WHERE id_tren_iklim = %s", (id_tren_iklim,))
    result = cursor.fetchone()
    if not result:
        print("ID tren iklim yang dimasukkan tidak ditemukan dalam database.")
        return

    # Input data baru untuk tren iklim
    while True:
        tanggal_input = input("Masukkan tanggal baru (format: DD/MM/YYYY): ")
        try:
            tanggal = datetime.strptime(tanggal_input, "%d/%m/%Y").strftime("%d/%m/%Y")
            break
        except ValueError:
            print("Format tanggal yang Anda masukkan tidak valid. Silakan masukkan dengan format DD/MM/YYYY.")

    curah_hujan = input("Masukkan curah hujan baru: ").strip()
    suhu = input("Masukkan suhu baru: ").strip()
    kelembaban = input("Masukkan kelembaban baru: ").strip()

    if not (curah_hujan and suhu and kelembaban):
        print("Semua kolom harus diisi. Silakan coba lagi.")
        return  

    try:
        # Mengonversi input menjadi tipe data yang diharapkan
        curah_hujan = float(curah_hujan)
        suhu = float(suhu)
        kelembaban = int(kelembaban)
        
        # Memanggil metode update_data() dari objek TrenIklim untuk mengupdate data tren iklim
        tren_iklim.update_data(id_tren_iklim, tanggal, f"{curah_hujan} mm", f"{suhu} derajat celcius", f"{kelembaban}%")
    except ValueError:
        print("Input yang Anda masukkan harus berupa bilangan bulat untuk kelembaban.")

def kelola_status_pengaduan():
        # Membuat koneksi ke database
    conn = connect_database()
    if not conn:
        print("Gagal terkoneksi dengan database. Program berhenti.")
        return

    # Membuat objek Pengaduan
    pengaduan = Pengaduan(conn)
    admin = Admin(conn)

    # Menampilkan daftar pengaduan
    pengaduan.lihat_pengaduan()

    # Meminta input dari pengguna
    while True:
        id_pengaduan = input("Masukkan ID pengaduan yang akan diubah statusnya: ")
        if id_pengaduan.isdigit():
            id_pengaduan = int(id_pengaduan)
            break
        else:
            print("Input tidak valid. Harap masukkan angka untuk ID pengaduan.")

    # Meminta input status baru dengan penanganan input yang lebih baik
    while True:
        new_status_input = input("Masukkan status baru (1 untuk Diproses, 2 untuk Selesai): ")
        if new_status_input in ('1', '2'):
            new_status = "Diproses" if new_status_input == '1' else "Selesai"
            break
        else:
            print("Input tidak valid. Harap masukkan angka 1 untuk Diproses atau 2 untuk Selesai.")

    while True:
        id_admin = input("Masukkan ID admin yang melakukan perubahan: ")
        if id_admin.isdigit():
            id_admin = int(id_admin)
            break
        else:
            print("Input tidak valid. Harap masukkan angka untuk ID admin.")

    # Memanggil metode ubah_status_pengaduan dengan parameter yang diberikan
    admin.ubah_status_pengaduan(id_pengaduan, new_status, id_admin)

def menuuser(user_id):
    # Membuat koneksi ke database
    conn = connect_database()
    if not conn:
        print("Gagal terkoneksi dengan database. Program berhenti.")
        return

    tren_iklim = TrenIklim(conn)
    pengaduan = Pengaduan(conn)

    while True:
        print("\n==============================")
        print("Halo Climaters.")
        print("Yuk Kepoin Iklim Di")
        print("==============================")
        print("1. Informasi tren iklim")
        print("2. Saya Mau Melapor Min")
        print("3. Kembali")
        pilihan = input("Pilih menu (1-3): ")

        if pilihan == "1":
            while True:
                tren_iklim.show_data()
                print("Menu Tren Iklim.")
                print("1. Cari Informasi tren iklim yang terjadi.")
                print("2. Urutkan Berdasarkan Informasi Terbaru.")
                print("3. Kembali")

                pilih = input("Silahkan Masukkan Pilihan (1-3) : ")
                if pilih == "1":
                    tanggal = input("Silahkan Masukkan tanggal Pencarian (format: DD/MM/YYYY): ")
                    tren_iklim.search_by_date(tanggal)
                    input("Tekan Enter Untuk Kembali")
                elif pilih == "2":
                    tren_iklim.sort_by_date()
                    print("="*30,"\n")
                elif pilih == "3":
                    break
                else:
                    print("Pilihan tidak valid. Silakan pilih menu yang tepat.\nTekan ENTER untuk Kembali.")

        elif pilihan == "2":
            # Meminta pengguna memasukkan tanggal dan judul pengaduan
            while True:
                tanggal_input = input("Masukkan tanggal pengaduan (format: DD/MM/YYYY): ")
                try:
                    tanggal = datetime.strptime(tanggal_input, "%d/%m/%Y").strftime("%d/%m/%Y")
                    break
                except ValueError:
                    print("Format tanggal yang Anda masukkan tidak valid. Silakan masukkan dengan format DD/MM/YYYY.")
            while True:
                judul_pengaduan = input("Masukkan judul pengaduan: ").strip()
                if judul_pengaduan.strip() == "":
                    print("Judul pengaduan tidak boleh kosong.")
                else:
                    break
            
            # Memanggil metode untuk menambahkan pengaduan baru
            pengaduan.tambah_pengaduan(user_id, tanggal, judul_pengaduan)
        elif pilihan == "3":
            return
        else:
            print("Pilihan tidak valid. Silakan pilih menu yang tepat.")

def menuadmin(admin_id):
    conn = connect_database()
    if not conn:
        print("Gagal terkoneksi dengan database. Program berhenti.")
        return
    
    # Mengambil informasi hak akses admin dari database berdasarkan ID admin yang login
    cursor = conn.cursor()
    sql = "SELECT hak_akses FROM admin WHERE id_admin = %s"
    cursor.execute(sql, (admin_id,))
    result = cursor.fetchone()

    if result:
        hak_akses = result[0]

        tren_iklim = TrenIklim(conn)
        pengaduan = Pengaduan(conn)

        while True:
            print("\nMenu Admin: ")
            print("1. Tambah Tren Iklim")
            print("2. Lihat Tren Iklim")
            print("3. Perbarui Tren Iklim")
            print("4. Hapus Tren Iklim")
            print("5. Lihat Pengaduan")
            print("6. Kelola Pengaduan")
            print("7. Keluar")
            
            pilih = input("Masukkan Pilihan (1-7): ")
            
            # Melakukan pengecekan hak akses untuk membatasi akses admin
            if hak_akses == "View" and pilih not in ["2", "5", "6", "7"]:
                print("Maaf, Anda hanya bisa melihat tren iklim.")
            elif hak_akses == "Update" and pilih not in ["2", "3", "5", "6", "7"]:
                print("Maaf, Anda hanya bisa mengubah tren iklim.")
            elif hak_akses == "Delete" and pilih not in ["2", "4", "5", "6", "7"]:
                print("Maaf, Anda hanya bisa menghapus tren iklim.")
            elif hak_akses == "Create" and pilih not in ["1", "2" ,"5", "6", "7"]:
                print("Maaf, Anda hanya bisa menambahkan tren iklim.")
            else:
                if pilih == "1":
                    create_iklim()
                elif pilih == "2":
                    tren_iklim.show_data()
                elif pilih == "3":
                    update_iklim()
                elif pilih == "4":
                    delete_iklim()
                elif pilih == "5":
                    pengaduan.lihat_pengaduan()
                elif pilih == "6":
                    kelola_status_pengaduan()
                elif pilih == "7":
                    print("Terima kasih!\n")
                    break
                else:
                    print("Pilihan yang Anda Masukkan tidak Valid, Silahkan Masukkan Pilihan 1-5")
    else:
        print("Admin tidak ditemukan.")


# Fungsi utama untuk menjalankan program
def main():
    conn = connect_database()
    if not conn:
        print("Gagal terkoneksi dengan database. Program berhenti.")
        return
    
    while True:
        print("="*30)
        print("Selamat Datang di Climate Care")
        print("="*30)
        print("\nMenu.")
        print("1. User")
        print("2. User Baru")
        print("3. Admin")
        print("4. Keluar")
        
        pilih = input("Masuk Sebagai (1-4) : ")

        if pilih == "1":
            user_id = user_login(conn)
            if user_id:
                # Lakukan sesuatu setelah login berhasil, misalnya menu pengguna
                menuuser(user_id)
        elif pilih == "2":
            regisuser(conn)
        elif pilih == "3":
            admin_id = admin_login(conn)
            if admin_id:
                menuadmin(admin_id) # Panggil fungsi menu untuk admin        
        elif pilih == "4":
            break
        else:
            print("Pilihan yang Anda Masukkan tidak Valid, Silahkan Masukkan Pilihan 1-4")

def regisuser(conn):
    print("Untuk Mendaftar Sebagai User, Silahkan Masukkan Beberapa data Anda.")
    
    # Meminta input pengguna untuk data pengguna baru
    nama_user = input("Masukkan Nama Anda: ").strip()  # Menghapus spasi di awal dan akhir input
    alamat_user = input("Masukkan Alamat Anda: ").strip()
    email_user = input("Masukkan E-mail Anda: ").strip()
    no_hp = input("Masukkan No Telepon Anda: ").strip()

    # Memeriksa apakah ada input yang kosong setelah di-strip
    if not (nama_user and alamat_user and email_user and no_hp):
        print("Semua kolom harus diisi. Silakan coba lagi.")
        return  # Menghentikan proses registrasi jika ada input yang kosong

    # Membuat objek User
    user = User(conn)
    # Memanggil metode add_data() dari objek User untuk menambahkan data user baru
    user.add_data(nama_user, alamat_user, email_user, no_hp)


def user_login(conn):
    username = input("Masukkan E-mail Pengguna : ")
    password = (pwinput.pwinput("Masukkan sandi : ", mask="*"))

    cursor = conn.cursor()
    sql = "SELECT id_user FROM user WHERE email_user = %s AND id_user = %s"
    val = (username, password)
    cursor.execute(sql, val)
    result = cursor.fetchone()

    if result:
        # print("Login berhasil!")
        return result[0]  # Mengembalikan ID pengguna jika login berhasil
    else:
        print("Login gagal. E-mail pengguna atau password salah.")
        return None  # Mengembalikan None jika login gagal

def admin_login(conn):
    username = input("Masukkan E-mail Admin: ")
    password = (pwinput.pwinput("Masukkan sandi : ", mask="*"))

    cursor = conn.cursor()
    sql = "SELECT id_admin FROM admin WHERE email_admin = %s AND id_admin = %s"
    val = (username, password)
    cursor.execute(sql, val)
    result = cursor.fetchone()

    if result:
        # print("Login berhasil!")
        return result[0]  # Mengembalikan ID admin jika login berhasil
    else:
        print("Login gagal. E-mail admin atau password salah.")
        return None  # Mengembalikan None jika login gagal

# Menjalankan program
if __name__ == "__main__":
    main()
    
