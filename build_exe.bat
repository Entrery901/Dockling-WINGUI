@echo off
chcp 65001 >nul
echo ================================================
echo   Dockling WINGUI — сборка EXE
echo ================================================
echo.

cd /d "%~dp0"
cd ..
if not exist "build_exe.spec" (
    echo [Ошибка] build_exe.spec не найден в родительской папке. Запускайте из папки release.
    pause
    exit /b 1
)

python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [Инфо] Установка PyInstaller...
    pip install pyinstaller
    if errorlevel 1 ( echo [Ошибка] Не удалось установить PyInstaller & pause & exit /b 1 )
)

echo [Инфо] Очистка build и dist...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo [Инфо] Запуск PyInstaller (5–15 мин)...
echo.

pyinstaller build_exe.spec

if errorlevel 1 (
    echo. & echo [Ошибка] Сборка не удалась. & pause & exit /b 1
)

if exist "dist\DocklingGUI.exe" (
    copy /Y "dist\DocklingGUI.exe" "release\"
    echo. & echo [Готово] EXE скопирован в release\DocklingGUI.exe
) else (
    echo [Внимание] dist\DocklingGUI.exe не найден.
)

echo.
echo ================================================
pause
