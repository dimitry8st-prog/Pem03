import requests
from pathlib import Path
from urllib.parse import quote

# Ваш запрос
prompt = "Космический крейсер в космосе в стиле киберпанк"

# Генерация изображения
url = f"https://image.pollinations.ai/prompt/{quote(prompt)}?width=1024&height=1024"
print(f"Генерирую: {prompt}")

response = requests.get(url)

if response.status_code == 200:
    # Сохранение в файл
    output_file = Path("kot.png")
    with open(output_file, 'wb') as f:
        f.write(response.content)
    
    print(f"✅ Изображение сохранено в {output_file.absolute()}")
    
    # Автоматически открыть изображение
    import os
    os.startfile(output_file)
else:
    print(f"❌ Ошибка: {response.status_code}")