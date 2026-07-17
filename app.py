import re
from urllib.parse import urlparse

import streamlit as st
import cv2
import numpy as np
from PIL import Image

# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="CyberShield AI",
    page_icon="🛡",
    layout="wide"
)


# ============================================================
# Custom CSS (Light Theme)
# ============================================================

st.markdown("""
<style>

.stApp{
    background-color:#F8FAFC;
    color:#1F2937;
}

.block-container{
    padding-top:2rem;
}

.title{
    text-align:center;
    color:#1565C0;
    font-weight:bold;
}

div[data-testid="stMetric"]{
    background-color:white;
    border:1px solid #E5E7EB;
    border-radius:12px;
    padding:15px;
    box-shadow:0 2px 8px rgba(0,0,0,0.08);
}

div[data-testid="stAlert"]{
    border-radius:12px;
}

textarea, input{
    border-radius:10px !important;
}

.stButton>button{
    background-color:#1976D2;
    color:white;
    border:none;
    border-radius:10px;
    padding:10px 18px;
    font-weight:bold;
}

.stButton>button:hover{
    background-color:#0D47A1;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# Title
# ============================================================

st.markdown(
    "<h1 class='title'>🛡 CyberShield AI</h1>",
    unsafe_allow_html=True
)

st.caption("Unified Phishing & Scam Detection System")

# ============================================================
# Top Metrics
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Modules", "4")

with col2:
    st.metric("Detection", "AI-Based")

with col3:
    st.metric("Status", "Active 🟢")

st.divider()

# ============================================================
# Sidebar
# ============================================================

st.sidebar.title("🛡 CyberShield AI")

module = st.sidebar.selectbox(
    "Choose Detection Module",
    [
        "Scam SMS Detection",
        "Phishing Email Detection",
        "Fake Website Detection",
        "QR Code Verification",
        "Dashboard"
    ]
)

# ============================================================
# Keyword Lists
# ============================================================

sms_keywords = [
    "otp",
    "verify",
    "winner",
    "claim",
    "click",
    "bank",
    "gift",
    "free",
    "payment",
    "password",
    "urgent",
    "limited offer",
    "prize"
]

email_keywords = [
    "verify",
    "login",
    "password",
    "account",
    "security",
    "click",
    "update",
    "bank",
    "payment",
    "invoice",
    "winner",
    "gift",
    "claim",
    "urgent"
]

url_keywords = [
    "login",
    "verify",
    "secure",
    "update",
    "bank",
    "paypal",
    "signin",
    "payment",
    "account"
]

# ============================================================
# Helper Function
# ============================================================

def analyze_text(text, keywords):

    text = text.lower()

    reasons = []

    score = 0

    for word in keywords:

        if word in text:

            score += 1

            reasons.append(f"Suspicious keyword detected: {word}")

    return score, reasons


# ============================================================
# URL Analyzer
# ============================================================

def analyze_url(url):

    reasons = []

    score = 0

    if len(url) > 60:
        score += 1
        reasons.append("Long URL")

    if "-" in url:
        score += 1
        reasons.append("Hyphen detected")

    if "@" in url:
        score += 2
        reasons.append("@ symbol detected")

    if url.count("//") > 1:
        score += 2
        reasons.append("Multiple // detected")

    for word in url_keywords:

        if word in url.lower():

            score += 1

            reasons.append(f"Suspicious keyword: {word}")

    return score, reasons


# ============================================================
# Confidence Calculator
# ============================================================

def confidence(score):

    if score == 0:
        return 99

    elif score == 1:
        return 90

    elif score == 2:
        return 80

    elif score == 3:
        return 70

    elif score == 4:
        return 60

    elif score == 5:
        return 45

    else:
        return 30


# ============================================================
# Dashboard Variables
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []

# ============================================================
# SMS Detection
# ============================================================

if module == "Scam SMS Detection":

    st.header("📱 Scam SMS Detection")

    sms = st.text_area(
        "Enter SMS Message",
        placeholder="Paste the SMS here..."
    )

    if st.button("Analyze SMS"):

        if sms.strip() == "":

            st.warning("Please enter an SMS.")

        else:

            score, reasons = analyze_text(
                sms,
                sms_keywords
            )

            conf = confidence(score)

            if score >= 5:

                st.error("🚨 Scam SMS Detected")

            elif score >= 2:

                st.warning("⚠ Suspicious SMS")

            else:

                st.success("✅ Safe SMS")

            st.progress(conf / 100)

            st.metric(
                "Confidence Score",
                f"{conf}%"
            )

            st.write("### AI Threat Explanation")

            if reasons:

                for reason in reasons:

                    st.write("•", reason)

            else:

                st.success(
                    "No suspicious keywords detected."
                )

            st.session_state.history.append(
                {
                    "Module": "SMS",
                    "Result": "Scanned",
                    "Confidence": conf
                }
            )

# ============================================================
# Email Detection
# ============================================================

elif module == "Phishing Email Detection":

    st.header("📧 Phishing Email Detection")

    email = st.text_area(
        "Paste Email Content",
        placeholder="Paste the email here..."
    )

    if st.button("Analyze Email"):

        if email.strip() == "":

            st.warning("Please paste an email.")

        else:

            score, reasons = analyze_text(
                email,
                email_keywords
            )

            conf = confidence(score)

            if score >= 5:

                st.error("🚨 Phishing Email")

            elif score >= 2:

                st.warning("⚠ Suspicious Email")

            else:

                st.success("✅ Safe Email")

            st.progress(conf / 100)

            st.metric(
                "Confidence Score",
                f"{conf}%"
            )

            st.write("### AI Threat Explanation")

            if reasons:

                for reason in reasons:

                    st.write("•", reason)

            else:

                st.success(
                    "No suspicious indicators detected."
                )

            st.session_state.history.append(
                {
                    "Module": "Email",
                    "Result": "Scanned",
                    "Confidence": conf
                }
            )
            # ============================================================
# Website Detection
# ============================================================

elif module == "Fake Website Detection":

    st.header("🌐 Fake Website Detection")

    url = st.text_input(
        "Enter Website URL",
        placeholder="https://example.com"
    )

    if st.button("Analyze Website"):

        if url.strip() == "":

            st.warning("Please enter a URL.")

        elif not (
            url.startswith("http://")
            or url.startswith("https://")
        ):

            st.error("Please enter a valid URL starting with http:// or https://")

        else:

            score, reasons = analyze_url(url)

            conf = confidence(score)

            if score >= 5:

                st.error("🚨 Phishing Website")

            elif score >= 2:

                st.warning("⚠ Suspicious Website")

            else:

                st.success("✅ Safe Website")

            st.progress(conf / 100)

            st.metric(
                "Confidence Score",
                f"{conf}%"
            )

            st.write("### AI Threat Explanation")

            if reasons:

                for reason in reasons:

                    st.write("•", reason)

            else:

                st.success("No suspicious indicators detected.")

            st.session_state.history.append(
                {
                    "Module": "Website",
                    "Result": "Scanned",
                    "Confidence": conf
                }
            )

# ============================================================
# QR Code Verification
# ============================================================

elif module == "QR Code Verification":

    st.header("📷 QR Code Verification")

    uploaded_file = st.file_uploader(
        "Upload QR Code Image",
        type=["png", "jpg", "jpeg"]
    )

    qr_data = ""

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        st.image(image, width=250)

        image_np = np.array(image)

        detector = cv2.QRCodeDetector()

        data, points, _ = detector.detectAndDecode(image_np)

        if data:

            qr_data = data

            st.success("QR Code detected successfully!")

            st.code(qr_data)

        else:

            st.warning("QR could not be detected from image.")

    manual = st.text_input(
        "Or paste the QR URL manually"
    )

    if manual != "":

        qr_data = manual

    if st.button("Verify QR"):

        if qr_data == "":

            st.warning("Upload a QR image or paste the URL.")

        elif not (
            qr_data.startswith("http://")
            or qr_data.startswith("https://")
        ):

            st.error("Invalid URL")

        else:

            score, reasons = analyze_url(qr_data)

            conf = confidence(score)

            if score >= 5:

                st.error("🚨 Malicious QR Code")

            elif score >= 2:

                st.warning("⚠ Suspicious QR Code")

            else:

                st.success("✅ Safe QR Code")

            st.progress(conf / 100)

            st.metric(
                "Confidence Score",
                f"{conf}%"
            )

            st.write("### AI Threat Explanation")

            if reasons:

                for reason in reasons:

                    st.write("•", reason)

            else:

                st.success("No suspicious indicators detected.")

            st.session_state.history.append(
                {
                    "Module": "QR",
                    "Result": "Scanned",
                    "Confidence": conf
                }
            )
            # ============================================================
# Dashboard
# ============================================================

elif module == "Dashboard":

    st.header("📊 CyberShield AI Dashboard")

    history = st.session_state.history

    if len(history) == 0:

        st.info("No scans have been performed yet.")

    else:

        total = len(history)

        sms = sum(1 for i in history if i["Module"] == "SMS")
        email = sum(1 for i in history if i["Module"] == "Email")
        website = sum(1 for i in history if i["Module"] == "Website")
        qr = sum(1 for i in history if i["Module"] == "QR")

        avg_conf = round(
            sum(i["Confidence"] for i in history) / total,
            1
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Scans", total)

        with col2:
            st.metric("Average Confidence", f"{avg_conf}%")

        with col3:
            st.metric("Modules Used", 4)

        st.divider()

        st.subheader("📈 Module Usage")

        chart_data = {
            "SMS": sms,
            "Email": email,
            "Website": website,
            "QR": qr
        }

        st.bar_chart(chart_data)

        st.divider()

        st.subheader("📝 Scan History")

        st.dataframe(history, use_container_width=True)

        if st.button("Clear History"):

            st.session_state.history = []

            st.success("History Cleared!")

            st.rerun()

# ============================================================
# Footer
# ============================================================

st.divider()

st.markdown(
"""
<center>

### 🛡 CyberShield AI

Unified Phishing & Scam Detection System

Built using **Python • Streamlit • OpenCV**

</center>
""",
unsafe_allow_html=True
)
