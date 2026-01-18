#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Internationalization (i18n) for Dockling WINGUI.
Supports Russian and English with runtime switching.
"""


class I18n:
    """Internationalization manager with Russian and English translations"""

    translations = {
        'ru': {
            # Application
            'app_title': 'Dockling WINGUI',
            'quit': 'Выход',
            'quit_confirmation': 'Конвертация в процессе. Вы уверены, что хотите выйти?',

            # Tabs
            'tab_api': 'API Настройки',
            'tab_paths': 'Пути к папкам',
            'tab_processing': 'Обработка',
            'tab_hardware': 'Аппаратное ускорение',
            'tab_limits': 'Ограничения',
            'tab_about': 'О авторе',

            # API Tab
            'api_key_label': 'OpenRouter API ключ:',
            'api_key_placeholder': 'sk-or-v1-...',
            'api_test_button': 'Проверить',
            'api_model_label': 'Модель:',
            'api_enable_api': 'Включить OpenAI API',
            'api_enable_desc': 'Включить AI описания изображений',
            'api_prompt_label': 'Промпт для описаний:',
            'api_prompt_default': 'Опишите это изображение в трех-пяти предложениях. Будьте точны и кратки.',
            'api_base_url_label': 'Base URL:',
            'api_timeout_label': 'Таймаут (сек):',
            'api_max_tokens_label': 'Макс токенов:',
            'api_temperature_label': 'Temperature:',

            # About Tab
            'about_title': 'Об авторе',
            'about_info': 'Ребята, меня зовут Павел. Я делал эту программу для себя и сам использую ее каждый день. Не судите строго :)',
            'about_site_label': 'Сайт:',
            'about_email_label': 'Почта:',
            'about_donation_title': 'Поддержать проект',
            'about_donation_phrase': 'Если программа оказалась вам полезна, я не откажусь от донатов:',
            'about_wallet_label': 'TRON (TRC20) кошелек:',
            'about_wallet_copy': 'Скопировать адрес',
            'about_wallet_copied': 'Адрес скопирован',
            'about_qr_crypto': 'Донат в крипте',
            'about_qr_rub': 'Донат рубли',
            'about_license_title': 'Лицензии',
            'about_license_docling': 'В приложении используются сторонние компоненты:\n— Docling (IBM). Лицензия MIT.\nДанная технология обеспечивает качественную конвертацию документов.\nМы выражаем благодарность разработчикам IBM за создание этого инструмента.',

            # Paths Tab
            'paths_title': 'Пути к файлам и папкам',
            'paths_input_section': 'Входные файлы',
            'paths_output_section': 'Сохранение результатов',
            'paths_input_label': 'Входящие документы:',
            'paths_output_label': 'Исходящие документы:',
            'paths_browse_button': 'Выбрать...',
            'paths_mode_folder': 'Обработать всю папку',
            'paths_mode_files': 'Выбрать отдельные файлы',
            'paths_select_files_button': 'Выбрать файлы...',
            'paths_clear_files': 'Очистить',
            'paths_selected_files': 'Выбрано файлов: {count}',
            'paths_auto_create': 'Создать папку автоматически, если не существует',

            # Processing Tab
            'proc_ocr_enable': 'Включить OCR распознавание',
            'proc_ocr_engine_label': 'OCR движок:',
            'proc_ocr_engine_easyocr': 'EasyOCR',
            'proc_ocr_engine_tesseract': 'Tesseract',
            'proc_ocr_languages_label': 'Языки OCR:',
            'proc_ocr_languages_hint': '(через запятую, например: rus,eng)',
            'proc_table_enable': 'Распознавание таблиц',
            'proc_table_mode_label': 'Режим таблиц:',
            'proc_table_mode_accurate': 'Точный',
            'proc_table_mode_fast': 'Быстрый',
            'proc_images_enable': 'Извлечение изображений',
            'proc_images_scale_label': 'Масштаб изображений:',
            'proc_images_scale_hint': '(1.0 = оригинальный размер)',

            # Hardware Tab
            'hw_accelerator_label': 'Ускоритель:',
            'hw_accelerator_auto': 'AUTO (автовыбор)',
            'hw_accelerator_cpu': 'CPU',
            'hw_accelerator_cuda': 'CUDA (NVIDIA GPU)',
            'hw_accelerator_gpu': 'GPU (общий)',
            'hw_accelerator_mps': 'MPS (Apple Metal)',
            'hw_cpu_threads_label': 'CPU потоков:',
            'hw_cpu_threads_hint': '(0 = автоматически)',
            'hw_gpu_status_label': 'Статус GPU:',
            'hw_gpu_detected': 'Обнаружен: {name}',
            'hw_gpu_not_detected': 'GPU не обнаружен',
            'hw_cuda_available': 'CUDA доступен',
            'hw_cuda_not_available': 'CUDA недоступен',

            # Limits Tab
            'limits_max_size_label': 'Макс размер файла (MB):',
            'limits_max_size_hint': '(0 = без ограничений)',
            'limits_max_pages_label': 'Макс страниц:',
            'limits_max_pages_hint': '(0 = без ограничений)',
            'limits_continue_error': 'Продолжать при ошибках',

            # Control Panel
            'control_start': 'Начать конвертацию',
            'control_stop': 'Остановить',
            'control_clear_log': 'Очистить журнал',
            'control_save_settings': 'Сохранить настройки',

            # Progress Panel
            'progress_current': 'Текущий файл:',
            'progress_file_count': '{current} из {total}',
            'progress_elapsed': 'Прошло:',
            'progress_remaining': 'Осталось:',
            'progress_calculating': 'Расчет...',
            'progress_idle': 'Ожидание...',

            # Stats Panel
            'stats_success': 'Успешно:',
            'stats_partial': 'Частично:',
            'stats_failed': 'Ошибок:',
            'stats_skipped': 'Пропущено:',
            'stats_total': 'Всего:',

            # Log Panel
            'log_title': 'Журнал обработки',
            'log_placeholder': 'Логи обработки будут отображаться здесь...',
            'log_clear_confirm': 'Очистить журнал?',

            # Language Switcher
            'lang_ru': 'Русский',
            'lang_en': 'English',

            # Messages
            'msg_settings_saved': 'Настройки сохранены успешно',
            'msg_settings_error': 'Ошибка сохранения настроек',
            'msg_validation_error': 'Ошибка валидации',
            'msg_no_files': 'Нет файлов для обработки',
            'msg_conversion_started': 'Конвертация запущена',
            'msg_conversion_stopped': 'Конвертация остановлена',
            'msg_conversion_completed': 'Конвертация завершена',
            'msg_conversion_error': 'Ошибка при конвертации',
            'msg_select_input_folder': 'Выберите папку с входящими документами',
            'msg_select_output_folder': 'Выберите папку для результатов',
            'msg_select_files': 'Выберите файлы для конвертации',
            'msg_api_key_required': 'Для AI описаний требуется API ключ',
            'msg_folders_not_exist': 'Папки не существуют',
            'msg_invalid_scale': 'Масштаб изображений должен быть больше 0',
            'msg_invalid_threads': 'Количество потоков должно быть >= 0',
            'msg_cuda_fallback': 'CUDA недоступен, используется CPU',

            # File types
            'file_types_all': 'Все поддерживаемые',
            'file_types_pdf': 'PDF документы',
            'file_types_word': 'Word документы',
            'file_types_powerpoint': 'PowerPoint презентации',
            'file_types_excel': 'Excel таблицы',
            'file_types_html': 'HTML файлы',
            'file_types_all_files': 'Все файлы',

            # Paths status (validate)
            'paths_status_folder_ok_files': '✓ Папка существует, найдено файлов: {count}',
            'paths_status_folder_missing': '✗ Папка не существует',
            'paths_status_folder_ok': '✓ Папка существует',
            'paths_status_folder_auto': '⚠ Папка будет создана автоматически',
            'paths_status_read_error': '⚠ Ошибка чтения: {err}',

            # Hardware
            'hw_pytorch_not_installed': 'PyTorch не установлен',

            # Controller/messages (доп.)
            'msg_conversion_in_progress': 'Конвертация уже выполняется!',
            'msg_input_dir_not_exist': 'Входная папка не существует: {path}',
            'msg_no_files_in_dir': 'В папке не найдено поддерживаемых файлов: {path}',
            'msg_select_files_please': 'Выберите файлы для конвертации',
            'msg_starting_conversion': 'Запуск конвертации {count} файлов...',
            'msg_stop_requested': 'Запрос остановки, завершение текущего файла...',
            'msg_clear_log_confirm': 'Конвертация идёт. Всё равно очистить журнал?',
            'msg_conversion_completed_body': 'Конвертация завершена!\n\nУспешно: {success}\nЧастично: {partial}\nОшибок: {failed}\nПропущено: {skipped}',
            'msg_conversion_completed_log': 'Конвертация завершена! Обработано файлов: {total} — ✓{success} ⚠{partial} ✗{failed} ⊝{skipped}',
            'msg_conversion_error_body': 'Во время конвертации произошла ошибка:\n\n{error}',
            'msg_error': 'Ошибка',
            'msg_unexpected_error': 'Произошла непредвиденная ошибка:\n\n{error}',

            # Tesseract install
            'proc_tesseract_install_btn': 'Установить Tesseract...',
            'proc_tesseract_already_installed': 'Tesseract уже установлен',
            'proc_tesseract_install_instructions': 'Tesseract не найден.\n\n1) Скачайте установщик по ссылке (откроется в браузере).\n2) Установите в папку по умолчанию: C:\\Program Files\\Tesseract-OCR\n3) Перезапустите программу.',
            'proc_tesseract_download_page': 'Страница загрузки Tesseract',

            # Tab hints (пояснения внизу вкладок)
            'hint_api': '🔑 Хотите, чтобы картинки в документах получали умные AI-описания? Вставьте сюда ключ OpenRouter — и нейросеть кратко опишет каждое изображение. Модель и лимит токенов можно менять под свой бюджет. Base URL обычно не трогаем. ✨',
            'hint_paths': '📂 Выберите, откуда брать документы: вся папка или только нужные файлы. Папка для результатов — куда складывать Markdown. Галочка «создать автоматически» избавит от ручного создания папок. 🚀',
            'hint_processing': '🔍 OCR вытащит текст из сканов и картинок. Таблицы можно распознавать точнее или быстрее. Изображения из PDF сохраняются отдельно; масштаб — на ваш вкус. Всё можно включать и выключать. 🎯',
            'hint_hardware': '⚡ Ускоритель: auto подберёт сам (CPU/GPU). CUDA — для NVIDIA, MPS — для Apple. Потоков CPU: 0 = авто. Статус покажет, видит ли программа вашу видеокарту. 🖥️',
            'hint_limits': '🛡️ Макс. размер файла и макс. страниц — чтобы не перегружать память. «Продолжать при ошибках» — если один файл упадёт, остальные всё равно обработаются. 0 = без лимита. 👍',
            'hint_about': '👋 Павел делал это для себя и пользуется каждый день. Если пригодилось — донат приветствуется: TRON (QR) или рубли. Сайт и почта — для связи. Спасибо, что пользуетесь! 💚',

            # Status messages
            'status_ready': 'Готов к работе',
            'status_processing': 'Обработка...',
            'status_stopping': 'Остановка...',
            'status_completed': 'Завершено',
            'status_error': 'Ошибка',

            # Emoji messages
            'emoji_success': 'Успешно',
            'emoji_warning': 'Предупреждение',
            'emoji_error': 'Ошибка',
            'emoji_info': 'Информация',
            'emoji_skipped': 'Пропущено',
        },

        'en': {
            # Application
            'app_title': 'Dockling WINGUI',
            'quit': 'Quit',
            'quit_confirmation': 'Conversion in progress. Are you sure you want to quit?',

            # Tabs
            'tab_api': 'API Settings',
            'tab_paths': 'Folder Paths',
            'tab_processing': 'Processing',
            'tab_hardware': 'Hardware Acceleration',
            'tab_limits': 'Limits',
            'tab_about': 'About',

            # API Tab
            'api_key_label': 'OpenRouter API Key:',
            'api_key_placeholder': 'sk-or-v1-...',
            'api_test_button': 'Test',
            'api_model_label': 'Model:',
            'api_enable_api': 'Enable OpenAI API',
            'api_enable_desc': 'Enable AI image descriptions',
            'api_prompt_label': 'Description prompt:',
            'api_prompt_default': 'Describe this image in three to five sentences. Be precise and concise.',
            'api_base_url_label': 'Base URL:',
            'api_timeout_label': 'Timeout (sec):',
            'api_max_tokens_label': 'Max tokens:',
            'api_temperature_label': 'Temperature:',

            # About Tab
            'about_title': 'About',
            'about_info': "Hi, I'm Pavel. I built this program for myself and use it every day. Please don't judge too strictly :)",
            'about_site_label': 'Website:',
            'about_email_label': 'Email:',
            'about_donation_title': 'Support the project',
            'about_donation_phrase': 'If the program was useful, I would appreciate a donation:',
            'about_wallet_label': 'TRON (TRC20) wallet:',
            'about_wallet_copy': 'Copy address',
            'about_wallet_copied': 'Address copied',
            'about_qr_crypto': 'Crypto donation',
            'about_qr_rub': 'Ruble donation',
            'about_license_title': 'Licenses',
            'about_license_docling': 'This application uses third-party components:\n— Docling (IBM). MIT License.\nThis technology provides high-quality document conversion.\nWe thank the IBM developers for creating this tool.',

            # Paths Tab
            'paths_title': 'File and folder paths',
            'paths_input_section': 'Input files',
            'paths_output_section': 'Output / Save results',
            'paths_input_label': 'Input documents:',
            'paths_output_label': 'Output documents:',
            'paths_browse_button': 'Browse...',
            'paths_mode_folder': 'Process entire folder',
            'paths_mode_files': 'Select individual files',
            'paths_select_files_button': 'Select files...',
            'paths_clear_files': 'Clear',
            'paths_selected_files': 'Selected files: {count}',
            'paths_auto_create': 'Create folder automatically if it doesn\'t exist',

            # Processing Tab
            'proc_ocr_enable': 'Enable OCR recognition',
            'proc_ocr_engine_label': 'OCR engine:',
            'proc_ocr_engine_easyocr': 'EasyOCR',
            'proc_ocr_engine_tesseract': 'Tesseract',
            'proc_ocr_languages_label': 'OCR languages:',
            'proc_ocr_languages_hint': '(comma-separated, e.g.: rus,eng)',
            'proc_table_enable': 'Table recognition',
            'proc_table_mode_label': 'Table mode:',
            'proc_table_mode_accurate': 'Accurate',
            'proc_table_mode_fast': 'Fast',
            'proc_images_enable': 'Image extraction',
            'proc_images_scale_label': 'Image scale:',
            'proc_images_scale_hint': '(1.0 = original size)',

            # Hardware Tab
            'hw_accelerator_label': 'Accelerator:',
            'hw_accelerator_auto': 'AUTO (auto-select)',
            'hw_accelerator_cpu': 'CPU',
            'hw_accelerator_cuda': 'CUDA (NVIDIA GPU)',
            'hw_accelerator_gpu': 'GPU (general)',
            'hw_accelerator_mps': 'MPS (Apple Metal)',
            'hw_cpu_threads_label': 'CPU threads:',
            'hw_cpu_threads_hint': '(0 = automatic)',
            'hw_gpu_status_label': 'GPU status:',
            'hw_gpu_detected': 'Detected: {name}',
            'hw_gpu_not_detected': 'GPU not detected',
            'hw_cuda_available': 'CUDA available',
            'hw_cuda_not_available': 'CUDA not available',

            # Limits Tab
            'limits_max_size_label': 'Max file size (MB):',
            'limits_max_size_hint': '(0 = unlimited)',
            'limits_max_pages_label': 'Max pages:',
            'limits_max_pages_hint': '(0 = unlimited)',
            'limits_continue_error': 'Continue on errors',

            # Control Panel
            'control_start': 'Start Conversion',
            'control_stop': 'Stop',
            'control_clear_log': 'Clear Log',
            'control_save_settings': 'Save Settings',

            # Progress Panel
            'progress_current': 'Current file:',
            'progress_file_count': '{current} of {total}',
            'progress_elapsed': 'Elapsed:',
            'progress_remaining': 'Remaining:',
            'progress_calculating': 'Calculating...',
            'progress_idle': 'Idle...',

            # Stats Panel
            'stats_success': 'Success:',
            'stats_partial': 'Partial:',
            'stats_failed': 'Failed:',
            'stats_skipped': 'Skipped:',
            'stats_total': 'Total:',

            # Log Panel
            'log_title': 'Processing Log',
            'log_placeholder': 'Processing logs will appear here...',
            'log_clear_confirm': 'Clear log?',

            # Language Switcher
            'lang_ru': 'Русский',
            'lang_en': 'English',

            # Messages
            'msg_settings_saved': 'Settings saved successfully',
            'msg_settings_error': 'Error saving settings',
            'msg_validation_error': 'Validation error',
            'msg_no_files': 'No files to process',
            'msg_conversion_started': 'Conversion started',
            'msg_conversion_stopped': 'Conversion stopped',
            'msg_conversion_completed': 'Conversion completed',
            'msg_conversion_error': 'Conversion error',
            'msg_select_input_folder': 'Select input documents folder',
            'msg_select_output_folder': 'Select output folder',
            'msg_select_files': 'Select files to convert',
            'msg_api_key_required': 'API key required for AI descriptions',
            'msg_folders_not_exist': 'Folders do not exist',
            'msg_invalid_scale': 'Image scale must be greater than 0',
            'msg_invalid_threads': 'Number of threads must be >= 0',
            'msg_cuda_fallback': 'CUDA unavailable, using CPU',

            # Paths status (validate)
            'paths_status_folder_ok_files': '✓ Folder exists, files found: {count}',
            'paths_status_folder_missing': '✗ Folder does not exist',
            'paths_status_folder_ok': '✓ Folder exists',
            'paths_status_folder_auto': '⚠ Folder will be created automatically',
            'paths_status_read_error': '⚠ Read error: {err}',

            # Hardware
            'hw_pytorch_not_installed': 'PyTorch not installed',

            # Controller/messages (extra)
            'msg_conversion_in_progress': 'Conversion already in progress!',
            'msg_input_dir_not_exist': 'Input directory does not exist: {path}',
            'msg_no_files_in_dir': 'No supported files found in: {path}',
            'msg_select_files_please': 'Please select files to convert',
            'msg_starting_conversion': 'Starting conversion of {count} files...',
            'msg_stop_requested': 'Stop requested, finishing current file...',
            'msg_clear_log_confirm': 'Conversion in progress. Clear log anyway?',
            'msg_conversion_completed_body': 'Conversion completed!\n\nSuccess: {success}\nPartial: {partial}\nFailed: {failed}\nSkipped: {skipped}',
            'msg_conversion_completed_log': 'Conversion completed! Processed {total} files: ✓{success} ⚠{partial} ✗{failed} ⊝{skipped}',
            'msg_conversion_error_body': 'An error occurred during conversion:\n\n{error}',
            'msg_error': 'Error',
            'msg_unexpected_error': 'An unexpected error occurred:\n\n{error}',

            # Tesseract install
            'proc_tesseract_install_btn': 'Install Tesseract...',
            'proc_tesseract_already_installed': 'Tesseract is already installed',
            'proc_tesseract_install_instructions': 'Tesseract not found.\n\n1) Download the installer from the link (opens in browser).\n2) Install to the default folder: C:\\Program Files\\Tesseract-OCR\n3) Restart the application.',
            'proc_tesseract_download_page': 'Tesseract download page',

            # File types
            'file_types_all': 'All supported',
            'file_types_pdf': 'PDF documents',
            'file_types_word': 'Word documents',
            'file_types_powerpoint': 'PowerPoint presentations',
            'file_types_excel': 'Excel spreadsheets',
            'file_types_html': 'HTML files',
            'file_types_all_files': 'All files',

            # Tab hints
            'hint_api': '🔑 Want smart AI descriptions for images in your docs? Paste your OpenRouter key here — the model will briefly describe each image. You can change the model and token limit to fit your budget. Base URL usually stays as is. ✨',
            'hint_paths': '📂 Choose where to get documents from: a whole folder or just the files you need. Output folder is where Markdown files go. The "create automatically" option saves you from creating folders by hand. 🚀',
            'hint_processing': '🔍 OCR extracts text from scans and pictures. Tables can be recognized more accurately or faster. Images from PDFs are saved separately; adjust scale to your liking. You can turn any of this on or off. 🎯',
            'hint_hardware': '⚡ Accelerator: auto picks CPU/GPU. CUDA for NVIDIA, MPS for Apple. CPU threads: 0 = automatic. Status shows whether your GPU is detected. 🖥️',
            'hint_limits': '🛡️ Max file size and max pages help avoid overloading memory. "Continue on errors" means if one file fails, the rest will still be processed. 0 = no limit. 👍',
            'hint_about': '👋 Pavel built this for himself and uses it every day. If it helps you, donations are welcome: TRON (QR) or rubles. Website and email for contact. Thanks for using it! 💚',

            # Status messages
            'status_ready': 'Ready',
            'status_processing': 'Processing...',
            'status_stopping': 'Stopping...',
            'status_completed': 'Completed',
            'status_error': 'Error',

            # Emoji messages
            'emoji_success': 'Success',
            'emoji_warning': 'Warning',
            'emoji_error': 'Error',
            'emoji_info': 'Info',
            'emoji_skipped': 'Skipped',
        }
    }

    current_language = 'ru'
    callbacks = []

    @classmethod
    def get(cls, key, **kwargs):
        """
        Get translated string for the current language

        Args:
            key: Translation key
            **kwargs: Optional formatting arguments

        Returns:
            Translated and formatted string
        """
        text = cls.translations.get(cls.current_language, {}).get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except (KeyError, ValueError):
                return text
        return text

    @classmethod
    def set_language(cls, lang):
        """
        Set current language and trigger UI update

        Args:
            lang: Language code ('ru' or 'en')
        """
        if lang in cls.translations:
            cls.current_language = lang
            # Trigger all registered callbacks to update UI
            for callback in cls.callbacks:
                try:
                    callback()
                except Exception as e:
                    print(f"Error in i18n callback: {e}")

    @classmethod
    def register_callback(cls, callback):
        """
        Register a callback to be called when language changes

        Args:
            callback: Function to call on language change
        """
        if callback not in cls.callbacks:
            cls.callbacks.append(callback)

    @classmethod
    def unregister_callback(cls, callback):
        """
        Unregister a language change callback

        Args:
            callback: Function to remove
        """
        if callback in cls.callbacks:
            cls.callbacks.remove(callback)

    @classmethod
    def get_available_languages(cls):
        """
        Get list of available language codes

        Returns:
            List of language codes
        """
        return list(cls.translations.keys())

    @classmethod
    def get_language_name(cls, lang):
        """
        Get display name for a language

        Args:
            lang: Language code

        Returns:
            Display name of the language
        """
        return cls.translations.get(lang, {}).get(f'lang_{lang}', lang.upper())


if __name__ == '__main__':
    # Test translations
    print("Testing I18n module...")

    print("\nRussian:")
    I18n.set_language('ru')
    print(f"App title: {I18n.get('app_title')}")
    print(f"Start button: {I18n.get('control_start')}")
    print(f"File count: {I18n.get('progress_file_count', current=3, total=10)}")

    print("\nEnglish:")
    I18n.set_language('en')
    print(f"App title: {I18n.get('app_title')}")
    print(f"Start button: {I18n.get('control_start')}")
    print(f"File count: {I18n.get('progress_file_count', current=3, total=10)}")

    print("\nAvailable languages:", I18n.get_available_languages())
    print("Test completed successfully!")
