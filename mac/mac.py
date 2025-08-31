# mac/mac.py
import os
import subprocess
import platform
from SystemQuery.system_query import SystemQuery

class MacLog:
    def __init__(self):
        self.sistem = SystemQuery()
        
        # Sadece macOS'ta çalışsın
        if platform.system().lower() != "darwin":
            print("⚠️ Bu modül sadece macOS'ta çalışır!")
            return
        
        print("🍎 macOS Log Okuyucu Hazır!")
        print(f"💻 Mac: {self.sistem.ps_name}")
        print(f"👤 Kullanıcı: {self.sistem.user}")
        
        # macOS log dosyaları
        self.log_files = {
            "system": "/var/log/system.log",
            "apache": "/var/log/apache2/error_log",
            "wifi": "/var/log/wifi.log",
            "install": "/var/log/install.log",
            "console": "~/Library/Logs/Console.log"
        }
        
        # Console uygulaması logları
        self.console_logs = [
            "~/Library/Logs/DiagnosticReports/",
            "~/Library/Logs/Adobe/",
            "~/Library/Logs/Google/",
            "~/Library/Logs/Microsoft/"
        ]
        
        self.output_dir = "macOS_Log_Toplama"
        os.makedirs(self.output_dir, exist_ok=True)

    def read_log_file(self, name, path):
        """Log dosyasını oku ve kaydet"""
        try:
            # ~ işaretini genişlet
            if path.startswith('~'):
                path = os.path.expanduser(path)
            
            if not os.path.exists(path):
                print(f"⚠️ {name} logu bulunamadı: {path}")
                return
            
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                logs = f.readlines()

            out_path = os.path.join(self.output_dir, f"{name}_log.txt")
            with open(out_path, 'w', encoding='utf-8') as out:
                out.writelines(logs)

            print(f"✅ {name} logları kaydedildi → {out_path} ({len(logs)} satır)")
            
        except PermissionError:
            print(f"🚫 {name} dosyasına erişim izni yok (sudo gerekli)")
        except Exception as e:
            print(f"❌ {name} okuma hatası: {e}")

    def read_console_logs(self):
        """Console uygulaması loglarını oku"""
        print("\n📱 Console Logları Okunuyor...")
        
        for log_path in self.console_logs:
            expanded_path = os.path.expanduser(log_path)
            if os.path.exists(expanded_path):
                log_name = os.path.basename(expanded_path.rstrip('/'))
                self.read_log_file(f"console_{log_name}", expanded_path)

    def read_unified_logs(self):
        """macOS Unified Logging System loglarını oku"""
        print("\n🔍 Unified Logs Okunuyor...")
        
        # log show komutu ile sistem loglarını al
        try:
            # Son 1 saatlik loglar
            command = [
                'log', 'show',
                '--predicate', 'eventMessage contains "error"',
                '--last', '1h',
                '--info'
            ]
            
            result = subprocess.run(command, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                out_path = os.path.join(self.output_dir, "unified_logs.txt")
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(result.stdout)
                
                line_count = len(result.stdout.splitlines())
                print(f"✅ Unified logs kaydedildi → {out_path} ({line_count} satır)")
            else:
                print("⚠️ Unified logs alınamadı")
                
        except subprocess.TimeoutExpired:
            print("⏰ Unified logs zaman aşımına uğradı")
        except Exception as e:
            print(f"❌ Unified logs hatası: {e}")

    def read_all_logs(self):
        """Tüm macOS loglarını oku"""
        print("🍎 macOS Logları Toplanıyor...\n")
        
        # Temel sistem logları
        for name, path in self.log_files.items():
            self.read_log_file(name, path)
        
        # Console logları
        self.read_console_logs()
        
        # Unified logs
        self.read_unified_logs()
        
        print(f"\n🎉 macOS log toplama tamamlandı! → {self.output_dir}/")

# Sadece macOS'ta çalıştır
if __name__ == "__main__" and platform.system().lower() == "darwin":
    logger = MacLog()
    logger.read_all_logs()