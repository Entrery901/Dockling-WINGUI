
# Dockling WINGUI

<img width="2048" height="2048" alt="icon" src="https://github.com/user-attachments/assets/65a33618-e42e-4bd4-a2d6-a9b17c91d001" />

**The main goal of the project is a solution that works out of the box:** converting documents (PDF, DOCX, PPTX, XLSX, HTML, etc.) to Markdown for loading into RAG and use in AI systems.

Ready-made tools for this are hard to find: you often have to wire scripts, set up Python, OCR models, and dependencies. **Dockling WINGUI** addresses this: one EXE, choose folders, convert. Built on [Docling](https://github.com/docling-project/docling) (IBM).

---

## Quick Start

1. **Copy** `env.example` to `.env` (in the same folder as `DocklingGUI.exe`).
2. **Create** `input` and `output` folders (or set your paths in the app settings).
3. **Run** `DocklingGUI.exe`.
4. In the GUI, choose folders, adjust OCR, tables, and GPU if needed, then click **«Start Conversion»**.

> **Note:** The **first run typically takes more than 2 minutes** (model init, EasyOCR download if needed). The window may appear to hang — this is normal; wait for the interface to appear. Later runs are much faster.

Works out of the box: EXE, `.env`, folders, convert. For more details: **START_HERE.txt**, **DOCUMENTATION_EN.md**.

---

## Release Contents

| File / folder        | Description |
|----------------------|-------------|
| `DocklingGUI.exe`    | Main application, works out of the box (Windows, 64‑bit). |
| `env.example`        | Settings template. Copy to `.env` and edit. |
| `images/`            | Icons and images for the GUI. |
| `README_RU.md`       | Short description in Russian. |
| `README_EN.md`       | This file (short description in English). |
| `DOCUMENTATION_RU.md`| Full documentation in Russian. |
| `DOCUMENTATION_EN.md`| Full documentation in English. |
| `START_HERE.txt`     | Quick reference for first run. |
| `*.py`, `requirements.txt`, `build_exe.spec` | Source code and build scripts for development. |
| `Images_frames/` | Interface screenshots (settings tabs). |

---

## Interface Screenshots

Screenshots of the main application tabs (folder `Images_frames/`).

### 1. API Settings tab

![frame 1](https://github.com/user-attachments/assets/27a6cd38-2bce-4e8f-9f0c-2d7b59d12f62)


OpenRouter API setup for AI image descriptions: key, model (e.g. x-ai/grok-4-fast), max tokens, Base URL. “Enable AI image descriptions” checkbox and “Description prompt” field. Hint at the bottom. Buttons: Start Conversion, Stop, Clear Log, Save Settings; status: Current file, Elapsed, Remaining.

---

### 2. Folder Paths tab

![frame 2](https://github.com/user-attachments/assets/f67a684a-3abb-48ec-b6be-f4c30f1e4700)


Modes: “Process entire folder” or “Select individual files”. “Input documents” field and “Browse...” button; warning if the folder does not exist. “Output / Save results” with “Create folder automatically if it doesn’t exist”. Hint at the bottom. Progress line: Current file, Elapsed, Remaining.

---

### 3. Folder Paths tab (file selection)

![Frame 3](https://github.com/user-attachments/assets/f7825682-c16a-4625-b8ba-f9705527175a)


Same screen with “Select individual files”: “Select files...” and “Clear” buttons, “Selected files: 0” counter and file list. Input/output folder status and hint.

---

### 4. Hardware Acceleration tab

![frame 4](https://github.com/user-attachments/assets/fb57dacf-0f5a-4285-b378-4670bd3b84d1)


Accelerator choice (AUTO, CPU, CUDA, GPU, MPS) and CPU threads (0 = automatic). GPU status, e.g. “Detected: NVIDIA GeForce RTX 3060 Ti”. Hint on acceleration. Bottom panel with control buttons and timer.

---

### 5. Limits tab

![frame 5](https://github.com/user-attachments/assets/73234abd-bc21-4c2c-a517-cd862909c3de)


“Max file size (MB)” and “Max pages” (0 = unlimited). “Continue on errors” checkbox. Explanatory text. Buttons: Start Conversion, Stop, Clear Log, Save Settings; status: Current file, Elapsed, Remaining.

---

## System Requirements

- **OS:** Windows 10/11 (64‑bit).
- **RAM:** 4 GB minimum, 8 GB recommended.
- **Disk:** ~3 GB (including the EXE and working folders).
- **GPU:** Optional; NVIDIA with CUDA for acceleration.

---

## Supported Formats

PDF, DOCX, DOC, PPTX, PPT, XLSX, XLS, HTML, HTM, XML, MD, AsciiDoc.

---

## Interface Language

Use the **RU** / **EN** switch in the top‑right corner of the window.

---

## Tesseract (OCR)

By default **EasyOCR** is used (bundled).  
If you choose **Tesseract**:

- Click **«Install Tesseract...»** on the **«Processing»** tab — it opens the download page and a short guide.
- Or install manually: [Tesseract at UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki), to the default folder `C:\Program Files\Tesseract-OCR`.

---

## Manual EXE Build

Instructions for building the executable from source are in **DOCUMENTATION_EN.md**, section **«9. Manual EXE Build»**.

## Documentation

- **DOCUMENTATION_RU.md** — full guide in Russian (settings, OCR, tables, API, manual build, troubleshooting).
- **DOCUMENTATION_EN.md** — same in English.

---

## Licenses

This application uses third-party components:

— **Docling (IBM).** MIT License.  
This technology provides high-quality document conversion.  
We thank the IBM developers for creating this tool.

See [Docling](https://github.com/docling-project/docling) for details.
