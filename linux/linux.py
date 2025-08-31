# linux/linux.py
import os
import platform
from SystemQuery.system_query import SystemQuery

class LinuxLog:
    def __init__(self):
        self.sistem = SystemQuery()
        
        # Sadece Linux'ta çalışsın
        if platform.system().lower() != "linux":
            print("⚠️ Bu modül sadece Linux'ta çalışır!")
            return
        
        print("🐧 Linux Log Okuyucu Hazır!")
        
        # Log dosyaları
        self.log_files = {
            "syslog": "/var/log/syslog",
            "auth": "/var/log/auth.log",
            "kernel": "/var/log/kern.log"
        }
        
        self.output_dir = "Linux_Log_Toplama"
        os.makedirs(self.output_dir, exist_ok=True)

    def read_and_save_logs(self, name, path):
        """Log dosyasını oku ve kaydet"""
        # Windows'ta çalışıyorsa atla
        if platform.system().lower() != "linux":
            print(f"⚠️ {name} logları sadece Linux'ta okunabilir!")
            return
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                logs = f.readlines()

            out_path = os.path.join(self.output_dir, f"{name}_log.txt")
            with open(out_path, 'w', encoding='utf-8') as out:
                out.writelines(logs)

            print(f"✅ {name} logları kaydedildi → {out_path} ({len(logs)} satır)")
            
        except FileNotFoundError:
            print(f"⚠️ {path} bulunamadı")
        except PermissionError:
            print(f"🚫 {path} dosyasına erişim izni yok (sudo gerekli)")
        except Exception as e:
            print(f"❌ {name} okuma hatası: {e}")

# Sadece Linux'ta çalıştır
if __name__ == "__main__" and platform.system().lower() == "linux":
    logger = LinuxLog()
    for name, path in logger.log_files.items():
        logger.read_and_save_logs(name, path)