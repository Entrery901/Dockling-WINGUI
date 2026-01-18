# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller spec file for Dockling GUI
Builds a standalone Windows executable
"""

block_cipher = None

import os
from pathlib import Path

# Tesseract: для включения в EXE установите Tesseract до сборки в C:\Program Files\Tesseract-OCR
# (или задайте TESSERACT_HOME / TESSERACT_PATH). Иначе: после сборки пользователь может
# нажать «Установить Tesseract...» во вкладке «Обработка» и установить вручную.
tesseract_home = (
    os.environ.get("TESSERACT_HOME")
    or os.environ.get("TESSERACT_PATH")
    or r"C:\Program Files\Tesseract-OCR"
)
tesseract_home_path = Path(tesseract_home)
tesseract_binaries = []
tesseract_datas = []
if tesseract_home_path.exists():
    tesseract_binaries = [(str(p), "tesseract") for p in tesseract_home_path.glob("*.dll")]
    tessdata_dir = tesseract_home_path / "tessdata"
    if tessdata_dir.exists():
        tesseract_datas.append((str(tessdata_dir), "tesseract\\tessdata"))

# Analysis: collect all dependencies
datas_base = [
    ('.env.example', '.'),
    ('README.md', '.'),
    # Package metadata for importlib.metadata
    ('venv311\\Lib\\site-packages\\docling-2.68.0.dist-info', 'docling-2.68.0.dist-info'),
    ('venv311\\Lib\\site-packages\\docling_core-2.59.0.dist-info', 'docling_core-2.59.0.dist-info'),
    ('venv311\\Lib\\site-packages\\docling_ibm_models-3.10.3.dist-info', 'docling_ibm_models-3.10.3.dist-info'),
    ('venv311\\Lib\\site-packages\\docling_parse-4.7.3.dist-info', 'docling_parse-4.7.3.dist-info'),
    # docling_parse PDF resources (REQUIRED for PDF parsing!)
    ('venv311\\Lib\\site-packages\\docling_parse\\pdf_resources', 'docling_parse\\pdf_resources'),
    ('venv311\\Lib\\site-packages\\docling_parse\\pdf_resources_v2', 'docling_parse\\pdf_resources_v2'),
    # EasyOCR models (REQUIRED to avoid 10+ minute download on first run!)
    ('C:\\Users\\conso\\.EasyOCR\\model', '.EasyOCR\\model'),
    # UI images (icons + donation QR)
    ('images', 'images'),
]

a = Analysis(
    ['gui_app.py'],
    pathex=[],
    binaries=tesseract_binaries,
    datas=datas_base + tesseract_datas,
    hiddenimports=[
        # Docling and dependencies
        'docling',
        'docling.document_converter',
        'docling.datamodel.accelerator_options',
        'docling.datamodel.base_models',
        'docling.datamodel.pipeline_options',
        'docling.datamodel.document',
        'docling.backend.pypdfium2_backend',
        'docling.pipeline.standard_pdf_pipeline',
        'docling.backend.docling_parse_backend',
        'docling_core',
        'docling_core.types',
        'docling_core.types.doc',
        'docling_core.types.doc.document',

        # Docling models (REQUIRED for document processing!)
        'docling.models',
        'docling.models.base_model',
        'docling.models.plugins',
        'docling.models.plugins.defaults',
        'docling.models.easyocr_model',
        'docling.models.layout_model',
        'docling.models.table_structure_model',
        'docling.models.base_layout_model',
        'docling.models.base_ocr_model',
        'docling.models.base_table_model',
        'docling.models.auto_ocr_model',
        'docling.models.page_assemble_model',
        'docling.models.page_preprocessing_model',
        'docling.models.readingorder_model',

        # Docling utilities
        'docling.utils',
        'docling.utils.accelerator_utils',
        'docling.utils.model_downloader',

        # OCR
        'easyocr',
        'easyocr.recognition',
        'easyocr.detection',
        'easyocr.utils',
        'easyocr.craft',
        'easyocr.craft_utils',
        'easyocr.imgproc',
        'easyocr.config',
        'python_bidi',
        'python_bidi.algorithm',
        'tesserocr',

        # Deep learning
        'torch',
        'torchvision',
        'torch.nn',
        'torch.cuda',
        'torch.backends',
        'torch.backends.cudnn',

        # Data processing (REQUIRED by docling_core!)
        'pandas',
        'pandas.core',
        'pandas.core.arrays',
        'pandas.core.dtypes',
        'scipy',
        'scipy.sparse',
        'scipy.spatial',

        # Image processing
        'PIL',
        'PIL.Image',
        'PIL._imaging',
        'cv2',
        'numpy',
        'numpy.core',
        'skimage',
        'skimage.io',
        'skimage.transform',
        'skimage.color',
        'skimage.filters',
        'imageio',
        'imageio.core',
        'tifffile',
        'lazy_loader',

        # Utilities
        'python-dotenv',
        'dotenv',
        'requests',
        'urllib3',

        # GUI
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',

        # Standard library
        'logging',
        'logging.handlers',
        'pathlib',
        'queue',
        'threading',
        'dataclasses',
        'typing',
        'time',
        'datetime',

        # Project modules
        'i18n',
        'config_manager',
        'logger_adapter',
        'progress_tracker',
        'gui_widgets',
        'gui_controller',
        'convert_to_markdown',
        'config',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary packages to reduce size
        'matplotlib',
        'jupyter',
        'notebook',
        'IPython',
        'pytest',
        'setuptools',
        'sphinx',
        'tkinter.test',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Filter out some large unnecessary binaries
# This helps reduce the final EXE size
a.binaries = [x for x in a.binaries if not x[0].startswith('matplotlib')]
# Note: scipy and pandas are REQUIRED by docling_core - do not exclude!

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Splash screen - показывает прогресс загрузки при запуске EXE
splash = Splash(
    'splash.png',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=(190, 250),
    text_size=11,
    text_color='white',
    text_default='Loading modules...',
    minify_script=True,
    always_on_top=True,
)

exe = EXE(
    pyz,
    splash,  # Add splash screen
    splash.binaries,  # Add splash binaries
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DocklingGUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # UPX compression to reduce size
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window (GUI only)
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='icon.ico'  # Uncomment and provide icon file if available
)
