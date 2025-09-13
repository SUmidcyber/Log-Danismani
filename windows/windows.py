import win32evtlog
import win32evtlogutil
from SystemQuery.system_query import SystemQuery  

class WindowsLog:
    def __init__(self):
        self.sistem = SystemQuery()
        print("📝 Log okuyucu hazırlandı")
    
    def read_event_log(self, log_name, computer_name="."):
        """Basit log okuma metodu"""
        try:
            print(f"📖 {log_name} okunuyor...")
            
            # Yerel bilgisayar için nokta kullan
            server = "." if computer_name.lower() in ["localhost", "127.0.0.1", "::1"] else computer_name
            
            handle = win32evtlog.OpenEventLog(server, log_name)
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            
            events = []
            try:
                # Küçük parçalar halinde oku
                while True:
                    chunk = win32evtlog.ReadEventLog(handle, flags, 0, 100)
                    if not chunk:
                        break
                    events.extend(chunk)
            except Exception as e:
                print(f"   ⚠️  Okuma hatası: {e}")
            
            win32evtlog.CloseEventLog(handle)
            return events
            
        except Exception as e:
            print(f"   ❌ {log_name} açılamadı: {e}")
            return []
    
    def windows_log_collection(self):
        """Tüm logları topla - basitleştirilmiş"""
        print("📊 Loglar toplanıyor...")
        
        bilgisayar_adi = self.sistem.get_computer_name()
        print(f"🔗 Bilgisayar: {bilgisayar_adi}")
        
        # Sadece temel loglarla başla
        log_types = ['Application', 'System']
        
        total_events = 0
        
        for log_name in log_types:
            events = self.read_event_log(log_name, bilgisayar_adi)
            event_count = len(events)
            total_events += event_count
            
            print(f"✅ {log_name}: {event_count} olay")
            
            # İlk birkaç olayı göster
            for i, event in enumerate(events[:2]):
                try:
                    if hasattr(event, 'TimeGenerated'):
                        print(f"   ⏰ {event.TimeGenerated} - {event.SourceName}")
                except:
                    pass
        
        # Security log'unu dene (opsiyonel)
        try:
            security_events = self.read_event_log('Security', bilgisayar_adi)
            print(f"🔒 Security: {len(security_events)} olay")
            total_events += len(security_events)
        except:
            print("⚠️  Security log'una erişilemedi")
        
        return total_events
import os
import win32evtlog
import win32evtlogutil
from SystemQuery.system_query import SystemQuery  

class WindowsLog:
    def __init__(self):
        self.sistem = SystemQuery()
        print("📝 Log okuyucu hazırlandı")

        # LOG klasörü yoksa oluştur
        self.log_folder = os.path.join(os.getcwd(), "LOG")
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)
            print(f"📂 LOG klasörü oluşturuldu: {self.log_folder}")

    def read_logs(self, log_name, computer_name="."):
        """Belirtilen logu oku"""
        try:
            print(f"📖 {log_name} okunuyor...")

            server = "." if computer_name in ["localhost", ".", "127.0.0.1"] else computer_name
            handle = win32evtlog.OpenEventLog(server, log_name)
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

            events = []
            while True:
                chunk = win32evtlog.ReadEventLog(handle, flags, 0, 100)
                if not chunk:
                    break
                events.extend(chunk)

            win32evtlog.CloseEventLog(handle)
            return events

        except Exception as e:
            print(f"❌ {log_name} okunamadı: {e}")
            return []

    def save_logs_to_file(self, events, filename):
        """Event'leri dosyaya kaydet"""
        if not events:
            print(f"⚠️ {filename} için kaydedilecek event yok!")
            return
        
        filepath = os.path.join(self.log_folder, filename)  
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                for event in events[:100]:  # İlk 100 event *** artira bilirsin
                    f.write(f"Event ID: {event.EventID}\n")
                    f.write(f"Time: {event.TimeGenerated}\n")
                    f.write(f"Source: {event.SourceName}\n")
                    f.write(f"Message: {str(event.StringInserts)}\n")
                    f.write("-" * 50 + "\n")
            
            print(f"✅ {len(events)} event {filename} dosyasına kaydedildi!")
            
        except Exception as e:
            print(f"❌ Dosya yazma hatası: {e}")

    def get_logs_as_text(self, events):
        """Event listesini text formatına çevir"""
        if not events:
            return ""
        
        log_text = ""
        for i, event in enumerate(events[:100]):  # İlk 100 event *** artira bilirsin
            try:
                log_text += f"=== EVENT {i+1} ===\n"
                log_text += f"Event ID: {event.EventID}\n"
                log_text += f"Time: {event.TimeGenerated}\n"
                log_text += f"Source: {event.SourceName}\n"
                
                # StringInserts None olabilir, kontrol edilir
                if event.StringInserts:
                    message = " ".join(str(item) for item in event.StringInserts if item)
                    log_text += f"Message: {message}\n"
                else:
                    log_text += "Message: No message content\n"
                    
                log_text += "-" * 50 + "\n\n"
                
            except Exception as e:
                log_text += f"Error reading event: {e}\n"
                log_text += "-" * 50 + "\n\n"
        
        return log_text

