import mysql.connector 
from mysql.connector import Error
import pandas as pd
from datetime import date, timedelta

class Query():
    """Kelas untuk mengumpulkan fungsi-fungsi penghubung dengan MySQL.

    Attributes:
        executed (bool): (class attribute) Mengembalikan nilai True juga eksekusi query terakhir berhasil atau sebaliknya.
        row_count (int): (class attribute) Mengembalikan banyak baris yang terpengaruh oleh query yang dieksekusi oleh method 
            `execute_query()` dan `read_query` atau mengembalikan -1 jika query terakhir gagal.
        connection (CMySQLConnection): (class attribute) Mengembalikan koneksi yang terakhir didefinisikan.
    """
    executed = False
    row_count = int
    connection = None

    #Fungsi Koneksi ke Server
    @staticmethod
    def create_server_connection(host_name, user_name, user_password):
        """Membuat koneksi ke server dan mengembalikan objek CMySQLConnection"""
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                password=user_password
            )
            print("MySQL connection successful")
        except Error as err:
            print(f"Error: {err}")
        return connection


    # Fungsi membuat database
    @staticmethod
    def create_database(connection, query):
        """Menjalankan query MySQL untuk membuat database"""
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            print("Database berhasil dibuat")
        except Error as err:
            print(f"Error: {err}")


    # Fungsi Koneksi ke database
    @staticmethod
    def create_db_connection(host_name, user_name, user_password, db_name):
        """Membuat koneksi ke server sekaligus database dan mengembalikan objek CMySQLConnection"""
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database=db_name)
            print("MySQL database connection successfull")
        except Error as err:
            print(f"Error: {err}")
        return connection
            
    # Fungsi untuk Eksekusi Query, Create, Update, Delete, Insert table and data
    @staticmethod
    def execute_query(connection, query):
        """Mengeksekusi query MySQL dengan klausa CREATE, UPDATE, DELETE, INSERT"""
        cursor = connection.cursor()
        try:
            cursor.execute(query, multi=True)
            connection.commit()
            Query.executed = True
            Query.row_count = cursor.rowcount
        except Error as err:
            print(f"Error: {err}")
            Query.executed = False
            Query.row_count = -1

    # Get Columns
    @staticmethod
    def get_columns(connection, query):
        """Mengeksekusi query MySQL dengan klausa SELECT dan mengembalikan kolom-kolom"""
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            Query.executed = True
            return pd.DataFrame(result)[0]
        except Error as err:
            print(f"Error: {err}")
            Query.executed = False
            
    # Fungsi Read Query
    @staticmethod
    def read_query(connection, query):
        """Mengeksekusi query MySQL dengan klausa SELECT dan mengembalikan tabel"""
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            columns = [i[0] for i in cursor.description]
            result = cursor.fetchall()
            Query.executed = True
            Query.row_count = cursor.rowcount
            return pd.DataFrame(result, columns=columns)
        except Error as err:
            print(f"Error: {err}")
            Query.executed = False
            Query.row_count = -1
    
    # Fungsi Read Query untuk nilai tunggal
    @staticmethod
    def read_query_single_value(connection, query):
        """Mengeksekusi query MySQL dengan klausa SELECT dan mengembalikan suatu nilai tunggal"""
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchone()[0]
            Query.executed = True
            return result
        except Error as err:
            print(f"Error: {err}")
            Query.executed = False


class User():
    """Kelas user (pengguna) fasilitas perpustakaan.

    Attributes:
        requirement_daftar (str): (class attribute) Menyimpan persyaratan pendaftaran user sesuai kolom pada database. Harus
            berbentuk tuple dalam format tuple.
        id (int): Menyimpan ID dari user.
        nama (str): Menyimpan nama dari user.
        tgl_lahir (str): Menyimpan tanggal lahir dari user dengan format (YYYY-MM-DD).
        alamat (str): Menyimpan alamat dari user.
    """
    requirement_daftar = '(nama, tgl_lahir, alamat)'

    def __init__(self, id=None, nama=None, tgl_lahir=None, alamat=None):
        self.id = id
        self.nama = nama
        self.tgl_lahir = tgl_lahir
        self.alamat = alamat
    
    def adalah_terdaftar(self):
        """Memastikan user terdaftar. Mengembalikan 1 jika terdaftar, 0 jika tidak."""
        query = f"""
            SELECT EXISTS(SELECT * FROM users WHERE id = '{self.id}')  
        """
        return Query.read_query_single_value(Query.connection, query)

    def minta_id(self):
        """Memunculkan prompt untuk memasukkan ID user lalu menyimpan atribut tersebut"""
        self.id = input("Masukkan ID user:\n >> ")

    def ambil_id(self):
        """Menyimpan atribut `id` sesuai database jika user sudah memiliki atribut `nama`, `tgl_lahir`, dan `alamat`."""
        query = f"""
            SELECT MAX(id)
            FROM users
            WHERE (nama, tgl_lahir, alamat) = {self.nama, self.tgl_lahir, self.alamat};
        """
        self.id = Query.read_query_single_value(Query.connection, query)

    def minta_nama(self):
        """Memunculkan prompt untuk memasukkan nama user lalu menyimpan atribut tersebut"""
        self.nama = input("Masukkan nama user:\n >> ")
    
    def minta_tgl_lahir(self):
        """Memunculkan prompt untuk memasukkan tanggal lahir user lalu menyimpan atribut tersebut"""
        self.tgl_lahir = input("Masukkan tanggal lahir (YYYY-MM-DD):\n >> ")
    
    def minta_alamat(self):
        """Memunculkan prompt untuk memasukkan alamat user lalu menyimpan atribut tersebut"""
        self.alamat = input("Masukkan alamat:\n >> ")

    def minta_data_daftar(self):
        """Memunculkan prompt untuk memasukkan data user yang diperlukan untuk pendaftaran lalu menyimpan atribut tersebut"""
        self.minta_nama()
        self.minta_tgl_lahir()
        self.minta_alamat()
        return (self.nama, self.tgl_lahir, self.alamat)
    
    def daftar(self):
        """Mendaftarkan user sesuai persyaratan"""
        data_daftar = str(self.minta_data_daftar())

        # membentuk query untuk mendaftarkan user
        query = f"""
            INSERT INTO users {self.requirement_daftar}
            VALUES {data_daftar};
        """
        # mengeksekusi query
        Query.execute_query(Query.connection, query)

    @classmethod
    def tampilkan_daftar(self):
        """Menampilkan user-user yang terdaftar pada database"""
        # membentuk query untuk menampilkan user yang terdaftar
        query = f"""
            SELECT *
            FROM users;
        """
        # membaca dan menampilkan tabel hasil query
        result = Query.read_query(Query.connection, query)
        if Query.row_count >= 1:
            print(result)
        else:
            print("Tidak ada user yang terdaftar.")


class Buku():
    """Kelas buku perpustakaan.

    Attributes:
        requirement_daftar (str): (class attribute) Menyimpan persyaratan pendaftaran buku sesuai kolom pada database. Harus
            berbentuk tuple dalam format tuple.
        id (int): Menyimpan ID dari buku.
        judul (str): Menyimpan judul dari buku.
        kategori (str): Menyimpan kategori buku.
        stok (int): Menyimpan banyak stok buku.
    """
    requirement_daftar = '(id, judul, kategori, jml_stok)'

    def __init__(self, id=None, judul=None, kategori=None, stok=None):
        self.id = id
        self.judul = judul
        self.kategori = kategori
        self.stok = stok

    def adalah_terdaftar(self):
        """Memastikan buku terdaftar. Mengembalikan 1 jika terdaftar, 0 jika tidak."""
        query = f"""
            SELECT EXISTS(SELECT * FROM books WHERE id = '{self.id}')  
        """
        return Query.read_query_single_value(Query.connection, query)

    def minta_id(self):
        """Memunculkan prompt untuk memasukkan ID buku lalu menyimpan atribut tersebut"""
        self.id = input("Masukkan ID buku:\n >> ")
    
    def minta_judul(self):
        """Memunculkan prompt untuk memasukkan judul buku lalu menyimpan atribut tersebut"""
        self.judul = input("Masukkan judul buku:\n >> ")
    
    def minta_kategori(self):
        """Memunculkan prompt untuk memasukkan kategori buku lalu menyimpan atribut tersebut"""
        self.kategori = input("Masukkan kategori buku:\n >> ")
    
    def minta_stok(self):
        """Memunculkan prompt untuk memasukkan stok buku lalu menyimpan atribut tersebut"""
        self.stok = input("Masukkan jumlah stok buku:\n >> ")

    def ambil_stok(self):
        """Menyimpan atribut `stok` sesuai database jika user sudah memiliki atribut `id`."""
        query = f"""
            SELECT jml_stok
            FROM books
            WHERE id = {self.id};
        """
        self.stok = Query.read_query_single_value(Query.connection, query)

    def minta_data_daftar(self):
        """Memunculkan prompt untuk memasukkan data buku yang diperlukan untuk pendaftaran lalu menyimpan atribut tersebut"""
        self.minta_id()
        self.minta_judul()
        self.minta_kategori()
        self.minta_stok()
        return (self.id, self.judul, self.kategori, self.stok)

    def daftar(self):
        """Mendaftarkan user sesuai persyaratan"""
        data_daftar = str(self.minta_data_daftar())

        # membentuk query untuk mendaftarkan buku
        query = f"""
            INSERT INTO books {self.requirement_daftar}
            VALUES {data_daftar};
        """
        # mengeksekusi query
        Query.execute_query(Query.connection, query)

    def tambah_stok(self):
        """Menambah stok buku sebanyak 1"""
        # membentuk query untuk menambahkan stok buku
        query = f"""
            UPDATE books
            SET jml_stok = jml_stok + 1
            WHERE id = {self.id};
        """
        # mengeksekusi query
        Query.execute_query(Query.connection, query)

    def kurangi_stok(self):
        """Mengurangi stok buku sebanyak 1"""
        # membentuk query untuk menambahkan stok buku
        query = f"""
            UPDATE books
            SET jml_stok = jml_stok - 1
            WHERE id = {self.id};
        """
        # mengeksekusi query
        Query.execute_query(Query.connection, query)

    @classmethod
    def tampilkan_daftar(self):
        """Menampilkan buku-buku yang terdaftar pada database"""
        # membentuk query untuk menampilkan buku yang terdaftar
        query = f"""
            SELECT *
            FROM books;
        """
        # membaca dan menampilkan tabel hasil query
        result = Query.read_query(Query.connection, query)
        if Query.row_count >= 1:
            print(result)
        else:
            print("Tidak ada buku yang terdaftar.")

    @classmethod
    def cari(self):
        """Memunculkan prompt untuk meminta kata kunci, lalu menampilkan buku yang terdaftar pada database sesuai kata kunci."""
        kata_kunci = input("Masukkan kata kunci:\n >> ")

        # membentuk query SELECT untuk menampilkan buku yang memiliki substring kata kunci
        # yang diberikan.
        query = f"""
            SELECT *
            FROM books
            WHERE judul LIKE '%{kata_kunci}%';
        """
        # membaca dan menampilkan tabel hasil query
        print(Query.read_query(Query.connection, query))


class Peminjaman():
    """Kelas peminjaman perpustakaan.

    Attributes:
        requirement_daftar (str): (class attribute) Menyimpan persyaratan pendaftaran buku sesuai kolom pada database. Harus
            berbentuk tuple dalam format tuple.
        id_user (int): Menyimpan ID dari user yang akan meminjam.
        id_buku (str): Menyimpan ID dari buku yang akan dipinjam.
        tgl_pinjam (str): Menyimpan tanggal peminjaman dilakukan dengan format (YYYY-MM-DD).
    """
    requirement_daftar = '(id_user, id_buku, tgl_pinjam)'

    def __init__(self, id_user=None, id_buku=None, tgl_pinjam=None):
        self.id_user = id_user
        self.id_buku = id_buku
        self.tgl_pinjam = tgl_pinjam
    
    def minta_id_user(self):
        """Memunculkan prompt untuk memasukkan ID user lalu menyimpan atribut tersebut"""
        self.id_user = input("Masukkan ID user:\n >> ")

    def minta_id_buku(self):
        """Memunculkan prompt untuk memasukkan ID buku lalu menyimpan atribut tersebut"""
        self.id_buku = input("Masukkan ID buku:\n >> ")

    def minta_tgl_pinjam(self):
        """Memunculkan prompt untuk memasukkan tanggal peminjaman lalu menyimpan atribut tersebut"""
        self.tgl_pinjam = input("Masukkan tanggal peminjaman (YYYY-MM-DD):\n >> ")

    def minta_data_daftar(self):
        """Memunculkan prompt untuk memasukkan data user dan buku yang diperlukan untuk pendaftaran lalu menyimpan atribut tersebut"""
        self.minta_id_user()
        self.minta_id_buku()
        tgl_pinjam = str(date.today())
        return (self.id_user, self.id_buku, tgl_pinjam)
    
    def daftar(self):
        """Mendaftarkan user sesuai persyaratan"""
        data_daftar = str(self.minta_data_daftar())

        # memeriksa apakah user dan buku terdaftar
        buku = Buku(id = self.id_buku)
        user = User(id = self.id_user)
        if buku.adalah_terdaftar() and user.adalah_terdaftar():
            #memeriksa stok buku
            buku.ambil_stok()
            if buku.stok < 1:
                print("Buku tidak tersedia.")
            else:
                # membentuk query untuk mendaftarkan peminjaman
                query = f"""
                    INSERT INTO peminjaman {self.requirement_daftar}
                    VALUES {data_daftar};
                """
                # mengeksekusi query
                Query.execute_query(Query.connection, query)
                if Query.executed:
                    print("Peminjaman berhasil didaftarkan.")

                    # meng-update stok buku
                    buku.kurangi_stok()
                    if Query.executed:
                        print("Stok buku berhasil diperbaharui.")

                    # memberikan tanggal tenggat pengembalian buku kepada user sesuai durasi peminjaman (dalam hari)
                    DURASI_PEMINJAMAN = 7
                    tgl_tenggat = date.today() + timedelta(days=DURASI_PEMINJAMAN)
                    print(f"Harap kembalikan buku sebelum tanggal {tgl_tenggat}\n")
        else:
            print("User atau buku belum terdaftar")

    def minta_data_pengembalian(self):
        """Memunculkan prompt untuk memasukkan data yang diperlukan untuk pendaftaran pengembalian lalu menyimpan atribut tersebut"""
        self.minta_id_user()
        self.minta_id_buku()
        self.minta_tgl_pinjam()
        # return (self.id_user, self.id_buku, self.tgl_pinjam)
        
    def kembalikan(self):
        """Mendaftarkan pengembalian pada database, mengubah status menjadi 'dikembalikan' dan menambahkan
        tanggal pengembalian hari ini
        """
        self.minta_data_pengembalian()
        # membentuk query untuk mengembalikan buku,
        # status_peminjaman diubah menjadi 'dikembalikan' dan
        # memasukkan tgl_kembali dengan tanggal hari ini.
        query = f"""
            UPDATE peminjaman
            SET status_peminjaman = 'dikembalikan', tgl_kembali = '{str(date.today())}'
            WHERE id_user = {self.id_user} AND id_buku = {self.id_buku} AND tgl_pinjam = '{self.tgl_pinjam}';
        """
        # mengeksekusi query
        Query.execute_query(Query.connection, query)
        

    @classmethod
    def tampilkan_daftar(self):
        """Menampilkan peminjaman yang terdaftar pada database dan masih berstatus 'dipinjam'"""
        # membentuk query untuk menampilkan peminjaman yang terdaftar dan belum dikembalikan
        query = f"""
            SELECT *
            FROM peminjaman
            WHERE status_peminjaman = 'dipinjam';
        """
        # membaca dan menampilkan tabel hasil query
        result = Query.read_query(Query.connection, query)
        if Query.row_count >= 1:
            print(result)
        else:
            print("Tidak ada peminjaman aktif.")


def daftar_user():
    """Mendaftarkan user baru"""
    print("---> Mendaftarkan user baru")

    # membuat objek user dan meminta data yang diperlukan
    user = User()
    user.daftar()
    if Query.executed:
        print("User berhasil didaftarkan.")

        user.ambil_id()
        print(f"ID user adalah {user.id}.")
        print("Harap simpan ID ini baik-baik untuk menggunakan fasilitas perpustakaan.\n")

def daftar_buku():
    """Mendaftarkan buku baru"""
    print("---> Mendaftarkan buku baru")

    # membuat objek buku dan meminta data yang diperlukan lalu mendaftarkan pada database
    buku = Buku()
    buku.daftar()
    if Query.executed:
        print("Buku berhasil didaftarkan.\n")

def pinjam_buku():
    """Mendaftarkan peminjaman buku"""
    print("---> Mendaftarkan peminjaman buku")
    peminjaman = Peminjaman()
    peminjaman.daftar()

def tampilkan_user():
    """Menampilkan user-user yang terdaftar pada database"""
    User.tampilkan_daftar()

def tampilkan_buku():
    """Menampilkan buku-buku yang terdaftar pada database"""
    Buku.tampilkan_daftar()

def tampilkan_peminjaman():
    """Menampilkan peminjaman yang terdaftar pada database dan masih berstatus 'dipinjam'"""
    Peminjaman.tampilkan_daftar()

def cari_buku():
    """Memunculkan prompt untuk meminta kata kunci, lalu menampilkan buku yang terdaftar pada database sesuai kata kunci."""
    Buku.cari()

def kembalikan_buku():
    """Mendaftarkan pengembalian pada database, mengubah status menjadi 'dikembalikan' dan menambahkan tanggal pengembalian hari ini"""
    peminjaman = Peminjaman()
    peminjaman.kembalikan()
    if Query.executed and Query.row_count == 1:
        print("Pengembalian berhasil didaftarkan.")
        # meng-update stok buku
        buku = Buku(id = peminjaman.id_buku)
        buku.tambah_stok()
        if Query.executed:
            print("Stok buku berhasil diperbaharui.")
    else:
        print("Pengembalian gagal, harap periksa kembali data anda.")

def main():
    """Fungsi utama program LMS.
    
    LMS ini terhubung dengan database pada server lokal. Desain data base dapat diakses pada skrip `simpleLMS.sql`.
    Data username, password, host, dan database tidak diminta melalui prompt namun melalui assignment pada bagian
    atas fungsi ini.
    """
    # mendefinisikan nama user dan database
    user = ""
    pw = ""
    host = ""
    db = "simple_lms"
    # membuat koneksi ke database
    Query.connection = Query.create_db_connection(host_name=host, user_name=user, user_password=pw, db_name=db)

    # Menggunakan variabel running untuk memastikan
    # program masih tetap berjalan sebelum Keluar dipilih.
    running = True
    no_tugas = None

    while running:
        print("""
-.-.-.-.-.-.-.-.-.-.-.- LIBRARY MANAGEMENT SYSTEM -.-.-.-.-.-.-.-.-.-.-.-
    1. Pendaftaran User Baru
    2. Pendaftaran Buku Baru
    3. Peminjaman
    4. Tampilkan Daftar User
    5. Tampilkan Daftar Buku
    6. Tampilkan Daftar Peminjaman
    7. Cari Buku
    8. Pengembalian
    9. Keluar 
""")    
        no_tugas = input("Masukkan nomor tugas: ")
        
        if no_tugas == '1':
            daftar_user()
        elif no_tugas == '2':
            daftar_buku()
        elif no_tugas == '3':
            pinjam_buku()
        elif no_tugas == '4':
            tampilkan_user()
        elif no_tugas == '5':
            tampilkan_buku()
        elif no_tugas == '6':
            tampilkan_peminjaman()
        elif no_tugas == '7':
            cari_buku()
        elif no_tugas == '8':
            kembalikan_buku()
        elif no_tugas == '9':
            running = False
        else:
            print("Input salah, silakan coba kembali.")
        
if __name__ == '__main__':
    main()

