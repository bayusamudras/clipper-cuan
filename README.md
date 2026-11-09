# Clipper Cuan (Potong Hook)

Alat untuk mengubah video panjang (podcast, wawancara, rekaman lapangan) menjadi clip vertikal 9:16 yang siap diunggah ke TikTok, Reels, dan Shorts. Semua proses berjalan di browser. Video tidak diunggah ke server mana pun, jadi file ratusan MB sampai GB aman.

## Isi repo

| Path | Fungsi |
|---|---|
| `app/index.html` | Website satu berkas. Buka langsung di Chrome atau Safari, tanpa server dan tanpa instalasi. |
| `skills/yt-to-explainer-clips/SKILL.md` | Skill untuk Claude: alur dari video sumber ke clip, plus SOP kualitas clip. |

## Cara pakai website

1. Buka `app/index.html` di browser (klik dua kali).
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
- Subtitle kata-per-kata, SFX sintetis, musik latar sintetis atau musik unggahan sendiri.
- Paket posting: judul layar, caption, hashtag. Pengecekan SOP di tiap momen.

## Batasan

- Auto-fokus hanya menebak dari area yang paling bergerak. Ini bukan pelacak wajah.
- Skor "menarik" berasal dari sinyal audio, gerakan, dan kata kunci, bukan pemahaman isi.
- Musik tren dari TikTok tidak bisa dipakai di sini. Tambahkan lewat aplikasi TikTok saat mengunggah.
- Render dan pemindaian butuh tab yang tetap terlihat.
