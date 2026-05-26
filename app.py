"""
Main application class for Mirantynius DDoS Tool
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

from styles import setup_styles
from animations import glitch_open_animation, glitch_close_animation
from widgets import create_title_bar, create_main_widgets
from attack_engine import AttackEngine

class ModernDDoSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mirantynius")
        self.root.geometry("700x600")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(True, True)
        
        # Убираем стандартную панель заголовка Windows
        self.root.overrideredirect(True)
        
        # Центрируем окно на экране
        self.center_window()
        
        # Initialize entry variables
        self.host_entry = None
        self.port_entry = None
        self.message_entry = None
        self.conn_entry = None
        
        # Переменные для перемещения окна
        self.x = 0
        self.y = 0
        
        # Стилизация
        setup_styles()
        
        # Attack engine
        self.attack_engine = AttackEngine(self)
        
        # Запускаем анимацию появления
        self.root.after(100, self.start_animation)
    
    def center_window(self):
        """Центрирование окна на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def start_animation(self):
        """Запуск анимации открытия"""
        glitch_open_animation(self.root, self.center_window, self.create_widgets)
    
    def close_animation(self):
        """Запуск анимации закрытия"""
        glitch_close_animation(self.root)
    
    def create_widgets(self):
        """Создание всех виджетов интерфейса"""
        # Создаем кастомную панель заголовка
        create_title_bar(self.root, self.close_animation, self.center_window)
        
        # Создаем основные виджеты
        create_main_widgets(self)
    
    def show_about(self):
        """Показать информацию о программе"""
        about_text = """✨ Mirantynius 1.0 beta

🚀 Advanced DDoS Testing Tool

Developed by:

🏢 Organization CVANTA! {
    👨‍💻 GovGer
    🔧 cLOCKER
    🎨 dablix
}


!!! The responsibility for use is on your shoulders !!!
"""
        messagebox.showinfo("About Mirantynius", about_text)
    
    def log_message(self, message):
        """Добавить сообщение в лог"""
        timestamp = time.strftime('%H:%M:%S')
        self.log_area.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_area.see(tk.END)
        self.status_var.set(f"📝 {message}")
    
    def clear_log(self):
        """Очистить лог"""
        self.log_area.delete(1.0, tk.END)
        self.log_message("Log cleared successfully")
        self.progress_var.set(0)
    
    def start_attack(self):
        """Начать DDoS атаку"""
        self.attack_engine.start_attack()
    
    def stop_attack(self):
        """Остановить DDoS атаку"""
        self.attack_engine.stop_attack()
    
    def attack_finished(self):
        """Завершение атаки"""
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress_var.set(100)
        self.log_message(f"✅ Attack finished! Total connections: {self.attack_engine.connections}")
        self.status_var.set("🟢 Ready - Attack completed")
    # В класс ModernDDoSApp добавить следующие методы:

    def get_host(self):
        return self.host_entry.get().strip()

    def get_port(self):
        return self.port_entry.get().strip()

    def get_message(self):
        return self.message_entry.get()

    def get_connections(self):
        return self.conn_entry.get().strip()

    def show_error(self, message):
        from tkinter import messagebox
        messagebox.showerror("Error", message)

    def on_attack_start(self):
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress_var.set(0)

    def update_progress(self, progress):
        self.progress_var.set(progress)

    def on_attack_finished(self, connections):
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress_var.set(100)
        self.log_message(f"✅ Attack finished! Total connections: {connections}")
        self.status_var.set("🟢 Ready - Attack completed")

    def on_attack_stop(self):
        self.stop_btn.config(state=tk.DISABLED)
        self.status_var.set("🟡 Stopping attack...")