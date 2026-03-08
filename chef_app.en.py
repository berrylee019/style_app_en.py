import streamlit as st
import google.generativeai as genai
import tempfile
import os
import json
import time

# 1. Page Configuration
st.set_page_config(
    page_title="Chef Noir AI | Master Your Fridge",
    page_icon="🍳",
    layout="centered"
)

# 2. AI Model Setup
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("API Key is missing or invalid. Please check your Streamlit Secrets.")

# 3. Custom CSS (Chef Noir Style)
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: white; }
    .stButton>button {
        width: 100%; border-radius: 10px; height: 3em;
        background-color: #f59e0b; color: black; font-weight: bold;
    }
    .recipe-card {
        padding: 25px; border-radius: 15px;
        background-color: #161b22; border: 1px solid #30363d;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Header Section
st.title("🍳 Chef Noir AI")
st.markdown("### *\"Turn your leftovers into a Masterpiece.\"*")
st.write("Upload a photo or video of your fridge/ingredients to get a gourmet recipe.")

st.divider()

# 5. User Interaction: Ingredient Input (Photo/Video)
st.subheader("Step 1: Show Me Your Ingredients")
uploaded_file = st.file_uploader("Upload a photo or video of your ingredients", type=['png', 'jpg', 'jpeg', 'mp4', 'mov'])

if uploaded_file is not None:
    # Display preview based on file type
    if uploaded_file.type.startswith('video'):
        st.video(uploaded_file)
    else:
        st.image(uploaded_file)
    
    if st.button("Generate Masterpiece Recipe"):
        with st.spinner("👨‍🍳 The AI Chef is inspecting your ingredients..."):
            # Create temporary file
            suffix = '.mp4' if uploaded_file.type.startswith('video') else '.jpg'
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tfile:
                tfile.write(uploaded_file.read())
                file_path = tfile.name

            try:
                # Gemini File Upload
                sample_file = genai.upload_file(path=file_path)
                
                # Wait for file to be processed
                while sample_file.state.name == "PROCESSING":
                    time.sleep(2)
                    sample_file = genai.get_file(sample_file.name)

                # AI Prompt for Gourmet Recipe (US Measurements)
                prompt = """
                Analyze the ingredients in this image/video. 
                Create a high-end, gourmet recipe that can be made using these ingredients.
                Use US customary units (cups, oz, tbsp).
                Provide the result in the following JSON format ONLY:
                {
                    "dish_name": "Elegant Name of the Dish",
                    "difficulty": "Easy/Medium/Hard",
                    "cook_time": "Time in minutes",
                    "ingredients_list": ["item 1", "item 2"],
                    "instructions": ["step 1", "step 2"],
                    "chef_secret": "One pro tip for better flavor"
                }
                """
                response = model.generate_content([prompt, sample_file])
                
                # Parse JSON
                raw_text = response.text.replace('```json', '').replace('```', '').strip()
                data = json.loads(raw_text)

                st.balloons()
                st.success("Recipe Created! Bon Appétit.")

                # 6. Recipe Section
                st.markdown("---")
                st.header(f"🏆 {data['dish_name']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**⏱️ Time:** {data['cook_time']} mins")
                with col2:
                    st.write(f"**👨‍🍳 Difficulty:** {data['difficulty']}")

                st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
                st.subheader("🛒 Ingredients")
                for item in data['ingredients_list']:
                    st.write(f"- {item}")
                st.markdown('</div>', unsafe_allow_html=True)

                st.subheader("👨‍🍳 Instructions")
                for i, step in enumerate(data['instructions'], 1):
                    st.write(f"{i}. {step}")

                st.info(f"💡 **Chef's Secret:** {data['chef_secret']}")

            except Exception as e:
                st.error(f"Recipe generation failed. (Error: {e})")
            finally:
                if os.path.exists(file_path):
                    os.remove(file_path)

# 7. Global Cross-Promotion Banner (Back to Style AI)
st.divider()
st.markdown(f"""
<div style="background: linear-gradient(135deg, #2a4858, #1a202c); padding: 30px; border-radius: 20px; color: white; text-align: center;">
    <h3 style="margin: 0; color: #81e6d9;">👗 Need a Look for Dinner?</h3>
    <p style="margin: 10px 0 20px; opacity: 0.9;">Get a professional style analysis in 10 seconds before your meal.</p>
    <a href="https://stylescan-ai.streamlit.app" target="_blank" style="display: inline-block; background: #ffffff; color: #2a4858; padding: 12px 25px; border-radius: 50px; text-decoration: none; font-weight: bold; font-size: 0.9rem;">Try StyleScan AI →</a>
</div>
""", unsafe_allow_html=True)

# 8. Footer
st.markdown("<br><p style='text-align: center; color: #718096; font-size: 0.8rem;'>© 2026 Chef Noir Global | Powered by Quantum AI Lifestyle</p>", unsafe_allow_html=True)