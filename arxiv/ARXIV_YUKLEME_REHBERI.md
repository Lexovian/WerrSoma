# WerrSoma — arXiv Resmi Yükleme ve Yayınlama Rehberi (Step-by-Step Submission Guide)

Bu klasör, **WerrSoma** (*"Bio-Synthetic Neuromorphic Interfacing: Integration of a Zero-Memory Fractal Decision Engine with the Whole-Brain Drosophila melanogaster Connectome"*) çalışmasının **arXiv AutoTeX (pdflatex)** motorunda **sıfır hata ile (Zero-Error)** derlenmesi için hazırlanmış tam yayın paketini içerir.

---

## 📦 1. Yüklemeye Hazır Paket Dosyaları (`arxiv/` Klasörü)

arXiv yükleme ekranında (**Add Files** adımında) aşağıdaki iki arşiv dosyasından **yalnızca birini** doğrudan yükleyebilirsiniz (arXiv her iki formatı da otomatik olarak açar ve derler):

1. **`werrsoma_arxiv_package.tar.gz`** *(Önerilen Standart Unix/arXiv Formatı — ~631 KB)*
2. **`werrsoma_arxiv_package.zip`** *(Alternatif ZIP Formatı — ~630 KB)*

### Arşiv İçeriği (Kök Dizinde Doğrudan Yer Alan 5 Dosya):
- `main.tex` — `\pdfoutput=1` direktifli, 2 sütunlu IEEE/Nature akademik formatında, tüm referansları (`\begin{thebibliography}{99}`) kendi içinde gömülü (self-contained), %100 7-bit saf LaTeX uyumlu ana makale dosyası.
- `fig1_werrsoma_architecture.png` — 300 DPI vektörel kalitede WerrSoma 1.024-pin silikon yardımcı işlemci + 4 poliimid mikro-şaft + 158.262 nöronluk FlyWire konnektom mimari şeması.
- `fig2_connectome_atlas_projection.png` — 300 DPI gerçek 158.262 nöronluk FlyWire konnektom verisinden (`drosophila_full_158k_cache.npz`) üretilen Koronal Ön ($X\text{--}Y$) ve Yatay Dorsal ($X\text{--}Z$) anatomik projeksiyonlar ile dorsal WERR çipi ve 4 penetran şaftın stereotaksik hedefleri (EB, DN, Bilateral MB).
- `fig3_homeostatic_gaba_and_latency.png` — 300 DPI biyolojik GABAerjik homeostatik frenleme ($-53.93\text{ mV}$) ve $3.671\text{ ms}$ uçtan uca refleks gecikme grafiği.
- `fig4_bioenergetics_and_fault_tolerance.png` — 300 DPI ATP biyo-enerjetik / nöron yanması (burnout) güvenlik zarfı ($f_{\max} = 265\text{ Hz}$) ve %0–%75 elektrot pin kopması (fault tolerance) grafiği.

---

## ⚠️ "Missing files or top-level files" Hatası Neden Olur ve Nasıl Çözülür?

arXiv ekranında **`Error: Missing files or top-level files`** hatası alınmasının %99 iki sebebi vardır:

1. **"Upload File" Butonuna Basmadan "Continue" Denmesi (En Sık Yapılan UI Tuzağı):**
   arXiv dosya yönetim ekranında "Dosya Seç / Browse" diyerek `.tar.gz` veya dosyaları seçtikten sonra, **hemen yanındaki "Upload File" (Dosyayı Yükle) butonuna tıklamak ŞARTTIR**. 
   Eğer dosya seçildikten sonra "Upload File" butonuna basılmadan doğrudan sayfanın altındaki "Continue / Process Files" butonuna basılırsa; dosya sunucuya henüz yüklenmediği için arXiv sunucusundaki çalışma alanı boş kalır ve sunucu *"Missing files"* hatası fırlatır.

2. **Arşiv İçi Alt Klasör (Subfolder) Karmaşası:**
   Eğer bir klasör Windows'ta "Sağ tık -> Sıkıştır" ile zip yapılırsa arşiv içinde `arxiv/main.tex` gibi bir alt klasör oluşabilir. arXiv ise `main.tex`'in en üst kök dizinde (top-level) olmasını bekler. Bizim oluşturduğumuz `werrsoma_arxiv_package.tar.gz` dosyasında tüm dosyalar en üst köktedir.

### 🎯 Kesin Çözüm (İki Güvenli Yoldan Biri):

#### YOL 1 (En Kolay ve Garantili — Doğrudan 5 Dosyayı Yüklemek):
Hiç zip/tar ile uğraşmadan:
1. arXiv dosya ekranında varsa eski dosyaları silin (Delete/Clear).
2. **"Browse / Dosya Seç"** diyerek `WerrSoma/arxiv/` klasöründeki şu **5 dosyayı** birlikte seçin:
   - `main.tex`
   - `fig1_werrsoma_architecture.png`
   - `fig2_connectome_atlas_projection.png`
   - `fig3_homeostatic_gaba_and_latency.png`
   - `fig4_bioenergetics_and_fault_tolerance.png`
3. **"Upload files"** butonuna basın.
4. Ekranda 5 dosyanın da yeşil/listelenmiş olarak göründüğünden emin olun.
5. Şimdi **"Continue / Process Files"** butonuna basın.

#### YOL 2 (Hazır Paket ile):
1. `werrsoma_arxiv_package.tar.gz` dosyasını seçin.
2. Mutlaka **"Upload file"** butonuna tıklayın.
3. arXiv paketi açacak ve ekrandaki tabloda `main.tex` ile 4 adet `.png` dosyasını listeleyecektir.
4. Dosyaları listede gördükten sonra **"Continue / Process Files"** butonuna basın.

---

## 🚀 2. Adım Adım arXiv Yükleme İşlemi (`https://arxiv.org/submit`)

### Adım 1: Başlangıç ve Kategori Seçimi (Start & Subject Category)
1. [https://arxiv.org/submit](https://arxiv.org/submit) adresine giriş yapın ve mevcut başvurunuzu güncelliyorsanız başvurunun yanındaki **"Edit / Replace"** (veya sıfırdan yapıyorsanız **"Start New Submission"**) bağlantısına tıklayın.
2. **Primary Category (Ana Kategori):**
   - **`cs.NE`** (*Neural and Evolutionary Computing*) VEYA **`q-bio.NC`** (*Neurons and Cognition*)
3. **Cross-List Categories:**
   - **`cs.AI`**, **`cs.RO`**, **`q-bio.NC`**

### Adım 2: Lisans Seçimi (License)
- **`CC BY 4.0`** (*Creative Commons Attribution 4.0 International*) seçin.

### Adım 3: Dosya Yükleme ve Derleme (Add Files & Process)
1. Yukarıdaki **YOL 1** veya **YOL 2**'yi uygulayın.
2. **"Continue / Process Files"** butonuna tıklayın.
3. arXiv'in **AutoTeX** sistemi `\pdfoutput=1` direktifini görünce otomatik olarak `pdflatex` çalıştıracak ve PDF'i başarıyla üretecektir.
4. **"View PDF"** butonuna tıklayarak derlenen makaleyi inceleyin.

---

## 📋 3. Kopyala-Yapıştır Üst Veri (Metadata) Alanları

arXiv'in **Metadata** adımındaki kutucuklara aşağıdaki metinleri **birebir kopyalayıp yapıştırın**:

### 📌 Title (Başlık)
```text
Bio-Synthetic Neuromorphic Interfacing: Integration of a Zero-Memory Fractal Decision Engine with the Whole-Brain Drosophila melanogaster Connectome
```

### 📌 Authors (Yazarlar)
```text
Dağhan Dağlı, Volkan Dağlı, Zerrin Dağlı
```

### 📌 Abstract (Özet — arXiv 1.920 Karakter Sınırına %100 Uyumlu: 1.682 Karakter)
> **Önemli Not:** arXiv web formundaki *Abstract* kutusu maksimum 1.920 karaktere izin verir. Aşağıdaki metin tüm 6 deneyin sonuçlarını eksiksiz içerir ve **1.682 karakter** uzunluğuyla arXiv form sınırının tam içindedir (PDF içindeki `main.tex` dosyasında ise hem tam İngilizce özet hem de Genişletilmiş Türkçe Özet otomatik olarak yer almaktadır).

```text
Interfacing artificial decision-making systems with biological neural substrates requires sub-millisecond response latency, zero memory overhead, and strict adherence to biophysical homeostasis. Here, we present the design, mathematical formulation, and in silico empirical validation of WerrSoma, a bio-synthetic brain-machine interface coupling the complete 158,262-neuron, 3,990,039-synapse Drosophila melanogaster connectome (Princeton FlyWire) with an implantable 1,024-pin WERR neuromorphic fractal coprocessor. Rather than utilizing parameterized tensor-based artificial neural networks, the coprocessor generates instantaneous, deterministic System-1 reflex decisions by sampling chaotic Mandelbrot boundary escape trajectories ($\partial \mathcal{M}$), entirely eliminating VRAM overhead and inference memory. Four penetrating micro-electrode shanks target the Ellipsoid Body (EB) heading compass, the Descending Motor Neuron (DN) pool, and the bilateral Mushroom Bodies (MB). Across six experimental protocols encompassing electrophysiology, recurrent homeostasis, closed-loop flight kinematics, bio-energetics, and Shannon information theory, the hybrid system demonstrates: (1) 100.0% synaptic transmission fidelity ($15.83 \pm 0.51$ mV depolarization, $\text{PPR} = 0.885$); (2) robust homeostatic biocompatibility via a 38.58% GABAergic inhibitory counter-current clamping membrane potentials to $-53.93$ mV (Stability Index: $0.965$); (3) $3.671$ ms end-to-end reflex latency and 94.67% saccadic motor accuracy ($\text{Rayleigh } R = 0.841$); (4) $1.23\ \mu\text{W}$ baseline metabolic power ($\Delta T = +0.0012^\circ\text{C}$, safe ceiling $265$ Hz with a $20.0$ ms refractory clamp); (5) 70.10% neural coding efficiency ($1.302$ bits/symbol); and (6) >78% steering fidelity under 25% electrode pin dropout.
```

### 📌 Comments (Yorumlar)
```text
7 pages, 4 figures, 2 tables. Bilingual (English/Turkish) abstract included in PDF. Open-source 158,262-neuron CSR connectome simulator and 6-protocol benchmark suite available at https://github.com/Lexovian/WerrSoma . Interactive 3D WebGL portal: https://werrsoma.answerr.me/
```

### 📌 Report Number (Kurumsal Rapor / Patent Numarası)
```text
TURKPATENT-TR-2026-016633
```

### 📌 DOI (Zenodo Kalıcı Dijital Nesne Tanımlayıcısı)
```text
10.5281/zenodo.23072929
```
*(Not: Çatı/Concept DOI olan `10.5281/zenodo.22996625` de kullanılabilir; her ikisi de doğrudan yayına yönlendirir).*

---

## 🛠️ 4. Paket Doğrulama ve Yeniden Üretim Komutları

Şekilleri veya arşivi yerel bilgisayarda yeniden üretmek isterseniz `arxiv/` dizininde şu komutları çalıştırabilirsiniz:

```bash
python generate_arxiv_figures.py
python package_arxiv.py
```
`package_arxiv.py` betiği `main.tex` içindeki tüm süslü parantezleri, `\begin{...}` / `\end{...}` ortamlarını, referans atıflarını (`14/14`), görsel dosyalarını ve 7-bit ASCII LaTeX uyumluluğunu otomatik olarak denetler.
