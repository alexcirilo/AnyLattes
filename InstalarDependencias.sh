#!/bin/bash

echo "Instalando dependencias"

sudo apt update
sudo apt upgrade -y
sudo apt install python3
sudo apt install python3-pip
sudo apt install python3-venv
pip3 install Flask
python3 -m venv venv
source venv/bin/activate
pip3 install xlrd
pip3 install -r requirements.txt
pip install PyPDF2
pip install matplotlib
sudo apt install sqlite3


echo "Dependencias Instaladas"

