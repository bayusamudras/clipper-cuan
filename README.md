# Clipper Cuan (Potong Hook)

Alat untuk mengubah video panjang (podcast, wawancara, rekaman lapangan) menjadi clip vertikal 9:16 yang siap diunggah ke TikTok, Reels, dan Shorts. Semua proses berjalan di browser. Video tidak diunggah ke server mana pun, jadi file ratusan MB sampai GB aman.

## Isi repo

| Path | Fungsi |
|---|---|
| `index.html` | Website satu berkas. Buka langsung di Chrome atau Safari, tanpa server dan tanpa instalasi. |
| `skills/yt-to-explainer-clips/SKILL.md` | Skill untuk Claude: alur dari video sumber ke clip, plus SOP kualitas clip. |

## Cara pakai website

1. Buka `index.html` di browser (klik dua kali), atau buka versi Pages bila sudah diaktifkan.
2. Pilih atau tarik file video. File .MOV dari iPhone yang berformat HEVC kadang ditolak browser; ubah dulu ke H.264:
   `ffmpeg -i asli.MOV -c:v libx264 -crf 20 -c:a aac baru.mp4`
3. Isi topik, dan tempel transkrip (SRT, VTT, atau baris `01:23 teks`) bila ada. Transkrip membuat pemangkasan basa-basi, subtitle, kata sorot, dan hashtag bekerja.
4. Tekan **Analisis momen menarik**. Biarkan tab terbuka dan terlihat.
5. Edit hook, lihat **Pratinjau**, lalu **Render clip**. Render berjalan waktu nyata dan hasilnya MP4 atau WebM, tergantung dukungan browser.

## Fitur

- Analisis suara, lonjakan tekanan, gerakan, dan kata kunci untuk memilih momen terbaik.
- Hook 1–3 detik: teks bergerak (slam, geser, glitch) dan/atau cold open dari momen puncak.
- Editan dinamis: punch-in, getar, cincin, kata sorot, jump cut, efek loop, lower third, kartu penutup.
- Tata letak: video di tengah dengan latar blur, isi penuh dengan fokus otomatis/manual, split atas-bawah.
- Animasi penerapan otomatis dari transkrip: langkah bernomor, angka berhitung, perbandingan, sebab-akibat, contoh, peringatan, dan tips. Bisa dimatikan, diedit, atau ditambah manual per clip.
- Subtitle kata-per-kata, SFX sintetis, musik latar sintetis atau musik unggahan sendiri.
- Paket posting: judul layar, caption, hashtag. Pengecekan SOP di tiap momen.

## Batasan

- Auto-fokus hanya menebak dari area yang paling bergerak. Ini bukan pelacak wajah.
- Skor "menarik" berasal dari sinyal audio, gerakan, dan kata kunci, bukan pemahaman isi.
- Musik tren dari TikTok tidak bisa dipakai di sini. Tambahkan lewat aplikasi TikTok saat mengunggah.
- Render dan pemindaian butuh tab yang tetap terlihat.

## Pembaruan terbaru
- **Hook sesuai topik**: tema satu seri dideteksi otomatis dari transkrip (atau isi sendiri di kolom Topik). Hook dibuat dari tema + isi tiap clip, contoh "Beli Bitcoin pasti kaya?", "Kenapa banyak yang rugi di Bitcoin?", "Bitcoin dan halving: yang jarang dibahas". Tiap clip diberi label Part n/N dan momen yang tidak nyambung dengan tema diberi peringatan.
- **Momen dipilih nyambung**: skor momen ditambah bobot kemunculan tema, jadi clip satu seri membahas topik yang sama.
- **Subtitle selalu aktif** dengan warna per kategori: kuning angka, merah peringatan, hijau solusi/untung, biru muda nama/istilah.
- Transkripsi otomatis (Whisper) hanya jalan di versi lokal atau GitHub Pages, bukan di claude.ai.

## Pembaruan: hook teks, render lebih lancar, analisis lebih cepat
- Hook default sekarang **teks saja** (tanpa cuplikan cold open), dibuat dari tema dan isi tiap clip.
- Pindai: pilihan **8× turbo (default)** dan 16×, sekitar 2-3 kali lebih cepat dari 4×.
- Render: jump cut dibatasi maksimal 6 per clip dan minimal 0,45 detik (seek adalah penyebab video tersendat), kanvas tanpa alfa, teks hook tanpa shadowBlur, pembaruan panel dibatasi. Tersedia resolusi 540×960 untuk komputer lambat.

## Perbaikan: render tidak jalan
- Subtitle tidak lagi memblokir render. Tanpa transkrip, clip tetap dirender (tanpa subtitle) dan muncul peringatan.
- Kesalahan saat render sekarang ditampilkan di status dan tidak lagi membuat tombol render macet.
