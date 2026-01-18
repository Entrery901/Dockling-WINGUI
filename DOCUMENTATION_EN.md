# Dockling WINGUI — Documentation (English)

**Dockling WINGUI** is an application that **works out of the box** and converts documents (PDF, DOCX, PPTX, XLSX, HTML, etc.) to Markdown for RAG and AI use. People often lack such a ready-made solution; Dockling WINGUI provides it in one program: EXE, folder selection, conversion.

Full guide for installing, configuring, and using the converter.

---

## 1. Installation and First Run

### 1.1. Setup

1. Unpack or copy the contents of the `release` folder to a suitable location.
2. Copy `env.example` to a file named `.env` in the same folder as `DocklingGUI.exe`.
3. Edit `.env` if needed (paths, OCR, limits, etc.).
4. Create folders for input and output (default: `input` and `output`), or set your own paths in the GUI.

### 1.2. Running the EXE

- Double‑click `DocklingGUI.exe`.
- On first run, a short splash screen may appear.
- **The first run typically takes more than 2 minutes** (Docling/PyTorch init, EasyOCR model download if needed). The window may seem to hang — this is normal; wait for the interface to appear. Later runs are much faster.
- The window opens in Russian by default; use the **RU / EN** switch in the top‑right to change the language.

### 1.3. Running from Source (Developers)

```powershell
cd release
pip install -r requirements.txt
python gui_app.py
```

Ensure `images` and `.env` (copied from `env.example`) are in the same folder.

---

## 2. Interface: Tabs and Settings

### 2.1. API Settings

- **OpenRouter API Key** — for AI image descriptions. Leave blank if you do not need them.
- **Model** — model for descriptions (e.g. `x-ai/grok-4-fast` or similar via OpenRouter).
- **Max tokens** — token limit per description request.
- **Base URL** — API base URL (default: OpenRouter).
- **Enable AI image descriptions** — turn API‑based image captions on or off.
- **Description prompt** — text that defines the style of descriptions.

Settings are saved to `.env` with **«Save Settings»**.

### 2.2. Folder Paths

- **Process entire folder** — convert all supported files from the chosen folder.
- **Select individual files** — convert only the selected files.
- **Input documents** — folder with source files (or base folder when selecting files).
- **Output documents** — folder for generated `.md` files.
- **Create folder automatically** — create the output folder if it does not exist.

**«Browse...»** selects folders; **«Select files...»** selects specific files.

### 2.3. Processing

- **Enable OCR recognition** — recognize text in scans and images.
- **OCR engine**:
  - **EasyOCR** — bundled, no extra install; slower and uses more memory.
  - **Tesseract** — faster and lighter, but requires Tesseract to be installed.
- **«Install Tesseract...»** — checks for Tesseract; if missing, opens the download page and a short guide.
- **OCR languages** — comma‑separated, e.g. `rus,eng` (Tesseract) or `ru,en` (EasyOCR; conversion is handled as needed).
- **Table recognition** — on/off.
- **Table mode** — **Accurate** or **Fast**.
- **Image extraction** — whether to save images from documents.
- **Image scale** — 1.0 = no scaling, 2.0 = upscale, etc.

### 2.4. Hardware Acceleration

- **Accelerator** — AUTO, CPU, CUDA (NVIDIA), GPU, MPS (Apple).
- **CPU threads** — 0 = automatic.
- **GPU status** — shows whether a GPU is detected.

### 2.5. Limits

- **Max file size (MB)** — 0 = no limit.
- **Max pages** — 0 = no limit.
- **Continue on errors** — if one file fails, continue with the rest.

### 2.6. About

- Author info, contacts, donations (including QR codes).

---

## 3. Using the Application

### 3.1. Starting Conversion

1. Set input/output folders or files (**Folder Paths** tab).
2. Adjust OCR, tables, images, accelerator, and limits if needed.
3. Click **«Start Conversion»**.

### 3.2. Progress and Log

- **Current file** — name of the file being processed and counter.
- **Progress bar** — progress for the current file.
- **Elapsed / Remaining** — runtime and estimated time left.
- **Statistics** — Success, Partial, Failed, Skipped.
- **Log** — messages with markers (success, warning, error, etc.). **«Clear Log»** only clears the display.

### 3.3. Stopping

- **«Stop»** — request to stop; the current file is finished, then conversion stops.
- Closing the window during conversion shows a confirmation prompt.

### 3.4. Saving Settings

- **«Save Settings»** — writes current settings to `.env` next to `DocklingGUI.exe`. They are loaded on the next run.

---

## 4. OCR: EasyOCR and Tesseract

### 4.1. EasyOCR (Default)

- Bundled in the EXE; no separate installation.
- **The first run of the app takes more than 2 minutes** — including EasyOCR init and model download if needed. Wait for the window to appear.
- Uses more RAM.
- Good for low‑quality scans.

### 4.2. Tesseract

- Requires Tesseract installed (e.g. from [UB‑Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)).
- Recommended install path: `C:\Program Files\Tesseract-OCR`.
- In the GUI: **Processing** tab → select **Tesseract** → use **«Install Tesseract...»** to check, get the download link, and a short guide.
- Languages in the form `rus,eng` etc.; install the matching Tesseract language packs.

---

## 5. The .env File

Create it by copying `env.example` to `.env`. Main groups:

- **OCR:** `ENABLE_OCR`, `OCR_ENGINE`, `OCR_LANGUAGES`
- **Tables:** `ENABLE_TABLE_STRUCTURE`, `TABLE_STRUCTURE_MODE`
- **Images:** `GENERATE_PICTURE_IMAGES`, `IMAGES_SCALE`, `ENABLE_PICTURE_DESCRIPTION`, `PICTURE_DESCRIPTION_PROMPT`
- **API:** `USE_OPENAI_API`, `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL_NAME`, `OPENAI_MAX_TOKENS`, `OPENAI_TIMEOUT`, `OPENAI_TEMPERATURE`, `ENABLE_REMOTE_SERVICES`
- **Limits:** `MAX_NUM_PAGES`, `MAX_FILE_SIZE`, `CONTINUE_ON_ERROR`
- **Paths:** `INPUT_DIR`, `OUTPUT_DIR`

See `env.example` for detailed comments.

---

## 6. Supported Formats

PDF, DOCX, DOC, PPTX, PPT, XLSX, XLS, HTML, HTM, XML, MD, AsciiDoc (.asciidoc, .adoc).

---

## 7. Troubleshooting

### 7.1. EXE Does Not Start

- **The first run takes more than 2 minutes** — if the window does not appear, wait (model initialization). Do not kill the process.
- Ensure `.env` is in the same folder as `DocklingGUI.exe`.
- Check antivirus and folder exclusions.
- Run from a command prompt: `DocklingGUI.exe` — some errors may appear in the console.

### 7.2. “Input directory does not exist” / “No files”

- Check the path in the **Paths** tab and that the folder contains supported extensions.
- In “Select individual files” mode, ensure files are actually selected.

### 7.3. Conversion Errors

- Check the **Log** in the GUI and `conversion.log` in the application folder.
- Check file size and limits (max size, max pages).
- For difficult PDFs, try turning off OCR or switching the OCR engine.

### 7.4. CUDA / GPU Not Detected

- In **Hardware Acceleration**, choose **CPU** or **AUTO**.
- Verify NVIDIA drivers and that the built PyTorch supports CUDA (in the EXE this is fixed at build time).

### 7.5. Tesseract Not Found

- Install Tesseract (see 4.2 and **«Install Tesseract...»**).
- Add the Tesseract folder to PATH or set `TESSERACT_HOME` / `TESSERACT_PATH` in `.env` if supported.

### 7.6. Slow Performance / Out of Memory

- Lower `IMAGES_SCALE`, disable `GENERATE_PICTURE_IMAGES` or OCR.
- Use **Fast** instead of **Accurate** for tables.
- Process fewer files at a time or increase RAM.

---

## 8. Logs

- **GUI Log** — real‑time conversion messages.
- **conversion.log** — written next to `DocklingGUI.exe` (or `gui_app.py` when run from source) with conversion details and errors.

---

## 9. Manual EXE Build

Step‑by‑step instructions for building `DocklingGUI.exe` from source on Windows.

### 9.1. Build Requirements

- **Windows 10/11 (64‑bit)**
- **Python 3.11** (recommended; 3.9–3.12 may work depending on dependencies)
- **pip**
- **~10 GB** free space (venv, PyTorch, Docling, EasyOCR models)
- **Internet** — for installing packages and for the first EasyOCR run (if models are not bundled in the spec)

### 9.2. Environment Setup

1. Open PowerShell in the project root (or in the `release` folder with the source).

2. Create and activate a virtual environment:

   ```powershell
   python -m venv venv311
   .\venv311\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   pip install pyinstaller
   ```

4. **EasyOCR models (required to bundle in EXE):**  
   To avoid a long download on the user’s first run, include the models in the package.  
   - Option A: Run `python gui_app.py` once and wait for EasyOCR to download models into `%USERPROFILE%\.EasyOCR\model`.  
   - Option B: Copy an existing `C:\Users\<user>\.EasyOCR\model` from another machine.  
   In `build_exe.spec`, `datas_base` has a path to this folder — **replace it with yours** (e.g. `C:\Users\YourName\.EasyOCR\model`). If the path is wrong, PyInstaller will skip the files and the EXE will download EasyOCR models on first run (slow).

### 9.3. Editing `build_exe.spec`

Open `build_exe.spec` and adjust if needed:

| What | Where in spec | Your values |
|------|---------------|-------------|
| venv path (docling, docling_parse, etc.) | `datas_base` | Replace `venv311\\Lib\\site-packages\\...` with your venv path (e.g. if venv is in the project root, keep or fix the pattern). |
| EasyOCR models | `('C:\\Users\\conso\\.EasyOCR\\model', '.EasyOCR\\model')` | Use your `%USERPROFILE%\\.EasyOCR\\model` path (after EasyOCR has run at least once). |

- `docling-*.dist-info`, `docling_parse`, `docling_core`, etc. must point to your venv’s `Lib\site-packages\`.
- The `images` folder should be in the project root (or update the path).

### 9.4. Tesseract (optional)

To **bundle Tesseract in the EXE**:

- Install Tesseract before building to `C:\Program Files\Tesseract-OCR` (or set `TESSERACT_HOME` / `TESSERACT_PATH`).
- The logic in `build_exe.spec` will pick up the DLLs and `tessdata` if that folder exists.

If Tesseract is not installed, it will not be included; users can install it separately and use «Install Tesseract...» in the Processing tab to verify.

### 9.5. Running the Build

1. Clean previous build (optional):

   ```powershell
   if (Test-Path build) { Remove-Item -Recurse -Force build }
   if (Test-Path dist)  { Remove-Item -Recurse -Force dist }
   ```

2. Run PyInstaller:

   ```powershell
   pyinstaller build_exe.spec --noconfirm
   ```

   Or, if available in the project root:

   ```powershell
   .\build.bat
   ```

3. **Build time:** usually **5–15 minutes**, depending on disk and CPU.

4. Output: `dist\DocklingGUI.exe`.

### 9.6. Verification

- Copy `DocklingGUI.exe` to a test folder with `.env` (from `env.example`), and create `input` and `output`.
- Run the EXE. **The first run takes more than 2 minutes** — this is normal.
- Test converting one PDF.

### 9.7. Common Build Errors

- **`ModuleNotFoundError` or `Hidden import not found`** — `build_exe.spec` already lists main modules in `hiddenimports`; add any missing ones if needed.
- **`FileNotFoundError` for `venv311\...` or `EasyOCR\model`** — fix the paths in `datas_base` to match your machine.
- **Very large EXE (2–3 GB)** — expected: the bundle includes PyTorch, Docling, EasyOCR, and dependencies.

---

## 10. Licenses and Third-Party Components

This application uses third-party components:

— **Docling (IBM).** MIT License.  
This technology provides high-quality document conversion.  
We thank the IBM developers for creating this tool.

See [Docling](https://github.com/docling-project/docling) for details.

---

## 11. Contact and Support

- Author and support links — in the **About** tab of the application.
- Docling documentation: [docling-project.github.io/docling](https://docling-project.github.io/docling/).
