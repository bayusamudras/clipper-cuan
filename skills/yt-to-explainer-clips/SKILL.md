---
name: yt-to-explainer-clips
description: Ubah satu video YouTube (link) menjadi beberapa video clip pendek 9:16 yang sudah diedit dengan bumbu explainer (hook teks, kata kunci kinetik, callout, angka, lower third) plus sound effect, memakai bang-motion dan bang-motion-sfx. Pakai skill ini setiap kali pengguna menempelkan link YouTube, atau bilang "jadikan clip", "potong video ini", "buat shorts/reels/TikTok dari video ini", "edit tiap clip seperti biasa", walau tidak menyebut nama skill.
---

# YouTube link → clip explainer

Pengguna ingin cukup memberi satu link YouTube lalu menerima clip pendek yang sudah dipotong, diberi bumbu explainer, dan ber-SFX. Muat `bang-motion` dan `bang-motion-sfx` lebih dulu: hukum visualnya (bukan slide, deterministik, teks terbaca, gaya lahir dari tema) tetap berlaku untuk lapisan overlay. Skill ini hanya menambah alur dari video sumber sampai clip jadi.

## Langkah 0 — Dapatkan video sumber (jangan lewati)

Workspace Claude hanya boleh menjangkau registri paket dan GitHub, jadi `yt-dlp` ke YouTube hampir pasti ditolak (403). Uji sekali dengan `curl -sI https://www.youtube.com`; jangan mencoba jalur memutar (mirror, proxy lain, cache) karena itu melanggar batas jaringan workspace.

Bila ditolak, katakan satu kalimat lalu minta salah satu dari pengguna, urut dari yang terbaik:

1. **File video (.mp4) dilampirkan ke chat.** Paling andal. Di komputer sendiri: `yt-dlp -f "bv*[height<=1080]+ba/b" --merge-output-format mp4 "<link>"`.
2. **Transkrip + file video.** Transkrip mempercepat pemilihan momen.
3. **Hanya transkrip/caption** (dari menu "Show transcript" YouTube). Cukup untuk memilih momen dan menyiapkan overlay, tapi pemotongan butuh videonya; serahkan daftar timestamp dan paket overlay agar pengguna bisa menempelkannya di editor.

Hanya olah video milik pengguna atau yang ia punya izinnya. Bila ia menyebut konten orang lain tanpa izin, ingatkan sekali dan tawarkan memakai materinya sendiri.

## Langkah 1 — Transkrip dan pemilihan momen

- Ada transkrip dari pengguna → pakai. Tidak ada → `ffmpeg` ambil audio, lalu transkripsi dengan `faster-whisper` (`pip install --break-system-packages faster-whisper`). Bila model gagal diunduh karena jaringan, minta transkrip dari pengguna.
- Pilih **5–8 kandidat momen**, tiap clip **20–60 detik**, bisa berdiri sendiri tanpa konteks, dimulai dari kalimat yang menarik (hook), diakhiri di akhir pikiran. Potong di jeda napas, bukan di tengah kata. Alasan: clip pendek ditonton tanpa konteks, jadi 3 detik pertama menentukan.
- Tampilkan tabel `no | mulai–selesai | hook | kenapa menarik` dan minta pengguna menyaring sebelum merender. Merender mahal, memilih ulang murah. Bila pengguna tidak ada (jalan tanpa pengawasan), ambil 5 teratas dan tulis di awal hasil bahwa itu pilihan Claude.

## Langkah 2 — Style brief satu kali, lalu jadi default

Tanya sekali (satu pesan): rasio (default 9:16, 1080×1920), jumlah clip, kata kunci/brand: warna, font, logo. Selebihnya diturunkan sendiri. Tulis style brief ringkas bergaya bang-motion: palet (hex + sumber), font display berkarakter, satu **tanda tangan gerak**, **palet bunyi**, satu momen istimewa. Setelah disetujui, brief ini menjadi **default pengguna**: clip berikutnya memakai brief yang sama kecuali ia minta ganti, supaya seluruh seri berwajah konsisten. Simpan brief di `brand-brief.md` di folder proyek.

## Langkah 3 — Potong clip

```bash
ffmpeg -ss <mulai> -to <selesai> -i sumber.mp4 -vf "scale=-2:1920,crop=1080:1920" \
  -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -c:a aac -b:a 160k clip-NN-raw.mp4
```

Video sumber 16:9 → pilih salah satu sebelum memotong: crop tengah, crop mengikuti pembicara (posisi x per segmen), atau **letterbox**: video 16:9 di tengah dan area atas-bawah dipakai untuk judul/callout. Letterbox paling aman karena tidak memotong wajah dan memberi ruang overlay.

## Langkah 4 — Bumbu explainer per clip (overlay bang-motion)

Overlay dibangun sebagai halaman HTML+GSAP **berlatar transparan** (jenis "title / lower third" di bang-motion) berukuran sama dengan clip, deterministik terhadap `tl.time()`, lalu dirender frame-demi-frame dengan puppeteer ke PNG beralfa dan ditempelkan di atas clip dengan ffmpeg. Jangan memakai screen recording.

Bumbu yang boleh dipilih per momen (bukan semuanya sekaligus, supaya tidak jadi tempelan):

| Bumbu | Kapan |
|---|---|
| **Hook teks** 0–2,5 dtk (satu kalimat, satu kata kunci beraksen) | selalu, di awal tiap clip |
| **Kata kunci kinetik** (kata penting muncul dari redup ke penuh mengikuti ucapan) | kata yang menjadi inti kalimat |
| **Callout menempel** (kartu kecil + garis penuntun ke objek/orang) | menyebut istilah, nama, alat |
| **Angka meletup** (counter + pil) | ada statistik/harga/durasi |
| **Lower third** nama pembicara/topik | 3–4 dtk pertama clip pertama dan clip yang berganti topik |
| **Zoom ukuran shot** (wide ↔ medium close-up) pada video | tiap 4–6 dtk atau di kalimat penekanan, supaya tidak statis |
| **Progress tipis + CTA akhir** | 1–2 dtk terakhir |

Teks maksimum dua tingkat per momen, ukuran minimum 44 px untuk kalimat dan 34 px untuk label pada stage 1080. Bayangan/pil solid di balik teks karena latarnya video yang ramai. Subtitle: tanyakan sekali; bila ya, pil gelap di zona bawah dan jangan tertimpa callout.

## Langkah 5 — SFX (bang-motion-sfx)

Daftarkan cue lewat helper yang sama dengan animasi overlay (pop untuk callout, tick untuk kata, thud untuk stempel, whoosh untuk zoom/transisi), render sekali dengan `OfflineAudioContext` menjadi `sfx.wav`, simpan `sfx-cues.json`. Mix di bawah ucapan dengan ducking dan `loudnorm` (rumus ffmpeg ada di bang-motion-sfx). SFX tidak boleh menutupi kata; beri jeda bersih sebelum kata kunci.

## Langkah 6 — Ekspor dan serahkan

- Nama berkas `clip-NN-<slug>.mp4`, 30 fps, H.264, −16 LUFS.
- Verifikasi tanpa telinga: `ffprobe` durasi video = audio, `ebur128` true peak ≤ −1,5 dBTP, potret 3–4 frame per clip (hook, tengah, callout, akhir) dan lihat sendiri: teks terpotong? menutup wajah? Perbaiki lalu potret ulang.
- Kirim tiap clip dengan SendUserFile, plus `clips.md` (tabel timestamp sumber, hook, bumbu yang dipakai). Katakan terus terang bahwa kualitas bunyi akhir dinilai di telinga pengguna.
- Penutup: satu kalimat hasil + satu langkah lanjutan (mis. "ganti palet", "tambah subtitle"). Tidak perlu mengulang langkah kerja.

## SOP clip (pelajaran dari klip sebelumnya)

Cek tiap clip terhadap daftar ini sebelum diserahkan. Alasannya: penonton memutuskan scroll dalam 3 detik, sebagian besar menonton tanpa suara, dan tempo lambat membuat retensi jatuh.

1. **Durasi 30–45 detik** setelah jeda dibuang.
2. **Detik 0–3 berisi premis paling kuat**: pengakuan, klaim mengejutkan, atau pernyataan kontroversial. Jangan masukkan sapaan, pengulangan pertanyaan, kalimat ragu-ragu ("ya berarti ya..."), atau kalimat yang masih menyambung dari bagian sebelumnya. Bila awal clip berupa basa-basi, geser awal ke kalimat inti. Bila inti ada di tengah, jadikan cold open 1–3 detik di depan.
3. **Jump cut agresif**: buang jeda napas dan kata pengisi (eum, anu, gitu) supaya tempo padat.
4. **Framing**: wajah pembicara aktif di tengah layar 9:16 dan tidak terpotong. Dua pembicara berdampingan: split atas-bawah. Satu kamera lebar: kunci fokus manual pada pembicara.
5. **Teks**: judul besar di 3 detik pertama, lalu subtitle per kata sepanjang video. Kata kunci krusial diberi warna kontras. Subtitle di tengah-atas, bukan paling bawah.
6. **Musik latar** tipis (lo-fi atau suspense) sekitar −25 sampai −30 dB. Musik tren TikTok tidak diambil: tambahkan lewat aplikasi TikTok saat mengunggah, atau pakai musik berlisensi/bebas royalti.
7. **Efek loop**: kalimat atau hook terakhir menyambung kembali ke awal.
8. **Paket posting**: judul layar, caption berpertanyaan, 3–5 hashtag niche + 1 hashtag tren.

Untuk video panjang, arahkan pengguna ke website Potong Hook (`app/index.html`): file tidak diunggah, jadi ukuran GB aman. Transkrip yang ditempel membuat pemangkasan basa-basi, subtitle, dan kata sorot bekerja.

## Kegagalan yang sudah diketahui

- Menunggu link YouTube bisa diunduh dari workspace: tidak akan bisa; langsung minta file (Langkah 0).
- Overlay dirender dengan `Date.now()`/`Math.random()` → clip berbeda tiap render; semuanya harus fungsi `tl.time()` dan PRNG ber-seed.
- Semua momen diberi semua bumbu → terasa tempelan; pilih 2–3 bumbu per clip dan variasikan antar clip.
- Memotong di tengah kata → selalu snap ke jeda (`silencedetect`) ±0,3 dtk.
