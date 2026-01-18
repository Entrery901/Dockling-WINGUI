"""
Конфигурационный файл для настройки параметров конвертации документов.
Использует переменные окружения из .env файла для хранения чувствительных данных.
"""

import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()


class Config:
    """Класс конфигурации для управления настройками конвертации."""
    
    # ==================== ПАРАМЕТРЫ OCR ====================
    # Включить/отключить распознавание текста (для сканированных документов)
    ENABLE_OCR = os.getenv('ENABLE_OCR', 'true').lower() == 'true'
    
    # OCR движок: 'easyocr' или 'tesseract'
    OCR_ENGINE = os.getenv('OCR_ENGINE', 'easyocr')
    
    # Языки для OCR (через запятую, например: 'rus,eng' или 'ru,en')
    # Для Tesseract: rus, eng, deu, fra и т.д.
    # Для EasyOCR: ru, en, de, fr и т.д.
    OCR_LANGUAGES = [lang.strip() for lang in os.getenv('OCR_LANGUAGES', 'rus,eng').split(',')]
    
    # ==================== ПАРАМЕТРЫ ТАБЛИЦ ====================
    # Включить/отключить распознавание структуры таблиц
    ENABLE_TABLE_STRUCTURE = os.getenv('ENABLE_TABLE_STRUCTURE', 'true').lower() == 'true'
    
    # Режим обработки таблиц: 'fast' (быстрый) или 'accurate' (точный)
    TABLE_STRUCTURE_MODE = os.getenv('TABLE_STRUCTURE_MODE', 'accurate')
    
    # ==================== ПАРАМЕТРЫ ИЗОБРАЖЕНИЙ ====================
    # Генерировать изображения из документа
    GENERATE_PICTURE_IMAGES = os.getenv('GENERATE_PICTURE_IMAGES', 'true').lower() == 'true'
    
    # Масштаб изображений (1.0 - оригинальный размер, 2.0 - двойной)
    IMAGES_SCALE = float(os.getenv('IMAGES_SCALE', '2.0'))
    
    # Включить описание изображений с помощью VLM модели
    ENABLE_PICTURE_DESCRIPTION = os.getenv('ENABLE_PICTURE_DESCRIPTION', 'false').lower() == 'true'
    
    # Промпт для описания изображений
    PICTURE_DESCRIPTION_PROMPT = os.getenv(
        'PICTURE_DESCRIPTION_PROMPT',
        'Опишите это изображение в трех-пяти предложениях. Будьте точны и кратки.'
    )
    
    # ==================== OPENAI API НАСТРОЙКИ ====================
    # Использовать OpenAI API для расширенных функций (VLM модели)
    USE_OPENAI_API = os.getenv('USE_OPENAI_API', 'false').lower() == 'true'
    
    # API ключ OpenAI (или совместимого сервиса)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Base URL для OpenAI API (для проксирования через OpenAI v1 совместимые сервисы)
    # Примеры: 
    # - OpenAI: https://api.openai.com/v1
    # - Локальный VLLM: http://localhost:8000/v1
    # - Другой proxy: https://your-proxy.example.com/v1
    OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://api.polza.ai/api/v1')
    
    # Имя модели для использования с OpenAI API
    OPENAI_MODEL_NAME = os.getenv('OPENAI_MODEL_NAME', 'openai/gpt-4o-mini')
    
    # Таймаут для запросов к OpenAI API (в секундах)
    OPENAI_TIMEOUT = int(os.getenv('OPENAI_TIMEOUT', '90'))
    
    # Максимальное количество токенов для генерации описаний
    OPENAI_MAX_TOKENS = int(os.getenv('OPENAI_MAX_TOKENS', '400'))
    
    # Temperature для генерации (0.0 - детерминированный, 1.0 - креативный)
    OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.0'))
    
    # Seed для воспроизводимости результатов
    OPENAI_SEED = int(os.getenv('OPENAI_SEED', '42'))

    # ==================== ПАРАМЕТРЫ УСКОРИТЕЛЯ ====================
    # Предпочтительное устройство: auto, cpu, cuda, gpu, mps
    ACCELERATOR_DEVICE = os.getenv('ACCELERATOR_DEVICE', 'cuda').lower()
    # Количество потоков для CPU (0 = по умолчанию библиотеки)
    ACCELERATOR_NUM_THREADS = int(os.getenv('ACCELERATOR_NUM_THREADS', '0'))
    
    # ==================== ПАРАМЕТРЫ КОНВЕРТАЦИИ ====================
    # Максимальное количество страниц для обработки (0 = без ограничений)
    MAX_NUM_PAGES = int(os.getenv('MAX_NUM_PAGES', '0'))
    
    # Максимальный размер файла в байтах (50MB по умолчанию, 0 = без ограничений)
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', '52428800'))
    
    # Продолжить обработку при ошибках (не прерывать весь процесс)
    CONTINUE_ON_ERROR = os.getenv('CONTINUE_ON_ERROR', 'true').lower() == 'true'
    
    # Включить подключение к удаленным сервисам (требуется для OpenAI API)
    ENABLE_REMOTE_SERVICES = os.getenv('ENABLE_REMOTE_SERVICES', 'false').lower() == 'true'
    
    # ==================== ПУТИ К ПАПКАМ ====================
    # Папка для входных документов
    INPUT_DIR = os.getenv('INPUT_DIR', 'input')
    
    # Папка для выходных Markdown файлов
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'output')
    
    # ==================== ПОДДЕРЖИВАЕМЫЕ ФОРМАТЫ ====================
    # Расширения файлов для обработки
    SUPPORTED_EXTENSIONS = [
        '.pdf',   # PDF документы
        '.docx',  # Microsoft Word
        '.doc',   # Microsoft Word (старый формат)
        '.pptx',  # Microsoft PowerPoint
        '.ppt',   # Microsoft PowerPoint (старый формат)
        '.xlsx',  # Microsoft Excel
        '.xls',   # Microsoft Excel (старый формат)
        '.html',  # HTML документы
        '.htm',   # HTML документы
        '.xml',   # XML документы (включая JATS)
        '.md',    # Markdown документы
        '.asciidoc', # AsciiDoc документы
        '.adoc',  # AsciiDoc документы
    ]
    
    @classmethod
    def validate(cls):
        """Проверка корректности конфигурации."""
        errors = []
        
        # Проверка OpenAI настроек если API включен
        if cls.USE_OPENAI_API:
            if not cls.OPENAI_API_KEY:
                errors.append("OPENAI_API_KEY не установлен, но USE_OPENAI_API=true")
            if not cls.OPENAI_BASE_URL:
                errors.append("OPENAI_BASE_URL не установлен")
        
        # Проверка путей к папкам
        if not os.path.exists(cls.INPUT_DIR):
            errors.append(f"Входная папка '{cls.INPUT_DIR}' не существует")
        
        # Проверка числовых значений
        if cls.IMAGES_SCALE <= 0:
            errors.append("IMAGES_SCALE должен быть больше 0")
        
        if cls.OPENAI_TIMEOUT <= 0:
            errors.append("OPENAI_TIMEOUT должен быть больше 0")
        
        if cls.MAX_NUM_PAGES < 0:
            errors.append("MAX_NUM_PAGES не может быть отрицательным")
        
        if cls.MAX_FILE_SIZE < 0:
            errors.append("MAX_FILE_SIZE не может быть отрицательным")

        if cls.ACCELERATOR_DEVICE not in {'auto', 'cpu', 'cuda', 'gpu', 'mps'}:
            errors.append("ACCELERATOR_DEVICE должен быть одним из: auto, cpu, cuda, gpu, mps")

        if cls.ACCELERATOR_NUM_THREADS < 0:
            errors.append("ACCELERATOR_NUM_THREADS не может быть отрицательным")
        
        return errors
    
    @classmethod
    def print_config(cls):
        """Вывод текущей конфигурации (без чувствительных данных)."""
        print("\n" + "="*60)
        print("ТЕКУЩАЯ КОНФИГУРАЦИЯ")
        print("="*60)
        print(f"OCR включен: {cls.ENABLE_OCR}")
        if cls.ENABLE_OCR:
            print(f"OCR движок: {cls.OCR_ENGINE}")
            print(f"OCR языки: {', '.join(cls.OCR_LANGUAGES)}")
        print(f"Обработка таблиц: {cls.ENABLE_TABLE_STRUCTURE} ({cls.TABLE_STRUCTURE_MODE})")
        print(f"Генерация изображений: {cls.GENERATE_PICTURE_IMAGES} (масштаб: {cls.IMAGES_SCALE}x)")
        print(f"Описание изображений: {cls.ENABLE_PICTURE_DESCRIPTION}")
        print(f"\nOpenAI API: {cls.USE_OPENAI_API}")
        if cls.USE_OPENAI_API:
            api_key_masked = cls.OPENAI_API_KEY[:8] + "..." if cls.OPENAI_API_KEY else "не установлен"
            print(f"  API ключ: {api_key_masked}")
            print(f"  Base URL: {cls.OPENAI_BASE_URL}")
            print(f"  Модель: {cls.OPENAI_MODEL_NAME}")
            print(f"  Таймаут: {cls.OPENAI_TIMEOUT}s")
        print(f"\nМакс. страниц: {cls.MAX_NUM_PAGES if cls.MAX_NUM_PAGES > 0 else 'без ограничений'}")
        print(f"Макс. размер файла: {cls.MAX_FILE_SIZE / 1024 / 1024:.1f} MB" if cls.MAX_FILE_SIZE > 0 else "без ограничений")
        print(f"Продолжать при ошибках: {cls.CONTINUE_ON_ERROR}")
        accel_threads = cls.ACCELERATOR_NUM_THREADS if cls.ACCELERATOR_NUM_THREADS > 0 else 'авто'
        print(f"Ускоритель: {cls.ACCELERATOR_DEVICE.upper()} (потоков: {accel_threads})")
        print(f"\nВходная папка: {cls.INPUT_DIR}")
        print(f"Выходная папка: {cls.OUTPUT_DIR}")
        print(f"Поддерживаемые форматы: {', '.join(cls.SUPPORTED_EXTENSIONS)}")
        print("="*60 + "\n")


# Пример использования
if __name__ == "__main__":
    # Проверка конфигурации
    errors = Config.validate()
    if errors:
        print("ОШИБКИ КОНФИГУРАЦИИ:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✓ Конфигурация валидна")
    
    # Вывод конфигурации
    Config.print_config()


