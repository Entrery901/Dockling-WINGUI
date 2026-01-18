"""
Скрипт для конвертации документов различных форматов в Markdown.
Использует библиотеку docling для обработки PDF, DOCX, HTML, PPTX, XLSX и других форматов.
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple
from collections import Counter

from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
    WordFormatOption,
    PowerpointFormatOption,
    MarkdownFormatOption,
    HTMLFormatOption,
)
from docling.datamodel.accelerator_options import (
    AcceleratorDevice,
    AcceleratorOptions,
)
from docling.datamodel.base_models import InputFormat, ConversionStatus
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    PictureDescriptionApiOptions,
    TesseractOcrOptions,
    EasyOcrOptions,
)

from config import Config

try:
    import torch
except ImportError:  # pragma: no cover - torch не является обязательной зависимостью
    torch = None


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('conversion.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class DocumentConversionStats:
    """Класс для отслеживания статистики конвертации."""
    
    def __init__(self):
        self.total_files = 0
        self.successful = 0
        self.partial_success = 0
        self.failed = 0
        self.skipped = 0
        self.errors = []
        self.start_time = datetime.now()
    
    def add_success(self):
        """Добавить успешную конвертацию."""
        self.successful += 1
    
    def add_partial_success(self, filename: str, errors: List[str]):
        """Добавить частично успешную конвертацию."""
        self.partial_success += 1
        self.errors.append({
            'file': filename,
            'status': 'partial',
            'errors': errors
        })
    
    def add_failure(self, filename: str, error: str):
        """Добавить неудачную конвертацию."""
        self.failed += 1
        self.errors.append({
            'file': filename,
            'status': 'failed',
            'error': error
        })
    
    def add_skipped(self, filename: str, reason: str):
        """Добавить пропущенный файл."""
        self.skipped += 1
        self.errors.append({
            'file': filename,
            'status': 'skipped',
            'reason': reason
        })
    
    def print_summary(self):
        """Вывести итоговую статистику."""
        duration = datetime.now() - self.start_time
        
        print("\n" + "="*70)
        print("ИТОГОВАЯ СТАТИСТИКА КОНВЕРТАЦИИ")
        print("="*70)
        print(f"Всего файлов обработано: {self.total_files}")
        print(f"✓ Успешно: {self.successful}")
        if self.partial_success > 0:
            print(f"⚠ Частично успешно: {self.partial_success}")
        if self.failed > 0:
            print(f"✗ Ошибки: {self.failed}")
        if self.skipped > 0:
            print(f"⊝ Пропущено: {self.skipped}")
        print(f"\nВремя выполнения: {duration}")
        
        # Вывод детальной информации об ошибках
        if self.errors:
            print("\n" + "-"*70)
            print("ДЕТАЛИ ОШИБОК И ПРЕДУПРЕЖДЕНИЙ:")
            print("-"*70)
            for error_info in self.errors:
                file_name = error_info['file']
                status = error_info['status']
                
                if status == 'partial':
                    print(f"\n⚠ {file_name} (частично успешно):")
                    for err in error_info['errors']:
                        print(f"  - {err}")
                elif status == 'failed':
                    print(f"\n✗ {file_name} (ошибка):")
                    print(f"  - {error_info['error']}")
                elif status == 'skipped':
                    print(f"\n⊝ {file_name} (пропущено):")
                    print(f"  - {error_info['reason']}")
        
        print("="*70 + "\n")


def scan_input_directory(input_dir: str, supported_extensions: List[str]) -> List[Path]:
    """
    Рекурсивно сканирует директорию и находит все поддерживаемые файлы.
    
    Args:
        input_dir: Путь к входной директории
        supported_extensions: Список поддерживаемых расширений файлов
    
    Returns:
        Список путей к найденным файлам
    """
    logger.info(f"Сканирование директории: {input_dir}")
    
    input_path = Path(input_dir)
    if not input_path.exists():
        logger.error(f"Директория не существует: {input_dir}")
        return []
    
    files = []
    for ext in supported_extensions:
        # Рекурсивный поиск файлов с данным расширением
        found = list(input_path.rglob(f"*{ext}"))
        files.extend(found)
        logger.debug(f"Найдено {len(found)} файлов с расширением {ext}")
    
    logger.info(f"Всего найдено файлов: {len(files)}")
    return files


def generate_unique_output_name(output_dir: Path, original_path: Path, used_names: set) -> str:
    """
    Генерирует уникальное имя для выходного файла.
    
    Args:
        output_dir: Директория для сохранения
        original_path: Путь к оригинальному файлу
        used_names: Множество уже использованных имен
    
    Returns:
        Уникальное имя файла
    """
    base_name = original_path.stem
    counter = 1
    
    # Если имя уже использовалось, добавляем номер
    output_name = f"{base_name}.md"
    while output_name in used_names:
        output_name = f"{base_name}_{counter}.md"
        counter += 1
    
    used_names.add(output_name)
    return output_name


def setup_document_converter(config: Config) -> DocumentConverter:
    """
    Настраивает и возвращает DocumentConverter с нужными параметрами.
    
    Args:
        config: Объект конфигурации
    
    Returns:
        Настроенный DocumentConverter
    """
    logger.info("Настройка конвертера документов...")
    
    # Настройка параметров PDF обработки
    pdf_options = PdfPipelineOptions()
    pdf_options.do_ocr = config.ENABLE_OCR
    pdf_options.do_table_structure = config.ENABLE_TABLE_STRUCTURE
    pdf_options.generate_picture_images = config.GENERATE_PICTURE_IMAGES
    pdf_options.images_scale = config.IMAGES_SCALE

    # Настройка ускорителя (CPU / GPU / MPS)
    accelerator_device = _determine_accelerator_device(config.ACCELERATOR_DEVICE)
    accelerator_kwargs = {'device': accelerator_device}
    if config.ACCELERATOR_NUM_THREADS > 0:
        accelerator_kwargs['num_threads'] = config.ACCELERATOR_NUM_THREADS

    pdf_options.accelerator_options = AcceleratorOptions(**accelerator_kwargs)

    logger.info(
        "Аппаратный ускоритель: %s%s",
        accelerator_device.name,
        f" (потоков: {config.ACCELERATOR_NUM_THREADS})" if config.ACCELERATOR_NUM_THREADS > 0 else "",
    )
    
    # Настройка OCR движка
    if config.ENABLE_OCR:
        if config.OCR_ENGINE.lower() == 'tesseract':
            _configure_tesseract_env()
            logger.info(f"Настройка OCR движка: Tesseract (языки: {', '.join(config.OCR_LANGUAGES)})")
            pdf_options.ocr_options = TesseractOcrOptions(
                lang=config.OCR_LANGUAGES
            )
        elif config.OCR_ENGINE.lower() == 'easyocr':
            # Преобразуем коды языков для EasyOCR (rus->ru, eng->en)
            easyocr_langs = []
            for lang in config.OCR_LANGUAGES:
                if lang.lower() == 'rus':
                    easyocr_langs.append('ru')
                elif lang.lower() == 'eng':
                    easyocr_langs.append('en')
                else:
                    easyocr_langs.append(lang.lower())
            
            logger.info(f"Настройка OCR движка: EasyOCR (языки: {', '.join(easyocr_langs)})")
            pdf_options.ocr_options = EasyOcrOptions(
                lang=easyocr_langs
            )
        else:
            logger.warning(f"Неизвестный OCR движок: {config.OCR_ENGINE}, используется auto")
            # auto выбор движка (по умолчанию)
    
    # Настройка описания изображений через OpenAI API
    pic_desc_enabled = bool(config.ENABLE_PICTURE_DESCRIPTION or config.USE_OPENAI_API)
    if config.USE_OPENAI_API and not config.ENABLE_PICTURE_DESCRIPTION:
        logger.info("USE_OPENAI_API включен — активируем описание изображений")

    if pic_desc_enabled:
        if not config.OPENAI_API_KEY:
            logger.warning("Описание изображений включено, но OPENAI_API_KEY не установлен")
        else:
            logger.info("Настройка описания изображений через OpenAI API")
            pdf_options.do_picture_description = True
            pdf_options.enable_remote_services = True

            # Настройка API для описания изображений
            pdf_options.picture_description_options = PictureDescriptionApiOptions(
                url=f"{config.OPENAI_BASE_URL.rstrip('/')}/chat/completions",
                params=dict(
                    model=config.OPENAI_MODEL_NAME,
                    seed=config.OPENAI_SEED,
                    max_completion_tokens=config.OPENAI_MAX_TOKENS,
                    temperature=config.OPENAI_TEMPERATURE,
                ),
                headers={
                    "Authorization": f"Bearer {config.OPENAI_API_KEY}",
                    "HTTP-Referer": "https://my-app-site.com",
                    "X-Title": "Markdown Converter"
                },
                prompt=config.PICTURE_DESCRIPTION_PROMPT,
                timeout=config.OPENAI_TIMEOUT,
            )

            # Установка API ключа в переменную окружения (если не установлена)
            if config.OPENAI_API_KEY and 'OPENAI_API_KEY' not in os.environ:
                os.environ['OPENAI_API_KEY'] = config.OPENAI_API_KEY
    
    # Создание конвертера с настройками для разных форматов
    format_options = {
        InputFormat.PDF: PdfFormatOption(pipeline_options=pdf_options),
        InputFormat.DOCX: WordFormatOption(),
        InputFormat.PPTX: PowerpointFormatOption(),
        InputFormat.MD: MarkdownFormatOption(),
        InputFormat.HTML: HTMLFormatOption(),
    }
    
    converter = DocumentConverter(format_options=format_options)
    logger.info("Конвертер настроен успешно")
    
    return converter


def _determine_accelerator_device(device_pref: str) -> AcceleratorDevice:
    """
    Возвращает тип ускорителя на основе предпочтений пользователя и доступности GPU.
    """
    normalized = (device_pref or "auto").strip().lower()
    mapping = {
        'auto': AcceleratorDevice.AUTO,
        'cpu': AcceleratorDevice.CPU,
        'cuda': AcceleratorDevice.CUDA,
        'gpu': AcceleratorDevice.CUDA,
        'mps': AcceleratorDevice.MPS,
    }

    requested_device = mapping.get(normalized, AcceleratorDevice.AUTO)

    if requested_device == AcceleratorDevice.CUDA and not _is_cuda_available():
        logger.warning("Запрошен CUDA, но GPU не обнаружен. Переключаемся на CPU.")
        return AcceleratorDevice.CPU

    if requested_device == AcceleratorDevice.MPS and not _is_mps_available():
        logger.warning("Запрошен MPS, но поддержка недоступна. Переключаемся на CPU.")
        return AcceleratorDevice.CPU

    if requested_device == AcceleratorDevice.CUDA and torch is not None:
        try:
            gpu_name = torch.cuda.get_device_name(0)
            logger.info("CUDA GPU активирован: %s", gpu_name)
        except Exception:
            logger.debug("Не удалось получить название CUDA устройства", exc_info=True)

    if requested_device == AcceleratorDevice.MPS:
        logger.info("Используем Apple MPS для OCR.")

    return requested_device


def _configure_tesseract_env():
    if os.environ.get("TESSDATA_PREFIX"):
        return

    candidates = []
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        candidates.append(Path(sys._MEIPASS) / "tesseract")

    env_home = os.environ.get("TESSERACT_HOME") or os.environ.get("TESSERACT_PATH")
    if env_home:
        candidates.append(Path(env_home))

    candidates.append(Path(r"C:\Program Files\Tesseract-OCR"))

    for base in candidates:
        if not base.exists():
            continue
        tessdata_dir = base / "tessdata"
        if tessdata_dir.exists():
            os.environ["TESSDATA_PREFIX"] = str(base)
            os.environ["PATH"] = f"{base};{os.environ.get('PATH', '')}"
            return


def _is_cuda_available() -> bool:
    if torch is None:
        return False
    return torch.cuda.is_available()


def _is_mps_available() -> bool:
    if torch is None:
        return False
    mps_backend = getattr(torch.backends, "mps", None)
    return bool(mps_backend and mps_backend.is_available())


def convert_documents(
    files: List[Path],
    converter: DocumentConverter,
    output_dir: Path,
    config: Config,
    stats: DocumentConversionStats,
    progress_callback=None,
    stop_check=None
):
    """
    Конвертирует список документов в Markdown.

    Args:
        files: Список файлов для конвертации
        converter: Настроенный DocumentConverter
        output_dir: Директория для сохранения результатов
        config: Объект конфигурации
        stats: Объект статистики
        progress_callback: Опциональный callback для прогресса (dict) -> None
        stop_check: Опциональная функция проверки остановки () -> bool
    """
    # Создание выходной директории если не существует
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Фильтрация файлов по размеру
    files_to_convert = []
    for file_path in files:
        file_size = file_path.stat().st_size
        
        if config.MAX_FILE_SIZE > 0 and file_size > config.MAX_FILE_SIZE:
            logger.warning(f"Пропуск файла (слишком большой: {file_size / 1024 / 1024:.1f} MB): {file_path.name}")
            stats.add_skipped(
                file_path.name,
                f"Размер файла ({file_size / 1024 / 1024:.1f} MB) превышает лимит ({config.MAX_FILE_SIZE / 1024 / 1024:.1f} MB)"
            )
            continue
        
        files_to_convert.append(file_path)
    
    stats.total_files = len(files_to_convert)

    if not files_to_convert:
        logger.warning("Нет файлов для конвертации")
        return
    
    logger.info(f"Начало конвертации {len(files_to_convert)} файлов...")
    if progress_callback:
        progress_callback({
            'type': 'log',
            'emoji': 'ℹ',
            'message': f"Начало конвертации {len(files_to_convert)} файлов...",
            'level': 'INFO'
        })

    # Множество для отслеживания использованных имен
    used_names = set()

    # Progress tracker для GUI
    from progress_tracker import ProgressTracker
    tracker = None
    if progress_callback:
        tracker = ProgressTracker(len(files_to_convert))

    # Пакетная конвертация всех файлов
    try:
        # Формируем параметры для convert_all
        convert_params = {
            'source': [str(f) for f in files_to_convert],
            'raises_on_error': not config.CONTINUE_ON_ERROR,
        }
        
        # Добавляем опциональные параметры только если они установлены
        if config.MAX_NUM_PAGES > 0:
            convert_params['max_num_pages'] = config.MAX_NUM_PAGES
        
        if config.MAX_FILE_SIZE > 0:
            convert_params['max_file_size'] = config.MAX_FILE_SIZE
        
        if tracker and files_to_convert:
            tracker.start_file(files_to_convert[0].name, 1)
            progress_callback(tracker.to_progress_message())

        conv_results = converter.convert_all(**convert_params)
        
        # Обработка результатов
        for idx, conv_result in enumerate(conv_results, 1):
            # Check for stop request
            if stop_check and stop_check():
                logger.warning("⚠ Остановка по запросу пользователя")
                break

            original_file = files_to_convert[idx - 1]
            file_name = original_file.name

            # Update progress tracker
            if tracker:
                tracker.start_file(file_name, idx)
                progress_callback(tracker.to_progress_message())

            logger.info(f"[{idx}/{len(files_to_convert)}] Обработка: {file_name}")

            if conv_result.status == ConversionStatus.SUCCESS:
                # Успешная конвертация
                try:
                    # Генерация уникального имени
                    output_name = generate_unique_output_name(
                        output_dir,
                        original_file,
                        used_names
                    )
                    output_path = output_dir / output_name
                    
                    # Сохранение в Markdown
                    conv_result.document.save_as_markdown(str(output_path))

                    logger.info(f"✓ Успешно сохранено: {output_name}")
                    if progress_callback:
                        progress_callback({
                            'type': 'log',
                            'emoji': '✓',
                            'message': f"Успешно сохранено: {output_name}",
                            'level': 'INFO'
                        })
                    stats.add_success()

                    # Update tracker for GUI
                    if tracker:
                        tracker.update_stats('success')
                        tracker.end_file(idx)
                        progress_callback(tracker.to_stats_message())
                        progress_callback(tracker.to_progress_message())

                except Exception as e:
                    logger.error(f"✗ Ошибка сохранения {file_name}: {str(e)}")
                    if progress_callback:
                        progress_callback({
                            'type': 'log',
                            'emoji': '✗',
                            'message': f"Ошибка сохранения: {file_name} — {str(e)}",
                            'level': 'ERROR'
                        })
                    stats.add_failure(file_name, f"Ошибка сохранения: {str(e)}")

                    # Update tracker for GUI
                    if tracker:
                        tracker.update_stats('failed')
                        tracker.end_file(idx)
                        progress_callback(tracker.to_stats_message())
                        progress_callback(tracker.to_progress_message())
            
            elif conv_result.status == ConversionStatus.PARTIAL_SUCCESS:
                # Частично успешная конвертация
                try:
                    output_name = generate_unique_output_name(
                        output_dir,
                        original_file,
                        used_names
                    )
                    output_path = output_dir / output_name
                    
                    # Сохранение частичного результата
                    conv_result.document.save_as_markdown(str(output_path))
                    
                    # Сбор ошибок
                    error_messages = [
                        error.error_message
                        for error in conv_result.errors
                    ]
                    
                    logger.warning(f"⚠ Частично успешно: {output_name}")
                    if progress_callback:
                        progress_callback({
                            'type': 'log',
                            'emoji': '⚠',
                            'message': f"Частично успешно: {output_name}",
                            'level': 'WARNING'
                        })
                    for err_msg in error_messages:
                        logger.warning(f"  - {err_msg}")
                        if progress_callback:
                            progress_callback({
                                'type': 'log',
                                'emoji': '⚠',
                                'message': f"  - {err_msg}",
                                'level': 'WARNING'
                            })

                    stats.add_partial_success(file_name, error_messages)

                    # Update tracker for GUI
                    if tracker:
                        tracker.update_stats('partial')
                        tracker.end_file(idx)
                        progress_callback(tracker.to_stats_message())
                        progress_callback(tracker.to_progress_message())

                except Exception as e:
                    logger.error(f"✗ Ошибка сохранения частичного результата {file_name}: {str(e)}")
                    if progress_callback:
                        progress_callback({
                            'type': 'log',
                            'emoji': '✗',
                            'message': f"Ошибка сохранения: {file_name} — {str(e)}",
                            'level': 'ERROR'
                        })
                    stats.add_failure(file_name, f"Ошибка сохранения: {str(e)}")

                    # Update tracker for GUI
                    if tracker:
                        tracker.update_stats('failed')
                        tracker.end_file(idx)
                        progress_callback(tracker.to_stats_message())
                        progress_callback(tracker.to_progress_message())

            else:
                # Ошибка конвертации
                error_msg = "Неизвестная ошибка"
                if conv_result.errors:
                    error_msg = "; ".join([err.error_message for err in conv_result.errors])

                logger.error(f"✗ Ошибка конвертации {file_name}: {error_msg}")
                if progress_callback:
                    progress_callback({
                        'type': 'log',
                        'emoji': '✗',
                        'message': f"Ошибка конвертации {file_name}: {error_msg}",
                        'level': 'ERROR'
                    })
                stats.add_failure(file_name, error_msg)

                # Update tracker for GUI
                if tracker:
                    tracker.update_stats('failed')
                    tracker.end_file(idx)
                    progress_callback(tracker.to_stats_message())
                    progress_callback(tracker.to_progress_message())
    
    except Exception as e:
        logger.error(f"Критическая ошибка при конвертации: {str(e)}")
        if not config.CONTINUE_ON_ERROR:
            raise


def main():
    """Главная функция скрипта."""
    print("\n" + "="*70)
    print("КОНВЕРТЕР ДОКУМЕНТОВ В MARKDOWN (на базе Docling)")
    print("="*70 + "\n")
    
    # Валидация конфигурации
    errors = Config.validate()
    if errors:
        logger.error("Ошибки конфигурации:")
        for error in errors:
            logger.error(f"  - {error}")
        sys.exit(1)
    
    # Вывод текущей конфигурации
    Config.print_config()
    
    # Инициализация статистики
    stats = DocumentConversionStats()
    
    try:
        # Шаг 1: Сканирование входной директории
        logger.info("Шаг 1: Сканирование входной директории")
        files = scan_input_directory(Config.INPUT_DIR, Config.SUPPORTED_EXTENSIONS)
        
        if not files:
            logger.warning("Файлы для конвертации не найдены")
            return
        
        # Вывод статистики по типам файлов
        file_extensions = Counter([f.suffix.lower() for f in files])
        logger.info("Найденные типы файлов:")
        for ext, count in file_extensions.items():
            logger.info(f"  {ext}: {count} файл(ов)")
        
        # Шаг 2: Настройка конвертера
        logger.info("\nШаг 2: Настройка конвертера")
        converter = setup_document_converter(Config)
        
        # Шаг 3: Конвертация документов
        logger.info("\nШаг 3: Конвертация документов")
        output_path = Path(Config.OUTPUT_DIR)
        convert_documents(files, converter, output_path, Config, stats)
        
        # Шаг 4: Вывод итоговой статистики
        stats.print_summary()
        
        logger.info(f"Результаты сохранены в: {output_path.absolute()}")
        
    except KeyboardInterrupt:
        logger.info("\nПрервано пользователем")
        stats.print_summary()
        sys.exit(0)
    
    except Exception as e:
        logger.error(f"Критическая ошибка: {str(e)}", exc_info=True)
        stats.print_summary()
        sys.exit(1)


if __name__ == "__main__":
    main()


