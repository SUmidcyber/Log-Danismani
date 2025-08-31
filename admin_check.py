import ctypes
import sys
import os
import subprocess
import time

def is_admin():
    """Yönetici olarak çalıştırılıp çalıştırılmadığını kontrol et"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Programı yönetici olarak yeniden başlat"""
    if is_admin():
        return True
        
    print("🔒 Yönetici hakları isteniyor...")
    
    # Mevcut script yolunu al
    script = os.path.abspath(sys.argv[0])
    
    # Parametreleri hazırla
    params = ' '.join([f'"{x}"' for x in sys.argv[1:]])
    
    try:
        # Yönetici olarak yeniden başlat
        result = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{script}" {params}', None, 1
        )
        
        if result <= 32:
            print(f"❌ Yönetici hakları alınamadı. Hata kodu: {result}")
            return False
            
        print("✅ Yönetici olarak yeniden başlatılıyor...")
        time.sleep(2)
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ Yönetici hatası: {e}")
        return False
    
    return True

def enable_privileges():
    """Gerekli Windows izinlerini etkinleştir"""
    try:
        import win32security
        import win32api
        
        print("🔓 Windows izinleri etkinleştiriliyor...")
        
        # Gerekli izinleri tanımla
        privileges = [
            win32security.SE_SECURITY_NAME,
            win32security.SE_SYSTEM_ENVIRONMENT_NAME,
            win32security.SE_DEBUG_NAME
        ]
        
        # Mevcut process token'ını al
        token = win32security.OpenProcessToken(
            win32api.GetCurrentProcess(),
            win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY
        )
        
        # Her bir izni etkinleştir
        for priv_name in privileges:
            try:
                privilege = win32security.LookupPrivilegeValue(None, priv_name)
                win32security.AdjustTokenPrivileges(
                    token, False, [(privilege, win32security.SE_PRIVILEGE_ENABLED)]
                )
                print(f"   ✅ {priv_name}")
            except Exception as e:
                print(f"   ⚠️  {priv_name}: {e}")
                
    except ImportError:
        print("⚠️  win32security modülü bulunamadı")
    except Exception as e:
        print(f"❌ İzinler etkinleştirilemedi: {e}")

def check_event_log_service():
    """Event Log servislerini kontrol et"""
    try:
        import psutil
        
        required_services = ['EventLog', 'EventSystem']
        
        for service_name in required_services:
            try:
                service = psutil.win_service_get(service_name)
                if service.status() == 'running':
                    print(f"✅ Servis çalışıyor: {service_name}")
                else:
                    print(f"⚠️  Servis durdu: {service_name}")
            except psutil.NoSuchProcess:
                print(f"❌ Servis bulunamadı: {service_name}")
            except Exception as e:
                print(f"⚠️  Servis kontrol hatası ({service_name}): {e}")
                
    except Exception as e:
        print(f"❌ Servis kontrolü yapılamadı: {e}")