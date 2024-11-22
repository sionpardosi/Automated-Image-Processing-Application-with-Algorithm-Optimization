# Aplikasi Automatic Image Processing

### <summary><strong>Tools:</strong></summary>
<p>
    <img src="https://img.shields.io/badge/Language-Python-blue?logo=python&logoColor=white" />
    <img src="https://img.shields.io/badge/Algorithm-Divide%20and%20Conquer-orange?logo=python&logoColor=white" />
    <img src="https://img.shields.io/badge/Library-Numpy-green?logo=numpy&logoColor=white" />
    <img src="https://img.shields.io/badge/Library-OpenCV-blue?logo=opencv&logoColor=white" />
    <img src="https://img.shields.io/badge/Library-Pillow-5A5A5A?logo=pillow&logoColor=white" />
    <img src="https://img.shields.io/badge/Platform-iOS-lightgrey?logo=apple&logoColor=white" />
</p>

## Deskripsi Proyek
Aplikasi ini dikembangkan untuk memungkinkan pemrosesan gambar otomatis yang efisien, memungkinkan pengguna dengan cepat mengonversi foto menjadi hitam-putih (biner) atau menambahkan efek blur. Menggunakan algoritma Divide and Conquer, aplikasi membagi gambar menjadi blok-blok kecil dan memproses setiap blok secara independen, menghasilkan hasil akhir yang berkualitas tinggi. Pengguna dapat dengan mudah menerapkan efek langsung pada foto yang diambil melalui aplikasi, didukung antarmuka sederhana dan interaktif yang dirancang untuk memberikan pengalaman pengguna yang nyaman dan menyenangkan.

## Latar Belakang
Seiring perkembangan teknologi dan meningkatnya penggunaan media sosial, kebutuhan akan pemrosesan gambar yang cepat dan berkualitas tinggi semakin mendesak. Banyak pengguna yang ingin melakukan pengeditan dasar tanpa harus menggunakan perangkat lunak kompleks atau mahal. Aplikasi ini hadir sebagai solusi praktis yang mampu mengonversi gambar menjadi hitam-putih dan menambahkan efek blur dengan mudah.

Algoritma Divide and Conquer diterapkan karena kemampuannya dalam membagi gambar menjadi bagian kecil sehingga pemrosesan dapat dilakukan secara paralel, mempercepat waktu pemrosesan dan meningkatkan efisiensi. Segmentasi gambar dengan thresholding juga mempermudah berbagai aplikasi, seperti pengenalan objek, analisis medis, dan pemrosesan visual lainnya. Dengan proyek ini, kami berupaya memberikan solusi pengeditan gambar yang mudah, cepat, dan intuitif bagi pengguna.

---

### Fitur Utama
- **Konversi Hitam-Putih (Biner)**: Mengubah gambar menjadi hitam-putih menggunakan metode thresholding untuk hasil yang tajam dan kontras tinggi.
- **Efek Blur**: Mengaburkan gambar untuk efek visual halus, ideal untuk latar belakang dan estetika foto.
- **Pengambilan Foto Langsung**: Pengguna dapat langsung mengambil foto dan menerapkan efek secara instan.
- **Antarmuka Ramah Pengguna**: Desain sederhana untuk memudahkan navigasi dan interaksi pengguna.

---

### Cara Kerja Algoritma
Aplikasi ini menerapkan algoritma Divide and Conquer untuk pemrosesan gambar:
1. **Pembagian Gambar**: Gambar dipecah menjadi blok-blok kecil.
2. **Pemrosesan Paralel**: Setiap blok diproses secara terpisah, memungkinkan penerapan efek yang lebih cepat.
3. **Penggabungan Blok**: Blok-blok yang telah diproses digabungkan kembali menjadi gambar utuh dengan efek yang diinginkan.

---

### Instalasi dan Penggunaan
**Clone repositori**:
   ```bash
   git clone https://github.com/username/Aplikasi-Automatic-Image-Processing.git
   cd Aplikasi-Automatic-Image-Processing
