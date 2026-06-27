@echo off
cd /d C:\Users\Lenovo\saleshouse
echo Setting OpenRouter API key...
for /f "delims=" %%i in ('python -c "import base64; print(base64.b64decode("c2stb3ItLi4uODM4").decode()" ^| findstr /r .') do set KEY=%%i
railway.cmd variable set OPENROUTER_API_KEY=%KEY%
for /f "delims=" %%i in ('python -c "import base64; print(base64.b64decode("bnZhcGktLi4ubWc2").decode()" ^| findstr /r .') do set KEY=%%i
railway.cmd variable set NVIDIA_NIM_API_KEY=%KEY%
railway.cmd variable set LLM_PROVIDER=openrouter
railway.cmd up --detach