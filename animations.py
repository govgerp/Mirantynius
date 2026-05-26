"""
Animation effects for Mirantynius DDoS Tool
"""

import random
import tkinter as tk

def glitch_open_animation(root, center_callback, create_widgets_callback):
    """Анимация глитча при открытии приложения"""
    colors = ['#2c3e50', '#3498db', '#e74c3c', '#1a1a2e']
    
    def apply_glitch(step):
        if step < 10:
            # Случайное изменение размера и положения
            if step % 2 == 0:
                width = 700 + random.randint(-20, 20)
                height = 600 + random.randint(-20, 20)
                x = (root.winfo_screenwidth() // 2) - (width // 2) + random.randint(-10, 10)
                y = (root.winfo_screenheight() // 2) - (height // 2) + random.randint(-10, 10)
                root.geometry(f'{width}x{height}+{x}+{y}')
            
            # Случайное изменение цвета фона
            root.configure(bg=random.choice(colors))
            
            # Следующий шаг анимации
            root.after(50, lambda: apply_glitch(step + 1))
        else:
            # Восстанавливаем нормальный вид
            root.configure(bg='#2c3e50')
            root.geometry('700x600')
            center_callback()
            
            # Создаем виджеты после завершения анимации
            create_widgets_callback()
    
    # Запускаем анимацию
    apply_glitch(0)

def glitch_close_animation(root):
    """Анимация глитча при закрытии приложения"""
    colors = ['#2c3e50', '#3498db', '#e74c3c', '#1a1a2e', '#000000']
    
    def apply_glitch(step):
        if step < 15:
            # Случайное изменение размера и положения
            width = 700 + random.randint(-50, 50)
            height = 600 + random.randint(-50, 50)
            x = (root.winfo_screenwidth() // 2) - (width // 2) + random.randint(-20, 20)
            y = (root.winfo_screenheight() // 2) - (height // 2) + random.randint(-20, 20)
            root.geometry(f'{width}x{height}+{x}+{y}')
            
            # Случайное изменение цвета фона
            root.configure(bg=random.choice(colors))
            
            # Следующий шаг анимации
            root.after(50, lambda: apply_glitch(step + 1))
        else:
            # Полностью закрываем приложение
            root.destroy()
    
    # Запускаем анимацию
    apply_glitch(0)