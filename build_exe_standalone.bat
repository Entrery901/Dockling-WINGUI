@echo off
chcp 65001 >nul
echo ================================================
echo   Dockling WINGUI — сборка EXE (только из release)
echo ================================================
echo.
echo ВАЖНО: build_exe.spec содержит пути к venv и .EasyOCR.
echo   — venv311: замените на путь к вашей venv с установленными
echo     requirements.txt и pyinstaller.
echo   — .EasyOCR\model: путь к моделям EasyOCR (например %%USERPROFILE%%\.EasyOCR\model).
echo   Либо сначала: python gui_app.py и дождитесь загрузки моделей.
echo.
echo Рекомендуется: если проект есть целиком — запускайте build_exe.bat.
echo.
pause

cd /d "%~dp0"

python -c "import PyInstaller" 2>nul
if errorlevel 1 ( pip install pyinstaller )

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo Запуск: pyinstaller build_exe.spec
pyinstaller build_exe.spec

if exist "dist\DocklingGUI.exe" ( echo [Готово] dist\DocklingGUI.exe ) else ( echo [Ошибка] EXE не создан. Проверьте пути в build_exe.spec. )
echo.
pause
