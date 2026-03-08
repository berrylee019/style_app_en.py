import streamlit as st
import time

# 1. Page Configuration (SEO & Tab Info)
st.set_page_config(
    page_title="StyleScan AI | Your 10s Personal Style Report",
    page_icon="✨",
    layout="centered"
)

# 2. Custom CSS for Global Aesthetic
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #1a202c;
        color: white;
        font-weight: bold;
    }
    .report-card {
        padding: 20px;
        border-radius: 15px;
        background-color: #f7fafc;
        border: 1px solid #edf2f7;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header Section
st.title("👗 StyleScan AI")
st.markdown("### *\"Stop guessing, start glowing.\"*")
st.write("Upload a 10-second video of yourself to get a professional style analysis powered by AI.")

st.divider()

# 4. User Interaction: Video Upload
st.subheader("Step 1: Upload Your Look")
uploaded_video = st.file_uploader("Choose a video file (MP4, MOV, AVI)", type=['mp4', 'mov', 'avi'])

if uploaded_video is not None:
    st.video(uploaded_video)
    
    # 5. Analysis Trigger
    if st.button("Generate My Style Report"):
        with st.spinner("🧠 AI is analyzing your body silhouette and skin undertones..."):
            # Simulation of AI Analysis Time
            time.sleep(3) 
            
            st.balloons()
            st.success("Analysis Complete! Here is your Personal Style Report.")

            # 6. Results Section (The Report)
            st.markdown("---")
            st.header("📊 Your Personal Style Report")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="report-card">', unsafe_allow_html=True)
                st.subheader("🎨 Color Palette")
                st.write("**Cool Winter**")
                st.caption("Deep, saturated colors like navy, emerald, and charcoal suit you best.")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="report-card">', unsafe_allow_html=True)
                st.subheader("⌛ Body Type")
                st.write("**Inverted Triangle**")
                st.caption("Structured bottoms and soft-shouldered tops will balance your silhouette.")
                st.markdown('</div>', unsafe_allow_html=True)

            # 7. AI Curation / Styling Tips
            with st.expander("💡 Pro Styling Tips for You"):
                st.write("""
                * **Wardrobe Essentials:** Navy Blazers, A-line Skirts, Deep V-neck Tops.
                * **Colors to Avoid:** Bright Orange, Mustard Yellow, Pastel Pink.
                * **Accessory Pick:** Silver or White Gold jewelry will enhance your skin tone better than yellow gold.
                """)

# 8. Global Cross-Promotion Banner (Chef AI)
st.divider()
st.markdown("""
<div style="background: linear-gradient(135deg, #111827, #374151); padding: 30px; border-radius: 20px; color: white; text-align: center;">
    <h3 style="margin: 0; color: #fbbf24;">👨‍🍳 Hungry for more AI?</h3>
    <p style="margin: 10px 0 20px; opacity: 0.9;">Turn your fridge leftovers into a Masterpiece with our <b>AI Master Chef</b>.</p>
    <a href="https://bw-chef.streamlit.app" target="_blank" style="display: inline-block; background: #ffffff; color: #111827; padding: 12px 25px; border-radius: 50px; text-decoration: none; font-weight: bold; font-size: 0.9rem;">Try Chef Noir AI 🚀</a>
</div>
""", unsafe_allow_html=True)

# 9. Footer
st.markdown("<br><p style='text-align: center; color: #a0aec0; font-size: 0.8rem;'>© 2026 StyleScan Global | Powered by Quantum AI Lifestyle</p>", unsafe_allow_html=True)