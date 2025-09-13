import re
import json
import os
import glob
from datetime import datetime, timedelta
import ipaddress
from collections import Counter
import platform

class LogAI:
    def __init__(self):
        self.detected_threats = []
        self.stats = {
            'total_lines': 0,
            'errors': 0,
            'warnings': 0,
            'suspicious_activities': 0,
            'unique_ips': set(),
            'attack_patterns': 0
        }
        
        # Log klasörleri
        self.log_directories = {
            'windows': 'LOG',
            'linux': 'Linux_Log_Toplama',
            'mac': 'macOS_Log_Toplama'
        }
        
        # Saldırı patternleri
        self.attack_patterns = [
            r'failed password',
            r'authentication failure',
            r'brute force',
            r'sql injection',
            r'xss',
            r'csrf',
            r'denial of service',
            r'port scan',
            r'malware',
            r'trojan',
            r'virus',
            r'ransomware',
            r'privilege escalation',
            r'rootkit',
            r'backdoor',
            r'phishing',
            r'spoofing',
            r'mitm',
            r'zero day',
            r'exploit'
        ]
        
        # Şüpheli IP aralıkları
        self.suspicious_ip_ranges = [
            '10.0.0.0/8',
            '172.16.0.0/12', 
            '192.168.0.0/16',
            '100.64.0.0/10'
        ]

    def collect_logs_from_directories(self):
        """
        Tüm log klasörlerinden logları topla
        """
        print("📁 Log klasörleri taranıyor...")
        all_logs = {}
        
        for os_type, directory in self.log_directories.items():
            if os.path.exists(directory):
                print(f"🔍 {directory} klasörü taranıyor...")
                log_files = self._get_log_files_from_directory(directory)
                
                for log_file in log_files:
                    log_content = self._read_log_file(log_file)
                    if log_content:
                        filename = os.path.basename(log_file)
                        all_logs[filename] = log_content
                        print(f"   ✅ {filename} eklendi ({len(log_content.splitlines())} satır)")
            else:
                print(f"⚠️ {directory} klasörü bulunamadı")
        
        return all_logs

    def _get_log_files_from_directory(self, directory):
        """Klasördeki tüm log dosyalarını bul"""
        log_extensions = ['.txt', '.log', '.csv', '.json']
        log_files = []
        
        for ext in log_extensions:
            pattern = os.path.join(directory, f"*{ext}")
            log_files.extend(glob.glob(pattern))
        
        return log_files

    def _read_log_file(self, file_path):
        """Log dosyasını oku"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            print(f"❌ {file_path} okunamadı: {e}")
            return None

    def analyze_logs(self, log_files=None):
        """
        Tüm log dosyalarını analiz et ve threat raporu oluştur
        """
        print("🧠 AI Log Analizi Başlıyor...\n")
        
        # Eğer log_files verilmediyse, klasörlerden toplar
        if log_files is None:
            log_files = self.collect_logs_from_directories()
        
        if not log_files:
            print("❌ Analiz edilecek log dosyası bulunamadı!")
            return self._generate_empty_report()
        
        for file_path, log_content in log_files.items():
            if log_content:
                print(f"📊 {file_path} analiz ediliyor...")
                self._analyze_single_log(file_path, log_content)
        
        return self._generate_report()

    def _analyze_single_log(self, file_path, log_content):
        """Tek bir log dosyasını analiz et"""
        try:
            # Eğer log_content liste ise string'e çevir
            if isinstance(log_content, list):
                log_content = "\n".join(str(item) for item in log_content)
            
            # Eğer log_content None veya boş ise
            if not log_content or not isinstance(log_content, str):
                print(f"⚠️ {file_path}: Geçersiz log içeriği, atlanıyor...")
                return
            
            lines = log_content.split('\n')
            self.stats['total_lines'] += len(lines)
            
            for line_num, line in enumerate(lines, 1):
                if not line or not isinstance(line, str):
                    continue
                    
                line_lower = line.lower()
                
                # Hata ve uyarıları say
                if 'error' in line_lower:
                    self.stats['errors'] += 1
                if 'warning' in line_lower:
                    self.stats['warnings'] += 1
                
                # IP adreslerini bulma ** isletim sistemin
                ips = self._extract_ips(line)
                self.stats['unique_ips'].update(ips)
                
                # Saldırı patternlerini tara
                for pattern in self.attack_patterns:
                    if re.search(pattern, line_lower, re.IGNORECASE):
                        self.stats['attack_patterns'] += 1
                        self._add_threat({
                            'type': 'attack_pattern',
                            'pattern': pattern,
                            'line': line_num,
                            'file': file_path,
                            'evidence': line[:200] + '...' if len(line) > 200 else line,
                            'severity': 'high'
                        })
                
                # Şüpheli aktiviteler
                if self._is_suspicious_activity(line):
                    self.stats['suspicious_activities'] += 1
                    self._add_threat({
                        'type': 'suspicious_activity',
                        'line': line_num,
                        'file': file_path,
                        'evidence': line[:200] + '...' if len(line) > 200 else line,
                        'severity': 'medium'
                    })
                
                # SSH başarısız girişleri
                if 'failed password' in line_lower and 'ssh' in line_lower:
                    self._analyze_ssh_attack(line, line_num, file_path)
                
                # Port tarama şüphesinin analizi
                if any(term in line_lower for term in ['port', 'scan', 'nmap', 'connection refused']):
                    self._analyze_port_scan(line, line_num, file_path)
                
        except Exception as e:
            print(f"❌ {file_path} analiz edilirken hata: {e}")

    def _generate_empty_report(self):
        """Boş rapor oluştur"""
        return {
            'scan_date': datetime.now().isoformat(),
            'system_info': {
                'platform': platform.platform(),
                'python_version': platform.python_version()
            },
            'statistics': {
                'total_lines_analyzed': 0,
                'errors_found': 0,
                'warnings_found': 0,
                'suspicious_activities': 0,
                'attack_patterns_detected': 0,
                'unique_ips_found': 0,
                'total_threats_detected': 0
            },
            'threats': [],
            'recommendations': [],
            'note': 'No log files found for analysis'
        }

    def _extract_ips(self, text):
        """Metinden IP adreslerini çıkar"""
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        return re.findall(ip_pattern, text)

    def _is_suspicious_ip(self, ip):
        """IP adresi şüpheli mi kontrol et"""
        try:
            ip_obj = ipaddress.ip_address(ip)
            for range_str in self.suspicious_ip_ranges:
                if ip_obj in ipaddress.ip_network(range_str):
                    return True
            return False
        except:
            return False

    def _is_suspicious_activity(self, line):
        """Şüpheli aktivite kontrolü"""
        suspicious_terms = [
            'root', 'admin', 'sudo', 'su ', 'password', 'login', 'ssh',
            'firewall', 'iptables', 'kill', 'process', 'injection',
            'script', 'exec', 'system32', 'cmd.exe', 'powershell'
        ]
        
        line_lower = line.lower()
        return any(term in line_lower for term in suspicious_terms)

    def _analyze_ssh_attack(self, line, line_num, file_path):
        """SSH saldırı analizi"""
        ips = self._extract_ips(line)
        for ip in ips:
            self._add_threat({
                'type': 'ssh_bruteforce',
                'ip': ip,
                'line': line_num,
                'file': file_path,
                'evidence': line[:200] + '...' if len(line) > 200 else line,
                'severity': 'high',
                'recommendation': 'SSH portunu değiştir, fail2ban kur, güçlü parola kullan'
            })

    def _analyze_port_scan(self, line, line_num, file_path):
        """Port tarama analizi"""
        ips = self._extract_ips(line)
        for ip in ips:
            self._add_threat({
                'type': 'port_scan',
                'ip': ip,
                'line': line_num,
                'file': file_path,
                'evidence': line[:200] + '...' if len(line) > 200 else line,
                'severity': 'medium',
                'recommendation': 'Gereksiz portları kapat, firewall kurallarını sıkılaştır'
            })

    def _add_threat(self, threat_info):
        """Yeni threat ekle"""
        threat_info['timestamp'] = datetime.now().isoformat()
        threat_info['id'] = f"threat_{len(self.detected_threats) + 1:04d}"
        self.detected_threats.append(threat_info)

    def _generate_report(self):
        """Detaylı analiz raporu oluştur"""
        report = {
            'scan_date': datetime.now().isoformat(),
            'system_info': {
                'platform': platform.platform(),
                'python_version': platform.python_version()
            },
            'statistics': {
                'total_lines_analyzed': self.stats['total_lines'],
                'errors_found': self.stats['errors'],
                'warnings_found': self.stats['warnings'],
                'suspicious_activities': self.stats['suspicious_activities'],
                'attack_patterns_detected': self.stats['attack_patterns'],
                'unique_ips_found': len(self.stats['unique_ips']),
                'total_threats_detected': len(self.detected_threats)
            },
            'threats': self.detected_threats,
            'recommendations': self._generate_recommendations()
        }
        
        return report

    def _generate_recommendations(self):
        """Otomatik öneriler oluştur"""
        recs = []
        
        # SSH saldırı varsa
        ssh_attacks = [t for t in self.detected_threats if t['type'] == 'ssh_bruteforce']
        if ssh_attacks:
            recs.append({
                'type': 'ssh_security',
                'priority': 'high',
                'action': 'SSH portunu değiştir (22 → 2222 gibi), fail2ban kur, root login disable et'
            })
        
        # Port scan varsa
        port_scans = [t for t in self.detected_threats if t['type'] == 'port_scan']
        if port_scans:
            recs.append({
                'type': 'network_security',
                'priority': 'medium',
                'action': 'Gereksiz portları kapat, firewall kur, port taramalarını monitor et'
            })
        
        # Çok sayıda hata varsa
        if self.stats['errors'] > 100:
            recs.append({
                'type': 'system_health',
                'priority': 'medium',
                'action': 'Sistemde çok sayıda hata var, logları detaylı incele'
            })
        
        return recs

    def print_report(self, report):
        """Raporu güzelce yazdır"""
        print("\n" + "="*60)
        print("🤖 AI LOG ANALİZ RAPORU")
        print("="*60)
        
        print(f"\n📊 İSTATİSTİKLER:")
        print(f"   Toplam Satır: {report['statistics']['total_lines_analyzed']}")
        print(f"   Hatalar: {report['statistics']['errors_found']}")
        print(f"   Uyarılar: {report['statistics']['warnings_found']}")
        print(f"   Şüpheli Aktiviteler: {report['statistics']['suspicious_activities']}")
        print(f"   Saldırı Patternleri: {report['statistics']['attack_patterns_detected']}")
        print(f"   Benzersiz IP'ler: {report['statistics']['unique_ips_found']}")
        print(f"   Toplam Tehdit: {report['statistics']['total_threats_detected']}")
        
        if report['threats']:
            print(f"\n⚠️  TESPİT EDİLEN TEHDİTLER ({len(report['threats'])}):")
            for threat in report['threats'][:10]:  # İlk 10 tehdit
                print(f"\n   🔴 {threat['type'].upper()} - {threat['severity'].upper()}")
                print(f"      📍 {threat['file']}:{threat['line']}")
                print(f"      🔍 {threat['evidence']}")
                if 'ip' in threat:
                    print(f"      🌐 IP: {threat['ip']}")
                if 'recommendation' in threat:
                    print(f"      💡 Öneri: {threat['recommendation']}")
        
        if report['recommendations']:
            print(f"\n💡 GÜVENLİK ÖNERİLERİ:")
            for rec in report['recommendations']:
                print(f"   {rec['priority'].upper()}: {rec['action']}")
        
        print(f"\n⏰ Tarama Zamanı: {report['scan_date']}")
        print("="*60)

    def save_report(self, report, filename="security_analysis_report.json"):
        """Raporu JSON dosyasına kaydet"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Rapor kaydedildi: {filename}")
            return True
        except Exception as e:
            print(f"❌ Rapor kaydedilemedi: {e}")
            return False

if __name__ == "__main__":
    ai = LogAI()
    
    report = ai.analyze_logs()
    
    ai.print_report(report)
    ai.save_report(report)