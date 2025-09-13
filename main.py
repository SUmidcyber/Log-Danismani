from SystemQuery.system_query import SystemQuery
from ai.ai import LogAI
import platform
import os

def main():
    print("🚀 Log Danışmanı Başlıyor...\n")

    # Bilgisayar bilgilerini alir
    system = SystemQuery()
    system.show_info()
    print("="*40)

    # Logları toplar
    collected_logs = {}
    
    if platform.system().lower() == "windows":
        # Sadece Windows'ta Windows modüllerini import eder
        from windows.windows import WindowsLog
        print("🪟 Windows logları okunuyor...")
        log_reader = WindowsLog()
        application_logs = log_reader.read_logs("Application")
        system_logs = log_reader.read_logs("System")
        
        collected_logs["application.log"] = log_reader.get_logs_as_text(application_logs)
        collected_logs["system.log"] = log_reader.get_logs_as_text(system_logs)
        
        log_reader.save_logs_to_file(application_logs, "application_logs.txt")
        log_reader.save_logs_to_file(system_logs, "system_logs.txt")
        
    elif platform.system().lower() == "linux":
        # Sadece Linux'ta Linux modüllerini import eder
        from linux.linux import LinuxLog
        print("🐧 Linux logları okunuyor...")
        log_reader = LinuxLog()
        
        for name, path in log_reader.log_files.items():
            log_content = log_reader.read_and_save_logs(name, path)
            collected_logs[name + ".log"] = log_content
        
        print("🎉 Linux logları kaydedildi!")

    elif platform.system().lower() == "darwin":
        # Sadece macOS'ta Mac modüllerini import eder
        from mac.mac import MacLog
        print("🍎 macOS logları okunuyor...")
        log_reader = MacLog()
        log_reader.read_all_logs()
        
        for filename in os.listdir("macOS_Log_Toplama"):
            with open(os.path.join("macOS_Log_Toplama", filename), 'r', encoding='utf-8') as f:
                collected_logs[filename] = f.read()

    # AI analizi
    print("\n🤖 AI Analiz Başlıyor...")
    
    ai_analyzer = LogAI()
    ai_report = ai_analyzer.analyze_logs()
    ai_analyzer.print_report(ai_report)
    ai_analyzer.save_report(ai_report, "security_analysis_report.json")

if __name__ == "__main__":
    main()

                           