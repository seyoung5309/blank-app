import streamlit as st
import datetime
import random
import string

# --- Configuration (설정) ---
# 각 색깔에 대한 운세 문구 리스트
FORTUNES = {
    "빨강": [
        "오늘은 열정과 에너지가 넘치는 하루입니다. 당신의 용감한 결정이 큰 성공을 가져올 것입니다.",
        "사랑과 행운이 당신을 따릅니다. 새로운 시작에 좋은 기운이 가득합니다.",
        "과감한 시도가 필요한 날입니다. 당신의 열정이 주변을 밝게 비출 것입니다."
    ],
    "주황": [
        "창의적인 아이디어가 샘솟는 하루입니다. 당신의 긍정적인 에너지가 주변에 좋은 영향을 줄 것입니다.",
        "즐거움과 행복이 가득한 날입니다. 새로운 만남이나 기회가 찾아올 수 있습니다.",
        "활기찬 하루가 예상됩니다. 당신의 아이디어가 빛을 발할 것입니다."
    ],
    "노랑": [
        "행복과 기쁨이 가득한 하루입니다. 긍정적인 마음으로 하루를 보내세요.",
        "지혜와 깨달음을 얻는 날입니다. 새로운 지식을 습득하기에 좋습니다.",
        "명랑하고 밝은 기운이 넘칩니다. 작은 행운들이 당신을 기다립니다."
    ],
    "초록": [
        "평온함과 안정감을 느끼는 하루입니다. 자연과 함께 휴식을 취해보세요.",
        "성장과 치유의 기운이 따릅니다. 건강과 재정 운이 좋습니다.",
        "마음의 평화가 찾아오는 날입니다. 복잡한 문제를 해결하기에 좋습니다."
    ],
    "하늘": [
        "마음이 맑아지는 하루입니다. 새로운 영감을 얻고, 자유로움을 느껴보세요.",
        "소통과 이해가 중요한 날입니다. 솔직한 대화가 관계를 돈독하게 합니다.",
        "희망과 가능성이 보이는 하루입니다. 긍정적인 변화를 기대해 보세요."
    ],
    "파랑": [
        "깊은 생각과 통찰력을 얻는 하루입니다. 침착하게 문제를 해결할 수 있습니다.",
        "신뢰와 믿음이 중요합니다. 주변 사람들과의 관계를 소중히 여기세요.",
        "평화롭고 안정적인 기운이 가득합니다. 중요한 결정을 내리기에 좋습니다."
    ],
    "보라": [
        "영적인 성숙과 통찰력을 얻는 하루입니다. 내면의 목소리에 귀 기울여 보세요.",
        "신비로운 행운이 따릅니다. 예술적인 영감이 풍부해질 것입니다.",
        "직관이 발달하는 날입니다. 중요한 선택을 앞두고 있다면 자신의 감을 믿으세요."
    ],
    "검정": [
        "강력한 에너지와 보호의 기운이 따릅니다. 내면의 힘을 기르는 데 집중하세요.",
        "새로운 시작을 위한 정리의 시간입니다. 불필요한 것을 정리하기에 좋습니다.",
        "자신을 돌아보고 재충전하는 하루입니다. 차분하게 미래를 계획해 보세요."
    ],
    "흰색": [
        "순수함과 새로운 시작의 기운이 가득합니다. 모든 것이 긍정적으로 변화할 것입니다.",
        "깨끗하고 명료한 사고가 가능한 하루입니다. 새로운 아이디어를 정리하기 좋습니다.",
        "평화와 조화가 중요한 날입니다. 주변과 긍정적인 관계를 유지해 보세요."
    ]
}

# 앱에서 사용할 색깔 리스트
COLORS = ["빨강", "주황", "노랑", "초록", "하늘", "파랑", "보라", "검정", "흰색"]
# 각 색깔에 대한 HTML HEX 코드 (텍스트 색상 지정에 사용)
COLOR_HEX = {
    "빨강": "#FF0000", "주황": "#FFA500", "노랑": "#FFFF00", "초록": "#008000",
    "하늘": "#87CEEB", "파랑": "#0000FF", "보라": "#800080", "검정": "#000000",
    "흰색": "#FFFFFF"
}

# --- Session State 초기화 (앱 상태를 유지하기 위함) ---
# 'current_page'는 앱이 어떤 페이지를 보여줄지 결정합니다.
# 초기 값은 'key_input'(키 입력 페이지)으로 설정됩니다.
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'key_input' 
# 'user_key'는 사용자가 입력한 키를 저장합니다. 키 없이 시작하면 None입니다.
if 'user_key' not in st.session_state:
    st.session_state.user_key = None
# 'selected_color_data'는 각 사용자 키별로 날짜별 선택 색상을 저장하는 딕셔너리입니다.
# 예: {'ABC123': {'2023-10-26': '빨강'}}
if 'selected_color_data' not in st.session_state:
    st.session_state.selected_color_data = {} 
# 'daily_fortunes'는 오늘 날짜에 대한 각 색깔별 운세 문구를 저장하는 딕셔너리입니다.
# 매일 새로운 운세가 생성되지만, 당일 동안은 같은 운세가 유지됩니다.
# 예: {'2023-10-26': {'빨강': '오늘의 운세 문구'}}
if 'daily_fortunes' not in st.session_state:
    st.session_state.daily_fortunes = {}

# --- Helper Functions (도움 함수) ---
def generate_fortune_for_today(color):
    """
    오늘의 운세를 생성하거나 이미 생성된 운세를 가져옵니다.
    매일 새로운 운세가 나오지만, 하루 동안은 같은 운세가 유지됩니다.
    """
    today_str = datetime.date.today().isoformat() # 오늘 날짜를 'YYYY-MM-DD' 형식의 문자열로 가져옵니다.
    
    if today_str not in st.session_state.daily_fortunes:
        # 오늘 날짜에 대한 운세 데이터가 없으면 새로 초기화합니다.
        st.session_state.daily_fortunes[today_str] = {}
    
    if color not in st.session_state.daily_fortunes[today_str]:
        # 특정 색깔에 대한 오늘의 운세가 없으면, FORTUNES 리스트에서 무작위로 하나를 선택하여 저장합니다.
        st.session_state.daily_fortunes[today_str][color] = random.choice(FORTUNES[color])
    
    return st.session_state.daily_fortunes[today_str][color] # 저장된 운세 문구를 반환합니다.

def set_page(page_name):
    """
    앱의 현재 페이지를 전환하고, 변경사항을 즉시 반영하기 위해 앱을 다시 실행합니다.
    """
    st.session_state.current_page = page_name
    st.experimental_rerun() # Streamlit 앱을 강제로 다시 실행하여 페이지 전환을 즉시 적용합니다.

def save_selected_color(user_key, color):
    """
    사용자 키와 함께 선택한 색상을 오늘 날짜와 매핑하여 저장합니다.
    """
    if user_key not in st.session_state.selected_color_data:
        # 해당 사용자 키에 대한 데이터 공간이 없으면 새로 생성합니다.
        st.session_state.selected_color_data[user_key] = {}
    
    today_str = datetime.date.today().isoformat() # 오늘 날짜를 'YYYY-MM-DD' 형식의 문자열로 가져옵니다.
    st.session_state.selected_color_data[user_key][today_str] = color # 오늘 날짜에 선택한 색상을 저장합니다.

# --- Pages (각 화면을 구성하는 함수) ---

def key_input_page():
    """앱 시작 시 사용자 키를 입력받는 화면입니다."""
    st.title("🔢 색깔을 통해 알아보는 오늘의 운세")
    st.subheader("환영합니다!")
    st.write("계속하려면 6자리 키를 입력하거나, 건너뛰고 바로 시작할 수 있습니다.")

    # 사용자로부터 6자리 영문/숫자 키를 입력받습니다. 입력값은 대문자로 변환됩니다.
    user_input_key = st.text_input("6자리 영문/숫자 키를 입력하세요 (예: ABC123):", max_chars=6).upper()
    
    col1, col2 = st.columns(2) # 버튼을 가로로 나열하기 위해 2개의 열을 생성합니다.

    with col1:
        # '내 키로 접속하기' 버튼
        if st.button("내 키로 접속하기"):
            # 입력된 키가 6자리 영문과 숫자로만 이루어져 있는지 확인합니다.
            if len(user_input_key) == 6 and user_input_key.isalnum():
                st.session_state.user_key = user_input_key # 유효한 키면 세션에 저장합니다.
                set_page('main') # 메인 페이지로 이동합니다.
                st.success(f"'{st.session_state.user_key}' 키로 접속했습니다.") # 성공 메시지를 표시합니다.
            else:
                st.error("키는 6자리 영문과 숫자의 조합이어야 합니다.") # 오류 메시지를 표시합니다.
    with col2:
        # '키 없이 시작하기' 버튼
        if st.button("키 없이 시작하기"):
            st.session_state.user_key = None # 키 없이 시작 (None으로 설정)합니다.
            set_page('main') # 메인 페이지로 이동합니다.
            st.info("키 없이 시작합니다. 운세 기록은 저장되지 않습니다.") # 정보 메시지를 표시합니다.

def main_page():
    """주요 색상 선택 및 운세 기록을 보여주는 메인 화면입니다."""
    st.title("🔢 색깔을 통해 알아보는 오늘의 운세")
    st.markdown("# 오늘의 운세 알아보기")
    st.markdown("## 당신의 기분은 어떤 색인가요?")

    # 각 색상에 대한 버튼 역할을 하는 마크다운 링크를 생성합니다.
    # HTML과 CSS를 사용하여 원 모양과 색상을 적용합니다.
    st.markdown("""
        <style>
            .color-box {
                width: 90px;
                height: 90px;
                border-radius: 15px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                cursor: pointer;
                text-decoration: none;
                color: black !important;
                margin: 5px;
                padding: 10px;
                transition: transform 0.2s;
                border: 1px solid #ddd;
            }
            .color-box:hover {
                transform: scale(1.05);
            }
            .color-box-content {
                text-align: center;
            }
            .circle {
                width: 50px;
                height: 50px;
                border-radius: 50%;
                margin-bottom: 5px;
            }
        </style>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    
    for i, color in enumerate(COLORS):
        with cols[i % 3]:
            # 색상별 CSS 클래스 추가
            bg_color = COLOR_HEX[color]
            text_color = "black" if color == "흰색" or color == "노랑" else "white"

            # <a> 태그를 사용하여 클릭 가능한 링크로 만들고, 쿼리 매개변수를 추가합니다.
            st.markdown(
                f"""
                <a href="?selected_color={color}" style="text-decoration: none;">
                    <div class="color-box" style="background-color: {bg_color}; color: {text_color};">
                        <div class="color-box-content">
                            <b>{color}</b>
                        </div>
                    </div>
                </a>
                """,
                unsafe_allow_html=True
            )

    # 쿼리 매개변수를 확인하여 페이지 이동 처리
    query_params = st.query_params
    if "selected_color" in query_params:
        selected_color = query_params["selected_color"]
        if selected_color in COLORS:
            st.session_state.selected_color = selected_color
            if st.session_state.user_key:
                save_selected_color(st.session_state.user_key, selected_color)
            set_page('fortune')
            # 쿼리 매개변수 제거 (중복 실행 방지)
            del st.query_params["selected_color"]
            st.experimental_rerun()

    st.write("---")

    # 기존의 키 입력 및 기록 표시 로직은 그대로 유지됩니다.
    if st.session_state.user_key:
        st.subheader(f"'{st.session_state.user_key}'님의 운세 기록")
        user_data_for_key = st.session_state.selected_color_data.get(st.session_state.user_key, {})
        
        if user_data_for_key:
            st.write("최근 30일간 선택한 색상:")
            today = datetime.date.today()
            parsed_dates_info = []
            for date_str in user_data_for_key.keys():
                try:
                    parsed_date = datetime.date.fromisoformat(date_str)
                    parsed_dates_info.append((parsed_date, date_str))
                except ValueError:
                    pass
            recent_dates_info = sorted(
                [(d_obj, d_str) for d_obj, d_str in parsed_dates_info if (today - d_obj).days <= 30],
                key=lambda x: x[0], reverse=True
            )
            for date_obj, date_str in recent_dates_info:
                color = user_data_for_key[date_str]
                st.markdown(f"- **{date_str}**: <span style='color: {COLOR_HEX[color]}; font-weight: bold;'>{color}</span>", unsafe_allow_html=True)
        else:
            st.info("아직 저장된 운세 기록이 없습니다.")
    
def fortune_page():
    """선택된 색깔에 따른 오늘의 운세를 보여주는 화면입니다."""
    st.title("✨ 오늘의 운세")
    
    # 세션에서 선택된 색깔을 가져옵니다.
    selected_color = st.session_state.get('selected_color')
    
    if selected_color:
        # 선택된 색깔을 강조하여 표시합니다.
        st.markdown(f"## 당신이 선택한 색깔: <span style='color: {COLOR_HEX[selected_color]}; font-weight: bold;'>{selected_color}</span>", unsafe_allow_html=True)
        
        # 오늘의 운세 문구를 가져와 표시합니다.
        fortune_text = generate_fortune_for_today(selected_color)
        st.write(f"### 🍀 오늘의 운세:")
        st.success(fortune_text) # 운세 문구를 성공 메시지 박스 형태로 표시합니다.
    else:
        st.warning("선택된 색깔이 없습니다. 메인 화면으로 돌아가세요.") # 선택된 색깔이 없을 때 경고 메시지를 표시합니다.
    
    st.write("---") # 구분선 추가
    # '메인 화면으로' 돌아가는 버튼
    if st.button("메인 화면으로", key="back_to_main_from_fortune_page"):
        set_page('main') # 메인 페이지로 이동합니다.

# --- 앱 실행 흐름 제어 ---
# 세션 상태에 따라 적절한 페이지 함수를 호출하여 앱을 렌더링합니다.
if st.session_state.current_page == 'key_input':
    key_input_page()
elif st.session_state.current_page == 'main':
    main_page()
elif st.session_state.current_page == 'fortune':
    fortune_page()

# Streamlit의 기본 테마는 흰색 배경과 검정 텍스트를 사용하므로,
# 별도의 CSS 스타일링은 대부분의 경우 필요하지 않습니다.
# 앱의 전체적인 인터페이스는 Streamlit의 기본 디자인 가이드라인을 따릅니다.
