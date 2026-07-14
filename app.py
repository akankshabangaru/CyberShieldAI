import streamlit as st

# ---------------- Page Settings ----------------
st.set_page_config(
    page_title="CyberShield AI",
    page_icon="🛡",
    layout="wide"
)

# ---------------- Title ----------------
st.title("🛡 CyberShield AI")
st.subheader("Unified Phishing & Scam Detection System")

# ---------------- Sidebar ----------------
st.sidebar.title("Detection Modules")

option = st.sidebar.selectbox(
    "Choose a module",
    (
        "Scam SMS Detection",
        "Phishing Email Detection",
        "Fake Website Detection",
        "QR Code Verification"
    )
)

# ---------------- Scam SMS Detection ----------------
if option == "Scam SMS Detection":

    st.header("📱 Scam SMS Detection")

    sms = st.text_area("Enter the SMS")

    if st.button("Analyze SMS"):

        sms_lower = sms.lower()

        scam_keywords = [
            "win",
            "winner",
            "claim",
            "click",
            "verify",
            "urgent",
            "bank",
            "otp",
            "password",
            "gift",
            "free",
            "limited offer",
            "payment",
            "prize"
        ]

        found = []

        for word in scam_keywords:
            if word in sms_lower:
                found.append(word)

        score = len(found)

        if score >= 3:
            st.error("🚨 Scam SMS Detected")
            confidence = min(95, 60 + score * 8)

        elif score >= 1:
            st.warning("⚠ Suspicious SMS")
            confidence = min(80, 50 + score * 10)

        else:
            st.success("✅ Safe SMS")
            confidence = 98

        st.write("### Confidence")
        st.progress(confidence / 100)
        st.write(f"**{confidence}%**")

        st.write("### AI Explanation")

        if found:
            for item in found:
                st.write("• Suspicious keyword detected:", item)
        else:
            st.write("No suspicious keywords found.")

# ---------------- Email ----------------
elif option == "Phishing Email Detection":

    st.header("📧 Phishing Email Detection")

    email = st.text_area("Paste the Email Content")

    if st.button("Analyze Email"):

        email_lower = email.lower()

        phishing_keywords = [
            "verify",
            "account",
            "password",
            "login",
            "click",
            "urgent",
            "update",
            "bank",
            "payment",
            "invoice",
            "security alert",
            "limited time",
            "gift",
            "winner"
        ]

        found = []

        for word in phishing_keywords:
            if word in email_lower:
                found.append(word)

        score = len(found)

        if score >= 3:
            st.error("🚨 Phishing Email Detected")
            confidence = min(95, 60 + score * 8)

        elif score >= 1:
            st.warning("⚠ Suspicious Email")
            confidence = min(80, 50 + score * 10)

        else:
            st.success("✅ Safe Email")
            confidence = 98

        st.write("### Confidence")
        st.progress(confidence / 100)
        st.write(f"**{confidence}%**")

        st.write("### AI Threat Explanation")

        if found:
            for word in found:
                st.write(f"• Suspicious keyword detected: **{word}**")
        else:
            st.write("No suspicious indicators detected.")
# ---------------- Website ----------------
elif option == "Fake Website Detection":

    st.header("🌐 Fake Website Detection")

    url = st.text_input("Enter Website URL")

    if st.button("Analyze Website"):

        if url == "":
            st.warning("Please enter a website URL.")

        elif not (url.startswith("http://") or url.startswith("https://")):
            st.error("❌ Invalid URL")

        else:

            suspicious_words = [
                "login",
                "verify",
                "secure",
                "update",
                "bank",
                "paypal",
                "payment",
                "signin",
                "account"
            ]

            reasons = []
            score = 0

            if len(url) > 50:
                score += 1
                reasons.append("Very long URL")

            if "-" in url:
                score += 1
                reasons.append("Hyphen detected")

            if "@" in url:
                score += 2
                reasons.append("@ symbol detected")

            if url.count("//") > 1:
                score += 2
                reasons.append("Multiple // detected")

            for word in suspicious_words:
                if word in url.lower():
                    score += 1
                    reasons.append(f"Suspicious keyword: {word}")

            if score >= 4:
                st.error("🚨 Phishing Website")

            elif score >= 2:
                st.warning("⚠ Suspicious Website")

            else:
                st.success("✅ Safe Website")

            confidence = min(98, 60 + score * 10)

            st.write("### Confidence")

            st.progress(confidence / 100)

            st.write(f"**{confidence}%**")

            st.write("### AI Threat Explanation")

            if reasons:
                for reason in reasons:
                    st.write("•", reason)
            else:
                st.write("No suspicious indicators detected.")

# ---------------- QR ----------------
elif option == "QR Code Verification":

    st.header("📷 QR Code Verification")

    st.write("Paste the URL obtained from a QR Code.")

    qr_url = st.text_input("QR Code URL")

    if st.button("Verify QR Code"):

        if qr_url == "":
            st.warning("Please enter a QR Code URL.")

        elif not (qr_url.startswith("http://") or qr_url.startswith("https://")):
            st.error("Invalid URL")

        else:

            suspicious = [
                "login",
                "verify",
                "bank",
                "payment",
                "secure",
                "update",
                "signin",
                "otp"
            ]

            reasons = []
            score = 0

            if "-" in qr_url:
                score += 1
                reasons.append("Hyphen detected")

            if len(qr_url) > 50:
                score += 1
                reasons.append("Long URL")

            for word in suspicious:
                if word in qr_url.lower():
                    score += 1
                    reasons.append(f"Suspicious keyword: {word}")

            if score >= 4:
                st.error("🚨 Malicious QR Code")

            elif score >= 2:
                st.warning("⚠ Suspicious QR Code")

            else:
                st.success("✅ Safe QR Code")

            confidence = min(98, 60 + score * 10)

            st.write("### Confidence")

            st.progress(confidence / 100)

            st.write(f"**{confidence}%**")

            st.write("### AI Threat Explanation")

            if reasons:
                for reason in reasons:
                    st.write("•", reason)
            else:
                st.write("No suspicious indicators detected.")