@echo off
RD>nul 2>nul /S /Q .\build .\dist .\qxtoolkit.egg-info
call python setup.py bdist_wheel
if %errorlevel% neq 0 (echo [31mFailed to build qxtoolkit[0m&&goto end)
for /r .\dist\ %%i in (qxtoolkit*.whl) do call pip install -U %%i
if %errorlevel% neq 0 (echo [31mFailed to install qxtoolkit[0m&&goto end)
RD>nul 2>nul /S /Q .\build .\dist .\qxtoolkit.egg-info
echo.
echo [32mSuccessfully installed qxtoolkit[0m"
:end