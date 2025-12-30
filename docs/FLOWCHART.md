# 📊 Akış Şeması (Flowchart)
## Doğrusal Eşlik Üreteci (LCG) Algoritması

Bu dokümanda LCG algoritmasının farklı açılardan görselleştirilmiş akış şemaları bulunmaktadır.

---

## 1. Ana Algoritma Akışı

```mermaid
flowchart TD
    subgraph INITIALIZATION["🚀 BAŞLATMA (Initialization)"]
        A[Başlat] --> B{Seed Parametresi<br/>Verildi mi?}
        B -->|Hayır| C["⏱️ Sistem Zamanını Al<br/>(Mikrosaniye Hassasiyeti)"]
        B -->|Evet| D["📥 Verilen Seed'i Al"]
        C --> E["🔢 seed = time mod m"]
        D --> E
        E --> F{seed = 0 ?}
        F -->|Evet| G["seed = 1"]
        F -->|Hayır| H["state = seed"]
        G --> H
    end
    
    subgraph GENERATION["🎲 SAYI ÜRETİMİ (Generation)"]
        H --> I["📊 X₀ = state"]
        I --> J["🔄 LCG Formülü Uygula"]
        J --> K["X_{n+1} = (a × Xₙ + c) mod m"]
        K --> L["state = X_{n+1}"]
        L --> M["📤 Değeri Döndür"]
    end
    
    subgraph CONTINUE["🔁 DEVAM"]
        M --> N{Devam Edilecek mi?}
        N -->|Evet| J
        N -->|Hayır| O["🏁 Bitir"]
    end
    
    style INITIALIZATION fill:#e1f5fe
    style GENERATION fill:#f3e5f5
    style CONTINUE fill:#e8f5e9
```

---

## 2. LCG Temel Formülü Detayı

```mermaid
flowchart LR
    subgraph INPUT["📥 GİRDİ"]
        X["Xₙ<br/>(Mevcut Durum)"]
    end
    
    subgraph CONSTANTS["📐 SABİTLER"]
        A["a = 48,271<br/>(Çarpan)"]
        C["c = 0<br/>(Artış)"]
        M["m = 2³¹-1<br/>(Modül)"]
    end
    
    subgraph CALCULATION["🧮 HESAPLAMA"]
        MULT["a × Xₙ"]
        ADD["+ c"]
        MOD["mod m"]
    end
    
    subgraph OUTPUT["📤 ÇIKTI"]
        Y["X_{n+1}<br/>(Yeni Durum)"]
    end
    
    X --> MULT
    A --> MULT
    MULT --> ADD
    C --> ADD
    ADD --> MOD
    M --> MOD
    MOD --> Y
    
    style INPUT fill:#bbdefb
    style CONSTANTS fill:#fff3e0
    style CALCULATION fill:#f3e5f5
    style OUTPUT fill:#c8e6c9
```

---

## 3. Normalize Edilmiş Sayı Üretimi

```mermaid
flowchart TD
    A["🎯 NextFloat Çağrıldı"] --> B["📊 rawValue = Next()"]
    B --> C["🔢 rawValue aralığı:<br/>[1, 2,147,483,646]"]
    C --> D["📐 normalized = rawValue / m"]
    D --> E["✅ normalized aralığı:<br/>[0.0, 1.0)"]
    E --> F["📤 normalized değeri döndür"]
    
    style A fill:#e3f2fd
    style F fill:#c8e6c9
```

---

## 4. Aralıkta Sayı Üretimi

```mermaid
flowchart TD
    A["🎯 NextInt(min, max) Çağrıldı"] --> B{min > max ?}
    B -->|Evet| C["❌ Hata Fırlat"]
    B -->|Hayır| D["📊 rangeSize = max - min + 1"]
    D --> E["🎲 rawValue = Next()"]
    E --> F["🔢 result = min + (rawValue mod rangeSize)"]
    F --> G["📤 result döndür"]
    
    style C fill:#ffcdd2
    style G fill:#c8e6c9
```

---

## 5. Sistem Mimarisi

```mermaid
flowchart TB
    subgraph CLIENT["👤 KULLANICI KODU"]
        U1["rng.next()"]
        U2["rng.next_float()"]
        U3["rng.next_int(1, 100)"]
        U4["rng.generate_sequence(10)"]
    end
    
    subgraph LCG["🎲 LCG SINIFI"]
        direction TB
        INIT["__init__()"]
        NEXT["next()"]
        FLOAT["next_float()"]
        INT["next_int()"]
        SEQ["generate_sequence()"]
        STATS["calculate_statistics()"]
    end
    
    subgraph STATE["💾 DURUM"]
        S["currentState"]
        SEED["initialSeed"]
    end
    
    subgraph CONSTANTS["📐 SABİTLER"]
        M["MODULUS = 2³¹-1"]
        A["MULTIPLIER = 48271"]
        C["INCREMENT = 0"]
    end
    
    U1 --> NEXT
    U2 --> FLOAT
    U3 --> INT
    U4 --> SEQ
    
    NEXT --> S
    S --> NEXT
    
    NEXT -.-> M
    NEXT -.-> A
    NEXT -.-> C
    
    style CLIENT fill:#e3f2fd
    style LCG fill:#f3e5f5
    style STATE fill:#fff3e0
    style CONSTANTS fill:#e8f5e9
```

---

## 6. Dil Seçimi Akışı

```mermaid
flowchart TD
    A["🌍 Dil Seçimi"] --> B{Language Parametresi}
    B -->|TURKISH| C["🇹🇷 Türkçe Mesajlar"]
    B -->|ENGLISH| D["🇬🇧 English Messages"]
    
    C --> E["LocalizationManager<br/>currentLanguage = TR"]
    D --> F["LocalizationManager<br/>currentLanguage = EN"]
    
    E --> G["get_message(key)"]
    F --> G
    
    G --> H["MESSAGES[currentLanguage][key]"]
    H --> I["📤 Yerelleştirilmiş Metin"]
    
    style C fill:#ffcdd2
    style D fill:#bbdefb
    style I fill:#c8e6c9
```

---

## 7. İstatistiksel Test Akışı

```mermaid
flowchart TD
    A["📊 CalculateStatistics(n)"] --> B["💾 savedState = currentState"]
    B --> C["🔄 n adet örnek üret"]
    C --> D["📈 sum = Σ samples[i]"]
    D --> E["📐 mean = sum / n"]
    E --> F["📉 variance = Σ(x - mean)² / n"]
    F --> G["♻️ currentState = savedState"]
    G --> H["📤 {mean, variance, n}"]
    
    style A fill:#e3f2fd
    style H fill:#c8e6c9
```

---

## 8. JPEG Demo Akışı

```mermaid
flowchart TD
    subgraph SETUP["🔧 HAZIRLIK"]
        A["📷 Görüntü Yükle"] --> B["🎲 LCG Oluştur"]
        B --> C["📊 Standart JPEG Tablosu"]
        B --> D["🔀 Rastgele LCG Tablosu"]
    end
    
    subgraph PROCESS["⚙️ İŞLEME"]
        C --> E["DCT Uygula"]
        D --> F["DCT Uygula"]
        E --> G["Standart Tablo ile Kuantala"]
        F --> H["Rastgele Tablo ile Kuantala"]
        G --> I["Ters DCT"]
        H --> J["Ters DCT"]
    end
    
    subgraph OUTPUT["📤 ÇIKTI"]
        I --> K["✅ Normal Görüntü"]
        J --> L["❌ Bozuk Görüntü"]
        K --> M["📊 Karşılaştır"]
        L --> M
    end
    
    style SETUP fill:#e3f2fd
    style PROCESS fill:#fff3e0
    style OUTPUT fill:#e8f5e9
```

---

## 📐 Şema Notasyonu

| Sembol | Anlam |
|--------|-------|
| ⬜ Dikdörtgen | İşlem / Komut |
| ◇ Eşkenar Dörtgen | Karar / Koşul |
| ⬭ Oval | Başlat / Bitir |
| ➡️ Ok | Akış Yönü |
| 📦 Alt Grup | Modül / Bileşen |

---

*Bu akış şemaları Mermaid formatında hazırlanmıştır ve GitHub'da otomatik render edilir.*
