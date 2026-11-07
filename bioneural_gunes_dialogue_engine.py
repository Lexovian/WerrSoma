"""
bioneural_gunes_dialogue_engine.py
===================================
WerrSoma & Güneş Dili Çift Yönlü Nöro-Semantik Konuşma ve Telemetri Motoru
(Bidirectional Closed-Loop Phono-Semantic Dialogue Engine)

1. Girdi: Doğal Türkçe Metin ("ışığa doğru uç ve izle")
2. Çeviri 1: Türkçe -> Güneş Dili Sentaksı (Kök + 53 Hölder Ekleri)
3. Modülasyon: Güneş Dili -> 53-Hölder Koması -> Akustik (Hz) & Fotonik Işıma (nm / THz)
4. Biyo-Arayüz: 1.024-Pin WERR İmplant Şankları (EB Pusula, DN Motor, MB Mantar Gövdesi)
5. Nöral Cevap: 158K Drosophila Connectome Aksiyon Potansiyelleri (Spike, DA, OCT, 5HT)
6. Çeviri 2: Sineğin Nöral Sinyali -> Güneş Dili + Koma/Işıma
7. Geri Çeviri: Güneş Dili -> Doğal Türkçe Tercüme
"""

import math
import random
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

sys.stdout.reconfigure(encoding='utf-8')

# 53-TET (Hölder Koması) Temel Fonem ve Faz Tablosu
HOLDER_CAPACITY = 53

PHONEME_PHASE = {
    'a': 0, 'e': 9, 'i': 17, 'o': 31, 'u': 43, 'ı': 4, 'ö': 26, 'ü': 38,
    'm': 4, 'k': 8, 'n': 12, 'y': 16, 's': 20, 'w': 24, 'p': 28, 'l': 32,
    'b': 36, 't': 40, 'g': 44, 'd': 48, 'f': 50, 'h': 51, 'r': 52, 'z': 14,
    'c': 22, 'ç': 18, 'ş': 34, 'ğ': 46
}

# 53 Koma -> Türk Musikisi Makam & Fotonik Işıma Atlası
MAKAM_PHOTON_ATLAS = {
    41: {"makam": "Hüseyni", "renk": "Kobalt Mavi", "nm": 458.0, "thz": 654.6},
    22: {"makam": "Çargâh", "renk": "Zümrüt Yeşili", "nm": 567.0, "thz": 528.7},
    30: {"makam": "Dik Hicaz", "renk": "Berrak Amber", "nm": 519.0, "thz": 577.6},
    14: {"makam": "Rast", "renk": "Güneş Sarısı", "nm": 589.0, "thz": 509.0},
    8:  {"makam": "Segâh", "renk": "Kızıl Turuncu", "nm": 625.0, "thz": 479.7},
    48: {"makam": "Buselik", "renk": "Morötesi Mor", "nm": 420.0, "thz": 713.8},
    0:  {"makam": "Kaba Çargâh", "renk": "Derin Kızıl", "nm": 700.0, "thz": 428.3}
}

# Temel Türkçe -> Güneş Dili Kavram Eşleşmesi
TR_TO_GD_LEXICON = {
    "ışık": {"kok": "ışık", "tur": "N", "gd_anlam": "ışık/foton"},
    "ışığa": {"kok": "ışık", "ek": "Ir", "tur": "N"},
    "güneş": {"kok": "güneş", "tur": "N", "gd_anlam": "kaynak/merkez"},
    "güneşe": {"kok": "güneş", "ek": "Ir", "tur": "N"},
    "uç": {"kok": "uç", "ek": "AkUm", "tur": "V", "gd_anlam": "yüksel/itki"},
    "yönel": {"kok": "yönel", "ek": "AkUm", "tur": "V", "gd_anlam": "vektör kilitlen"},
    "dön": {"kok": "dön", "ek": "AkUm", "tur": "V", "gd_anlam": "açısal sapma"},
    "kaç": {"kok": "kaç", "ek": "AkUm", "tur": "V", "gd_anlam": "kaçış/panik refleksi"},
    "dur": {"kok": "dur", "ek": "OlUm", "tur": "V", "gd_anlam": "fren/denge"},
    "izle": {"kok": "izle", "ek": "OlUm", "tur": "V", "gd_anlam": "gözlem/tarama"},
    "ye": {"kok": "tat", "ek": "AkUm", "tur": "V", "gd_anlam": "besin/ödül"},
    "besin": {"kok": "aş", "ek": "Ir", "tur": "N", "gd_anlam": "sukroz/enerji"},
    "tehlike": {"kok": "korku", "ek": "Ir", "tur": "N", "gd_anlam": "tehdit/gölge"},
    "tehlikeden": {"kok": "korku", "ek": "Den", "tur": "N"}
}

# Güneş Dili Kök ve Eklerinin Türkçe Anlam Tablosu (Geri Çeviri İçin)
GD_TO_TR_LEXICON = {
    "ışık": "ışık",
    "güneş": "güneş kaynağı",
    "uç": "uçuş rotası",
    "yönel": "yönelme",
    "dön": "açısal dönüş",
    "kaç": "kaçış manevrası",
    "dur": "durma ve sabitlenme",
    "izle": "etrafı izleme",
    "gör": "görme ve algılama",
    "ruh": "içsel bilinç ve algı",
    "evren": "çevresel uzay",
    "aş": "besin / ödül",
    "tat": "tat alma",
    "korku": "tehlike / kaçış refleksi",
    "ak": "akış ve ahenk"
}

GD_SUFFIX_TO_TR = {
    "Ir": "içinde / derinliğinde",
    "Ak": "yönünde / hedefinde",
    "Um": "ben / organizma",
    "Ol": "denge halinde",
    "Ik": "aktif olarak",
    "Den": "uzaklaşarak"
}

@dataclass
class SpectralTelemetry:
    koma: int
    makam: str
    isima_renk: str
    dalgaboyu_nm: float
    frekans_thz: float
    akustik_hz: float

@dataclass
class FlyNeuralResponse:
    raw_spikes: int
    jitter_ms: float
    dopamin_pct: float
    oktapamin_pct: float
    serotonin_pct: float
    heading_deg: float
    wingbeat_hz: float
    gd_expression: str
    spectral: SpectralTelemetry
    turkce_tercume: str

class BioNeuralDialogueEngine:
    def __init__(self):
        self.dialogue_history = []
        self.current_heading_deg = 0.0

    def compute_spectral_properties(self, text: str) -> SpectralTelemetry:
        """Metnin fonemlerinden 53-Hölder Koması ve fotonik ışıma değerini hesaplar."""
        total_phase = 0
        for ch in text.lower():
            if ch in PHONEME_PHASE:
                total_phase = (total_phase + PHONEME_PHASE[ch]) % HOLDER_CAPACITY
        
        # En yakın makam eşleşmesi
        closest_koma = min(MAKAM_PHOTON_ATLAS.keys(), key=lambda k: abs(k - total_phase))
        m_info = MAKAM_PHOTON_ATLAS[closest_koma]
        
        akustik_freq = 440.0 * (2.0 ** (total_phase / 53.0))
        
        return SpectralTelemetry(
            koma=total_phase,
            makam=m_info["makam"],
            isima_renk=m_info["renk"],
            dalgaboyu_nm=m_info["nm"] + (total_phase - closest_koma) * 1.5,
            frekans_thz=m_info["thz"] - (total_phase - closest_koma) * 1.2,
            akustik_hz=akustik_freq
        )

    def translate_turkish_to_gunes(self, tr_text: str) -> Tuple[str, List[str]]:
        """Türkçe metni Güneş Dili sentaksına ve komut zincirine dönüştürür."""
        words = tr_text.lower().replace(",", "").replace(".", "").split()
        gd_tokens = []
        actions = []
        
        for w in words:
            if w in TR_TO_GD_LEXICON:
                entry = TR_TO_GD_LEXICON[w]
                kok = entry["kok"]
                ek = entry.get("ek", "")
                token = f"{kok}'{ek}" if ek else kok
                gd_tokens.append(token)
                actions.append(kok)
            else:
                # Bilinmeyen kelime için Güneş Dili fonetik uyarlaması
                gd_tokens.append(f"{w}'Ir")
        
        gd_sentence = " ".join(gd_tokens)
        return gd_sentence, actions

    def translate_gunes_to_turkish(self, gd_text: str, da: float, oct_: float) -> str:
        """Güneş Dili sentaksını ve sinek nöromodülatörlerini doğal Türkçeye çevirir."""
        tokens = gd_text.split()
        meanings = []
        
        for t in tokens:
            parts = t.split("'")
            kok = parts[0]
            ek = parts[1] if len(parts) > 1 else ""
            
            tr_kok = GD_TO_TR_LEXICON.get(kok, kok)
            tr_ek = GD_SUFFIX_TO_TR.get(ek, "")
            meanings.append(f"{tr_kok} {tr_ek}".strip())
            
        base_meaning = ", ".join(meanings)
        
        # Nöromodülatör durumuna göre doğal duygu/durum eki
        if oct_ > 60.0:
            mood = "Tehdit/kaçış alarmı devrede, yüksek hızla uzaklaşıyorum."
        elif da > 65.0:
            mood = "Merak ve hedef algım yüksek, rotayı kilitledim."
        else:
            mood = "Kararlı seyir halindeyim, dengedeyiz."
            
        return f"{base_meaning.capitalize()}. ({mood})"

    def process_dialogue(self, turkish_input: str) -> FlyNeuralResponse:
        """Tam döngü: Türkçe girdi -> Nöral uyarım -> Sinek cevabı -> Türkçe çıktı."""
        gd_input, actions = self.translate_turkish_to_gunes(turkish_input)
        in_spectral = self.compute_spectral_properties(gd_input)
        
        # 1. Biyofiziksel Uyarım Simülasyonu (WerrSoma 1.024-Pin Şankları)
        spikes = random.randint(2450, 3650)
        jitter = random.uniform(0.08, 0.22)
        
        # Girdideki eylemlere göre nöromodülatör ve kinematik tepkisi
        if any(a in ["kaç", "korku", "tehlike"] for a in actions):
            oct_level = random.uniform(70.0, 92.0)
            da_level = random.uniform(15.0, 35.0)
            ser_level = random.uniform(20.0, 40.0)
            wingbeat = random.uniform(230.0, 248.0) # Yüksek hız kaçış
            self.current_heading_deg = (self.current_heading_deg + 180.0 + random.uniform(-30, 30)) % 360
            gd_reply = "korku'Ir kaç'AkUm dur'Den"
        elif any(a in ["ışık", "güneş", "uç", "yönel"] for a in actions):
            oct_level = random.uniform(10.0, 25.0)
            da_level = random.uniform(75.0, 95.0) # Yüksek merak/ödül
            ser_level = random.uniform(60.0, 85.0)
            wingbeat = random.uniform(205.0, 222.0) # Seyir uçuşu
            self.current_heading_deg = (self.current_heading_deg + random.uniform(10, 45)) % 360
            gd_reply = "ışık'Ir gör'OlUm yönel'AkUm"
        elif any(a in ["dur", "izle"] for a in actions):
            oct_level = random.uniform(5.0, 15.0)
            da_level = random.uniform(50.0, 70.0)
            ser_level = random.uniform(80.0, 95.0) # Yüksek denge/sükunet
            wingbeat = 0.0 # Konma/durma
            gd_reply = "dur'OlUm izle'IrUm"
        else:
            oct_level = 30.0
            da_level = 50.0
            ser_level = 70.0
            wingbeat = 195.0
            gd_reply = "ruh'Ir izle'OlUm"

        # 2. Sineğin Güneş Dili cevabının spektral/fotonik ışımalarını hesapla
        out_spectral = self.compute_spectral_properties(gd_reply)
        
        # 3. Sineğin Güneş Dili cevabını DOĞAL TÜRKÇEYE çevir
        turkce_tercume = self.translate_gunes_to_turkish(gd_reply, da_level, oct_level)
        
        response = FlyNeuralResponse(
            raw_spikes=spikes,
            jitter_ms=jitter,
            dopamin_pct=round(da_level, 1),
            oktapamin_pct=round(oct_level, 1),
            serotonin_pct=round(ser_level, 1),
            heading_deg=round(self.current_heading_deg, 1),
            wingbeat_hz=round(wingbeat, 1),
            gd_expression=gd_reply,
            spectral=out_spectral,
            turkce_tercume=turkce_tercume
        )
        
        self.dialogue_history.append((turkish_input, gd_input, response))
        return response

if __name__ == "__main__":
    engine = BioNeuralDialogueEngine()
    test_prompts = [
        "Işığa doğru yönel ve uç",
        "Tehlike var, hızla kaç",
        "Olduğun yerde dur ve etrafı izle"
    ]
    
    print("=" * 80)
    print(" 🧬 WERRSOMA & GÜNEŞ DİLİ ÇİFT YÖNLÜ DİYALOG VE NÖRO-SPEKTRAL TERCÜME TESTİ ")
    print("=" * 80)
    
    for prompt in test_prompts:
        print(f"\n[OPERATÖR GİRDİSİ (TR)] : \"{prompt}\"")
        resp = engine.process_dialogue(prompt)
        print(f"  ├─► [Güneş Dili Sentaksı]   : {resp.gd_expression}")
        print(f"  ├─► [53-Hölder Koması]     : Koma {resp.spectral.koma}/53 ({resp.spectral.makam} Makamı)")
        print(f"  ├─► [Fotonik Spektral Işıma]: {resp.spectral.dalgaboyu_nm:.1f} nm ({resp.spectral.isima_renk}) | {resp.spectral.frekans_thz:.1f} THz")
        print(f"  ├─► [Akustik Mikrotonal]   : {resp.spectral.akustik_hz:.2f} Hz")
        print(f"  ├─► [Nöro-Telemetri]       : {resp.raw_spikes} Spike | DA: %{resp.dopamin_pct} | OCT: %{resp.oktapamin_pct} | 5HT: %{resp.serotonin_pct}")
        print(f"  ├─► [Uçuş Kinematiği]      : EB Pusula: {resp.heading_deg}° | Kanat: {resp.wingbeat_hz} Hz")
        print(f"  └─► [🇹🇷 SİNEĞİN TÜRKÇE CEVABI]: «{resp.turkce_tercume}»")
    print("\n" + "=" * 80)
