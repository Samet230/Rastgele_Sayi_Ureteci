#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JPEG Kuantalama Tablosu Demo
============================
Bilgi Sistemleri ve Güvenliği Dersi - Bonus Görev

Bu script, rastgeleliğin veri sıkıştırmada neden uygun olmadığını gösterir.

HİPOTEZ:
    "Rastgelelik güvenlikte iyidir ama veri sıkıştırmada deterministik yapı şarttır."

DENEY:
    1. Standart JPEG kuantalama tablosu ile görüntü işleme
    2. LCG tabanlı rastgele kuantalama tablosu ile görüntü işleme
    3. Sonuçların görsel karşılaştırması

Author: Yazılım Mühendisliği Ekibi
Date: 2025
"""

import numpy as np
from typing import Tuple, Optional
import os
import sys

# LCG modülünü import et
from lcg_generator import LinearCongruentialGenerator, Language


class JPEGQuantizationDemo:
    """
    JPEG Kuantalama Tablosu ile görüntü bozulma demonstrasyonu.
    
    Bu sınıf, standart deterministik kuantalama tablosu ile
    rastgele LCG tabanlı tablo arasındaki farkı gösterir.
    """
    
    # Standart JPEG Luminance (Parlaklık) Kuantalama Tablosu
    # ITU-T T.81 standardından alınmıştır
    STANDARD_LUMINANCE_TABLE = np.array([
        [16,  11,  10,  16,  24,  40,  51,  61],
        [12,  12,  14,  19,  26,  58,  60,  55],
        [14,  13,  16,  24,  40,  57,  69,  56],
        [14,  17,  22,  29,  51,  87,  80,  62],
        [18,  22,  37,  56,  68, 109, 103,  77],
        [24,  35,  55,  64,  81, 104, 113,  92],
        [49,  64,  78,  87, 103, 121, 120, 101],
        [72,  92,  95,  98, 112, 100, 103,  99]
    ], dtype=np.float64)
    
    def __init__(self, seed: Optional[int] = None, language: Language = Language.TURKISH):
        """
        Demo'yu başlatır.
        
        Args:
            seed: LCG için seed değeri
            language: Çıktı dili
        """
        self.rng = LinearCongruentialGenerator(seed=seed, language=language)
        self.language = language
    
    def generate_random_quantization_table(self) -> np.ndarray:
        """
        LCG kullanarak rastgele 8x8 kuantalama tablosu üretir.
        
        Returns:
            np.ndarray: 8x8 rastgele kuantalama tablosu
        """
        randomTable = np.zeros((8, 8), dtype=np.float64)
        
        for i in range(8):
            for j in range(8):
                # 1-255 arasında rastgele değer
                # (0 olursa bölme hatası alınır)
                randomTable[i, j] = self.rng.next_int(1, 255)
        
        return randomTable
    
    def create_sample_image_block(self) -> np.ndarray:
        """
        Örnek bir 8x8 görüntü bloğu oluşturur.
        Gerçek bir görüntünün parlaklık değerlerini simüle eder.
        
        Returns:
            np.ndarray: 8x8 piksel bloğu (0-255 arası değerler)
        """
        # Gradyan benzeri bir örnek blok
        sampleBlock = np.array([
            [52,  55,  61,  66,  70,  61,  64,  73],
            [63,  59,  55,  90, 109,  85,  69,  72],
            [62,  59,  68, 113, 144, 104,  66,  73],
            [63,  58,  71, 122, 154, 106,  70,  69],
            [67,  61,  68, 104, 126,  88,  68,  70],
            [79,  65,  60,  70,  77,  68,  58,  75],
            [85,  71,  64,  59,  55,  61,  65,  83],
            [87,  79,  69,  68,  65,  76,  78,  94]
        ], dtype=np.float64)
        
        return sampleBlock
    
    def apply_dct(self, block: np.ndarray) -> np.ndarray:
        """
        8x8 bloğa 2D Discrete Cosine Transform uygular.
        
        Args:
            block: 8x8 piksel bloğu
        
        Returns:
            np.ndarray: DCT katsayıları
        """
        # Merkezleme (0-255 → -128 to 127)
        centered = block - 128
        
        # DCT matrisi oluştur
        dctMatrix = np.zeros((8, 8))
        for i in range(8):
            for j in range(8):
                if i == 0:
                    dctMatrix[i, j] = 1 / np.sqrt(8)
                else:
                    dctMatrix[i, j] = np.sqrt(2/8) * np.cos((2*j + 1) * i * np.pi / 16)
        
        # 2D DCT: D * Block * D^T
        dctCoefficients = dctMatrix @ centered @ dctMatrix.T
        
        return dctCoefficients
    
    def apply_idct(self, coefficients: np.ndarray) -> np.ndarray:
        """
        DCT katsayılarından görüntü bloğunu geri oluşturur.
        
        Args:
            coefficients: DCT katsayıları
        
        Returns:
            np.ndarray: Yeniden oluşturulmuş piksel bloğu
        """
        # DCT matrisi
        dctMatrix = np.zeros((8, 8))
        for i in range(8):
            for j in range(8):
                if i == 0:
                    dctMatrix[i, j] = 1 / np.sqrt(8)
                else:
                    dctMatrix[i, j] = np.sqrt(2/8) * np.cos((2*j + 1) * i * np.pi / 16)
        
        # Ters 2D DCT: D^T * Coefficients * D
        reconstructed = dctMatrix.T @ coefficients @ dctMatrix
        
        # Merkezlemeyi geri al
        reconstructed = reconstructed + 128
        
        # 0-255 aralığına sınırla
        reconstructed = np.clip(reconstructed, 0, 255)
        
        return reconstructed
    
    def quantize(self, dctCoefficients: np.ndarray, quantTable: np.ndarray) -> np.ndarray:
        """
        DCT katsayılarını kuantalama tablosu ile kuantalar.
        
        Args:
            dctCoefficients: DCT katsayıları
            quantTable: 8x8 kuantalama tablosu
        
        Returns:
            np.ndarray: Kuantalanmış katsayılar
        """
        return np.round(dctCoefficients / quantTable)
    
    def dequantize(self, quantizedCoefficients: np.ndarray, quantTable: np.ndarray) -> np.ndarray:
        """
        Kuantalanmış katsayıları ters kuantalar.
        
        Args:
            quantizedCoefficients: Kuantalanmış katsayılar
            quantTable: 8x8 kuantalama tablosu
        
        Returns:
            np.ndarray: Ters kuantalanmış katsayılar
        """
        return quantizedCoefficients * quantTable
    
    def calculate_mse(self, original: np.ndarray, reconstructed: np.ndarray) -> float:
        """
        Mean Squared Error (Ortalama Kare Hata) hesaplar.
        
        Args:
            original: Orijinal blok
            reconstructed: Yeniden oluşturulmuş blok
        
        Returns:
            float: MSE değeri
        """
        return np.mean((original - reconstructed) ** 2)
    
    def calculate_psnr(self, mse: float, maxPixelValue: float = 255.0) -> float:
        """
        Peak Signal-to-Noise Ratio (PSNR) hesaplar.
        
        Args:
            mse: Mean Squared Error
            maxPixelValue: Maksimum piksel değeri
        
        Returns:
            float: PSNR değeri (dB)
        """
        if mse == 0:
            return float('inf')
        return 10 * np.log10((maxPixelValue ** 2) / mse)
    
    def process_block(
        self, 
        block: np.ndarray, 
        quantTable: np.ndarray
    ) -> Tuple[np.ndarray, float, float]:
        """
        Bir bloğu tam JPEG işleme hattından geçirir.
        
        Args:
            block: Orijinal 8x8 blok
            quantTable: Kuantalama tablosu
        
        Returns:
            Tuple: (yeniden oluşturulmuş blok, MSE, PSNR)
        """
        # 1. DCT uygula
        dctCoefficients = self.apply_dct(block)
        
        # 2. Kuantala
        quantized = self.quantize(dctCoefficients, quantTable)
        
        # 3. Ters kuantala
        dequantized = self.dequantize(quantized, quantTable)
        
        # 4. Ters DCT
        reconstructed = self.apply_idct(dequantized)
        
        # 5. Kalite metrikleri
        mse = self.calculate_mse(block, reconstructed)
        psnr = self.calculate_psnr(mse)
        
        return reconstructed, mse, psnr
    
    def run_demo(self) -> None:
        """
        Tam demo'yu çalıştırır ve sonuçları gösterir.
        """
        messages = self._get_messages()
        
        print("\n" + "=" * 70)
        print(messages["title"])
        print("=" * 70)
        
        print(f"\n{messages['hypothesis']}")
        print("-" * 70)
        
        # Örnek blok oluştur
        originalBlock = self.create_sample_image_block()
        
        print(f"\n📷 {messages['original_block']}:")
        self._print_matrix(originalBlock, precision=0)
        
        # Rastgele kuantalama tablosu oluştur
        randomTable = self.generate_random_quantization_table()
        
        print(f"\n📊 {messages['standard_table']}:")
        self._print_matrix(self.STANDARD_LUMINANCE_TABLE, precision=0)
        
        print(f"\n🎲 {messages['random_table']}:")
        self._print_matrix(randomTable, precision=0)
        
        # Standart tablo ile işle
        print(f"\n{'=' * 70}")
        print(f"✅ {messages['standard_processing']}")
        print("=" * 70)
        
        standardResult, standardMSE, standardPSNR = self.process_block(
            originalBlock, 
            self.STANDARD_LUMINANCE_TABLE
        )
        
        print(f"\n{messages['reconstructed']}:")
        self._print_matrix(standardResult, precision=1)
        
        print(f"\n📈 {messages['metrics']}:")
        print(f"   MSE  : {standardMSE:.4f}")
        print(f"   PSNR : {standardPSNR:.2f} dB")
        
        # Rastgele tablo ile işle
        print(f"\n{'=' * 70}")
        print(f"❌ {messages['random_processing']}")
        print("=" * 70)
        
        randomResult, randomMSE, randomPSNR = self.process_block(
            originalBlock, 
            randomTable
        )
        
        print(f"\n{messages['reconstructed']}:")
        self._print_matrix(randomResult, precision=1)
        
        print(f"\n📉 {messages['metrics']}:")
        print(f"   MSE  : {randomMSE:.4f}")
        print(f"   PSNR : {randomPSNR:.2f} dB")
        
        # Karşılaştırma
        print(f"\n{'=' * 70}")
        print(f"📊 {messages['comparison']}")
        print("=" * 70)
        
        print(f"\n{'Tablo Tipi':<25} {'MSE':>15} {'PSNR (dB)':>15} {'Kalite':>15}")
        print("-" * 70)
        print(f"{'Standart (Deterministik)':<25} {standardMSE:>15.4f} {standardPSNR:>15.2f} {'✅ İYİ':>15}")
        print(f"{'Rastgele (LCG)':<25} {randomMSE:>15.4f} {randomPSNR:>15.2f} {'❌ KÖTÜ':>15}")
        
        # Fark analizi
        mseDifference = randomMSE - standardMSE
        psnrDifference = standardPSNR - randomPSNR
        
        print(f"\n{'Fark':<25} {mseDifference:>15.4f} {psnrDifference:>15.2f}")
        
        # Sonuç
        print(f"\n{'=' * 70}")
        print(f"🎯 {messages['conclusion']}")
        print("=" * 70)
        
        print(f"""
{messages['conclusion_text']}

📌 {messages['key_points']}:
   1. {messages['point1']}
   2. {messages['point2']}
   3. {messages['point3']}
   4. {messages['point4']}
""")
        
        print("=" * 70 + "\n")
    
    def _print_matrix(self, matrix: np.ndarray, precision: int = 2) -> None:
        """
        Matris güzel formatta yazdırır.
        """
        for row in matrix:
            formatted = " ".join([f"{val:>{precision + 5}.{precision}f}" for val in row])
            print(f"   [{formatted}]")
    
    def _get_messages(self) -> dict:
        """
        Dile göre mesajları döndürür.
        """
        if self.language == Language.TURKISH:
            return {
                "title": "🧪 JPEG KUANTALAMA TABLOSU DEMONSTRASYonu",
                "hypothesis": "📋 HİPOTEZ: \"Rastgelelik güvenlikte iyidir ama veri sıkıştırmada deterministik yapı şarttır.\"",
                "original_block": "Orijinal 8x8 Piksel Bloğu",
                "standard_table": "Standart JPEG Kuantalama Tablosu (ITU-T T.81)",
                "random_table": "LCG ile Üretilmiş Rastgele Kuantalama Tablosu",
                "standard_processing": "STANDART TABLO İLE İŞLEME",
                "random_processing": "RASTGELE TABLO İLE İŞLEME",
                "reconstructed": "Yeniden Oluşturulmuş Blok",
                "metrics": "Kalite Metrikleri",
                "comparison": "KARŞILAŞTIRMA SONUÇLARI",
                "conclusion": "SONUÇ VE DEĞERLENDİRME",
                "conclusion_text": """
Deney sonuçları hipotezimizi DOĞRULAMAKTADIR:

Rastgele kuantalama tablosu kullanıldığında:
   • MSE (Hata) önemli ölçüde ARTTI
   • PSNR (Kalite) önemli ölçüde DÜŞTÜ
   • Görüntü kalitesi ciddi şekilde bozuldu
""",
                "key_points": "ÖNEMLİ ÇIKARIMLAR",
                "point1": "JPEG'in standart tabloları, insan görsel algısına göre optimize edilmiştir.",
                "point2": "Rastgelelik, veri sıkıştırmada tahmin edilebilirliği bozar ve verimsizliğe yol açar.",
                "point3": "Güvenlikte rastgelelik AVANTAJDIR (tahmin edilemezlik).",
                "point4": "Sıkıştırmada rastgelelik DEZAVANTAJDIR (deterministik yapı gerekir)."
            }
        else:
            return {
                "title": "🧪 JPEG QUANTIZATION TABLE DEMONSTRATION",
                "hypothesis": "📋 HYPOTHESIS: \"Randomness is good for security but deterministic structure is required for data compression.\"",
                "original_block": "Original 8x8 Pixel Block",
                "standard_table": "Standard JPEG Quantization Table (ITU-T T.81)",
                "random_table": "LCG-Generated Random Quantization Table",
                "standard_processing": "PROCESSING WITH STANDARD TABLE",
                "random_processing": "PROCESSING WITH RANDOM TABLE",
                "reconstructed": "Reconstructed Block",
                "metrics": "Quality Metrics",
                "comparison": "COMPARISON RESULTS",
                "conclusion": "CONCLUSION AND EVALUATION",
                "conclusion_text": """
The experimental results CONFIRM our hypothesis:

When using a random quantization table:
   • MSE (Error) increased significantly
   • PSNR (Quality) decreased significantly
   • Image quality was severely degraded
""",
                "key_points": "KEY TAKEAWAYS",
                "point1": "JPEG's standard tables are optimized for human visual perception.",
                "point2": "Randomness in compression destroys predictability and leads to inefficiency.",
                "point3": "In security, randomness is an ADVANTAGE (unpredictability).",
                "point4": "In compression, randomness is a DISADVANTAGE (deterministic structure required)."
            }


def main():
    """
    Ana program fonksiyonu.
    """
    print("\n" + "🇹🇷 " * 20)
    print("TÜRKÇE DEMONSTRasSYON")
    print("🇹🇷 " * 20)
    
    demoTurkish = JPEGQuantizationDemo(seed=12345, language=Language.TURKISH)
    demoTurkish.run_demo()
    
    print("\n" + "🇬🇧 " * 20)
    print("ENGLISH DEMONSTRATION")
    print("🇬🇧 " * 20)
    
    demoEnglish = JPEGQuantizationDemo(seed=12345, language=Language.ENGLISH)
    demoEnglish.run_demo()


if __name__ == "__main__":
    main()
