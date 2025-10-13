import streamlit as st
from datetime import datetime
from fpdf import FPDF
import pandas as pd
from backend.src.crew.agents import create_symptom_crew


def generate_pdf_bytes(title: str, username: str, df=None, table_md=None, advice_text=None) -> bytes:
    """Generate PDF and return bytes."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, title, ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", "", 11)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(0, 8, f"User: {username}", ln=True)
    pdf.cell(0, 8, f"Generated: {now_str}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Severity & Risk Assessment", ln=True)
    pdf.ln(3)

    if df is not None:
        col_w = [60, 35, 25, 65]
        headers = list(df.columns)
        pdf.set_font("Arial", "B", 10)
        for i, h in enumerate(headers):
            pdf.cell(col_w[i], 7, h[:20].ljust(18), border=1)
        pdf.ln()
        pdf.set_font("Arial", "", 10)
        for _, row in df.iterrows():
            for i, v in enumerate(row):
                text = str(v)
                if len(text) > 40:
                    text = text[:37] + "..."
                pdf.cell(col_w[i], 6, text.ljust(18), border=1)
            pdf.ln()
    elif table_md:
        pdf.set_font("Courier", size=10)
        for line in table_md.splitlines():
            pdf.multi_cell(0, 6, line)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Medical Advice", ln=True)
    pdf.ln(3)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, advice_text or "No advice provided.")
    return pdf.output(dest="S").encode("latin-1", "replace")


def main_ui():
    st.sidebar.markdown(f"""
    <div style='background-color: #e8f4fd; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
        <h4>👋 Welcome back!</h4>
        <p><strong>{st.session_state.username}</strong></p>
    </div>
    """, unsafe_allow_html=True)

    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.token = None
        st.session_state.username = None
        st.rerun()

    st.sidebar.markdown("""
    ### 💡 Tips for Better Analysis
    - Be specific about your symptoms  
    - Mention duration and severity  
    - Include any related factors  
    - Note recent changes in health  
    - Remember: This is not medical advice
    """)

    st.sidebar.markdown("""
    <div style='background-color: #ffe6e6; padding: 15px; border-radius: 10px; border-left: 5px solid #dc3545;'>
        <h4>🚨 Emergency Notice</h4>
        <p>If you're experiencing a medical emergency, please call your local emergency number immediately.</p>
    </div>
    """, unsafe_allow_html=True)

    # Header
    # st.markdown('<h1 style="text-align:center; color:#1f77b4;">🩺 AI Symptom Checker</h1>', unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h3>Describe Your Symptoms</h3>
        <p>Please provide detailed information for the most accurate analysis.</p>
    </div>
    """, unsafe_allow_html=True)

    # Yellow disclaimer box
    st.markdown("""
    <div style="background-color: #fff3cd; padding: 15px; border-radius: 10px; border-left: 5px solid #ffc107; margin-bottom: 25px;">
        <h4>⚠️ Important Disclaimer</h4>
        <p>This AI symptom checker is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment.</p>
    </div>
    """, unsafe_allow_html=True)

    # Symptom input
    st.markdown('<div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #1f77b4;">', unsafe_allow_html=True)
    user_input = st.text_area(
        "📝 Describe your symptoms",
        height=200,
        placeholder="Please describe your main symptoms, when they started, severity, patterns, and any relevant info."
    )

    analyze_clicked = st.button("🔍 Analyze Symptoms", use_container_width=True, disabled=not user_input.strip())
    st.markdown('</div>', unsafe_allow_html=True)

    if analyze_clicked and user_input:
        with st.spinner("🧠 Analyzing your symptoms..."):
            try:
                result = create_symptom_crew(user_input)
                parts = result.split("### Medical Advice") if "### Medical Advice" in result else result.split("💡 Advice:")
                table_part = parts[0].strip()
                advice_part = parts[1].strip() if len(parts) > 1 else ""

                st.markdown("---")
                st.subheader("📊 Severity & Risk Assessment")
                st.markdown(table_part)

                df = None
                if "|" in table_part:
                    lines = [
                        line.strip() for line in table_part.splitlines()
                        if "|" in line and "---" not in line and not line.startswith("| Condition")
                    ]
                    if lines:
                        data = [line.split("|")[1:-1] for line in lines]
                        df = pd.DataFrame(data, columns=["Condition", "Likelihood", "Severity", "Suggested Action"])
                        st.dataframe(df, use_container_width=True)

                st.subheader("💬 Medical Advice")
                st.markdown(advice_part or "No advice available.")

                # ✅ Generate PDF and store it in session state
                pdf_bytes = generate_pdf_bytes(
                    "Symptom Analysis Report",
                    st.session_state.username,
                    df=df,
                    table_md=table_part,
                    advice_text=advice_part,
                )
                st.session_state.pdf_bytes = pdf_bytes

                # ✅ Safe Download Button (persistent)
                st.download_button(
                    label="⬇️ Download PDF Report",
                    data=st.session_state.pdf_bytes,
                    file_name=f"symptom_report_{st.session_state.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                )

                # Recommended Next Steps (restored UI)
                st.markdown("---")
                st.subheader("🎯 Recommended Next Steps")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.info("📋 **Monitor Symptoms**\n\nKeep track of any changes.")
                with col2:
                    st.info("💊 **Self-Care**\n\nGet rest and stay hydrated.")
                with col3:
                    st.info("🏥 **Professional Care**\n\nConsult a doctor if symptoms persist.")

                st.success("✅ Analysis completed successfully!")

            except Exception as e:
                st.error(f"❌ Error during analysis: {e}")

    elif analyze_clicked and not user_input.strip():
        st.warning("⚠️ Please describe your symptoms before analyzing.")

    # Footer
    # st.markdown("---")
    # st.markdown("""
    # <div style='text-align: center; color: #6c757d;'>
    #     🩺 AI Symptom Checker | For informational purposes only | Always consult healthcare professionals.
    # </div>
    # """, unsafe_allow_html=True)
