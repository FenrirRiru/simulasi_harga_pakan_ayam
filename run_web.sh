#!/bin/bash

# 1. Pindah ke folder tempat file ini berada
cd "$(dirname "$0")"

# 2. Aktifkan Virtual Environment (Path Mac)
source venv/bin/activate

# 3. Jalankan Streamlit
echo "Starting Streamlit App..."
streamlit run streamlit_app.py