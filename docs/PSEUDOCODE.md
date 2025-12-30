# 📝 Sözde Kod (Pseudo-Code)
## Doğrusal Eşlik Üreteci (LCG) Algoritması

---

## 1. Algoritma Genel Yapısı

```
ALGORITHM LinearCongruentialGenerator

    CONSTANTS:
        m ← 2³¹ - 1         // Modül (Mersenne Prime)
        a ← 48271           // Çarpan (Park-Miller)
        c ← 0               // Artış (Multiplicative LCG)
    
    VARIABLES:
        state: INTEGER      // Mevcut durum
        seed: INTEGER       // Başlangıç tohumu
```

---

## 2. Başlatma (Initialization)

```
PROCEDURE Initialize(inputSeed)
    
    IF inputSeed IS NULL THEN
        // Sistem zamanından seed oluştur
        currentTime ← GET_SYSTEM_TIME_MICROSECONDS()
        seed ← currentTime MOD m
        
        // Sıfır seed'den kaçın
        IF seed = 0 THEN
            seed ← 1
        END IF
    ELSE
        seed ← inputSeed MOD m
        IF seed = 0 THEN
            seed ← 1
        END IF
    END IF
    
    state ← seed
    RETURN seed
    
END PROCEDURE
```

---

## 3. Sonraki Sayı Üretimi

```
FUNCTION Next() → INTEGER
    
    // LCG Temel Formülü
    // X_{n+1} = (a × X_n + c) mod m
    
    state ← (a × state + c) MOD m
    
    RETURN state
    
END FUNCTION
```

---

## 4. Normalize Edilmiş Sayı [0,1)

```
FUNCTION NextFloat() → REAL
    
    rawValue ← Next()
    normalizedValue ← rawValue / m
    
    RETURN normalizedValue
    
END FUNCTION
```

---

## 5. Aralıkta Tam Sayı

```
FUNCTION NextInt(minValue, maxValue) → INTEGER
    
    // Girdi doğrulama
    IF minValue > maxValue THEN
        RAISE ERROR "Invalid range"
    END IF
    
    rangeSize ← maxValue - minValue + 1
    rawValue ← Next()
    result ← minValue + (rawValue MOD rangeSize)
    
    RETURN result
    
END FUNCTION
```

---

## 6. Dizi Üretimi

```
FUNCTION GenerateSequence(count) → ARRAY OF INTEGER
    
    sequence ← NEW ARRAY[count]
    
    FOR i ← 0 TO count - 1 DO
        sequence[i] ← Next()
    END FOR
    
    RETURN sequence
    
END FUNCTION
```

---

## 7. İstatistiksel Analiz

```
FUNCTION CalculateStatistics(sampleSize) → STATISTICS
    
    // Mevcut durumu kaydet
    savedState ← state
    
    // Örnekleri topla
    sum ← 0
    samples ← NEW ARRAY[sampleSize]
    
    FOR i ← 0 TO sampleSize - 1 DO
        samples[i] ← NextFloat()
        sum ← sum + samples[i]
    END FOR
    
    // Ortalama hesapla
    mean ← sum / sampleSize
    
    // Varyans hesapla
    varianceSum ← 0
    FOR i ← 0 TO sampleSize - 1 DO
        deviation ← samples[i] - mean
        varianceSum ← varianceSum + (deviation × deviation)
    END FOR
    variance ← varianceSum / sampleSize
    
    // Durumu geri yükle
    state ← savedState
    
    RETURN {
        mean: mean,
        variance: variance,
        sampleSize: sampleSize
    }
    
END FUNCTION
```

---

## 8. Sıfırlama

```
PROCEDURE Reset(newSeed)
    
    IF newSeed IS NOT NULL THEN
        Initialize(newSeed)
    ELSE
        state ← seed    // Orijinal seed'e dön
    END IF
    
END PROCEDURE
```

---

## 9. Ana Program Akışı

```
PROGRAM Main
    
    // Üreteci oluştur
    rng ← NEW LinearCongruentialGenerator()
    rng.Initialize(NULL)    // Otomatik seed
    
    // Parametreleri göster
    PRINT "Modül (m):", m
    PRINT "Çarpan (a):", a
    PRINT "Seed:", seed
    
    // 5 adet sayı üret
    FOR i ← 1 TO 5 DO
        rawValue ← rng.Next()
        normalized ← rawValue / m
        PRINT i, ":", rawValue, "→", normalized
    END FOR
    
    // İstatistiksel test
    stats ← rng.CalculateStatistics(10000)
    PRINT "Ortalama:", stats.mean, "(Beklenen: 0.5)"
    PRINT "Varyans:", stats.variance, "(Beklenen: 0.0833)"
    
END PROGRAM
```

---

## 📊 Karmaşıklık Analizi

| İşlem | Zaman | Bellek |
|-------|-------|--------|
| Initialize | O(1) | O(1) |
| Next | O(1) | O(1) |
| NextFloat | O(1) | O(1) |
| NextInt | O(1) | O(1) |
| GenerateSequence(n) | O(n) | O(n) |
| CalculateStatistics(n) | O(n) | O(n) |

---

## 🔐 Güvenlik Notları

```
⚠️ SECURITY WARNING:

Bu algoritma için ASLA kullanılmamalıdır:
    - Kriptografik anahtar üretimi
    - Güvenlik token'ları
    - Şifreleme IV/nonce değerleri
    - Online kumar sistemleri

NEDEN?
    - Durum tahmin edilebilir
    - Ardışık çıktılardan seed türetilebilir
    - Periyot sonlu ve bilinen
```

---

*Yazılım Mühendisliği - Bilgi Sistemleri ve Güvenliği*
