import streamlit as st
import google.generativeai as genai
import tempfile
import os
import json

# 1. Page Configuration
st.set_page_config(
    page_title="StyleScan AI | Your 10s Personal Style Report",
    page_icon="✨",
    layout="centered"
)

# 2. AI Model Setup (Secrets에서 API 키 호출)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("API Key is missing or invalid. Please check your Streamlit Secrets.")

# 3. Custom CSS
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stButton>button {
        width: 100%; border-radius: 10px; height: 3em;
        background-color: #1a202c; color: white; font-weight: bold;
    }
    .report-card {
        padding: 20px; border-radius: 15px;
        background-color: #f7fafc; border: 1px solid #edf2f7;
        margin-bottom: 20px; min-height: 150px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Header Section
st.title("👗 StyleScan AI")
st.markdown("### *\"Stop guessing, start glowing.\"*")
st.write("Upload a 10-second video to get a professional style analysis.")

st.divider()

# 5. User Interaction: Video Upload
st.subheader("Step 1: Upload Your Look")
uploaded_video = st.file_uploader("Choose a video file", type=['mp4', 'mov', 'avi'])

if uploaded_video is not None:
    st.video(uploaded_video)
    
    if st.button("Generate My Style Report"):
        with st.spinner("🧠 AI is analyzing your style from the video..."):
            # 임시 파일 생성 및 영상 처리
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tfile:
                tfile.write(uploaded_video.read())
                video_path = tfile.name

            try:
                # Gemini 영상 업로드 및 분석
                sample_file = genai.upload_file(path=video_path)
                
                # AI에게 구조화된 응답을 요구하는 프롬프트
                prompt = """
                Analyze the style of the person in this video. 
                Provide the result in the following JSON format ONLY:
                {
                    "color_palette": "Name of Palette (e.g. Warm Autumn)",
                    "color_desc": "Brief explanation",
                    "body_type": "Name of Body Shape",
                    "body_desc": "Brief explanation",
                    "essentials": "List 3 items",
                    "avoid": "List 3 items",
                    "accessory": "Recommendation"
                }
                """
                response = model.generate_content([prompt, sample_file])
                
                # JSON 파싱 (AI 응답에서 데이터 추출)
                # 응답에서 JSON 부분만 추출하기 위한 처리
                raw_text = response.text.replace('```json', '').replace('```', '').strip()
                data = json.loads(raw_text)

                st.balloons()
                st.success("Analysis Complete!")

                # 6. Results Section (AI 데이터 반영)
                st.markdown("---")
                st.header("📊 Your Personal Style Report")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f'''<div class="report-card">
                        <h3>🎨 Color Palette</h3>
                        <p><strong>{data['color_palette']}</strong></p>
                        <small>{data['color_desc']}</small>
                    </div>''', unsafe_allow_html=True)

                with col2:
                    st.markdown(f'''<div class="report-card">
                        <h3>⌛ Body Type</h3>
                        <p><strong>{data['body_type']}</strong></p>
                        <small>{data['body_desc']}</small>
                    </div>''', unsafe_allow_html=True)

                # 7. AI Curation / Styling Tips
                with st.expander("💡 Pro Styling Tips for You"):
                    st.write(f"**Wardrobe Essentials:** {data['essentials']}")
                    st.write(f"**Colors to Avoid:** {data['avoid']}")
                    st.write(f"**Accessory Pick:** {data['accessory']}")

            except Exception as e:
                st.error(f"Analysis failed. Please try again. (Error: {e})")
            finally:
                if os.path.exists(video_path):
                    os.remove(video_path)

# 8. Footer & Banner (기존과 동일)
st.divider()
st.markdown("""
<div style="background: linear-gradient(135deg, #111827, #374151); padding: 30px; border-radius: 20px; color: white; text-align: center;">
    <h3 style="margin: 0; color: #fbbf24;">👨‍🍳 Hungry for more AI?</h3>
    <p style="margin: 10px 0 20px; opacity: 0.9;">Turn your fridge leftovers into a Masterpiece with our <b>AI Master Chef</b>.</p>
    <a href="https://bw-chef.streamlit.app" target="_blank" style="display: inline-block; background: #ffffff; color: #111827; padding: 12px 25px; border-radius: 50px; text-decoration: none; font-weight: bold; font-size: 0.9rem;">Try Chef Noir AI 🚀</a>
</div>
""", unsafe_allow_html=True)
