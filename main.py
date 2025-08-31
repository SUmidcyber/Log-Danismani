# main.py
from SystemQuery.system_query import SystemQuery
from windows.windows import WindowsLog
from linux.linux import LinuxLog
from mac.mac import MacLog
from ai.ai import LogAI
import platform
import os

def main():
    print("🚀 Log Danışmanı Başlıyor...\n")

    # Bilgisayar bilgilerini al
    system = SystemQuery()
    system.show_info()
    print("="*40)

    # Logları topla
    collected_logs = {}
    
    if platform.system().lower() == "windows":
        print("🪟 Windows logları okunuyor...")
        log_reader = WindowsLog()
        application_logs = log_reader.read_logs("Application")
        system_logs = log_reader.read_logs("System")
        
        # Listeyi text'e çevir
        collected_logs["application.log"] = log_reader.get_logs_as_text(application_logs)
        collected_logs["system.log"] = log_reader.get_logs_as_text(system_logs)
        
        # Dosyaya da kaydet
        log_reader.save_logs_to_file(application_logs, "application_logs.txt")
        log_reader.save_logs_to_file(system_logs, "system_logs.txt")
        
    elif platform.system().lower() == "linux":
        print("🐧 Linux logları okunuyor...")
        log_reader = LinuxLog()
        
        # Linux loglarını oku ve kaydet
        for name, path in log_reader.log_files.items():
            log_content = log_reader.read_and_save_logs(name, path)
            collected_logs[name + ".log"] = log_content
        
        print("🎉 Linux logları kaydedildi!")

    elif platform.system().lower() == "darwin":
        print("🍎 macOS logları okunuyor...")
        log_reader = MacLog()
        log_reader.read_all_logs()
        # macOS logları dosyadan oku
        for filename in os.listdir("macOS_Log_Toplama"):
            with open(os.path.join("macOS_Log_Toplama", filename), 'r', encoding='utf-8') as f:
                collected_logs[filename] = f.read()

    # AI analizi - Önce logları kontrol et
    print("\n🤖 AI Analiz Başlıyor...")
    
    ai_analyzer = LogAI()
    ai_report = ai_analyzer.analyze_logs()  # Parametre vermeden çağır
    ai_analyzer.print_report(ai_report)
    ai_analyzer.save_report(ai_report, "security_analysis_report.json")

if __name__ == "__main__":
    main()