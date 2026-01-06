# Akis Semalari (Flowcharts)
## LCG ve CSPRNG Algoritmalari

Bu dokumanda hem basit LCG hem de kriptografik guvenli CSPRNG algoritmasinin akis semalari bulunmaktadir.

---

# BOLUM 1: BASIT LCG

## 1.1 LCG Ana Algoritma Akisi

```mermaid
flowchart TD
    subgraph INIT["BASLATMA"]
        A[Baslat] --> B{Seed Verildi mi?}
        B -->|Hayir| C["Sistem Zamani Al"]
        B -->|Evet| D["Verilen Seed Al"]
        C --> E["seed = time mod m"]
        D --> E
        E --> F["state = seed"]
    end
    
    subgraph GEN["URETIM"]
        F --> G["Xn+1 = a x Xn mod m"]
        G --> H["Degeri Dondur"]
    end
    
    subgraph LOOP["DEVAM"]
        H --> I{Devam?}
        I -->|Evet| G
        I -->|Hayir| J["Bitir"]
    end
    
    style INIT fill:#e1f5fe
    style GEN fill:#f3e5f5
    style LOOP fill:#e8f5e9
```

---

# BOLUM 2: KRIPTOGRAFIK GUVENLI CSPRNG

## 2.1 CSPRNG Genel Mimari

```mermaid
flowchart TB
    subgraph ENTROPY["ENTROPI KAYNAKLARI"]
        E1["OS urandom"]
        E2["Nanosaniye"]
        E3["PID/Thread"]
        E4["Bellek Adresi"]
    end
    
    subgraph POOL["ENTROPI HAVUZU"]
        P["256 Byte Havuz"]
    end
    
    subgraph GENERATORS["COKLU LCG"]
        L1["LCG-1 64-bit"]
        L2["LCG-2 64-bit"]
        L3["LCG-3 64-bit"]
    end
    
    subgraph MIX["KARISTIRMA"]
        X["XOR Birlestirme"]
        H["SHA-256 Hash"]
    end
    
    subgraph OUTPUT["CIKTI"]
        O["Guvenli Rastgele Sayi"]
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

## 2.2 Entropi Havuzu Detayi

```mermaid
flowchart TD
    subgraph SOURCES["ENTROPI KAYNAKLARI"]
        S1["os.urandom 64 byte"]
        S2["time.time_ns"]
        S3["os.getpid"]
        S4["id self - ASLR"]
    end
    
    subgraph COLLECT["TOPLAMA"]
        C["Bayt Dizisi Olustur"]
    end
    
    subgraph MIXZONE["KARISTIRMA"]
        M1["XOR ile Havuza Karistir"]
        M2["Position = pos+1 mod 256"]
    end
    
    subgraph POOL["HAVUZ"]
        P["256 Byte Dongusel Buffer"]
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
    style MIXZONE fill:#f3e5f5
    style POOL fill:#e8f5e9
```

---

## 2.3 Coklu LCG Kombinasyonu

```mermaid
flowchart LR
    subgraph SEED["TOHUMLAMA"]
        S["Entropi Havuzundan 24 Byte Al"]
        S --> S1["Seed 1 - 8 byte"]
        S --> S2["Seed 2 - 8 byte"]
        S --> S3["Seed 3 - 8 byte"]
    end
    
    subgraph LCG["3x LCG"]
        S1 --> L1["LCG-1"]
        S2 --> L2["LCG-2"]
        S3 --> L3["LCG-3"]
    end
    
    subgraph TRANSFORM["DONUSUM"]
        L1 --> T1["XorShift + Rotation"]
        L2 --> T2["XorShift + Rotation"]
        L3 --> T3["XorShift + Rotation"]
    end
    
    subgraph COMBINE["BIRLESTIRME"]
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

## 2.4 SHA-256 Hash Karistirma

```mermaid
flowchart TD
    subgraph INPUT["GIRDILER"]
        I1["LCG Kombinasyonu 64-bit"]
        I2["Nanosaniye Zaman 64-bit"]
        I3["Entropi Havuzu 16 byte"]
    end
    
    subgraph HASH["SHA-256"]
        H1["Girdileri Birlestir"]
        H2["SHA-256 Hesapla"]
        H3["32 Byte Digest"]
    end
    
    subgraph OUTPUT["CIKTI"]
        O1["Ilk 8 Byte = 64-bit Sayi"]
        O2["Geri Kalan = Gelecek Ciktilar"]
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
    A["Sayi Uretim Istegi"] --> B["outputCounter++"]
    B --> C{outputCounter >= 1000?}
    
    C -->|Hayir| D["Normal Uretim"]
    
    C -->|Evet| E["YENIDEN TOHUMLAMA"]
    E --> F["Yeni Entropi Al"]
    F --> G["3 LCG yi Yeniden Baslat"]
    G --> H["outputCounter = 0"]
    H --> D
    
    D --> I["Cikti Uret"]
    I --> J["Ciktiyi Entropiye Geri Besle"]
    
    style E fill:#ffcdd2
    style F fill:#e3f2fd
    style G fill:#c8e6c9
```

---

## 2.6 Moduler Bias Onleme - Rejection Sampling

```mermaid
flowchart TD
    A["next_int min max Cagrildi"] --> B["rangeSize = max - min + 1"]
    B --> C["maxAcceptable hesapla"]
    
    C --> D["DONGU"]
    D --> E["randomValue = next"]
    E --> F{randomValue < maxAcceptable?}
    
    F -->|Hayir| G["REDDET - Biasli Bolge"]
    G --> D
    
    F -->|Evet| H["KABUL"]
    H --> I["result = min + randomValue mod rangeSize"]
    I --> J["result dondur"]
    
    style G fill:#ffcdd2
    style H fill:#c8e6c9
```

---

## 2.7 Tam Uretim Akisi

```mermaid
flowchart TD
    subgraph REQUEST["ISTEK"]
        R["next cagrildi"]
    end
    
    subgraph CHECK["KONTROLLER"]
        R --> C1["Thread Lock Al"]
        C1 --> C2{Reseed Gerekli?}
        C2 -->|Evet| RS["Yeniden Tohumlama"]
        RS --> G1
        C2 -->|Hayir| G1
    end
    
    subgraph GENERATE["URETIM"]
        G1["LCG-1.next"] 
        G2["LCG-2.next"]
        G3["LCG-3.next"]
        G1 --> X["XOR Birlestir"]
        G2 --> X
        G3 --> X
    end
    
    subgraph HASHZONE["HASH"]
        X --> H1["+ Nanosaniye Zaman"]
        H1 --> H2["+ 16 Byte Entropi"]
        H2 --> H3["SHA-256"]
    end
    
    subgraph OUTPUT["CIKTI"]
        H3 --> O1["64-bit Sayi Cikar"]
        O1 --> O2["8 Byte Entropi Geri Besleme"]
        O2 --> O3["outputCounter++"]
        O3 --> O4["Lock Birak"]
        O4 --> O5["Guvenli Rastgele Sayi"]
    end
    
    style REQUEST fill:#e3f2fd
    style CHECK fill:#fff3e0
    style GENERATE fill:#c8e6c9
    style HASHZONE fill:#f3e5f5
    style OUTPUT fill:#ffcdd2
```

---

# BOLUM 3: KARSILASTIRMA

## 3.1 LCG vs CSPRNG

```mermaid
flowchart LR
    subgraph LCG["BASIT LCG"]
        L1["time.time"] --> L2["Tek LCG 31-bit"]
        L2 --> L3["Dogrudan Cikti"]
        L3 --> L4["TAHMIN EDILEBILIR"]
    end
    
    subgraph CSPRNG["GUVENLI CSPRNG"]
        C1["OS Entropi + Coklu Kaynak"] --> C2["3x LCG 64-bit"]
        C2 --> C3["XOR + SHA-256"]
        C3 --> C4["TAHMIN EDILEMEZ"]
    end
    
    style L4 fill:#ffcdd2
    style C4 fill:#c8e6c9
```

---

## Sema Notasyonu

| Sembol | Anlam |
|--------|-------|
| Dikdortgen | Islem / Komut |
| Eskenar Dortgen | Karar / Kosul |
| Oval | Baslat / Bitir |
| Ok | Akis Yonu |
| Kesikli Ok | Geri Besleme |
| Alt Grup | Modul / Bilesen |

---

*Bu akis semalari Mermaid formatinda hazirlanmistir ve GitHub da otomatik render edilir.*
