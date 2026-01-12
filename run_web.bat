@echo off
cd /d "%~dp0"

echo [1/2] Mengaktifkan Virtual Environment...
:: Perintah ini wajib ada untuk masuk ke venv
call venv\Scripts\activate

echo [2/2] Menjalankan Aplikasi Streamlit...
echo.
echo Tekan Ctrl+C untuk menutup aplikasi.
echo.

:: Menjalankan aplikasi
streamlit run streamlit_app.py

:: Agar jendela tidak langsung tertutup jika ada error
pause