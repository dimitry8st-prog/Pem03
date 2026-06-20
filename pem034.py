import os
import requests
import argparse
from pathlib import Path
from urllib.parse import quote
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Gemini через OpenAI-совместимый интерфейс
client_gemini = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),  # Исправлено
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"  # Добавлена точка
)

if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY не найден в .env")

def generate_text(prompt: str, model: str = "gemini-2.0-flash") -> str:
    """Генерация текста с помощью Gemini"""
    response = client_gemini.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Ты полезный ассистент."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=1024,
    )
    if response.choices and response.choices[0].message.content:
        return response.choices[0].message.content
    else:
        raise Exception("Пустой ответ от API")


def generate_image(prompt: str, output_path: Path) -> None:
    """Генерация изображения через Pollinations.ai"""
    url = f"https://image.pollinations.ai/prompt/{quote(prompt)}?width=1024&height=1024"
    
    print("Генерирую изображение...")
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"Изображение сохранено: {output_path}")
    else:
        print(f"Ошибка генерации изображения: {response.status_code}")


def main():
    parser = argparse.ArgumentParser(description="Генерация через Gemini + Pollinations")
    parser.add_argument("-p", "--prompt", type=str, required=True, help="Текстовое описание")
    parser.add_argument("-o", "--output", type=Path, default=Path("image.png"), help="Путь для сохранения")
    args = parser.parse_args()
    
    # Шаг 1: Gemini улучшает промпт
    print("Улучшаю промпт через Gemini...")
    improved_prompt = generate_text(
        f"Создай детальное английское описание для генерации изображения: {args.prompt}. "
        f"Отвечай только описанием, без лишних слов."
    )
    print(f"Улучшенный промпт: {improved_prompt}\n")
    
    # Шаг 2: Pollinations генерирует изображение
    generate_image(improved_prompt, args.output)


if __name__ == "__main__":
    main()

