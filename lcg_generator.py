#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Linear Congruential Generator (LCG) - Doğrusal Eşlik Üreteci
============================================================
Bilgi Sistemleri ve Güvenliği Dersi Projesi
Yazılım Mühendisliği - 4. Sınıf

Bu modül, POSIX standartlarına uygun sabitler kullanarak
deterministik bir sözde-rastgele sayı üreteci (PRNG) implementasyonu sunar.

Author: Yazılım Mühendisliği Ekibi
Date: 2025
License: MIT
"""

import time
from enum import Enum
from typing import List, Optional, Tuple
from abc import ABC, abstractmethod


class Language(Enum):
    """
    Desteklenen dil seçenekleri.
    Supported language options.
    """
    TURKISH = "TR"
    ENGLISH = "EN"


class LocalizationManager:
    """
    Çoklu dil desteği için yerelleştirme yöneticisi.
    Localization manager for multi-language support.
    """
    
    # Dil sözlükleri / Language dictionaries
    MESSAGES = {
        Language.TURKISH: {
            "welcome": "=== Doğrusal Eşlik Üreteci (LCG) ===",
            "seed_info": "Tohum Değeri (Seed)",
            "generated_numbers": "Üretilen Rastgele Sayılar",
            "normalized": "Normalize Edilmiş [0,1]",
            "raw": "Ham Değer",
            "parameters": "Algoritma Parametreleri",
            "modulus": "Modül (m)",
            "multiplier": "Çarpan (a)",
            "increment": "Artış (c)",
            "period_info": "Periyot Bilgisi",
            "max_period": "Maksimum Periyot",
            "security_warning": "⚠️ UYARI: Bu algoritma kriptografik amaçlar için GÜVENLİ DEĞİLDİR!",
            "educational_purpose": "Bu implementasyon yalnızca eğitim amaçlıdır.",
            "language_selected": "Dil seçildi: Türkçe",
            "generating": "Sayılar üretiliyor...",
            "complete": "İşlem tamamlandı.",
            "range_output": "Aralık çıktısı [{}, {}]",
            "statistical_test": "İstatistiksel Test Sonuçları",
            "mean": "Ortalama",
            "variance": "Varyans",
            "expected_mean": "Beklenen Ortalama (Uniform): 0.5",
            "expected_variance": "Beklenen Varyans (Uniform): 0.0833"
        },
        Language.ENGLISH: {
            "welcome": "=== Linear Congruential Generator (LCG) ===",
            "seed_info": "Seed Value",
            "generated_numbers": "Generated Random Numbers",
            "normalized": "Normalized [0,1]",
            "raw": "Raw Value",
            "parameters": "Algorithm Parameters",
            "modulus": "Modulus (m)",
            "multiplier": "Multiplier (a)",
            "increment": "Increment (c)",
            "period_info": "Period Information",
            "max_period": "Maximum Period",
            "security_warning": "⚠️ WARNING: This algorithm is NOT SECURE for cryptographic purposes!",
            "educational_purpose": "This implementation is for educational purposes only.",
            "language_selected": "Language selected: English",
            "generating": "Generating numbers...",
            "complete": "Operation complete.",
            "range_output": "Range output [{}, {}]",
            "statistical_test": "Statistical Test Results",
            "mean": "Mean",
            "variance": "Variance",
            "expected_mean": "Expected Mean (Uniform): 0.5",
            "expected_variance": "Expected Variance (Uniform): 0.0833"
        }
    }
    
    def __init__(self, language: Language = Language.TURKISH):
        """
        Yerelleştirme yöneticisini başlatır.
        Initializes the localization manager.
        
        Args:
            language: Kullanılacak dil / Language to use
        """
        self.currentLanguage = language
    
    def set_language(self, language: Language) -> None:
        """
        Aktif dili değiştirir.
        Changes the active language.
        """
        self.currentLanguage = language
    
    def get_message(self, key: str) -> str:
        """
        Belirtilen anahtar için yerelleştirilmiş mesajı döndürür.
        Returns the localized message for the specified key.
        """
        return self.MESSAGES[self.currentLanguage].get(key, key)
    
    def get(self, key: str) -> str:
        """
        Kısa erişim metodu / Short access method.
        """
        return self.get_message(key)


class RandomNumberGenerator(ABC):
    """
    Soyut Rastgele Sayı Üreteci temel sınıfı.
    Abstract base class for Random Number Generators.
    """
    
    @abstractmethod
    def next(self) -> int:
        """Bir sonraki rastgele sayıyı üretir / Generates the next random number."""
        pass
    
    @abstractmethod
    def next_float(self) -> float:
        """[0,1) aralığında normalize edilmiş sayı üretir / Generates normalized number in [0,1)."""
        pass
    
    @abstractmethod
    def reset(self, seed: Optional[int] = None) -> None:
        """Üreteci sıfırlar / Resets the generator."""
        pass


class LinearCongruentialGenerator(RandomNumberGenerator):
    """
    Doğrusal Eşlik Üreteci (Linear Congruential Generator - LCG)
    
    Matematiksel Formül / Mathematical Formula:
        X_{n+1} = (a * X_n + c) mod m
    
    Burada / Where:
        - X_n  : Mevcut durum (current state)
        - a    : Çarpan (multiplier)
        - c    : Artış (increment)
        - m    : Modül (modulus)
    
    POSIX Standart Sabitleri (minstd_rand):
        - m = 2^31 - 1 = 2,147,483,647 (Mersenne Asal / Mersenne Prime)
        - a = 48271 (Park-Miller çarpanı / Park-Miller multiplier)
        - c = 0 (Çarpımsal LCG / Multiplicative LCG)
    
    Bu sabitler, tam periyot garantisi ve iyi istatistiksel özellikler sağlar.
    These constants ensure full period and good statistical properties.
    """
    
    # POSIX uyumlu sabitler / POSIX compliant constants
    # Mersenne Prime: 2^31 - 1 (7. Mersenne asal sayısı)
    MODULUS: int = 2**31 - 1  # 2,147,483,647
    
    # Park-Miller çarpanı (POSIX minstd_rand standardı)
    MULTIPLIER: int = 48271
    
    # Çarpımsal LCG için artış değeri sıfır
    INCREMENT: int = 0
    
    def __init__(
        self, 
        seed: Optional[int] = None, 
        language: Language = Language.TURKISH
    ):
        """
        LCG'yi başlatır.
        Initializes the LCG.
        
        Args:
            seed: Başlangıç tohum değeri. None ise sistem zamanı kullanılır.
                  Initial seed value. If None, system time is used.
            language: Çıktı dili / Output language
        """
        self.localization = LocalizationManager(language)
        self._initialize_seed(seed)
        self.initialSeed = self.currentState
    
    def _initialize_seed(self, seed: Optional[int]) -> None:
        """
        Tohum değerini başlatır.
        Initializes the seed value.
        
        Eğer seed verilmezse, sistem zamanının mikrosaniye hassasiyetinde
        değeri kullanılır. Bu, her çalıştırmada farklı bir dizi sağlar.
        
        If no seed is provided, the microsecond precision of system time
        is used. This ensures a different sequence on each run.
        """
        if seed is None:
            # Mikrosaniye hassasiyetinde sistem zamanı
            # System time with microsecond precision
            currentTimeMicroseconds = int(time.time() * 1_000_000)
            # Modül aralığına sığdır / Fit within modulus range
            seed = currentTimeMicroseconds % self.MODULUS
            # Sıfır seed'den kaçın / Avoid zero seed
            if seed == 0:
                seed = 1
        
        self.currentState = seed % self.MODULUS
        if self.currentState == 0:
            self.currentState = 1
    
    def next(self) -> int:
        """
        Bir sonraki sözde-rastgele sayıyı üretir.
        Generates the next pseudo-random number.
        
        LCG Formülü / LCG Formula:
            X_{n+1} = (a * X_n + c) mod m
        
        Returns:
            int: [1, m-1] aralığında tam sayı / Integer in range [1, m-1]
        """
        # X_{n+1} = (a * X_n + c) mod m
        self.currentState = (
            self.MULTIPLIER * self.currentState + self.INCREMENT
        ) % self.MODULUS
        
        return self.currentState
    
    def next_float(self) -> float:
        """
        [0, 1) aralığında normalize edilmiş rastgele sayı üretir.
        Generates a normalized random number in [0, 1) range.
        
        Returns:
            float: [0, 1) aralığında ondalıklı sayı / Float in [0, 1) range
        """
        return self.next() / self.MODULUS
    
    def next_int(self, minValue: int, maxValue: int) -> int:
        """
        Belirtilen aralıkta rastgele tam sayı üretir.
        Generates a random integer within the specified range.
        
        Args:
            minValue: Minimum değer (dahil) / Minimum value (inclusive)
            maxValue: Maksimum değer (dahil) / Maximum value (inclusive)
        
        Returns:
            int: [minValue, maxValue] aralığında tam sayı
        """
        if minValue > maxValue:
            raise ValueError("minValue cannot be greater than maxValue")
        
        rangeSize = maxValue - minValue + 1
        return minValue + (self.next() % rangeSize)
    
    def generate_sequence(self, count: int) -> List[int]:
        """
        Belirtilen sayıda rastgele sayı dizisi üretir.
        Generates a sequence of random numbers.
        
        Args:
            count: Üretilecek sayı adedi / Number of values to generate
        
        Returns:
            List[int]: Rastgele sayı listesi / List of random numbers
        """
        return [self.next() for _ in range(count)]
    
    def generate_normalized_sequence(self, count: int) -> List[float]:
        """
        Normalize edilmiş [0,1) aralığında sayı dizisi üretir.
        Generates a normalized sequence in [0,1) range.
        
        Args:
            count: Üretilecek sayı adedi / Number of values to generate
        
        Returns:
            List[float]: Normalize edilmiş sayı listesi
        """
        return [self.next_float() for _ in range(count)]
    
    def reset(self, seed: Optional[int] = None) -> None:
        """
        Üreteci başlangıç durumuna sıfırlar.
        Resets the generator to initial state.
        
        Args:
            seed: Yeni tohum değeri. None ise orijinal tohum kullanılır.
                  New seed value. If None, original seed is used.
        """
        if seed is not None:
            self._initialize_seed(seed)
            self.initialSeed = self.currentState
        else:
            self.currentState = self.initialSeed
    
    def set_language(self, language: Language) -> None:
        """
        Çıktı dilini değiştirir.
        Changes the output language.
        """
        self.localization.set_language(language)
    
    def get_parameters(self) -> dict:
        """
        Algoritma parametrelerini döndürür.
        Returns the algorithm parameters.
        """
        return {
            "modulus": self.MODULUS,
            "multiplier": self.MULTIPLIER,
            "increment": self.INCREMENT,
            "initial_seed": self.initialSeed,
            "max_period": self.MODULUS - 1
        }
    
    def calculate_statistics(self, sampleSize: int = 10000) -> dict:
        """
        Üretilen sayılar için istatistiksel analiz yapar.
        Performs statistical analysis on generated numbers.
        
        Args:
            sampleSize: Örnek büyüklüğü / Sample size
        
        Returns:
            dict: İstatistiksel metrikler / Statistical metrics
        """
        # Mevcut durumu kaydet / Save current state
        savedState = self.currentState
        
        # Örnek üret / Generate samples
        samples = self.generate_normalized_sequence(sampleSize)
        
        # Ortalama hesapla / Calculate mean
        mean = sum(samples) / len(samples)
        
        # Varyans hesapla / Calculate variance
        variance = sum((x - mean) ** 2 for x in samples) / len(samples)
        
        # Durumu geri yükle / Restore state
        self.currentState = savedState
        
        return {
            "sample_size": sampleSize,
            "mean": mean,
            "variance": variance,
            "expected_mean": 0.5,
            "expected_variance": 1/12  # Uniform [0,1] için / For Uniform [0,1]
        }
    
    def display_info(self) -> None:
        """
        Algoritma bilgilerini ve örnek çıktıları gösterir.
        Displays algorithm information and sample outputs.
        """
        loc = self.localization
        
        print("\n" + "=" * 60)
        print(loc.get("welcome"))
        print("=" * 60)
        
        # Güvenlik uyarısı / Security warning
        print(f"\n{loc.get('security_warning')}")
        print(f"{loc.get('educational_purpose')}\n")
        
        # Parametreler / Parameters
        print(f"\n📊 {loc.get('parameters')}:")
        print("-" * 40)
        params = self.get_parameters()
        print(f"   {loc.get('modulus')}: {params['modulus']:,}")
        print(f"   {loc.get('multiplier')}: {params['multiplier']:,}")
        print(f"   {loc.get('increment')}: {params['increment']}")
        print(f"   {loc.get('seed_info')}: {params['initial_seed']:,}")
        
        # Periyot bilgisi / Period info
        print(f"\n📈 {loc.get('period_info')}:")
        print("-" * 40)
        print(f"   {loc.get('max_period')}: {params['max_period']:,}")
        
        # Örnek sayılar / Sample numbers
        print(f"\n🎲 {loc.get('generated_numbers')}:")
        print("-" * 40)
        print(f"   {loc.get('generating')}")
        
        for i in range(5):
            rawValue = self.next()
            normalized = rawValue / self.MODULUS
            print(f"   [{i+1}] {loc.get('raw')}: {rawValue:>15,} | "
                  f"{loc.get('normalized')}: {normalized:.10f}")
        
        # İstatistiksel test / Statistical test
        print(f"\n📉 {loc.get('statistical_test')}:")
        print("-" * 40)
        stats = self.calculate_statistics(10000)
        print(f"   {loc.get('mean')}: {stats['mean']:.6f}")
        print(f"   {loc.get('variance')}: {stats['variance']:.6f}")
        print(f"   {loc.get('expected_mean')}")
        print(f"   {loc.get('expected_variance')}")
        
        print(f"\n{loc.get('complete')}")
        print("=" * 60 + "\n")


def demonstrate_language_feature():
    """
    Dil özelliğini gösterir.
    Demonstrates the language feature.
    """
    print("\n" + "=" * 60)
    print("🌍 DİL DESTEĞİ GÖSTERİMİ / LANGUAGE SUPPORT DEMONSTRATION")
    print("=" * 60)
    
    # Aynı seed ile iki üreteci oluştur
    # Create two generators with the same seed
    fixedSeed = 12345
    
    # Türkçe versiyon / Turkish version
    print("\n🇹🇷 TÜRKÇE ÇIKTI:")
    print("-" * 40)
    lcgTurkish = LinearCongruentialGenerator(seed=fixedSeed, language=Language.TURKISH)
    print(f"   {lcgTurkish.localization.get('seed_info')}: {fixedSeed}")
    print(f"   {lcgTurkish.localization.get('generated_numbers')}:")
    for i in range(3):
        print(f"      [{i+1}] {lcgTurkish.next():,}")
    
    # İngilizce versiyon / English version
    print("\n🇬🇧 ENGLISH OUTPUT:")
    print("-" * 40)
    lcgEnglish = LinearCongruentialGenerator(seed=fixedSeed, language=Language.ENGLISH)
    print(f"   {lcgEnglish.localization.get('seed_info')}: {fixedSeed}")
    print(f"   {lcgEnglish.localization.get('generated_numbers')}:")
    for i in range(3):
        print(f"      [{i+1}] {lcgEnglish.next():,}")
    
    print("\n✅ Aynı seed, aynı sayılar, farklı dil çıktısı!")
    print("✅ Same seed, same numbers, different language output!")
    print("=" * 60 + "\n")


def main():
    """
    Ana program fonksiyonu.
    Main program function.
    """
    # Dil özelliğini göster / Demonstrate language feature
    demonstrate_language_feature()
    
    # Türkçe tam gösterim / Full Turkish demonstration
    print("\n" + "🇹🇷 " * 20)
    print("TÜRKÇE TAM GÖSTERİM")
    print("🇹🇷 " * 20)
    lcgTurkish = LinearCongruentialGenerator(language=Language.TURKISH)
    lcgTurkish.display_info()
    
    # İngilizce tam gösterim / Full English demonstration
    print("\n" + "🇬🇧 " * 20)
    print("ENGLISH FULL DEMONSTRATION")
    print("🇬🇧 " * 20)
    lcgEnglish = LinearCongruentialGenerator(language=Language.ENGLISH)
    lcgEnglish.display_info()


if __name__ == "__main__":
    main()
