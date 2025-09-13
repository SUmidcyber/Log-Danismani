# Log Danışmanı - AI Destekli Log Analiz ve Güvenlik Aracı
<p align="center"> <img src="https://img.shields.io/badge/Python-3.8%2B-blue"> <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey"> <img src="https://img.shields.io/badge/AI-Powered-green"> <img src="https://img.shields.io/badge/License-MIT-yellow"> <img src="https://img.shields.io/badge/Status-Aktif%20Geliştirme-brightgreen"> <img src="https://img.shields.io/badge/Katkılar-Açık-orange"> </p><p align="center"> <b>Akıllı Log Analizi için Yapay Zeka Destekli Çözüm</b> </p><p align="center"> <a href="#-özellikler">Özellikler</a> • <a href="#-kurulum">Kurulum</a> • <a href="#-kullanım">Kullanım</a> • <a href="#-katkıda-bulunma">Katkıda Bulunma</a> • <a href="#-lisans">Lisans</a> </p>

# 🚀Proje Hakkında
Log Danışmanı, Windows, Linux ve macOS işletim sistemlerinde otomatik olarak log toplayan, yapay zeka destekli analiz yapan ve güvenlik açıklarını tespit eden yenilikçi bir siber güvenlik aracıdır.

Geliştiriciler, sistem yöneticileri ve siber güvenlik uzmanları için tasarlanan bu araç, karmaşık log dosyalarını anlaşılır güvenlik raporlarına dönüştürerek proaktif güvenlik önlemleri almanıza olanak sağlar.

# ✨ Özellikler
# 🔍 Çoklu Platform Desteği
    Windows: Event Viewer loglarını otomatik okuma
    
    Linux: Syslog, auth.log, kern.log analizi
    
    macOS: Sistem ve uygulama loglarını tarama

# 🤖 Yapay Zeka Destekli Analiz
    20+ saldırı patterni tanıma
    
    Anormal aktivite tespiti
    
    IP tabanlı tehdit analizi
    
    Otomatik güvenlik önerileri

# 📊 Kapsamlı Raporlama
    Detaylı güvenlik istatistikleri
    
    Görsel tehdit dağılımı
    
    Önceliklendirilmiş öneriler
    
    JSON ve metin tabanlı çıktılar

# ⚡ Kolay Kullanım
    Tek komutla çalıştırma
    
    Otomatik log toplama
    
    Gerçek zamanlı analiz
    
    Modüler yapı

# 📦 Kurulum
    Gereksinimler
    Python 3.8 veya üzeri
    
    pip (Python paket yöneticisi)
# Kurulum Adımları
# 1. Depoyu Klonlayın
    git clone https://github.com/umidmammadov/Log-Danismani.git
    cd Log-Danismani
# 2. Sanal Ortam Oluşturun (Opsiyonel)
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # veya
    venv\Scripts\activate     # Windows
# 3. Gerekli Paketleri Yükleyin
    pip install -r requirements.txt

# 🎯 Kullanım
# Temel Kullanım
    python main.py
# Program otomatik olarak:
    
    İşletim sisteminizi tespit eder
    
    İlgili log dosyalarını toplar
    
    AI destekli analiz yapar
    
    Güvenlik raporu oluşturur

# Gelişmiş Kullanım
    # Belirli log dizinlerini tarama
    python main.py --path /custom/log/directory
    
    # Detaylı rapor modu
    python main.py --verbose
    
    # Özel çıktı dizini
    python main.py --output my_reports/
# Örnek Çıktı
    🚀 Log Danışmanı Başlıyor...
    
    🖥️  Sistem Bilgileri:
       İşletim Sistemi: Linux
       Sistem: Kali Linux 2023.3
       Çekirdek: 6.1.0-kali5-amd64
       İşlemci: Intel i7-10750H
       Bellek: 16 GB
    
    🐧 Linux logları okunuyor...
    ✅ syslog logları kaydedildi → Linux_Log_Toplama/syslog_log.txt (14250 satır)
    ✅ auth logları kaydedildi → Linux_Log_Toplama/auth_log.txt (8923 satır)
    
    🤖 AI Analiz Başlıyor...
    📊 23170 satır log analiz edildi
    ⚠️  12 güvenlik tehdidi tespit edildi
    💡 7 güvenlik önerisi oluşturuldu
    
    💾 Rapor kaydedildi: security_analysis_report.json

# 🏗️ Proje Mimarisi
    Log-Danismani/
    ├── ai/
    │   ├── __init__.py
    │   └── ai.py                 # AI analiz motoru
    ├── windows/
    │   └── windows.py            # Windows log okuyucu
    ├── linux/
    │   └── linux.py              # Linux log okuyucu
    ├── mac/
    │   └── mac.py                # macOS log okuyucu
    ├── SystemQuery/
    │   └── system_query.py       # Sistem bilgileri
    ├── LOG/                      # Toplanan loglar
    ├── main.py                   Ana uygulama
    ├── requirements.txt          Gereksinimler
    └── README.md                 Bu dosya   
# 🔧 Özelleştirme
# Özel Log Konfigürasyonu
Linux için yeni log dosyaları eklemek:
# linux/linux.py içinde
    self.log_files = {
        "syslog": "/var/log/syslog",
        "auth": "/var/log/auth.log",
        "kernel": "/var/log/kern.log",
        "custom": "/var/log/your_custom.log"  # Yeni log dosyası
    }

# 🤝 Katkıda Bulunma
    Katkılarınızı bekliyoruz! Katkıda bulunmak için:
    
    Fork edin
    
    Feature branch oluşturun (git checkout -b feature/AmazingFeature)
    
    Değişikliklerinizi commit edin (git commit -m 'Add AmazingFeature')
    
    Branch'inizi push edin (git push origin feature/AmazingFeature)
    
    Pull Request oluşturun
# 📄 Lisans
    Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için LICENSE dosyasına bakın.

# 👨‍💻 Geliştirici
    Ümit Mammadov
    
    Website: sibermerkez.com
    
    LinkedIn: Ümit Mammadov
    
    GitHub: @umidmammadov
