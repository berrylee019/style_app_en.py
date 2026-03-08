import streamlit as st
import google.generativeai as genai
import tempfile
import os
import json
import time

# 1. Page Configuration
st.set_page_config(
    page_title="StyleScan AI | Your 10s Personal Style Report",
    page_icon="✨",
    layout="centered"
)

# 2. AI Model Setup
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
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tfile:
                tfile.write(uploaded_video.read())
                video_path = tfile.name

            try:
                # Gemini Video Upload
                sample_file = genai.upload_file(path=video_path)
                
                # Wait for video to be processed
                while sample_file.state.name == "PROCESSING":
                    time.sleep(2)
                    sample_file = genai.get_file(sample_file.name)
                
                if sample_file.state.name == "FAILED":
                    raise Exception("Video processing failed.")

                # AI Prompt
                prompt = """
                Analyze the style of the person in this video. 
                Provide the result in the following JSON format ONLY:
                {
                    "color_palette": "Name of Palette",
                    "color_desc": "Brief explanation",
                    "body_type": "Name of Body Shape",
                    "body_desc": "Brief explanation",
                    "essentials": "List 3 items",
                    "avoid": "List 3 items",
                    "accessory": "Recommendation"
                }
                """
                response = model.generate_content([prompt, sample_file])
                
                # Parse JSON
                raw_text = response.text.replace('```json', '').replace('```', '').strip()
                data = json.loads(raw_text)

                st.balloons()
                st.success("Analysis Complete!")

                # 6. Results Section
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

                # 7. Styling Tips (깔끔하게 다듬은 버전)
                with st.expander("💡 Pro Styling Tips for You"):
                    # 리스트 형태의 텍스트를 깔끔한 문장으로 변환
                    essentials = ", ".join(data['essentials']) if isinstance(data['essentials'], list) else data['essentials']
                    avoid = ", ".join(data['avoid']) if isinstance(data['avoid'], list) else data['avoid']
                    
                    st.write(f"**✅ Wardrobe Essentials:** {essentials}")
                    st.write(f"**❌ Colors to Avoid:** {avoid}")
                    st.write(f"**✨ Accessory Pick:** {data['accessory']}")

            except Exception as e:
                st.error(f"Analysis failed. Please try again. (Error: {e})")
            finally:
                if os.path.exists(video_path):
                    os.remove(video_path)

# 8. Global Cross-Promotion Banner
st.divider()
st.markdown("""
<div style="background: linear-gradient(135deg, #111827, #374151); padding: 30px; border-radius: 20px; color: white; text-align: center;">
    <h3 style="margin: 0; color: #fbbf24;">👨‍🍳 Hungry for more AI?</h3>
    <p style="margin: 10px 0 20px; opacity: 0.9;">Turn your fridge leftovers into a Masterpiece with our <b>AI Master Chef</b>.</p>
    <a href="https://chef-noir.streamlit.app" target="_blank" style="display: inline-block; background: #ffffff; color: #111827; padding: 12px 25px; border-radius: 50px; text-decoration: none; font-weight: bold; font-size: 0.9rem;">Try Chef Noir AI 🚀</a>
</div>
""", unsafe_allow_html=True)

# 9. Footer
st.markdown("<br><p style='text-align: center; color: #a0aec0; font-size: 0.8rem;'>© 2026 StyleScan Global | Powered by Quantum AI Lifestyle</p>", unsafe_allow_html=True)



