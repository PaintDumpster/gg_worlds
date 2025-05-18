@echo off
setlocal

echo ==========================
echo GG Worlds Backend Launcher (Alpha)
echo ==========================

REM Get directory where this script lives
set "BASEDIR=%~dp0"
cd /d "%BASEDIR%"

REM Check for Python
where python >nul 2>nul
if errorlevel 1 (
    echo ❌ Python is not installed or not on PATH.
    echo    Please install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b
)

REM Optional: create venv if it doesn’t exist
if not exist "venv" (
    echo 🔧 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Check for requirements.txt
if not exist "requirements.txt" (
    echo ❌ Missing requirements.txt in %BASEDIR%
    pause
    exit /b
)

REM Install dependencies
echo 📦 Installing Python packages...
pip install --upgrade pip

REM Install GPU-enabled PyTorch with CUDA 11.8
echo ⚡ Installing PyTorch with CUDA support...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

REM Then install the rest of the dependencies
pip install -r requirements.txt

REM Check for model folders
if not exist "models\sdxl-base" (
    echo ⚠️  Missing models\sdxl-base folder!
    echo     Please place the SDXL model in: %BASEDIR%models\sdxl-base
    pause
    exit /b
)

if not exist "models\lora-topogen\pytorch_lora_weights.safetensors" (
    echo ⚠️  Missing LoRA weights!
    echo     Please place them in: models\lora-topogen\pytorch_lora_weights.safetensors
    pause
    exit /b
)

REM Run the backend
echo 🚀 Starting TopoGen backend...
python topogen_api_lora_reapplied.py

pause
endlocal
