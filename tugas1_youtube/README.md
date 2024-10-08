# ▶️ **Youtube Video Metadata Scraping**

Faiz Muhammad Kautsar (5054231013)  
Shalahuddin Ahmad Cahyoga (5054231014)

[EN](#-what) | [ID](#-apa)

## ❓ **What**

[ID](#-apa)

This repository, or, well, at least this folder, contains the first week assignment of the Data Mining course of Faiz and Addin.

## 🗒️ **Description**

The dataset is comprised of two JSON-formatted sets, scraped off Youtube with undetected-chromedriver. No post-processing has been done to it. Used were personal accounts of Faiz and Addin to obtain the curated feed.

`...3013ed129353.json` contains our initial attempt for a larger-scale scrape. Although we didn't extract as much information there, it contains the description, hrefs, and titles of 1421 videos along with the likes on each of them.

The `...8544a64d571d.json` set is our latest iteration with more selectors and a more comprehensive scrape. It contains the metadata of 1409 videos, described by the following fields:

1. title: The title of the video
2. desc: The description of the video
3. likes: The number of likes on the video
4. duration: The duration of the video
5. channelName: The channel name of the uploader
6. subCount: The subscriber count of the uploader
7. dateAndViews: The views and date of upload

## 🤖 **Scraper**

Our scraper is based on undetected-chromedriver, which itself wraps selenium. The reasoning for this is because my (Faiz) personal browser is Brave, and selenium's default chromedriver doesn't play nice with it.

To run, you can copy `.env.example` to `.env` and fill it in with your environment's variables. You can obtain both of the variables in `chrome://version` if you're working with Chrome, and `brave://version` if you're working with Brave.

The scraper works in a Depth-Limited Search (DLS) manner, starting with the homepage and grabbing all of the recommendations that follows after you click on each of them. So, i.e.,

```mermaid
graph TD;
    Homepage --> Video_1;
    Homepage --> Video_2;
    Homepage --> Video_...;
    Video_1 --> Video_1_1;
    Video_1 --> Video_1_2;
    Video_1 --> Video_1_...;
    Video_2 --> Video_2_1;
    Video_2 --> Video_2_2;
    Video_2 --> Video_2_...;
    Video_... --> Video_..._...;
```

(assuming depth of 1, we're working with depth of 2 for the current configuration)

## 😦 **Caveats/Appendix**

As said before, no post-processing steps' been done on the scrape. This means some malformations do exist on the set, although due to the scale, we believe that for the most part, the data is relatively clean.

Some notable malformations after a few brief glances through the set:

1. The `likes` selector misses sometimes, this is due to the fact that Youtube has added this animated like feature that screws with the actual HTML that's sent to the browser, i.e. the numbers scroll when you tap on the button and this is achieved by having the numbers actually be on the HTML. This resulted in the `0123456789` artifacts.
2. `dateAndViews` sometimes also contain hashtags, this is because our selector grabs the general row of that information instead of selecting them individually, which itself is because of the inconsistencies in length when the number of items don't add up, i.e., when hashtags are there.

---

## ❓ **Apa**

[EN](#-what)

Folder ini berisi hasil tugas minggu pertama Data Mining Faiz dan Addin.

## 🗒️ **Deskripsi**

Dataset terdiri dari dua set yang terformat sebagai JSON, yang kami _scrape_ dari Youtube menggunakan undetected-chromedriver. Belum ada step-step _post-processing_ yang dilakukan pada hasilnya. Digunakan merupakan akun pribadi Faiz dan Addin untuk mendapatkan beranda Youtube yang telah dikurasi.

`...3013ed129353.json` berisi percobaan awal kami untuk sebuah _scrape_ dengan skala yang lebih besar. Walaupun kami tidak mengekstrak informasi yang cukup banyak di sana, set ini berisi deskripsi, href, dan judul dari 1421 video bersama dengan data _like_ pada tiap-tiap videonya.

Set `...8544a64d571d.json` adalah iterasi terbaru kami, dengan jumlah selector lebih banyak dan _scrape_ yang lebih komprehensif. Set ini berisi metadata dari 1409 video, sebagai berikut:

1. title: Judul dari video
2. desc: Deskripsi dari video
3. likes: Jumlah _like_ pada video
4. duration: Durasi dari video
5. channelName: Nama _channel_ yang mengunggah
6. subCount: Jumlah _subscriber channel_ yang mengunggah
7. dateAndViews: Jumlah berapa kali ditonton dan tanggal pengunggahan

## 🤖 **Scraper**

Scraper kami menggunakan undetected-chromedriver, yang meng-_wrap_ selenium. Alasan penggunaannya di sini adalah karena browser saya (Faiz) Brave, dan chromedriver selenium tidak berfungsi dengan baik dengan Brave.

Untuk menggunakannya, bisa anda _copy_ `.env.example` ke `.env` dan diisi dengan variabel pada _environment_ anda. Variabel-variabelnya bisa anda dapatkan di `chrome://version` jika anda menggunakan Chrome, dan `brave://version` jika anda menggunakan Brave.

Scrapernya berfungsi dengan cara _Depth-Limited Search_ (DLS), dimulai dari beranda, diambil semua rekomendasi yang terdapat pada tiap-tiap videonya. Jadi, i.e.,

```mermaid
graph TD;
    Homepage --> Video_1;
    Homepage --> Video_2;
    Homepage --> Video_...;
    Video_1 --> Video_1_1;
    Video_1 --> Video_1_2;
    Video_1 --> Video_1_...;
    Video_2 --> Video_2_1;
    Video_2 --> Video_2_2;
    Video_2 --> Video_2_...;
    Video_... --> Video_..._...;
```

(dengan asumsi kedalaman 1, konfigurasi saat ini kedalaman 2)

## 😦 **Caveats/Appendix**

Seperti sebelumnya dijelaskan, belum ada post-processing yang dilakukan pada _scrape_-nya. Artinya ada beberapa malformasi pada setnya, tetapi menurut kami karena skala dari setnya, setnya relatif bersih.

Beberapa malformasi setelah dicek beberapa kali:

1. _Selector_ `likes` kadang meleset, ini karena Youtube menambahkan fitur _like_ yang teranimasi yang mengubah HTML yang terkirim ke browser, i.e. angkanya _scroll_ ketika di-klik dan ini dilakukan dengan benar-benar mengubah di HTML-nya. Ini berakibat pada _artifact_ `0123456789`.
2. `dateAndViews` kedang berisi _hashtags_ juga, ini karena _selector_ kami mengambil barisnya secara _general_, inipun karena terkadang ukuran dari selector akan inkonsisten akibat dari _hashtags_ tersebut.
