import streamlit as st
from analysis import analyze_stock
from llm_report import generate_swot_report, save_swot_pdf
from voiceover import generate_voice_report
import matplotlib.pyplot as plt

st.set_page_config(page_title="📊 Stock Analyzer & Reporter", layout="wide")

# -------------------------------
# UI Header
# -------------------------------
st.markdown("""
<style>
.title {
    font-size: 36px;
    font-weight: bold;
    color: #f8a900;
}
.subtitle {
    font-size: 20px;
    color: #999;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>📈 Stock Market Analyzer & Reporter</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Analyze Indian stocks with technical indicators, LLM-based SWOT, and voice reports</div>", unsafe_allow_html=True)
st.markdown("---")

# -------------------------------
# Indian Stocks Dropdown + Time Range
# -------------------------------
stock_options = {
    "Reliance Industries": "RELIANCE.NS",
    "Tata Consultancy Services (TCS)": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "State Bank of India": "SBIN.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "Asian Paints": "ASIANPAINT.NS",
    "Wipro": "WIPRO.NS",
    "Hindustan Unilever": "HINDUNILVR.NS",

    "Adani Enterprises": "ADANIENT.NS",
    "Adani Green Energy": "ADANIGREEN.NS",
    "Adani Ports": "ADANIPORTS.NS",
    "Bajaj Finance": "BAJFINANCE.NS",
    "Bajaj Finserv": "BAJAJFINSV.NS",
    "Maruti Suzuki": "MARUTI.NS",
    "Mahindra & Mahindra": "M&M.NS",
    "Larsen & Toubro (L&T)": "LT.NS",
    "Tata Motors": "TATAMOTORS.NS",
    "Tech Mahindra": "TECHM.NS",
    "Nestle India": "NESTLEIND.NS",
    "NTPC": "NTPC.NS",
    "Coal India": "COALINDIA.NS",
    "JSW Steel": "JSWSTEEL.NS",
    "HCL Technologies": "HCLTECH.NS",
    "Zomato": "ZOMATO.NS",
    "Paytm (One97 Communications)": "PAYTM.NS",
    "Nykaa (FSN E-Commerce)": "NYKAA.NS",
    "Tata Power": "TATAPOWER.NS",
    "Tata Steel": "TATASTEEL.NS",
    "IndusInd Bank": "INDUSINDBK.NS",
    "Bank of Baroda": "BANKBARODA.NS",
    "Yes Bank": "YESBANK.NS",
    "IDFC First Bank": "IDFCFIRSTB.NS",
    "DMart (Avenue Supermarts)": "DMART.NS",
    "IRCTC": "IRCTC.NS",
    "LIC Housing Finance": "LICHSGFIN.NS",
    "PNB (Punjab National Bank)": "PNB.NS",
    "Vodafone Idea": "IDEA.NS",
    "SpiceJet": "SPICEJET.NS",
    "Titan Company": "TITAN.NS",
    "Britannia Industries": "BRITANNIA.NS",
    "Godrej Consumer": "GODREJCP.NS",
    "Havells India": "HAVELLS.NS",
    "SBI Life Insurance": "SBILIFE.NS",
    "Sun Pharmaceutical": "SUNPHARMA.NS",
    "Dr. Reddy's Laboratories": "DRREDDY.NS",
    "Cipla": "CIPLA.NS",
    "Divi's Laboratories": "DIVISLAB.NS",
    "Apollo Hospitals": "APOLLOHOSP.NS",
    "ICICI Prudential Life Insurance": "ICICIPRULI.NS",
    "HDFC Life Insurance": "HDFCLIFE.NS",
    "Tata Elxsi": "TATAELXSI.NS",
    "Dixon Technologies": "DIXON.NS",
    "IndiaMART InterMESH": "INDIAMART.NS",
    "MCX (Multi Commodity Exchange)": "MCX.NS",
    "PVR INOX": "PVRINOX.NS",
    "Nazara Technologies": "NAZARA.NS",
    "ABB India": "ABB.NS",
    "Bharat Electronics": "BEL.NS",
    "Bharat Petroleum Corporation Ltd (BPCL)": "BPCL.NS",
    "Indian Oil Corporation": "IOC.NS",
    "GAIL India": "GAIL.NS",
    "BEL (Bharat Electronics)": "BEL.NS",
    "Torrent Power": "TORNTPOWER.NS",
    "Container Corporation of India": "CONCOR.NS",
    "MRF": "MRF.NS",
    "Ashok Leyland": "ASHOKLEY.NS",
    "TVS Motor": "TVSMOTOR.NS",
    "Hero MotoCorp": "HEROMOTOCO.NS",
    "Bharat Forge": "BHARATFORG.NS",
    "Pidilite Industries": "PIDILITIND.NS",
    "Colgate-Palmolive": "COLPAL.NS",
    "Berger Paints": "BERGEPAINT.NS",
    "L&T Technology Services": "LTTS.NS",
    "L&T Infotech (LTI Mindtree)": "LTIM.NS",
    "Mphasis": "MPHASIS.NS",
    "Persistent Systems": "PERSISTENT.NS",
    "Coforge": "COFORGE.NS",
    "Oracle Financial Services Software": "OFSS.NS",
    "Ramco Systems": "RAMCOSYS.NS",
    "Zensar Technologies": "ZENSARTECH.NS",
    "Sonata Software": "SONATSOFTW.NS",
    "Cyient": "CYIENT.NS",
    "Birlasoft": "BSOFT.NS",
    "Happiest Minds Technologies": "HAPPSTMNDS.NS",
    "NIIT Technologies": "NIITTECH.NS",  # Now part of Coforge
    "Newgen Software": "NEWGEN.NS",
    "Intellect Design Arena": "INTELLECT.NS"
}

selected_company = st.selectbox("📌 Select a Company", options=list(stock_options.keys()))
ticker = stock_options[selected_company]

period = st.radio("📅 Select Time Period", ["1mo", "3mo", "6mo", "1y", "2y"], horizontal=True)

# -------------------------------
# Analyze Button
# -------------------------------
if st.button("🚀 Run Full Analysis"):
    with st.spinner("⏳ Fetching data and running analysis..."):
        hist, info, sentiment = analyze_stock(ticker, period)
        swot = generate_swot_report(info, sentiment)
        pdf_file = save_swot_pdf(swot)
        audio_file = generate_voice_report(swot)

    # -------------------------------
    # TABS Layout
    # -------------------------------
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Price & Indicators", "📰 Sentiment", "🧠 SWOT + PDF", "🔊 Voice Report"])

    # --- Tab 1: Price Chart
    with tab1:
        st.subheader("📈 Stock Price + Indicators")
        fig, ax = plt.subplots(3, figsize=(12, 9))
        ax[0].plot(hist['Close'], label="Close", color='blue')
        ax[0].plot(hist['MA20'], label="MA20", color='orange')
        ax[0].plot(hist['MA50'], label="MA50", color='green')
        ax[0].legend()
        ax[0].set_title("Price + Moving Averages")

        ax[1].bar(hist.index, hist['Volume'], label="Volume", color='purple')
        ax[1].legend()
        ax[1].set_title("Volume")

        ax[2].plot(hist['RSI'], label="RSI", color='red')
        ax[2].axhline(70, color='black', linestyle='--')
        ax[2].axhline(30, color='black', linestyle='--')
        ax[2].legend()
        ax[2].set_title("RSI Indicator")
        st.pyplot(fig)

    # --- Tab 2: Sentiment Summary
    with tab2:
        st.subheader("📰 Real-Time News Sentiment (Powered by Gemini Flash 🔥)")
        st.markdown(f"**{selected_company}** sentiment analysis based on live news:")
        st.markdown(sentiment)

    # --- Tab 3: SWOT Report
    with tab3:
        st.subheader("🧠 AI SWOT Analysis (EURI GPT-4.1 Nano)")
        st.code(swot, language='markdown')
        st.download_button("📥 Download SWOT PDF", data=open(pdf_file, "rb"), file_name=pdf_file)

    # --- Tab 4: Voice Report
    with tab4:
        st.subheader("🔊 Voice Report (Text-to-Speech)")
        st.audio(audio_file)

else:
    st.markdown("👈 Choose a stock and run the analysis to see results.")
