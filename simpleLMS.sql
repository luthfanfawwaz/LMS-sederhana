CREATE DATABASE simple_lms;

USE simple_lms;

CREATE TABLE users(
	id INT AUTO_INCREMENT,
    nama VARCHAR(255),
    tgl_lahir DATE,
    alamat VARCHAR(255),
    PRIMARY KEY (id)
);

CREATE TABLE books(
	id INT NOT NULL,
    judul VARCHAR(255),
    kategori VARCHAR(255),
    jml_stok INT UNSIGNED,
    PRIMARY KEY (id)
);

CREATE TABLE peminjaman(
	id_user INT NOT NULL,
    id_buku INT NOT NULL,
    status_peminjaman VARCHAR(12) DEFAULT 'dipinjam',
    tgl_pinjam DATE,
    tgl_kembali DATE,
    PRIMARY KEY (id_user, id_buku, tgl_pinjam),
    FOREIGN KEY (id_user) REFERENCES users(id),
    FOREIGN KEY (id_buku) REFERENCES books(id)
);
