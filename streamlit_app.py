import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io

# 앱 제목 설정
st.set_page_config(
    page_title="간단한 그림 그리기",
    page_icon="🎨",
)

st.title("그림 그리기")

# 세션 상태 초기화 (색상만 관리)
if "stroke_color" not in st.session_state:
    st.session_state.stroke_color = "#000000"  # 기본 펜 색상: 검정

# 캔버스 설정
drawing_mode = "freedraw"  # 기본 그리기 모드
stroke_width = 3
canvas_width = 700
canvas_height = 500

# 캔버스 및 컨트롤러 레이아웃
col1, col2 = st.columns([4, 1])

with col2:
    st.subheader("도구")
    
    # 색상 선택
    stroke_color = st.color_picker("색상 선택", st.session_state.stroke_color)
    # 선택된 색상을 세션 상태에 저장하여 유지
    st.session_state.stroke_color = stroke_color
    
    # 펜, 지우개 선택
    # 툴바의 펜/지우개 모드와 연동되도록 변경
    tool = st.radio("도구 선택", ("펜", "지우개"))
    
    # 지우개를 선택하면 stroke_color를 흰색으로 변경
    # drawing_mode를 "transform"으로 설정하여 지우개 모드를 활성화
    if tool == "지우개":
        drawing_mode = "transform" # 'transform' 모드를 사용하여 객체를 선택하고 삭제하는 방식으로 지우개처럼 활용
        stroke_color = "#FFFFFF" # 지우개 색상을 배경색과 동일하게 설정
    else:
        drawing_mode = "freedraw" # 펜 모드
        stroke_color = st.session_state.stroke_color # 펜 선택 시 저장된 색상 사용
    
    st.markdown("---")
    st.subheader("내보내기")
    
    # 내보내기 버튼은 캔버스 결과가 있을 때만 표시
    # '현재 그림 JPG로 내보내기' 버튼이 보이려면, 캔버스에 뭔가 그려져서 image_data가 생성되어야 함.


with col1:
    # 캔버스 위젯
    # display_toolbar=True를 통해 캔버스 자체의 되돌리기/다시 실행, 지우개 등을 활성화
    draw_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # 채우기 색상
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color="#FFFFFF",  # 배경색: 흰색
        height=canvas_height,
        width=canvas_width,
        drawing_mode=drawing_mode, # 동적으로 펜/지우개 모드 변경
        display_toolbar=True, # 툴바를 표시하여 Ctrl+Z/Y 및 버튼 활성화
        update_streamlit=True, # 실시간 업데이트
        # key는 고정하지 않고 한번만 설정하여 캔버스 상태 유지.
        # 매번 변경하면 캔버스 전체가 초기화되어 이전 이력이 사라짐.
        key="drawing_canvas" 
    )
    
    # JPG 내보내기 버튼은 캔버스 결과가 있을 때만 표시
    if draw_result.image_data is not None:
        # 'JPG로 내보내기' 기능 추가
        if st.button("현재 그림 JPG로 내보내기"):
            # Pillow 라이브러리를 사용하여 PNG 이미지를 JPEG로 변환
            # 주의: JPEG는 투명도를 지원하지 않으므로, 투명한 부분이 흰색으로 채워질 수 있습니다.
            img = Image.fromarray(draw_result.image_data)
            
            with io.BytesIO() as jpg_buffer:
                # JPEG로 저장 시, RGB 모드로 변환 (투명도 채널 제거)
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                img.save(jpg_buffer, format='JPEG')
                st.download_button(
                    label="JPG 다운로드",
                    data=jpg_buffer.getvalue(),
                    file_name="my_drawing.jpg",
                    mime="image/jpeg"
                )
