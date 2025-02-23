import streamlit as st
import subprocess
import json
import time
import os
import sys


st.set_page_config(page_title="Live News Scraper", page_icon="📰", layout="wide")


st.markdown("""
    <style>
        .big-title { font-size: 32px !important; font-weight: bold; color: #E63946; text-align: center; }
        .sub-text { font-size: 16px !important; color: #555; text-align: center; }
        .article-title { font-size: 22px; font-weight: bold; color: #1D3557; }
        .article-summary { font-size: 16px; color: #333; }
        .read-more { color: #E63946; font-weight: bold; text-decoration: none; }
        .sidebar-title { font-size: 18px !important; font-weight: bold; color: #1D3557; }
        .stButton>button { background-color: #457B9D; color: white; border-radius: 10px; }
        .stButton>button:hover { background-color: #1D3557; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">Live News Scraper & Summarizer 📰</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Get the latest news with summarized content and Hindi translation!</p>', unsafe_allow_html=True)

CATEGORY_MAPPING = {
    "uttar pradesh": ["lucknow", "kanpur", "meerut", "prayagraj", "noida", "ghaziabad", "agra", "varanasi"],
    "maharashtra": ["mumbai", "pune", "navi-mumbai", "nagpur", "nashik", "aurangabad", "thane"],
    "karnataka": ["bengaluru", "mysuru", "mangaluru", "hubballi"],
    "tamil nadu": ["chennai", "coimbatore", "madurai", "trichy", "salem"],
    "west bengal": ["kolkata"],
    "andhra pradesh": ["amaravati", "vijayawada", "visakhapatnam"],
    "telangana": ["hyderabad"],
    "madhya pradesh": ["bhopal", "indore"],
    "gujarat": ["ahmedabad", "vadodara", "rajkot", "surat"],
    "rajasthan": ["jaipur", "jodhpur", "udaipur", "ajmer"],
    "punjab": ["amritsar", "ludhiana", "chandigarh"],
    "haryana": ["faridabad", "gurgaon"],
    "bihar": ["patna"],
    "assam": ["guwahati"],
    "kerala": [], "goa": [], "manipur": [], "mizoram": [], "tripura": [], "nagaland": [], "sikkim": [],
    "arunachal pradesh": [], "meghalaya": [], "chhattisgarh": [], "jharkhand": [], "uttarakhand": [],
    "odisha": [], "himachal pradesh": [], "ladakh": [], "jammu and kashmir": [], "andaman and nicobar": [],
    "chandigarh": [], "dadra and nagar haveli and daman and diu": [], "lakshadweep": [], "delhi": []
}

SPECIAL_CATEGORIES = {
    "world": ["us", "uk", "pakistan", "europe", "china", "middle-east", "rest-of-world"],
    "business": ["financial-literacy", "india-business", "international-business"],
    "sports": ["cricket", "cricket/ipl", "tennis", "badminton", "hockey", "football", "chess"],
    "entertainment": ["etimes"],
    "lifestyle": ["life-style", "life-style/health-fitness"],
    "technology": ["technology"]
}


st.sidebar.markdown('<p class="sidebar-title">Select News Category:</p>', unsafe_allow_html=True)
category = st.sidebar.text_input("Enter state, city, or topic", "")
selected_subcategory = None

if category:
    category_lower = category.lower()
    subcategories = []
    base_path = ""

    if category_lower in CATEGORY_MAPPING:
        subcategories = CATEGORY_MAPPING[category_lower]
        if subcategories:
            base_path = "city"
            selected_subcategory = st.sidebar.selectbox("Choose a subcategory:", subcategories)
        else:
            base_path = "india"
    elif category_lower in SPECIAL_CATEGORIES:
        subcategories = SPECIAL_CATEGORIES[category_lower]
        base_path = category_lower
        selected_subcategory = st.sidebar.selectbox("Choose a subcategory:", subcategories)
    elif any(category_lower in v for v in CATEGORY_MAPPING.values()):
        subcategories = [category_lower]
        base_path = "city"
        selected_subcategory = category_lower
    else:
        st.sidebar.warning("Invalid category. Try again.")
        st.stop()


if st.sidebar.button("Fetch News 📰"):
    if category and (selected_subcategory or not subcategories):
        urls = []
        if selected_subcategory:
            urls.append(f"https://timesofindia.indiatimes.com/city/{selected_subcategory}")
        elif not subcategories:
            urls.append(f"https://timesofindia.indiatimes.com/india/{category_lower}")
        
        with open("urls.json", "w", encoding="utf-8") as f:
            json.dump(urls, f, indent=4)

        with open("scraper_log.txt", "w") as log:
            result = subprocess.run([sys.executable, "scraper.py"], stdout=log, stderr=log)
        
        if result.returncode != 0:
            st.error("Error in scraper.py! Check scraper_log.txt.")
            st.stop()

        if os.path.exists("toi_articles.json"):
            with open("summarizer_log.txt", "w") as log:
                result = subprocess.run([sys.executable, "summarizer.py"], stdout=log, stderr=log)
            
            if result.returncode != 0:
                st.error("Error in summarizer.py! Check summarizer_log.txt.")
                st.stop()

            time.sleep(3)
            try:
                with open("processed_articles.json", "r", encoding="utf-8") as f:
                    articles = json.load(f)
                
                if articles:
                    for i, article in enumerate(articles, 1):
                        with st.container():
                            st.markdown(f'<p class="article-title">{i}. {article["title"]}</p>', unsafe_allow_html=True)
                            st.markdown(f'<p class="article-summary">{article["summary"]} <a href="{article["url"]}" class="read-more">[Read more]</a></p>', unsafe_allow_html=True)
                            with st.expander("Show Hindi Translation"):
                                st.write(article["translated_text"])
                            st.markdown("---")
                else:
                    st.warning("No articles found.")
            except FileNotFoundError:
                st.error("Failed to find processed data.")
    else:
        st.warning("Enter a category and select a subcategory if required.")
