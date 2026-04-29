import hashlib
import requests
import tkinter as tk
from tkinter import messagebox

def проверить_пароль(пароль):
    sha1 = hashlib.sha1(пароль.encode('utf-8')).hexdigest().upper()
    первые_5 = sha1[:5]
    остаток = sha1[5:]
    
    try:
        ответ = requests.get(f'https://api.pwnedpasswords.com/range/{первые_5}')
        for строка in ответ.text.splitlines():
            хеш, количество = строка.split(':')
            if хеш == остаток:
                return int(количество)
        return 0
    except:
        return -1

def нажать_кнопку():
    пароль = поле_ввода.get()
    
    if not пароль:
        messagebox.showwarning('Ошибка', 'Введите пароль!')
        return
    
    if len(пароль) < 6:
        текст_результата.config(
            text='⚠️ Пароль слишком короткий.\nМинимум 6 символов.',
            fg='orange'
        )
        return
    
    результат = проверить_пароль(пароль)

    # Оценка надёжности
    надёжность = 0
    советы = []
    
    if len(пароль) >= 8:
        надёжность += 1
    else:
        советы.append('• минимум 8 символов')
    
    if any(c.isupper() for c in пароль):
        надёжность += 1
    else:
        советы.append('• добавьте заглавные буквы')
    
    if any(c.islower() for c in пароль):
        надёжность += 1
    else:
        советы.append('• добавьте строчные буквы')
    
    if any(c.isdigit() for c in пароль):
        надёжность += 1
    else:
        советы.append('• добавьте цифры')
    
    if any(c in '!@#$%№^&*()_+-=[]{}' for c in пароль):
        надёжность += 1
    else:
        советы.append('• добавьте спецсимволы (!@#$%)')
    
    уровни = {1: ('Очень слабый', 'red'),
              2: ('Слабый', 'orange'),
              3: ('Средний', 'yellow'),
              4: ('Хороший', 'lightgreen'),
              5: ('Отличный', 'green')}
    
    уровень, цвет = уровни.get(надёжность, ('Очень слабый', 'red'))
    текст_надёжности.config(text=f'Надёжность: {уровень}', fg=цвет)
    
    if советы:
        текст_советов.config(text='Как улучшить:\n' + '\n'.join(советы), fg='gray')
    else:
        текст_советов.config(text='')
    
    if результат == -1:
        текст_результата.config(text='Ошибка подключения к интернету', fg='orange')
    elif результат > 0:
        текст_результата.config(
            text=f'⚠️ Пароль найден в утечках {результат:,} раз!\nРекомендуется сменить пароль.',
            fg='red'
        )
        # Если пароль в утечке — надёжность сбрасывается
        текст_надёжности.config(text='Надёжность: Скомпрометирован', fg='red')
        текст_советов.config(text='Этот пароль есть в базах взломщиков.\nСмените его даже если он сложный.', fg='gray')
    else:
        текст_результата.config(
            text='✅ Пароль не найден в известных утечках.',
            fg='green'
        )

# Создаём окно
окно = tk.Tk()
окно.title('Сканер паролей')
окно.geometry('450x400')
окно.resizable(False, False)
окно.configure(bg='#1e1e1e')

# Заголовок
заголовок = tk.Label(окно, text='🔐 Проверка пароля на утечки',
                     font=('Arial', 14, 'bold'),
                     bg='#1e1e1e', fg='white')
заголовок.pack(pady=20)

# Поле ввода
поле_ввода = tk.Entry(окно, width=35, font=('Arial', 12),
                      bg='#2d2d2d', fg='white',
                      insertbackground='white')
поле_ввода.pack(pady=5)

# Кнопка
кнопка = tk.Button(окно, text='Проверить',
                   font=('Arial', 11),
                   bg='#0078d4', fg='white',
                   padx=20, pady=5,
                   command=нажать_кнопку)
кнопка.pack(pady=15)

# Результат
текст_результата = tk.Label(окно, text='',
                            font=('Arial', 11),
                            bg='#1e1e1e', fg='white',
                            wraplength=400, justify='center')
текст_результата.pack(pady=5)

текст_надёжности = tk.Label(окно, text='',
                            font=('Arial', 11, 'bold'),
                            bg='#1e1e1e', fg='white')
текст_надёжности.pack(pady=2)

текст_советов = tk.Label(окно, text='',
                         font=('Arial', 9),
                         bg='#1e1e1e', fg='gray',
                         justify='left')
текст_советов.pack(pady=2)

окно.mainloop()
