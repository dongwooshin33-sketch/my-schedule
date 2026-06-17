import streamlit as st
import gspread
import pandas as pd
from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials
import json
import os

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# 1. 인증 정보 로드 (배포 서버용 Secrets 우선)
if 'GCP_CREDENTIALS' in st.secrets:
    creds_dict = json.loads(st.secrets["GCP_CREDENTIALS"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
else:
    # 로컬 테스트용: 프로젝트 폴더에 key.json이 있어야 함
    creds = Credentials.from_service_account_file('key.json', scopes=SCOPES)

client = gspread.authorize(creds)
SPREADSHEET_ID = '15z-7zo8H8Epe6N5fT8mtg0iIQqvgkKEWgSQ8AAHS1xo'
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# 2. UI 설정
st.set_page_config(layout="wide")
st.title("📋 팀 근무 스케줄 현황판")

# 3. 데이터 및 날짜 처리
def get_schedule_dates():
    today = datetime.now()
    monday_this_week = today - timedelta(days=today.weekday())
    dates = [monday_this_week + timedelta(days=i) for i in range(5)]
    dates += [monday_this_week + timedelta(days=i) for i in range(7, 12)]
    return dates

target_days = get_schedule_dates()
dates = [f"{d.strftime('%m/%d')}({d.strftime('%a')})" for d in target_days]
names = ["서승원", "이현석", "신동우", "이준용", "박진용", "이한영", "최현지", "주자윤"]

data = sheet.get_all_records()
df = pd.DataFrame(data)
empty_df = pd.DataFrame(index=names, columns=dates)

for row in data:
    if row['날짜'] in empty_df.columns and row['이름'] in empty_df.index:
        empty_df.at[row['이름'], row['날짜']] = None if row['근무형태'] == "취소" else row['근무형태']

st.table(empty_df.fillna('-'))

# 4. 입력 폼
st.subheader("일정 등록/수정")
col1, col2, col3 = st.columns(3)
with col1: name = st.selectbox("이름", names)
with col2: date = st.selectbox("날짜", dates)
with col3: work = st.selectbox("근무", ["본사", "재택", "휴가", "취소"])

if st.button("스케줄 반영"):
    sheet.append_row([name, date, work])
    st.rerun()