# Library Management System (LMS) Sederhana

Sebuah LMS sederhana yang terhubung dengan database berbasis MySQL.

## Cara Kerja

```mermaid
flowchart TD;
    1(Membuat database dan mendefinisikan tabel-tabel)--> 2
    2(Menjalankan program) --> 3
    3(Memilih perintah tugas) --> 4
    4(Membuat query sesuai tugas yang dipilih) --> 5
    5(Mengeksekusi query) --> 3
```

Tugas yang tersedia yaitu:

1. Pendaftaran User Baru
2. Pendaftaran Buku Baru
3. Peminjaman
4. Tampilkan Daftar User
5. Tampilkan Daftar Buku
6. Tampilkan Daftar Peminjaman
7. Cari Buku
8. Pengembalian
9. Keluar

## Cara Penggunaan Program

Berikut ini adalah panduan menjalankan program.

- Pastikan MySQL terinstall
- Jalankan `simpleLMS.sql` untuk membuat database yang diperlukan
- Pada variabel yang terletak pada bagian atas fungsi `main()`, isi data:
  - username,
  - password, dan
  - host
- Jalankan `simpleLMS.py`

## Hasil Kasus Uji

### Pendaftaran User

#### Menginputkan data user

![Kasus Uji a. i.](kasus-uji/1.png)

#### Menampilkan data user setelah insert

![Kasus Uji a. ii.](kasus-uji/2.png)

### Pendaftaran Buku

#### Menginputkan data buku

![Kasus Uji b. i.](kasus-uji/3.png)

#### Menampilkan data buku setelah insert

![Kasus Uji b. ii.](kasus-uji/4.png)

### Peminjaman

#### Menginputkan data peminjaman

![Kasus Uji c. i.](kasus-uji/5.png)

#### Menampilkan data peminjaman setelah insert

![Kasus Uji c. ii.](kasus-uji/6.png)

#### Menampilkan data buku setelah peminjaman

![Kasus Uji c. iii.](kasus-uji/7.png)

### Pengembalian

#### Menginputkan data pengembalian

![Kasus Uji d. i.](kasus-uji/8.png)

#### Menampilkan data peminjaman setelah pengembalian

![Kasus Uji d. ii.](kasus-uji/9.png)

#### Menampilkan data buku setelah pengembalian

![Kasus Uji d. iii.](kasus-uji/10.png)

### Pencarian Buku

![Kasus Uji e.](kasus-uji/11.png)

## Saran Perbaikan

Perbaikan yang dapat dilakukan antara lain:

- menambahkan tugas baru seperti menghapus record
- menambahkan prompt untuk meminta username dan password MySQL
- mempercantik interface.
