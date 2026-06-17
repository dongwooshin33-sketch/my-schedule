import streamlit as st
import gspread
import pandas as pd
from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials
import json
import os

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# 1. 인증 설정 (Secrets와 로컬 key.json 둘 다 확인)
if 'GCP_CREDENTIALS' in st.secrets:
    creds_dict = json.loads(st.secrets["GCP_CREDENTIALS"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
else:
    creds = Credentials.from_service_account_file('key.json', scopes=SCOPES)

client = gspread.authorize(creds)
SPREADSHEET_ID = '15z-7zo8H8Epe6N5fT8mtg0iIQqvgkKEWgSQ8AAHS1xo'
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# ... (이하 날짜 계산 및 표 생성 코드는 동일)