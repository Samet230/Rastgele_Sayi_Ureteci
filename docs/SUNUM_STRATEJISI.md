# 🎤 Sunum Stratejisi
## 5 Dakikalık Ekip Sunumu Planı

---

## 👥 Ekip Yapısı ve Rol Dağılımı

| Rol | Üye | Sorumluluk | Süre |
|-----|-----|------------|------|
| 🎯 **Moderatör** | Üye 1 | Giriş, geçişler, sonuç | 1:00 |
| 💻 **Teknik Lider** | Üye 2 | Algoritma, kod açıklama | 1:30 |
| 🧪 **Demo Uzmanı** | Üye 3 | Canlı demo, JPEG testi | 1:30 |
| 🌍 **Global Temsilci** | Uluslararası Üye | İngilizce demo, Q&A | 1:00 |

---

## ⏱️ Dakika Dakika Zamanlama

### 00:00 - 01:00 | 📢 GİRİŞ (Moderatör - Üye 1)

```
[00:00 - 00:15] Selamlama ve ekip tanıtımı
   "Merhaba hocam, merhaba arkadaşlar. Ben [İsim], 
    yanımda [isimler] ile birlikte Rastgele Sayı Üreteci 
    projemizi sunacağız."

[00:15 - 00:30] Proje motivasyonu
   "Bilgi güvenliğinin temel taşlarından biri rastgeledir. 
    Bugün size bir RNG algoritmasının hem güçlü hem de 
    zayıf yanlarını göstereceğiz."

[00:30 - 00:45] Gündem açıklama
   "Sunumumuz 4 bölümden oluşuyor:
    1. Algoritma açıklaması
    2. Canlı kod demosu
    3. JPEG sıkıştırma deneyi
    4. Uluslararası erişilebilirlik"

[00:45 - 01:00] Geçiş
   "Şimdi teknik detaylar için arkadaşım [İsim]'e 
    bırakıyorum."
```

---

### 01:00 - 02:30 | 💻 TEKNİK AÇIKLAMA (Teknik Lider - Üye 2)

```
[01:00 - 01:30] LCG Formülü
   [EKRANA: Formül görseli]
   "LCG, matematiksel olarak basit ama güçlü bir algoritma.
    
    X_{n+1} = (a × X_n + c) mod m
    
    3 sabitimiz var:
    • m = 2^31 - 1 (Mersenne Asal - 2 milyar+)
    • a = 48271 (Park-Miller çarpanı)
    • c = 0 (Multiplicative LCG)"

[01:30 - 02:00] POSIX Standardı
   "Neden bu sabitler? Çünkü bunlar POSIX standardında 
    tanımlı. Unix sistemlerinde minstd_rand fonksiyonu 
    tam olarak bu değerleri kullanıyor. 
    Yani endüstri standardı."

[02:00 - 02:15] OOP Yapısı
   [EKRANA: Sınıf diyagramı]
   "Kodumuzu OOP prensiplerine uygun yazdık:
    • Soyut RandomNumberGenerator sınıfı
    • LinearCongruentialGenerator implementasyonu
    • LocalizationManager ile dil desteği"

[02:15 - 02:30] Geçiş
   "Şimdi bunu çalışırken görelim. [İsim]?"
```

---

### 02:30 - 04:00 | 🧪 CANLI DEMO (Demo Uzmanı - Üye 3)

```
[02:30 - 03:00] LCG Demo
   [EKRANA: Terminal - lcg_generator.py çalıştır]
   
   "python lcg_generator.py komutunu çalıştırıyorum..."
   
   [Program çıktısını göster]
   
   "Gördüğünüz gibi:
    • Seed otomatik sistem zamanından alındı
    • 5 adet rastgele sayı üretildi
    • İstatistiksel test sonuçları gösteriliyor"

[03:00 - 03:30] JPEG Sıkıştırma Deneyi
   [EKRANA: Terminal - jpeg_quantization_demo.py]
   
   "Şimdi bonus görevimiz: JPEG deneyi.
    
    HİPOTEZ: Rastgelelik güvenlikte iyidir ama 
    sıkıştırmada deterministik yapı şarttır.
    
    Çalıştırıyorum..."
   
   [Sonuçları yorumla]
   
   "Bakın:
    • Standart tablo: PSNR = XX dB (iyi kalite)
    • Rastgele tablo: PSNR = XX dB (kötü kalite)
    
    Hipotezimiz DOĞRULANDI!"

[03:30 - 04:00] Güvenlik Uyarısı
   "ÖNEMLİ BİR NOT: Bu algoritma eğitim amaçlıdır.
    Kriptografik uygulamalarda kullanılMAZ çünkü
    tahmin edilebilir. Gerçek güvenlik için /dev/random
    veya secrets modülü kullanılmalı."
```

---

### 04:00 - 05:00 | 🌍 ULUSLARARASI ERİŞİLEBİLİRLİK (Global Temsilci)

```
[04:00 - 04:30] İngilizce Demo
   [EKRANA: İngilizce çıktı]
   
   "As you can see, our project supports multiple languages.
    
    This is important for:
    • International collaboration
    • Open source contribution
    • Industry standard documentation
    
    Let me show you the English output..."
   
   [İngilizce çıktıyı göster]

[04:30 - 04:45] Global Standartlar
   "We followed international standards:
    • POSIX compliant constants
    • IEEE floating-point precision
    • ISO documentation format"

[04:45 - 05:00] Kapanış
   [Moderatöre dön]
   
   "Thank you. Teşekkürler. 
    Sorularınızı bekliyoruz."
```

---

## 🎨 Görsel Materyaller

### Slide 1: Kapak
```
╔══════════════════════════════════════════════════╗
║     🎲 RASTGELE SAYI ÜRETECİ (RNG)               ║
║     Linear Congruential Generator                ║
║                                                  ║
║     Bilgi Sistemleri ve Güvenliği                ║
║     Ekip: [İsimler]                              ║
╚══════════════════════════════════════════════════╝
```

### Slide 2: Formül
```
╔══════════════════════════════════════════════════╗
║     📐 MATEMATİKSEL FORMÜL                       ║
║                                                  ║
║         X_{n+1} = (a × X_n + c) mod m            ║
║                                                  ║
║     ┌─────────────────────────────────────────┐  ║
║     │  m = 2³¹ - 1  (Mersenne Asal)           │  ║
║     │  a = 48,271   (Park-Miller)             │  ║
║     │  c = 0        (Multiplicative)          │  ║
║     └─────────────────────────────────────────┘  ║
╚══════════════════════════════════════════════════╝
```

### Slide 3: Demo Ekranı
```
╔══════════════════════════════════════════════════╗
║     💻 CANLI DEMO                                ║
║                                                  ║
║     [Terminal penceresi burada gösterilecek]     ║
║                                                  ║
║     python lcg_generator.py                      ║
╚══════════════════════════════════════════════════╝
```

### Slide 4: JPEG Karşılaştırma
```
╔══════════════════════════════════════════════════╗
║     🧪 JPEG SIKISTIRMA DENEYİ                    ║
║                                                  ║
║     Standart Tablo    vs    Rastgele Tablo       ║
║     ✅ İyi Kalite           ❌ Kötü Kalite       ║
║                                                  ║
║     HİPOTEZ DOĞRULANDI!                          ║
╚══════════════════════════════════════════════════╝
```

---

## 💡 Sunum İpuçları

### ✅ Yapılması Gerekenler

1. **Göz teması** - Sunucu değil dinleyicilere bakın
2. **Net ses** - Mikrofon varsa kullanın
3. **Zamanlama** - Her bölümü rehearse edin
4. **Yedek plan** - Demo çalışmazsa screenshot'lar hazır olsun
5. **Sorulara hazırlık** - Olası soruları tahmin edin

### ❌ Yapılmaması Gerekenler

1. Slaytları okumayın
2. Sırtınızı dinleyicilere dönmeyin
3. Çok hızlı konuşmayın
4. Teknik jargon ile boğmayın
5. Panik yapmayın - hatalar olabilir

---

## ❓ Olası Sorular ve Cevaplar

### S1: "Bu algoritma ne kadar güvenli?"
> **C1:** "LCG, kriptografik açıdan güvenli DEĞİLDİR. Eğitim ve 
> simülasyon amaçlıdır. Gerçek güvenlik için CSPRNG (Cryptographically 
> Secure PRNG) kullanılmalıdır."

### S2: "Neden Mersenne Asal?"
> **C2:** "Mersenne Asallar (2^n - 1 formunda) modüler aritmetikte 
> verimlidir ve tam periyot garantisi sağlar. Ayrıca bit düzeyinde 
> işlemler için optimize edilmiştir."

### S3: "Periyot ne kadar?"
> **C3:** "m-1 yani yaklaşık 2.1 milyar. Bu, bir sayı tekrar etmeden 
> önce 2.1 milyar farklı sayı üretebileceğimiz anlamına gelir."

### S4: "Dil desteği neden önemli?"
> **C4:** "Açık kaynak projeler uluslararası katkı alır. Ayrıca 
> ekibimizde yabancı uyruklu arkadaşımız var, bu sayede herkes 
> kodu anlayabiliyor."

### S5: "JPEG deneyi gerçek dünyada ne anlama geliyor?"
> **C5:** "Rastgelelik her yerde iyi değildir. Güvenlikte AVANTAJ, 
> sıkıştırmada DEZAVANTAJ. Doğru aracı doğru yerde kullanmak önemli."

---

## 📝 Sunum Öncesi Kontrol Listesi

- [ ] Python kurulu ve çalışıyor mu?
- [ ] NumPy yüklü mü? (`pip install numpy`)
- [ ] İki script de hatasız çalışıyor mu?
- [ ] Projeksiyon/ekran paylaşımı test edildi mi?
- [ ] Yedek screenshot'lar hazır mı?
- [ ] Zamanlama rehearse edildi mi?
- [ ] Her üye kendi bölümünü biliyor mu?
- [ ] Sorulara hazırlandınız mı?

---

*Başarılar! 🎯*
