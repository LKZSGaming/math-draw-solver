import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import google.generativeai as genai
import os

# ================= CONFIG =================
st.set_page_config(layout="wide", page_title="Math Draw Solver")

genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# ================= UI =================
st.title("✍️ Vẽ bài toán để giải")

col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Vẽ tại đây 👇")

    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 0)",
        stroke_width=8,
        stroke_color="#FFFFFF",
        background_color="#000000",
        height=400,
        width=600,
        drawing_mode="freedraw",
        key="canvas",
    )

with col2:
    st.subheader("Kết quả 🤖")
    output_container = st.empty()

# ================= AI =================
def sendToAI(image):
    prompt = "Giải bài toán trong hình. Trình bày ngắn gọn, dễ hiểu. Dùng LaTeX nếu có công thức."

    try:
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Lỗi: {e}"

# ================= LOGIC =================
if st.button("🚀 Giải bài toán"):
    if canvas_result.image_data is not None:
        img = Image.fromarray((canvas_result.image_data).astype('uint8'))

        with st.spinner("Đang giải..."):
            result = sendToAI(img)
            output_container.markdown(result)
    else:
        st.warning("Bạn chưa vẽ gì!")
