# 🔍 Code Review Kopya Kağıdı
## Güvensiz RNG Tespit Kriterleri

---

## 📋 Hızlı Referans Tablosu

| ⚠️ Kırmızı Bayrak | 🔴 Risk Seviyesi | 🔎 Nerede Ara |
|-------------------|------------------|---------------|
| Sabit Seed | KRİTİK | `seed = 12345` |
| Küçük Modül | YÜKSEK | `% 1000`, `% 65536` |
| Zayıf Çarpan | ORTA | `a = 1`, `a = 2` |
| Tahmin Edilebilir Seed | YÜKSEK | `seed = time.time()` (saniye) |
| Durumun Sızdırılması | KRİTİK | `return self.state` |

---

## 1️⃣ SABİT SEED (Constant Seed)

### ❌ Güvensiz Örnek
```python
class BadRNG:
    def __init__(self):
        self.seed = 12345  # ⚠️ SABİT SEED!
        self.state = self.seed
```

### 📖 Teknik Açıklama
- **Problem:** Her çalıştırmada aynı dizi üretilir
- **Saldırı:** Saldırgan seed'i bilirse TÜM çıktıları tahmin edebilir
- **Etki:** Kriptografik olarak tamamen kırılmış

### ✅ Doğru Yaklaşım
```python
import os
seed = int.from_bytes(os.urandom(4), 'big')  # Kriptografik rastgele
```

### 🎯 Code Review'da Dikkat:
```
ARAMA TERİMLERİ:
   seed = [herhangi bir sabit sayı]
   self.seed = 
   SEED = 
   random.seed(
```

---

## 2️⃣ KÜÇÜK MODÜL (Small Modulus)

### ❌ Güvensiz Örnek
```python
def next(self):
    self.state = (self.state * 1103515245 + 12345) % 65536  # ⚠️ KÜÇÜK!
    return self.state
```

### 📖 Teknik Açıklama
- **Problem:** Kısa periyot → sayılar çabuk tekrar eder
- **Matematiksel:** Periyot ≤ m (modül değeri)
- **Örnek:** m = 65536 → en fazla 65536 farklı sayı

### 📊 Karşılaştırma Tablosu

| Modül | Periyot | Güvenlik |
|-------|---------|----------|
| 100 | ≤100 | ❌ Tamamen güvensiz |
| 65,536 (2¹⁶) | ≤65,536 | ❌ Zayıf |
| 2,147,483,647 (2³¹-1) | ~2 milyar | ⚠️ Kabul edilebilir* |
| 2⁶⁴ | ~18 kentilyon | ✅ İyi |

*Simülasyon için kabul edilebilir, kriptografi için DEĞİL

### 🎯 Code Review'da Dikkat:
```
ARAMA TERİMLERİ:
   % 1000
   % 256
   % 65536
   modulus = [küçük sayı]
```

---

## 3️⃣ ZAYIF ÇARPAN (Weak Multiplier)

### ❌ Güvensiz Örnek
```python
MULTIPLIER = 1  # ⚠️ Çarpım etkisiz!
# veya
MULTIPLIER = 2  # ⚠️ Sadece bit kaydırma
```

### 📖 Teknik Açıklama
- **Problem:** Zayıf çarpan → düşük periyot, kötü dağılım
- **Matematiksel:** İyi bir çarpan için Hull-Dobell teoremi:
  1. c ve m aralarında asal olmalı
  2. a-1, m'nin tüm asal çarpanlarına bölünmeli
  3. m, 4'e bölünüyorsa a-1 de 4'e bölünmeli

### ✅ Bilinen İyi Çarpanlar

| Standart | Çarpan (a) | Modül (m) |
|----------|------------|-----------|
| POSIX minstd_rand | 48,271 | 2³¹-1 |
| Numerical Recipes | 1,664,525 | 2³² |
| Borland C | 22,695,477 | 2³² |

### 🎯 Code Review'da Dikkat:
```
ARAMA TERİMLERİ:
   multiplier = 
   MULTIPLIER =
   * 1 +
   * 2 +
```

---

## 4️⃣ TAHMİN EDİLEBİLİR SEED (Predictable Seed)

### ❌ Güvensiz Örnekler
```python
# SANİYE hassasiyeti - tahmin edilebilir!
seed = int(time.time())

# İşlem ID'si - sınırlı aralık!
seed = os.getpid()

# Kullanıcı girişi - manipüle edilebilir!
seed = int(input("Seed girin: "))
```

### 📖 Teknik Açıklama

| Kaynak | Aralık | Kırılma Süresi |
|--------|--------|----------------|
| `time.time()` (saniye) | ~10 yıl = ~315M | Saniyeler |
| `os.getpid()` | 0-32768 | Milisaniyeler |
| Kullanıcı girişi | Sınırsız | Sosyal mühendislik |

### ✅ Güvenli Alternatifler
```python
import secrets
seed = secrets.randbits(64)  # 64-bit kriptografik rastgele

import os
seed = int.from_bytes(os.urandom(8), 'big')  # OS entropi havuzu
```

### 🎯 Code Review'da Dikkat:
```
ARAMA TERİMLERİ:
   time.time()
   datetime.now()
   os.getpid()
   input(
```

---

## 5️⃣ DURUMUN SIZDIRILMASI (State Leakage)

### ❌ Güvensiz Örnek
```python
class LeakyRNG:
    def __init__(self, seed):
        self.state = seed
    
    def next(self):
        self.state = (self.state * 48271) % (2**31 - 1)
        return self.state  # ⚠️ İÇ DURUMU DOĞRUDAN DÖNDÜRÜYOR!
    
    def get_state(self):  # ⚠️ GETTER METODU!
        return self.state
```

### 📖 Teknik Açıklama
- **Problem:** İç durum bilinirse gelecek TÜM çıktılar hesaplanabilir
- **Saldırı Senaryosu:**
  1. Saldırgan bir çıktı (X_n) elde eder
  2. Formülü bildiği için X_{n+1} = (a × X_n + c) mod m hesaplar
  3. Tüm gelecek değerleri tahmin eder

### ✅ Daha Güvenli Yaklaşım
```python
def next(self):
    self.state = (self.state * 48271) % (2**31 - 1)
    # Ham durumu değil, dönüştürülmüş değeri döndür
    return (self.state >> 16) & 0x7fff  # Sadece orta bitleri döndür
```

### 🎯 Code Review'da Dikkat:
```
ARAMA TERİMLERİ:
   return self.state
   get_state(
   @property
   def state
   __state
```

---

## 🚨 BONUS: Diğer Kırmızı Bayraklar

### 6. Modüler Bias
```python
# ⚠️ Bias problemi!
def roll_dice(self):
    return (self.next() % 6) + 1  # 6, 2³¹-1'i tam bölmüyor!
```

### 7. Yetersiz Entropi
```python
# ⚠️ Sadece 8-bit seed!
seed = random.randint(0, 255)
```

### 8. Standart Kütüphane Yanlış Kullanımı
```python
import random
# ⚠️ random modülü kriptografi için uygun DEĞİL!
token = ''.join(random.choices(string.ascii_letters, k=32))
```

---

## 📝 Code Review Kontrol Listesi

```
□ Seed sabit mi?
□ Seed nasıl üretiliyor? (time, pid, user input?)
□ Modül yeterince büyük mü? (en az 2³¹)
□ Çarpan bilinen iyi bir değer mi?
□ İç durum dışarıya sızıyor mu?
□ Kriptografik amaç için mı kullanılıyor?
□ secrets veya os.urandom ile mi seed alınıyor?
□ Modüler bias kontrol edilmiş mi?
```

---

## 🎓 Final Sınavı Strateji

1. **İlk olarak seed'e bak** - En yaygın hata
2. **Modül değerini kontrol et** - Küçükse alarm
3. **Çarpanı araştır** - Bilinen iyi değer mi?
4. **Return statement'ları incele** - State sızıyor mu?
5. **Import'lara bak** - `secrets` vs `random`

---

## 📚 Referanslar

- Knuth, D. E. "The Art of Computer Programming, Vol. 2"
- NIST SP 800-90A "Recommendation for Random Number Generation"
- RFC 4086 "Randomness Requirements for Security"

---

*İyi sınavlar! 🎯*
