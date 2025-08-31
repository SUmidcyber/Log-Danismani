import platform
import socket
import psutil

class SystemQuery:
    def __init__(self):
        try:
            self.query = platform.system()
            self.ps_name = platform.node()
            self.ip = socket.gethostbyname(self.ps_name)
            self.domain = socket.getfqdn()
            self.user = psutil.Process().username()
        except Exception as e:  
            print(f"‼️ Hata: {str(e)}")

    def show_info(self):
        print(f"🎯 Hedef bilgisayar: {self.ps_name}")
        print(f"🌐 IP: {self.ip}")
        print(f"🏷️ Domain: {self.domain}")
        print(f"👤 Kullanıcı: {self.user}")
        print(f"🖥️ İşletim Sistemi: {self.query}")

    def get_computer_name(self):
        return self.ps_name
    
    def get_ip(self):
        return self.ip
    
    def get_user_info(self):
        return {
            'computer_name': self.ps_name,
            'ip': self.ip,
            'domain': self.domain,
            'username': self.user
        }
