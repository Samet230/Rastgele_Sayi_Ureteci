<div align="center">

# 🎲 Rastgele Sayı Üreteci (RNG)
### LCG + Kriptografik Güvenli CSPRNG

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge)](.)
[![POSIX Compliant](https://img.shields.io/badge/POSIX-Compliant-orange?style=for-the-badge)](.)
[![Cryptographically Secure](https://img.shields.io/badge/🔐_Crypto-Secure-red?style=for-the-badge)](.)
[![Language Support](https://img.shields.io/badge/🌍_Language-TR_|_EN-purple?style=for-the-badge)](.)

<br>

**Bilgi Sistemleri ve Güvenliği Dersi Projesi**  
*Yazılım Mühendisliği - 4. Sınıf*

<br>

[🚀 Hızlı Başlangıç](#-hızlı-başlangıç) •
[📖 Dokümantasyon](#-dokümantasyon) •
[🔐 Güvenli RNG](#-kriptografik-güvenli-csprng) •
[👥 Ekip](#-katkıda-bulunanlar)

</div>

---

## 📋 İçindekiler

- [Proje Hakkında](#-proje-hakkında)
- [İki Algoritma](#-iki-algoritma)
- [Hızlı Başlangıç](#-hızlı-başlangıç)
- [Kullanım](#-kullanım)
- [Kriptografik Güvenli CSPRNG](#-kriptografik-güvenli-csprng)
- [Güvenlik Karşılaştırması](#-güvenlik-karşılaştırması)
- [Dokümantasyon](#-dokümantasyon)
- [Katkıda Bulunanlar](#-katkıda-bulunanlar)

---

## 🎯 Proje Hakkında

Bu proje, **iki farklı rastgele sayı üreteci** implementasyonu içermektedir:

1. **Basit LCG** - Eğitim amaçlı, matematiksel temelleri anlamak için
2. **CSPRNG** - Kriptografik güvenli, gerçek dünya uygulamaları için

---

## 🔄 İki Algoritma

### 🔓 Basit LCG (Linear Congruential Generator)

```
X_{n+1} = (a × X_n + c) mod m

m = 2³¹ - 1 (Mersenne Asal)
a = 48271   (Park-Miller)
c = 0       (Multiplicative)
```

⚠️ **Eğitim amaçlıdır, kriptografik kullanım için uygun DEĞİLDİR!**

### 🔐 CSPRNG (Cryptographically Secure PRNG)

```
┌──────────────┐
│ OS Entropi   │──┐
│ Nanosec Time │  │    ┌─────────────────────────────────┐
│ PID/Thread   │──┼──→ │  ENTROPİ HAVUZU (256 byte)     │
│ ASLR Address │  │    └─────────────┬───────────────────┘
└──────────────┘──┘                  │
                                     ▼
              ┌─────────┐  ┌─────────┐  ┌─────────┐
              │ LCG-1   │  │ LCG-2   │  │ LCG-3   │
              │ 64-bit  │  │ 64-bit  │  │ 64-bit  │
              └────┬────┘  └────┬────┘  └────┬────┘
                   │           │           │
                   └─────┬─────┴─────┬─────┘
                         ▼           ▼
                   ┌──────────────────────┐
                   │   XOR + SHA-256      │
                   └──────────┬───────────┘
                              ▼
                   ┌──────────────────────┐
                   │  GÜVENLİ ÇIKTI 🔐    │
                   └──────────────────────┘
```

✅ **Kriptografik uygulamalar için uygundur!**

---

## 🚀 Hızlı Başlangıç

### Gereksinimler

- Python 3.8+

### Kurulum

```bash
git clone https://github.com/Samet230/Rastgele_Sayi_Ureteci.git
cd Rastgele_Sayi_Ureteci
```

### Çalıştırma

```bash
# Basit LCG
python lcg_generator.py

# Kriptografik Güvenli CSPRNG
python secure_rng.py

# JPEG Demo
python jpeg_quantization_demo.py
```

---

## 📖 Kullanım

### Basit LCG

```python
from lcg_generator import LinearCongruentialGenerator, Language

rng = LinearCongruentialGenerator(language=Language.TURKISH)

# Rastgele sayı
print(rng.next())           # 595905495
print(rng.next_float())     # 0.6782...
print(rng.next_int(1, 6))   # 4 (zar)
```

### Kriptografik Güvenli CSPRNG

```python
from secure_rng import CryptographicallySecureRNG

rng = CryptographicallySecureRNG()

# Rastgele sayı (tahmin edilemez!)
print(rng.next())           # 5214068341740065145

# Güvenli token
print(rng.generate_token(32))  # "87147e4a07f19715b48e1f2c6183e554"

# Güvenli şifre
print(rng.generate_password(16))  # "$9}|zwK_MaiO@Yk6"

# Bias'sız zar atışı
print(rng.next_int(1, 6))   # 4
```

---

## 🔐 Kriptografik Güvenli CSPRNG

### Güvenlik Özellikleri

| Özellik | Açıklama |
|---------|----------|
| 🎲 **OS Entropi** | `/dev/urandom` veya `CryptGenRandom` |
| 🔀 **Çoklu LCG** | 3 farklı 64-bit LCG paralel çalışır |
| 🔒 **SHA-256** | Her çıktı hash'lenir, iç durum gizlenir |
| ♻️ **Auto Reseed** | Her 1000 çıktıda yeni entropi |
| 🛡️ **Bias Önleme** | Rejection sampling ile eşit dağılım |
| 🔐 **Thread-Safe** | Lock mekanizması ile senkronizasyon |

### Neden Güvenli?

```
SALDIRI ZORLUK ANALİZİ:

1. Entropi Kırma
   └── 256 byte havuz = 2^2048 olasılık → İMKANSIZ

2. LCG Kırma
   └── 3 × 64-bit = 2^192 durum → İMKANSIZ

3. SHA-256 Kırma
   └── 2^256 brute force → EVRENİN ÖMRÜNDEN UZUN

4. Forward Secrecy
   └── Eski çıktılar yeni çıktıdan türetilemez
```

---

## ⚡ Güvenlik Karşılaştırması

| Özellik | 🔓 Basit LCG | 🔐 CSPRNG |
|---------|-------------|-----------|
| Entropi Kaynağı | `time.time()` | OS + Donanım |
| Modül Boyutu | 31-bit | 64-bit × 3 |
| Çıktı Dönüşümü | Yok | SHA-256 |
| Yeniden Tohumlama | Yok | Her 1000 çıktı |
| Tahmin Edilebilirlik | **KOLAY** | **İMKANSIZ** |
| Kriptografik Kullanım | ❌ DEĞİL | ✅ UYGUN |
| Kırma Süresi | Milisaniye | Yıllar (brute force) |

---

## 📚 Dokümantasyon

| Dosya | Açıklama |
|-------|----------|
| [📝 PSEUDOCODE.md](docs/PSEUDOCODE.md) | LCG ve CSPRNG sözde kodu |
| [📊 FLOWCHART.md](docs/FLOWCHART.md) | Mermaid akış şemaları |
| [🎯 SUNUM_STRATEJISI.md](docs/SUNUM_STRATEJISI.md) | Ekip sunumu planı |
| [🔍 CODE_REVIEW_CHEATSHEET.md](docs/CODE_REVIEW_CHEATSHEET.md) | Güvensiz RNG tespit kriterleri |

---

## 🧪 JPEG Sıkıştırma Testi

**Hipotez:** *"Rastgelelik güvenlikte iyidir ama veri sıkıştırmada deterministik yapı şarttır."*

```bash
python jpeg_quantization_demo.py
```

| Tablo Tipi | MSE | PSNR | Sonuç |
|------------|-----|------|-------|
| Standart (Deterministik) | Düşük | Yüksek | ✅ İyi |
| Rastgele (LCG) | Yüksek | Düşük | ❌ Kötü |

---

## ⚠️ Güvenlik Uyarısı

> [!CAUTION]
> **Basit LCG** kriptografik amaçlar için **GÜVENLİ DEĞİLDİR!**
> 
> Güvenli rastgelelik gereken yerlerde **secure_rng.py** veya Python'un `secrets` modülünü kullanın.

> [!TIP]
> **CSPRNG** şu uygulamalar için uygundur:
> - 🔑 API anahtarı üretimi
> - 🔐 Şifre üretimi
> - 🎫 Token üretimi
> - 🎰 Adaletli şans oyunları

---


---

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.

---

<div align="center">

**Yazılım Mühendisliği Bölümü**  
*Bilgi Sistemleri ve Güvenliği Dersi*  
*2025*

[![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red?style=flat-square)](.)
[![Secure by Design](https://img.shields.io/badge/Secure_by-Design-blue?style=flat-square)](.)

</div>
