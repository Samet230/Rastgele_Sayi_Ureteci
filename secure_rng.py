#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kriptografik Güvenli Rastgele Sayı Üreteci (CSPRNG)
====================================================
Cryptographically Secure Pseudo-Random Number Generator

Bu modül, LCG'nin zayıflıklarını gidererek tahmin edilemez
ve kırılması son derece zor bir RNG implementasyonu sunar.

GÜVENLİK ÖZELLİKLERİ:
    1. OS Entropi Havuzu (os.urandom / /dev/urandom)
    2. SHA-256 Hash Karıştırma
    3. Çoklu LCG Kombinasyonu
    4. Sürekli Yeniden Tohumlama (Re-seeding)
    5. Durum Gizleme (Output Transformation)
    6. Entropi Biriktirme (Entropy Accumulation)

Author: Yazılım Mühendisliği Ekibi
Date: 2025
License: MIT
"""

import os
import time
import hashlib
import struct
import threading
from typing import List, Optional, Tuple
from enum import Enum


class Language(Enum):
    """Dil seçenekleri / Language options"""
    TURKISH = "TR"
    ENGLISH = "EN"


class EntropyPool:
    """
    Entropi Havuzu - Birden fazla kaynaktan entropi toplar.
    
    Entropy Pool - Collects entropy from multiple sources.
    
    Kaynaklar / Sources:
        - os.urandom (işletim sistemi entropi havuzu)
        - Sistem zamanı (nanosaniye hassasiyeti)
        - İşlem ID ve thread ID
        - Bellek adresleri
        - Önceki çıktılar (feedback)
    """
    
    def __init__(self, poolSize: int = 256):
        """
        Entropi havuzunu başlatır.
        
        Args:
            poolSize: Havuz boyutu (byte)
        """
        self.poolSize = poolSize
        self.pool = bytearray(poolSize)
        self.position = 0
        self.lock = threading.Lock()
        
        # İlk entropi toplama
        self._collect_initial_entropy()
    
    def _collect_initial_entropy(self) -> None:
        """Başlangıç entropisi toplar / Collects initial entropy."""
        sources = []
        
        # 1. OS entropi havuzu (en güvenilir kaynak)
        sources.append(os.urandom(64))
        
        # 2. Yüksek hassasiyetli zaman
        sources.append(struct.pack('d', time.time()))
        sources.append(struct.pack('q', time.time_ns()))
        
        # 3. İşlem bilgileri
        sources.append(struct.pack('i', os.getpid()))
        sources.append(struct.pack('q', threading.current_thread().ident or 0))
        
        # 4. Bellek adresleri (ASLR sayesinde rastgele)
        sources.append(struct.pack('q', id(self)))
        sources.append(struct.pack('q', id(sources)))
        
        # Tüm kaynakları karıştır
        combinedEntropy = b''.join(sources)
        self._mix_into_pool(combinedEntropy)
    
    def _mix_into_pool(self, data: bytes) -> None:
        """
        Veriyi havuza karıştırır.
        
        Args:
            data: Karıştırılacak veri
        """
        with self.lock:
            for byte in data:
                self.pool[self.position] ^= byte
                self.position = (self.position + 1) % self.poolSize
    
    def add_entropy(self, data: bytes) -> None:
        """
        Havuza ek entropi ekler.
        
        Args:
            data: Eklenecek entropi verisi
        """
        # Zamanı da ekle (timing attack koruması)
        timeBytes = struct.pack('q', time.time_ns())
        self._mix_into_pool(timeBytes + data)
    
    def get_entropy(self, numBytes: int) -> bytes:
        """
        Havuzdan entropi çeker ve havuzu günceller.
        
        Args:
            numBytes: İstenen byte sayısı
        
        Returns:
            bytes: Entropi verisi
        """
        with self.lock:
            # Havuzu hash'le
            hasher = hashlib.sha256()
            hasher.update(bytes(self.pool))
            hasher.update(struct.pack('q', time.time_ns()))
            digest = hasher.digest()
            
            # Havuzu güncelle (forward secrecy)
            newHasher = hashlib.sha256()
            newHasher.update(digest)
            newHasher.update(os.urandom(32))
            newPool = newHasher.digest() * (self.poolSize // 32 + 1)
            self.pool = bytearray(newPool[:self.poolSize])
            
            # İstenen miktarı döndür
            if numBytes <= 32:
                return digest[:numBytes]
            else:
                # Daha fazla byte gerekiyorsa
                result = bytearray()
                while len(result) < numBytes:
                    hasher = hashlib.sha256()
                    hasher.update(digest)
                    hasher.update(struct.pack('i', len(result)))
                    digest = hasher.digest()
                    result.extend(digest)
                return bytes(result[:numBytes])


class SecureLCG:
    """
    Güçlendirilmiş LCG - Tek başına kullanılmaz, kombinasyon için.
    
    Enhanced LCG - Not used alone, for combination purposes.
    
    64-bit modül ve güçlü çarpanlar kullanır.
    """
    
    # Farklı LCG parametreleri (birden fazla kullanılacak)
    PARAMS = [
        # (multiplier, increment, modulus) - PCG ailesinden esinlenilmiş
        (6364136223846793005, 1442695040888963407, 2**64),
        (2862933555777941757, 3037000493, 2**64),
        (3935559000370003845, 2691343689449507681, 2**64),
    ]
    
    def __init__(self, seed: int, paramIndex: int = 0):
        """
        SecureLCG başlatır.
        
        Args:
            seed: 64-bit seed değeri
            paramIndex: Kullanılacak parametre seti
        """
        params = self.PARAMS[paramIndex % len(self.PARAMS)]
        self.multiplier = params[0]
        self.increment = params[1]
        self.modulus = params[2]
        self.state = seed % self.modulus
        
        # Warmup - ilk değerleri at (başlangıç zayıflığını gider)
        for _ in range(20):
            self._advance()
    
    def _advance(self) -> int:
        """İç durumu ilerletir / Advances internal state."""
        self.state = (self.multiplier * self.state + self.increment) % self.modulus
        return self.state
    
    def next(self) -> int:
        """
        Sonraki değeri üretir (output transformation ile).
        
        XorShift ve rotation uygulayarak iç durumu gizler.
        """
        value = self._advance()
        
        # Output transformation (PCG tarzı)
        # İç durumdan tahmin edilemez çıktı üret
        xorshifted = ((value >> 18) ^ value) >> 27
        rot = value >> 59
        
        return ((xorshifted >> rot) | (xorshifted << ((-rot) & 31))) & 0xFFFFFFFF


class CryptographicallySecureRNG:
    """
    Kriptografik Güvenli Rastgele Sayı Üreteci
    
    Cryptographically Secure Random Number Generator
    
    Özellikler / Features:
        - OS entropisinden beslenir
        - Çoklu LCG kombinasyonu
        - SHA-256 karıştırma
        - Otomatik yeniden tohumlama
        - Forward secrecy (geçmiş çıktılar kırılamaz)
        - Durum tahmin edilemezliği
    """
    
    # Kaç çıktıdan sonra yeniden tohumlanacak
    RESEED_INTERVAL = 1000
    
    def __init__(self, language: Language = Language.TURKISH):
        """
        CSPRNG'yi başlatır.
        
        Args:
            language: Çıktı dili
        """
        self.language = language
        self.entropyPool = EntropyPool()
        self.outputCounter = 0
        self.lock = threading.Lock()
        
        # Birden fazla LCG oluştur (farklı parametrelerle)
        self._initialize_generators()
    
    def _initialize_generators(self) -> None:
        """Jeneratörleri başlatır / Initializes generators."""
        # Entropi havuzundan seed al
        seedBytes = self.entropyPool.get_entropy(24)  # 3 x 8 byte
        
        seeds = [
            int.from_bytes(seedBytes[0:8], 'big'),
            int.from_bytes(seedBytes[8:16], 'big'),
            int.from_bytes(seedBytes[16:24], 'big'),
        ]
        
        self.generators = [
            SecureLCG(seeds[0], 0),
            SecureLCG(seeds[1], 1),
            SecureLCG(seeds[2], 2),
        ]
    
    def _reseed_if_needed(self) -> None:
        """Gerekirse yeniden tohumlar / Reseeds if necessary."""
        if self.outputCounter >= self.RESEED_INTERVAL:
            # Yeni entropi al ve jeneratörleri yeniden başlat
            self._initialize_generators()
            self.outputCounter = 0
    
    def _combine_generators(self) -> int:
        """
        Tüm jeneratörlerin çıktılarını birleştirir.
        
        XOR + rotation ile kombinasyon.
        """
        values = [gen.next() for gen in self.generators]
        
        # XOR kombinasyonu
        combined = values[0] ^ values[1] ^ values[2]
        
        # Ek karıştırma
        combined ^= (combined >> 16)
        combined *= 0x85ebca6b
        combined &= 0xFFFFFFFF
        combined ^= (combined >> 13)
        combined *= 0xc2b2ae35
        combined &= 0xFFFFFFFF
        combined ^= (combined >> 16)
        
        return combined
    
    def _hash_with_entropy(self, value: int) -> bytes:
        """
        Değeri entropi ile hash'ler.
        
        Args:
            value: Hash'lenecek değer
        
        Returns:
            bytes: 32-byte hash
        """
        hasher = hashlib.sha256()
        hasher.update(struct.pack('Q', value))
        hasher.update(struct.pack('q', time.time_ns()))
        hasher.update(self.entropyPool.get_entropy(16))
        return hasher.digest()
    
    def next_bytes(self, numBytes: int) -> bytes:
        """
        Kriptografik güvenli rastgele byte dizisi üretir.
        
        Args:
            numBytes: İstenen byte sayısı
        
        Returns:
            bytes: Rastgele byte dizisi
        """
        with self.lock:
            self._reseed_if_needed()
            
            result = bytearray()
            while len(result) < numBytes:
                combined = self._combine_generators()
                hashOutput = self._hash_with_entropy(combined)
                result.extend(hashOutput)
                self.outputCounter += 1
            
            # Kullanılan çıktıyı entropiye geri besle
            self.entropyPool.add_entropy(bytes(result[:8]))
            
            return bytes(result[:numBytes])
    
    def next(self) -> int:
        """
        64-bit rastgele tam sayı üretir.
        
        Returns:
            int: [0, 2^64) aralığında
        """
        randomBytes = self.next_bytes(8)
        return int.from_bytes(randomBytes, 'big')
    
    def next_int(self, minValue: int, maxValue: int) -> int:
        """
        Belirtilen aralıkta rastgele tam sayı üretir.
        
        Modüler bias'ı önlemek için rejection sampling kullanır.
        
        Args:
            minValue: Minimum değer (dahil)
            maxValue: Maksimum değer (dahil)
        
        Returns:
            int: [minValue, maxValue] aralığında
        """
        if minValue > maxValue:
            raise ValueError("minValue cannot be greater than maxValue")
        
        rangeSize = maxValue - minValue + 1
        
        # Bias'ı önlemek için rejection sampling
        # 2^64'ten büyük en yakın rangeSize katını bul
        maxAcceptable = (2**64 // rangeSize) * rangeSize
        
        while True:
            randomValue = self.next()
            if randomValue < maxAcceptable:
                return minValue + (randomValue % rangeSize)
    
    def next_float(self) -> float:
        """
        [0.0, 1.0) aralığında rastgele ondalıklı sayı üretir.
        
        53-bit hassasiyet (IEEE 754 double precision).
        """
        # 53-bit mantissa için
        randomBytes = self.next_bytes(7)
        value = int.from_bytes(randomBytes, 'big') >> 3  # 53 bit
        return value / (2**53)
    
    def shuffle(self, sequence: list) -> None:
        """
        Listeyi yerinde karıştırır (Fisher-Yates).
        
        Args:
            sequence: Karıştırılacak liste
        """
        for i in range(len(sequence) - 1, 0, -1):
            j = self.next_int(0, i)
            sequence[i], sequence[j] = sequence[j], sequence[i]
    
    def choice(self, sequence: list):
        """
        Listeden rastgele eleman seçer.
        
        Args:
            sequence: Seçim yapılacak liste
        
        Returns:
            Rastgele seçilen eleman
        """
        if not sequence:
            raise ValueError("Cannot choose from empty sequence")
        return sequence[self.next_int(0, len(sequence) - 1)]
    
    def generate_token(self, length: int = 32) -> str:
        """
        Kriptografik güvenli token üretir.
        
        Args:
            length: Token uzunluğu (karakter)
        
        Returns:
            str: Hex formatında token
        """
        numBytes = (length + 1) // 2
        return self.next_bytes(numBytes).hex()[:length]
    
    def generate_password(self, length: int = 16, 
                          includeSpecial: bool = True) -> str:
        """
        Güvenli şifre üretir.
        
        Args:
            length: Şifre uzunluğu
            includeSpecial: Özel karakter eklensin mi
        
        Returns:
            str: Rastgele şifre
        """
        lowercase = "abcdefghijklmnopqrstuvwxyz"
        uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        digits = "0123456789"
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if includeSpecial:
            alphabet = lowercase + uppercase + digits + special
        else:
            alphabet = lowercase + uppercase + digits
        
        password = [self.choice(list(alphabet)) for _ in range(length)]
        
        # En az 1 küçük, 1 büyük, 1 rakam olduğundan emin ol
        password[0] = self.choice(list(lowercase))
        password[1] = self.choice(list(uppercase))
        password[2] = self.choice(list(digits))
        if includeSpecial and length > 3:
            password[3] = self.choice(list(special))
        
        # Karıştır
        self.shuffle(password)
        
        return ''.join(password)
    
    def display_security_info(self) -> None:
        """Güvenlik bilgilerini gösterir / Displays security info."""
        if self.language == Language.TURKISH:
            print("\n" + "=" * 70)
            print("🔐 KRIPTOGRAFİK GÜVENLİ RASTGELE SAYI ÜRETECİ (CSPRNG)")
            print("=" * 70)
            print("""
    ✅ GÜVENLİK ÖZELLİKLERİ:
    
    1. 🎲 OS Entropi Havuzu
       - /dev/urandom (Linux) veya CryptGenRandom (Windows)
       - Donanım gürültüsü, kesme zamanlamaları, disk I/O
    
    2. 🔀 Çoklu LCG Kombinasyonu
       - 3 farklı 64-bit LCG paralel çalışır
       - XOR ile birleştirilir (tek başına kırılamaz)
    
    3. 🔒 SHA-256 Karıştırma
       - Her çıktı hash'lenir
       - İç durum çıktıdan türetilemez
    
    4. ♻️ Otomatik Yeniden Tohumlama
       - Her 1000 çıktıda yeni entropi eklenir
       - Forward secrecy garantisi
    
    5. 🛡️ Modüler Bias Önleme
       - Rejection sampling ile eşit dağılım
       - Aralık seçiminde yanlılık yok
    
    6. 🔐 Thread-Safe
       - Çoklu iş parçacığı güvenli
       - Lock mekanizması ile senkronizasyon
""")
        else:
            print("\n" + "=" * 70)
            print("🔐 CRYPTOGRAPHICALLY SECURE RANDOM NUMBER GENERATOR (CSPRNG)")
            print("=" * 70)
            print("""
    ✅ SECURITY FEATURES:
    
    1. 🎲 OS Entropy Pool
       - /dev/urandom (Linux) or CryptGenRandom (Windows)
       - Hardware noise, interrupt timing, disk I/O
    
    2. 🔀 Multiple LCG Combination
       - 3 different 64-bit LCGs run in parallel
       - Combined with XOR (cannot be broken individually)
    
    3. 🔒 SHA-256 Mixing
       - Every output is hashed
       - Internal state cannot be derived from output
    
    4. ♻️ Automatic Reseeding
       - New entropy added every 1000 outputs
       - Forward secrecy guarantee
    
    5. 🛡️ Modular Bias Prevention
       - Equal distribution with rejection sampling
       - No bias in range selection
    
    6. 🔐 Thread-Safe
       - Safe for multi-threaded use
       - Synchronized with lock mechanism
""")
        print("=" * 70 + "\n")


def compare_security():
    """LCG ve CSPRNG güvenlik karşılaştırması / Security comparison."""
    print("\n" + "=" * 70)
    print("🔍 GÜVENLİK KARŞILAŞTIRMASI / SECURITY COMPARISON")
    print("=" * 70)
    
    # Import original LCG
    from lcg_generator import LinearCongruentialGenerator, Language as LCGLanguage
    
    print("""
    ┌─────────────────────────┬─────────────────┬─────────────────────┐
    │ Özellik                 │ Basit LCG       │ CSPRNG (Güvenli)    │
    ├─────────────────────────┼─────────────────┼─────────────────────┤
    │ Entropi Kaynağı         │ Sistem zamanı   │ OS + Donanım        │
    │ Modül Boyutu            │ 31-bit          │ 64-bit × 3          │
    │ Çıktı Dönüşümü          │ Yok             │ SHA-256 hash        │
    │ Yeniden Tohumlama       │ Yok             │ Her 1000 çıktı      │
    │ Bias Önleme             │ Yok             │ Rejection sampling  │
    │ Thread Safety           │ Yok             │ Lock mekanizması    │
    │ Tahmin Edilebilirlik    │ KOLAY           │ İMKANSIZ            │
    │ Kriptografik Kullanım   │ ❌ UYGUN DEĞİL  │ ✅ UYGUN            │
    └─────────────────────────┴─────────────────┴─────────────────────┘
    """)
    
    # Örnek karşılaştırma
    print("\n📊 ÖRNEK ÇIKTILAR:\n")
    
    print("🔓 Basit LCG (tahmin edilebilir):")
    lcg = LinearCongruentialGenerator(seed=12345, language=LCGLanguage.TURKISH)
    for i in range(5):
        print(f"   {lcg.next():>15,}")
    
    print("\n🔐 CSPRNG (tahmin edilemez):")
    csprng = CryptographicallySecureRNG()
    for i in range(5):
        print(f"   {csprng.next():>20,}")
    
    print("\n" + "=" * 70 + "\n")


def demo():
    """Ana demo fonksiyonu / Main demo function."""
    csprng = CryptographicallySecureRNG(language=Language.TURKISH)
    
    # Güvenlik bilgilerini göster
    csprng.display_security_info()
    
    print("🧪 DEMO ÇIKTILARI:\n")
    
    # Token üretimi
    print("🔑 Güvenli Token (32 karakter):")
    print(f"   {csprng.generate_token(32)}\n")
    
    # Şifre üretimi
    print("🔐 Güvenli Şifre (16 karakter):")
    print(f"   {csprng.generate_password(16)}\n")
    
    # Rastgele sayılar
    print("🎲 Rastgele Sayılar (64-bit):")
    for i in range(5):
        print(f"   [{i+1}] {csprng.next():,}")
    
    # Aralıkta sayı
    print("\n🎯 Zar Atışları (1-6):")
    dice = [csprng.next_int(1, 6) for _ in range(10)]
    print(f"   {dice}")
    
    # Float
    print("\n📊 Normalize [0,1):")
    for i in range(3):
        print(f"   [{i+1}] {csprng.next_float():.15f}")
    
    print("\n" + "=" * 70)
    print("✅ Tüm çıktılar kriptografik olarak güvenlidir!")
    print("=" * 70 + "\n")
    
    # Karşılaştırma
    compare_security()


if __name__ == "__main__":
    demo()
