# 📝 Sözde Kod (Pseudo-Code)
## LCG ve CSPRNG Algoritmaları

---

# BÖLÜM 1: BASİT LCG

## 1.1 Algoritma Yapısı

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

## 1.2 LCG Sayı Üretimi

```
FUNCTION LCG_Next() → INTEGER
    state ← (a × state + c) MOD m
    RETURN state
END FUNCTION
```

---

# BÖLÜM 2: KRIPTOGRAFİK GÜVENLİ CSPRNG

## 2.1 Entropi Havuzu

```
CLASS EntropyPool
    
    CONSTANTS:
        POOL_SIZE ← 256     // Byte
    
    VARIABLES:
        pool: BYTE_ARRAY[256]
        position: INTEGER
        lock: MUTEX
    
    PROCEDURE Initialize()
        // Birden fazla kaynaktan entropi topla
        sources ← []
        
        // 1. OS entropi havuzu (en güvenilir)
        sources.APPEND(OS_RANDOM(64))
        
        // 2. Yüksek hassasiyetli zaman
        sources.APPEND(PACK_BYTES(TIME_NANOSECONDS()))
        
        // 3. İşlem bilgileri
        sources.APPEND(PACK_BYTES(PROCESS_ID()))
        sources.APPEND(PACK_BYTES(THREAD_ID()))
        
        // 4. Bellek adresleri (ASLR)
        sources.APPEND(PACK_BYTES(MEMORY_ADDRESS(self)))
        
        // Tüm kaynakları karıştır
        combined ← CONCATENATE(sources)
        MixIntoPool(combined)
    END PROCEDURE
    
    PROCEDURE MixIntoPool(data: BYTE_ARRAY)
        ACQUIRE lock
        FOR EACH byte IN data DO
            pool[position] ← pool[position] XOR byte
            position ← (position + 1) MOD POOL_SIZE
        END FOR
        RELEASE lock
    END PROCEDURE
    
    FUNCTION GetEntropy(numBytes: INTEGER) → BYTE_ARRAY
        ACQUIRE lock
        
        // Havuzu hash'le
        digest ← SHA256(pool + TIME_NANOSECONDS())
        
        // Havuzu güncelle (forward secrecy)
        newDigest ← SHA256(digest + OS_RANDOM(32))
        pool ← EXPAND(newDigest, POOL_SIZE)
        
        RELEASE lock
        RETURN digest[0:numBytes]
    END FUNCTION
    
END CLASS
```

---

## 2.2 Güvenli LCG (64-bit)

```
CLASS SecureLCG
    
    // 3 farklı parametre seti (PCG ailesinden)
    CONSTANTS:
        PARAMS ← [
            (a=6364136223846793005, c=1442695040888963407, m=2^64),
            (a=2862933555777941757, c=3037000493,          m=2^64),
            (a=3935559000370003845, c=2691343689449507681, m=2^64)
        ]
    
    VARIABLES:
        multiplier, increment, modulus: INTEGER
        state: INTEGER
    
    PROCEDURE Initialize(seed: INTEGER, paramIndex: INTEGER)
        params ← PARAMS[paramIndex MOD 3]
        multiplier ← params.a
        increment ← params.c
        modulus ← params.m
        state ← seed MOD modulus
        
        // Warmup - başlangıç zayıflığını gider
        FOR i ← 1 TO 20 DO
            Advance()
        END FOR
    END PROCEDURE
    
    FUNCTION Advance() → INTEGER
        state ← (multiplier × state + increment) MOD modulus
        RETURN state
    END FUNCTION
    
    FUNCTION Next() → INTEGER
        value ← Advance()
        
        // Output Transformation (PCG tarzı)
        // İç durumu gizle
        xorshifted ← ((value >> 18) XOR value) >> 27
        rot ← value >> 59
        
        // Döndürülmüş sonuç
        result ← (xorshifted >> rot) OR (xorshifted << ((-rot) AND 31))
        RETURN result AND 0xFFFFFFFF
    END FUNCTION
    
END CLASS
```

---

## 2.3 Ana CSPRNG Sınıfı

```
CLASS CryptographicallySecureRNG
    
    CONSTANTS:
        RESEED_INTERVAL ← 1000
    
    VARIABLES:
        entropyPool: EntropyPool
        generators: ARRAY[3] OF SecureLCG
        outputCounter: INTEGER
        lock: MUTEX
    
    PROCEDURE Initialize()
        entropyPool ← NEW EntropyPool()
        outputCounter ← 0
        InitializeGenerators()
    END PROCEDURE
    
    PROCEDURE InitializeGenerators()
        // Entropi havuzundan 24 byte seed al
        seedBytes ← entropyPool.GetEntropy(24)
        
        seeds ← [
            BYTES_TO_INT(seedBytes[0:8]),
            BYTES_TO_INT(seedBytes[8:16]),
            BYTES_TO_INT(seedBytes[16:24])
        ]
        
        // 3 farklı LCG oluştur
        FOR i ← 0 TO 2 DO
            generators[i] ← NEW SecureLCG(seeds[i], i)
        END FOR
    END PROCEDURE
    
    PROCEDURE ReseedIfNeeded()
        IF outputCounter >= RESEED_INTERVAL THEN
            InitializeGenerators()
            outputCounter ← 0
        END IF
    END PROCEDURE
    
    FUNCTION CombineGenerators() → INTEGER
        // 3 LCG'nin çıktılarını al
        values ← [gen.Next() FOR gen IN generators]
        
        // XOR kombinasyonu
        combined ← values[0] XOR values[1] XOR values[2]
        
        // MurmurHash benzeri karıştırma
        combined ← combined XOR (combined >> 16)
        combined ← combined × 0x85ebca6b
        combined ← combined AND 0xFFFFFFFF
        combined ← combined XOR (combined >> 13)
        combined ← combined × 0xc2b2ae35
        combined ← combined AND 0xFFFFFFFF
        combined ← combined XOR (combined >> 16)
        
        RETURN combined
    END FUNCTION
    
    FUNCTION HashWithEntropy(value: INTEGER) → BYTE_ARRAY
        hasher ← NEW SHA256()
        hasher.UPDATE(INT_TO_BYTES(value))
        hasher.UPDATE(INT_TO_BYTES(TIME_NANOSECONDS()))
        hasher.UPDATE(entropyPool.GetEntropy(16))
        RETURN hasher.DIGEST()
    END FUNCTION
    
    FUNCTION NextBytes(numBytes: INTEGER) → BYTE_ARRAY
        ACQUIRE lock
        ReseedIfNeeded()
        
        result ← []
        WHILE LENGTH(result) < numBytes DO
            combined ← CombineGenerators()
            hashOutput ← HashWithEntropy(combined)
            result.EXTEND(hashOutput)
            outputCounter ← outputCounter + 1
        END WHILE
        
        // Geri besleme
        entropyPool.AddEntropy(result[0:8])
        
        RELEASE lock
        RETURN result[0:numBytes]
    END FUNCTION
    
    FUNCTION Next() → INTEGER
        // 64-bit rastgele sayı
        randomBytes ← NextBytes(8)
        RETURN BYTES_TO_INT(randomBytes)
    END FUNCTION
    
    FUNCTION NextInt(minValue, maxValue: INTEGER) → INTEGER
        // Modüler bias önleme
        IF minValue > maxValue THEN
            RAISE ERROR "Invalid range"
        END IF
        
        rangeSize ← maxValue - minValue + 1
        maxAcceptable ← (2^64 / rangeSize) × rangeSize
        
        // Rejection Sampling
        LOOP
            randomValue ← Next()
            IF randomValue < maxAcceptable THEN
                RETURN minValue + (randomValue MOD rangeSize)
            END IF
            // Bias'lı değeri reddet, tekrar dene
        END LOOP
    END FUNCTION
    
    FUNCTION NextFloat() → FLOAT
        // 53-bit hassasiyet (IEEE 754 double)
        randomBytes ← NextBytes(7)
        value ← BYTES_TO_INT(randomBytes) >> 3
        RETURN value / 2^53
    END FUNCTION
    
END CLASS
```

---

## 2.4 Güvenlik Özellikleri Özeti

```
CSPRNG GÜVENLİK MEKANİZMALARI:

1. ENTROPİ TOPLAMA
   ├── os.urandom() → Donanım gürültüsü
   ├── time_ns() → Nanosaniye hassasiyeti
   ├── getpid() → İşlem ID
   └── id(obj) → ASLR bellek adresi

2. ÇOKLU LCG (Defense in Depth)
   ├── LCG-1: 64-bit, a=6364136223846793005
   ├── LCG-2: 64-bit, a=2862933555777941757
   └── LCG-3: 64-bit, a=3935559000370003845

3. OUTPUT TRANSFORMATION
   └── XorShift + Rotation → İç durum gizleme

4. SHA-256 HASH
   ├── Tek yönlü fonksiyon
   ├── Çığ etkisi (1 bit fark = tamamen farklı çıktı)
   └── Çarpışma direnci

5. YENİDEN TOHUMLAMA
   ├── Her 1000 çıktıda
   ├── Yeni entropi eklenir
   └── Forward secrecy garantisi

6. BIAS ÖNLEME
   └── Rejection sampling → Eşit dağılım

7. THREAD SAFETY
   └── Lock mekanizması
```

---

## 2.5 Karmaşıklık Analizi

| İşlem | Basit LCG | CSPRNG |
|-------|-----------|--------|
| Initialize | O(1) | O(1) |
| Next | O(1) | O(1)* |
| NextInt (rejection) | O(1) | O(1) expected |
| Memory | O(1) | O(256) bytes |

*SHA-256 maliyeti sabit ama LCG'den yüksek

---

## 2.6 Güvenlik Karşılaştırması

```
┌─────────────────────────┬─────────────────┬─────────────────────┐
│ Özellik                 │ Basit LCG       │ CSPRNG              │
├─────────────────────────┼─────────────────┼─────────────────────┤
│ Entropi Kaynağı         │ time.time()     │ OS + Donanım        │
│ Modül Boyutu            │ 31-bit          │ 64-bit × 3          │
│ Çıktı Dönüşümü          │ Yok             │ SHA-256             │
│ Yeniden Tohumlama       │ Yok             │ Her 1000 çıktı      │
│ Tahmin Edilebilirlik    │ KOLAY           │ İMKANSIZ            │
│ Kriptografik Kullanım   │ ❌ UYGUN DEĞİL  │ ✅ UYGUN            │
└─────────────────────────┴─────────────────┴─────────────────────┘
```

---

*Yazılım Mühendisliği - Bilgi Sistemleri ve Güvenliği*
