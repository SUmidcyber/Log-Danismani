import os
from SystemQuery.system_query import SystemQuery


class LinuxlogSS:
    def __init__(self):
        self.sistem = SystemQuery()
        print("Log analizi basliyor")


        self.log_files = {
            "syslog": "/var/log/syslog",
            "auth": "/var/log/auth.log",
            "kernel": "/var/log/kern.log",
            "boot": "/var/log/boot.log",
            "apache2": "/var/log/apache2/error.log",
            "mysql": "/var/log/mysql/error.log"
        }

        self.output_ls = "log_Files"
        os.makedirs(output_ls, exist_ok=True)

    def save_or_read_logs(self, name , path):
        
            with open(path, 'r') as f:
                logs = f.readlines()
            
            out_path = os.path.join(self.output_ls, f"{name}_log.txt")

            with open(path, 'w') as out:
                reads = out.writelines()


