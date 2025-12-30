# 📊 Akış Şemaları (Flowcharts)
## LCG ve CSPRNG Algoritmaları

Bu dokümanda hem basit LCG hem de kriptografik güvenli CSPRNG algoritmasının akış şemaları bulunmaktadır.

---

# BÖLÜM 1: BASİT LCG

## 1.1 LCG Ana Algoritma Akışı

```mermaid
flowchart TD
    subgraph INIT["🚀 BAŞLATMA"]
        A[Başlat] --> B{Seed Verildi mi?}
        B -->|Hayır| C["⏱️ Sistem Zamanı Al"]
        B -->|Evet| D["📥 Verilen Seed'i Al"]
        C --> E["seed = time mod m"]
        D --> E
        E --> F["state = seed"]
    end
    
    subgraph GEN["🎲 ÜRETİM"]
        F --> G["X_{n+1} = (a × Xₙ) mod m"]
        G --> H["📤 Değeri Döndür"]
    end
    
    subgraph LOOP["🔁 DEVAM"]
        H --> I{Devam?}
        I -->|Evet| G
        I -->|Hayır| J["🏁 Bitir"]
    end
    
    style INIT fill:#e1f5fe
    style GEN fill:#f3e5f5
    style LOOP fill:#e8f5e9
```

---

# BÖLÜM 2: KRIPTOGRAFİK GÜVENLİ CSPRNG

## 2.1 CSPRNG Genel Mimari

```mermaid
flowchart TB
    subgraph ENTROPY["🎲 ENTROPİ KAYNAKLARI"]
        E1["🔐 OS urandom"]
        E2["⏱️ Nanosaniye"]
        E3["🔢 PID/Thread"]
        E4["📍 Bellek Adresi"]
    end
    
    subgraph POOL["🏊 ENTROPİ HAVUZU"]
        P["256 Byte Havuz"]
    end
    
    subgraph GENERATORS["⚙️ ÇOKLU LCG"]
        L1["LCG-1<br/>64-bit"]
        L2["LCG-2<br/>64-bit"]
        L3["LCG-3<br/>64-bit"]
    end
    
    subgraph MIX["🔀 KARIŞTIRMA"]
        X["XOR Birleştirme"]
        H["SHA-256 Hash"]
    end
    
    subgraph OUTPUT["📤 ÇIKTI"]
        O["Güvenli<br/>Rastgele Sayı"]
    end
    
    E1 --> P
    E2 --> P
    E3 --> P
    E4 --> P
    
    P --> L1
    P --> L2
    P --> L3
    
    L1 --> X
    L2 --> X
    L3 --> X
    
    X --> H
    H --> O
    O -.->|Geri Besleme| P
    
    style ENTROPY fill:#ffecb3
    style POOL fill:#b3e5fc
    style GENERATORS fill:#c8e6c9
    style MIX fill:#f3e5f5
    style OUTPUT fill:#ffcdd2
```

---

## 2.2 Entropi Havuzu Detayı

```mermaid
flowchart TD
    subgraph SOURCES["� ENTROPİ KAYNAKLARI"]
        S1["os.urandom(64)<br/>Donanım Gürültüsü"]
        S2["time.time_ns()<br/>Nanosaniye Zaman"]
        S3["os.getpid()<br/>İşlem ID"]
        S4["id(self)<br/>ASLR Bellek Adresi"]
    end
    
    subgraph COLLECT["🔄 TOPLAMA"]
        C["Bayt Dizisi Oluştur"]
    end
    
    subgraph MIX["🔀 KARIŞTIRMA"]
        M1["XOR ile Havuza Karıştır"]
        M2["Position = (pos + 1) mod 256"]
    end
    
    subgraph POOL["🏊 HAVUZ"]
        P["256 Byte Döngüsel Buffer"]
    end
    
    S1 --> C
    S2 --> C
    S3 --> C
    S4 --> C
    C --> M1
    M1 --> M2
    M2 --> P
    
    style SOURCES fill:#fff3e0
    style COLLECT fill:#e3f2fd
    style MIX fill:#f3e5f5
    style POOL fill:#e8f5e9
```

---

## 2.3 Çoklu LCG Kombinasyonu

```mermaid
flowchart LR
    subgraph SEED["🌱 TOHUMLAMA"]
        S["Entropi Havuzundan<br/>24 Byte Al"]
        S --> S1["Seed 1<br/>8 byte"]
        S --> S2["Seed 2<br/>8 byte"]
        S --> S3["Seed 3<br/>8 byte"]
    end
    
    subgraph LCG["⚙️ 3x LCG"]
        S1 --> L1["LCG-1<br/>a=6364136223846793005"]
        S2 --> L2["LCG-2<br/>a=2862933555777941757"]
        S3 --> L3["LCG-3<br/>a=3935559000370003845"]
    end
    
    subgraph TRANSFORM["🔄 DÖNÜŞÜM"]
        L1 --> T1["XorShift + Rotation"]
        L2 --> T2["XorShift + Rotation"]
        L3 --> T3["XorShift + Rotation"]
    end
    
    subgraph COMBINE["🔀 BİRLEŞTİRME"]
        T1 --> X["XOR"]
        T2 --> X
        T3 --> X
        X --> MX["MurmurHash Mix"]
    end
    
    style SEED fill:#e1f5fe
    style LCG fill:#c8e6c9
    style TRANSFORM fill:#fff3e0
    style COMBINE fill:#f3e5f5
```

---

## 2.4 SHA-256 Hash Karıştırma

```mermaid
flowchart TD
    subgraph INPUT["� GİRDİLER"]
        I1["LCG Kombinasyonu<br/>(64-bit)"]
        I2["Nanosaniye Zaman<br/>(64-bit)"]
        I3["Entropi Havuzu<br/>(16 byte)"]
    end
    
    subgraph HASH["� SHA-256"]
        H1["Girdileri Birleştir"]
        H2["SHA-256 Hesapla"]
        H3["32 Byte Digest"]
    end
    
    subgraph OUTPUT["📤 ÇIKTI"]
        O1["İlk 8 Byte<br/>= 64-bit Sayı"]
        O2["Geri Kalan<br/>= Gelecek Çıktılar"]
    end
    
    I1 --> H1
    I2 --> H1
    I3 --> H1
    H1 --> H2
    H2 --> H3
    H3 --> O1
    H3 --> O2
    
    style INPUT fill:#e3f2fd
    style HASH fill:#ffcdd2
    style OUTPUT fill:#c8e6c9
```

---

## 2.5 Otomatik Yeniden Tohumlama

```mermaid
flowchart TD
    A["Sayı Üretim İsteği"] --> B["outputCounter++"]
    B --> C{outputCounter >= 1000?}
    
    C -->|Hayır| D["Normal Üretim"]
    
    C -->|Evet| E["🔄 YENİDEN TOHUMLAMA"]
    E --> F["Yeni Entropi Al<br/>(os.urandom)"]
    F --> G["3 LCG'yi Yeniden Başlat"]
    G --> H["outputCounter = 0"]
    H --> D
    
    D --> I["Çıktı Üret"]
    I --> J["Çıktıyı Entropiye<br/>Geri Besle"]
    
    style E fill:#ffcdd2
    style F fill:#e3f2fd
    style G fill:#c8e6c9
```

---

## 2.6 Modüler Bias Önleme (Rejection Sampling)

```mermaid
flowchart TD
    A["next_int(min, max) Çağrıldı"] --> B["rangeSize = max - min + 1"]
    B --> C["maxAcceptable = (2^64 / rangeSize) × rangeSize"]
    
    C --> D["� DÖNGÜ"]
    D --> E["randomValue = next()"]
    E --> F{randomValue < maxAcceptable?}
    
    F -->|Hayır| G["❌ REDDET<br/>(Bias'lı Bölge)"]
    G --> D
    
    F -->|Evet| H["✅ KABUL"]
    H --> I["result = min + (randomValue mod rangeSize)"]
    I --> J["📤 result döndür"]
    
    style G fill:#ffcdd2
    style H fill:#c8e6c9
```

---

## 2.7 Tam Üretim Akışı

```mermaid
flowchart TD
    subgraph REQUEST["� İSTEK"]
        R["next() çağrıldı"]
    end
    
    subgraph CHECK["✅ KONTROLLER"]
        R --> C1["Thread Lock Al"]
        C1 --> C2{Reseed Gerekli?}
        C2 -->|Evet| RS["Yeniden Tohmlama"]
        RS --> G1
        C2 -->|Hayır| G1
    end
    
    subgraph GENERATE["⚙️ ÜRETİM"]
        G1["LCG-1.next()"] 
        G2["LCG-2.next()"]
        G3["LCG-3.next()"]
        G1 --> X["XOR Birleştir"]
        G2 --> X
        G3 --> X
    end
    
    subgraph HASH["🔒 HASH"]
        X --> H1["+ Nanosaniye Zaman"]
        H1 --> H2["+ 16 Byte Entropi"]
        H2 --> H3["SHA-256"]
    end
    
    subgraph OUTPUT["📤 ÇIKTI"]
        H3 --> O1["64-bit Sayı Çıkar"]
        O1 --> O2["8 Byte → Entropi Geri Besleme"]
        O2 --> O3["outputCounter++"]
        O3 --> O4["Lock Bırak"]
        O4 --> O5["🎲 Güvenli Rastgele Sayı"]
    end
    
    style REQUEST fill:#e3f2fd
    style CHECK fill:#fff3e0
    style GENERATE fill:#c8e6c9
    style HASH fill:#f3e5f5
    style OUTPUT fill:#ffcdd2
```

---

# BÖLÜM 3: KARŞILAŞTIRMA

## 3.1 LCG vs CSPRNG

```mermaid
flowchart LR
    subgraph LCG["🔓 BASİT LCG"]
        L1["time.time()"] --> L2["Tek LCG<br/>31-bit"]
        L2 --> L3["Doğrudan Çıktı"]
        L3 --> L4["❌ TAHMİN EDİLEBİLİR"]
    end
    
    subgraph CSPRNG["🔐 CSPRNG"]
        C1["OS Entropi<br/>+ Çoklu Kaynak"] --> C2["3x LCG<br/>64-bit"]
        C2 --> C3["XOR + SHA-256"]
        C3 --> C4["✅ TAHMİN EDİLEMEZ"]
    end
    
    style L4 fill:#ffcdd2
    style C4 fill:#c8e6c9
```

---

## 📐 Şema Notasyonu

| Sembol | Anlam |
|--------|-------|
| ⬜ Dikdörtgen | İşlem / Komut |
| ◇ Eşkenar Dörtgen | Karar / Koşul |
| ⬭ Oval | Başlat / Bitir |
| ➡️ Ok | Akış Yönü |
| - - -> | Geri Besleme |
| 📦 Alt Grup | Modül / Bileşen |

---

*Bu akış şemaları Mermaid formatında hazırlanmıştır ve GitHub'da otomatik render edilir.*
