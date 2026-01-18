@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ================================================
echo   Dockling WINGUI — сборка пакета для распространения
echo ================================================
echo.

cd /d "%~dp0"
cd ..

set VERSION=%date:~-4%%date:~3,2%%date:~0,2%
set PKG=releases\DocklingWINGUI_v%VERSION%

if exist "dist\DocklingGUI.exe" (set "EXE=dist\DocklingGUI.exe") else if exist "release\DocklingGUI.exe" (set "EXE=release\DocklingGUI.exe") else (
    echo [Ошибка] Не найден ни dist\DocklingGUI.exe, ни release\DocklingGUI.exe. Сначала запустите build_exe.bat
    pause
    exit /b 1
)

echo [Инфо] Пакет: %PKG%
if exist "releases" rmdir /s /q releases
mkdir "%PKG%"
mkdir "%PKG%\input"
mkdir "%PKG%\output"

copy /Y "!EXE!" "%PKG%\DocklingGUI.exe"
copy "release\env.example" "%PKG%\.env"
copy "release\README_RU.md" "%PKG%\"
copy "release\README_EN.md" "%PKG%\"
copy "release\DOCUMENTATION_RU.md" "%PKG%\"
copy "release\DOCUMENTATION_EN.md" "%PKG%\"
copy "release\START_HERE.txt" "%PKG%\"
if exist "release\Images_frames" xcopy "release\Images_frames" "%PKG%\Images_frames\" /E /I /Q
if exist "release\images" xcopy "release\images" "%PKG%\images\" /E /I /Q

echo.
echo [Готово] Содержимое:
dir /b "%PKG%"
echo.
echo Архивируйте папку: %PKG%
echo ================================================
pause
