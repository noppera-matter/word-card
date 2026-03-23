import streamlit as st
import pandas as pd
import os

# 페이지 설정
st.set_page_config(page_title="단어 카드 프로그램", layout="wide")

st.title("🗂️ 맞춤형 단어 카드")
st.write("엑셀 파일을 수정하고 저장하면 실시간으로 반영됩니다.")

# 데이터 로드 함수
def load_data():
    file_path = "words.xlsx"
    if os.path.exists(file_path):
        # A, B, C열을 순서대로 읽어옴
        df = pd.read_excel(file_path)
        # 컬럼명이 다를 경우를 대비해 인덱스로 접근하거나 이름을 재지정
        df.columns = ['단어', '틀린횟수', '의미']
        return df
    else:
        st.error(f"'{file_path}' 파일을 찾을 수 없습니다. 같은 폴더에 파일을 놓아주세요.")
        return None

df = load_data()

if df is not None:
    # 한 줄에 3개씩 배치
    cols = st.columns(3)
    
    for idx, row in df.iterrows():
        # 틀린 횟수만큼 별표(*) 생성 (예: 3 -> ★★★)
        try:
            error_count = int(row['틀린횟수'])
            stars = "★" * error_count if error_count > 0 else "정답률 100% ✨"
        except (ValueError, TypeError):
            stars = "데이터 오류"

        with cols[idx % 3]:
            # 카드 스타일 구현
            with st.container(border=True):
                # 카드 앞면: 단어
                st.markdown(f"### 🔤 {row['단어']}")
                
                # 카드 뒷면 (토글 방식)
                with st.expander("뒷면 확인 (의미/횟수)"):
                    st.markdown(f"**틀린 횟수:** {stars}")
                    st.divider()
                    st.markdown(f"**의미:** {row['의미']}")

# 실행 방법 안내
st.sidebar.header("사용 방법")
st.sidebar.info(
    "1. `words.xlsx` 파일을 수정하고 저장합니다.\n"
    "2. 브라우저의 새로고침(R) 버튼을 누릅니다.\n"
    "3. 수정한 내용이 즉시 반영됩니다."
)
