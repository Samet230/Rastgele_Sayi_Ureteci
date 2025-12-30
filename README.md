<div align="center">

# 🎲 Rastgele Sayı Üreteci (RNG)
### Linear Congruential Generator - Doğrusal Eşlik Üreteci

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge)](.)
[![POSIX Compliant](https://img.shields.io/badge/POSIX-Compliant-orange?style=for-the-badge)](.)
[![Language Support](https://img.shields.io/badge/🌍_Language-TR_|_EN-purple?style=for-the-badge)](.)

<br>

**Bilgi Sistemleri ve Güvenliği Dersi Projesi**  
*Yazılım Mühendisliği - 4. Sınıf*

<br>

[🚀 Hızlı Başlangıç](#-hızlı-başlangıç) •
[📖 Dokümantasyon](#-dokümantasyon) •
[🧪 Testler](#-jpeg-sıkıştırma-testi) •
[👥 Ekip](#-katkıda-bulunanlar)

</div>

---

## 📋 İçindekiler

- [Proje Hakkında](#-proje-hakkında)
- [Algoritma](#-algoritma)
- [Özellikler](#-özellikler)
- [Hızlı Başlangıç](#-hızlı-başlangıç)
- [Kullanım](#-kullanım)
- [Dokümantasyon](#-dokümantasyon)
- [JPEG Sıkıştırma Testi](#-jpeg-sıkıştırma-testi)
- [Güvenlik Uyarısı](#-güvenlik-uyarısı)
- [Katkıda Bulunanlar](#-katkıda-bulunanlar)

---

## 🎯 Proje Hakkında

Bu proje, **Doğrusal Eşlik Üreteci (Linear Congruential Generator - LCG)** algoritmasının Python ile nesne yönelimli (OOP) implementasyonunu içermektedir. 

Proje, sözde-rastgele sayı üretecilerinin (PRNG) matematiksel temellerini, güvenlik implikasyonlarını ve deterministik yapının önemini göstermeyi amaçlamaktadır.

### 🌟 Öne Çıkan Özellikler

| Özellik | Açıklama |
|---------|----------|
| 🔢 **POSIX Uyumlu** | Mersenne Prime (2³¹-1) ve Park-Miller çarpanı |
| 🌍 **Çoklu Dil** | Türkçe ve İngilizce çıktı desteği |
| ⏱️ **Mikrosaniye Seed** | Sistem zamanından yüksek hassasiyetli tohum |
| 📊 **İstatistiksel Test** | Ortalama ve varyans analizi |
| 🧪 **JPEG Demo** | Deterministik yapı kanıtı |

---

## 🧮 Algoritma

### Matematiksel Formül

LCG, aşağıdaki özyineleme formülünü kullanır:

$$X_{n+1} = (a \times X_n + c) \mod m$$

Burada:
- $X_n$ — Mevcut durum (state)
- $a$ — Çarpan (multiplier)  
- $c$ — Artış (increment)
- $m$ — Modül (modulus)

### POSIX Standart Sabitleri

```
┌─────────────────────────────────────────────────────────────┐
│  Parametre    │  Değer            │  Açıklama               │
├─────────────────────────────────────────────────────────────┤
│  Modül (m)    │  2³¹ - 1          │  Mersenne Prime         │
│               │  2,147,483,647    │  (7. Mersenne Asal)     │
├─────────────────────────────────────────────────────────────┤
│  Çarpan (a)   │  48,271           │  Park-Miller Multiplier │
│               │                   │  (POSIX minstd_rand)    │
├─────────────────────────────────────────────────────────────┤
│  Artış (c)    │  0                │  Multiplicative LCG     │
└─────────────────────────────────────────────────────────────┘
```

### Akış Şeması

```mermaid
flowchart TD
    A[🚀 Başlat] --> B{Seed Verildi mi?}
    B -->|Hayır| C[⏱️ Sistem Zamanı Al<br/>Mikrosaniye Hassasiyeti]
    B -->|Evet| D[📥 Seed Değerini Al]
    C --> E[🔢 Seed = Time mod m]
    D --> E
    E --> F[📊 X₀ = Seed]
    F --> G[🔄 Döngü Başlat]
    G --> H[📐 X_{n+1} = a × Xₙ + c mod m]
    H --> I[📤 Sayıyı Çıktı Ver]
    I --> J{Devam?}
    J -->|Evet| G
    J -->|Hayır| K[🏁 Bitir]
```

---

## ✨ Özellikler

### 🌍 Çoklu Dil Desteği

```python
from lcg_generator import LinearCongruentialGenerator, Language

# Türkçe çıktı
rng_tr = LinearCongruentialGenerator(language=Language.TURKISH)
rng_tr.display_info()

# English output
rng_en = LinearCongruentialGenerator(language=Language.ENGLISH)
rng_en.display_info()
```

### 🎯 Tekrarlanabilirlik

Aynı seed değeri ile her zaman aynı dizi üretilir:

```python
rng1 = LinearCongruentialGenerator(seed=42)
rng2 = LinearCongruentialGenerator(seed=42)

assert rng1.next() == rng2.next()  # ✅ Her zaman eşit!
```

---

## 🚀 Hızlı Başlangıç

### Gereksinimler

- Python 3.8+
- NumPy (JPEG demo için)
- Pillow (JPEG demo için)

### Kurulum

```bash
# Repository'yi klonla
git clone https://github.com/[username]/Rastgele_Sayi_Ureteci.git
cd Rastgele_Sayi_Ureteci

# Bağımlılıkları yükle (JPEG demo için)
pip install numpy pillow
```

### Çalıştırma

```bash
# Ana programı çalıştır
python lcg_generator.py

# JPEG demo'yu çalıştır
python jpeg_quantization_demo.py
```

---

## 📖 Kullanım

### Temel Kullanım

```python
from lcg_generator import LinearCongruentialGenerator

# Otomatik seed ile oluştur (sistem zamanı)
rng = LinearCongruentialGenerator()

# Tek bir rastgele sayı
value = rng.next()
print(f"Rastgele sayı: {value}")

# [0,1) aralığında normalize edilmiş sayı
normalized = rng.next_float()
print(f"Normalize: {normalized}")

# Belirli aralıkta sayı
dice = rng.next_int(1, 6)
print(f"Zar atışı: {dice}")
```

### Dizi Oluşturma

```python
# 10 adet rastgele sayı dizisi
sequence = rng.generate_sequence(10)
print(sequence)

# Normalize edilmiş dizi
normalized_seq = rng.generate_normalized_sequence(10)
print(normalized_seq)
```

### İstatistiksel Analiz

```python
stats = rng.calculate_statistics(sample_size=100000)
print(f"Ortalama: {stats['mean']:.4f} (Beklenen: 0.5)")
print(f"Varyans: {stats['variance']:.4f} (Beklenen: 0.0833)")
```

---

## 📚 Dokümantasyon

| Dosya | Açıklama |
|-------|----------|
| [📝 PSEUDOCODE.md](docs/PSEUDOCODE.md) | Algoritmanın sözde kodu |
| [📊 FLOWCHART.md](docs/FLOWCHART.md) | Mermaid formatında akış şeması |
| [🎯 SUNUM_STRATEJISI.md](docs/SUNUM_STRATEJISI.md) | Ekip sunumu planı |
| [🔍 CODE_REVIEW_CHEATSHEET.md](docs/CODE_REVIEW_CHEATSHEET.md) | Güvensiz RNG tespit kriterleri |

---

## 🧪 JPEG Sıkıştırma Testi

Bu bonus modül, rastgeleliğin veri sıkıştırmada neden uygun olmadığını gösterir.

### Hipotez

> *"Rastgelelik güvenlikte iyidir ama veri sıkıştırmada deterministik yapı şarttır."*

### Deney

1. **Standart JPEG kuantalama tablosu** ile görüntü işleme
2. **Rastgele LCG tabanlı tablo** ile görüntü işleme
3. Sonuçların görsel karşılaştırması

```bash
python jpeg_quantization_demo.py
```

### Beklenen Sonuç

| Tablo Tipi | Kalite | Boyut Oranı |
|------------|--------|-------------|
| Standart (Deterministik) | Optimum | Düşük |
| Rastgele (LCG) | Bozuk | Yüksek |

---

## ⚠️ Güvenlik Uyarısı

> [!CAUTION]
> **Bu algoritma kriptografik amaçlar için GÜVENLİ DEĞİLDİR!**
> 
> LCG, tahmin edilebilir bir algoritma olduğu için:
> - 🔓 Şifreleme anahtarı üretiminde kullanılmamalıdır
> - 🎰 Gerçek kumar/şans oyunlarında kullanılmamalıdır
> - 🔐 Güvenlik token üretiminde kullanılmamalıdır
>
> **Güvenli alternatifler:** `secrets` modülü, `os.urandom()`, `/dev/random`

---

## 👥 Katkıda Bulunanlar

<table>
  <tr>
    <td align="center">
      <strong>Ekip Üyesi 1</strong><br>
      <sub>Algoritma Geliştirme</sub>
    </td>
    <td align="center">
      <strong>Ekip Üyesi 2</strong><br>
      <sub>Dokümantasyon</sub>
    </td>
    <td align="center">
      <strong>Ekip Üyesi 3</strong><br>
      <sub>Test & Demo</sub>
    </td>
    <td align="center">
      <strong>International Member</strong><br>
      <sub>🌍 Global Accessibility</sub>
    </td>
  </tr>
</table>

---

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.

---

<div align="center">

**Yazılım Mühendisliği Bölümü**  
*Bilgi Sistemleri ve Güvenliği Dersi*  
*2025*

[![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red?style=flat-square)](.)

</div>
