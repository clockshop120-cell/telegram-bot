import subprocess
import sys
import os

print("Запуск бота...")
print("Наблюдаю за изменениями...")

# Путь к bot.py
bot_path = os.path.join(os.path.dirname(__file__), "bot.py")

# Запуск bot.py тем же Python, который запустил run.py
subprocess.run([sys.executable, bot_path])