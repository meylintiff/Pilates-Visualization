import streamlit as st
from pymongo import MongoClient
from collections import Counter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns

# === SETUP ===
st.set_page_config(layout="centered", page_title="Visualisasi Pilates")
sns.set(style="whitegrid")

# Pengaturan font global
plt.rcParams.update({
    'font.size': 14,
    'axes.titlesize': 18,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
})

# === MONGODB CONNECTION ===
client = MongoClient(st.secrets["mongo"]["uri"])
db = client["pilates"]
poses_collection = db["poses"]
videos_collection = db["pilates_videos"]

# === HELPER STYLE ===
def set_plot_style(title):
    plt.title(title, fontsize=18, fontweight="bold", pad=20)
    plt.xlabel("", fontsize=14)
    plt.ylabel("", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

def garis_pembatas():
    st.markdown("<hr style='margin-top: 40px; margin-bottom: 40px; height: 2px; background-color: #CCC;'>", unsafe_allow_html=True)

# === VISUALISASI SCRAPING ===
def visualisasi_scraping():
    st.header("Visualisasi Data Gerakan Pilates")
    data = list(poses_collection.find())
    nama_gerakan = [d['nama_gerakan'] for d in data]
    frekuensi = Counter(nama_gerakan)

    # Bar Chart - 10 gerakan teratas
    top_gerakan_10 = frekuensi.most_common(10)
    labels_10, counts_10 = zip(*top_gerakan_10)
    colors = sns.color_palette('pastel')[0:5]
    plt.figure(figsize=(11, 8))
    sns.barplot(x=list(counts_10), y=list(labels_10), palette="Set2")
    plt.title("10 Gerakan Pilates Paling Sering Muncul", fontsize=25, weight="bold", pad=20)
    plt.xlabel("Jumlah Kemunculan", fontsize=22.5, labelpad=10)
    plt.ylabel("Gerakan", fontsize=22.5)
    plt.xticks(fontsize=17)
    plt.yticks(fontsize=17)
    st.pyplot(plt.gcf())
    plt.close()
    garis_pembatas()

    # WordCloud
    teks = " ".join(nama_gerakan)
    wordcloud = WordCloud(width=800, height=400, background_color='white', max_font_size=100).generate(teks)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title("WordCloud Gerakan Pilates", fontsize=18, fontweight="bold", pad=20)
    st.pyplot(plt.gcf())
    plt.close()
    garis_pembatas()

    # Pie Chart - 5 gerakan teratas
    top_gerakan_5 = frekuensi.most_common(5)
    labels_5, counts_5 = zip(*top_gerakan_5)
    colors = sns.color_palette('pastel')[0:5]
    plt.figure(figsize=(4, 4))
    plt.pie(counts_5, labels=labels_5, autopct='%1.1f%%', startangle=140, colors=colors, textprops={'fontsize': 8})
    plt.axis('equal')
    plt.title("Komposisi Gerakan Pilates Paling Banyak Disebut", fontsize=9.5, fontweight="bold", pad=15)
    st.pyplot(plt.gcf())
    plt.close()
    garis_pembatas()

# === VISUALISASI CRAWLING ===
def visualisasi_crawling():
    st.header("Visualisasi Data Video Pilates")
    df = pd.DataFrame(list(videos_collection.find()))
    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
    df['year'] = df['publishedAt'].dt.year
    df['month'] = df['publishedAt'].dt.month_name()

    # Bar Chart: Jumlah video per tahun
    video_per_year = df['year'].value_counts().sort_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(x=video_per_year.index, y=video_per_year.values, palette="Set2")
    set_plot_style("Jumlah Video Pilates per Tahun")
    plt.xlabel("Tahun", fontsize=16, labelpad=10)
    plt.ylabel("Jumlah Video", fontsize=16)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=13.5)
    st.pyplot(plt.gcf())
    plt.close()
    garis_pembatas()

    # Lollipop Chart: Top 10 Channel
    top_channels = df['channelTitle'].value_counts().nlargest(10)
    labels = top_channels.index.tolist()
    counts = top_channels.values.tolist()
    plt.figure(figsize=(12, 9))
    plt.hlines(y=labels, xmin=0, xmax=counts, color="#FF93C6", linewidth=4)
    plt.plot(counts, labels, "o", color="#AC4675", markersize=15) 
    plt.title("Top 10 Channel tentang Pilates", fontsize=30, fontweight="bold", pad=30)
    plt.xlabel("Jumlah Video", fontsize=24, labelpad=15)
    plt.ylabel("Nama Channel", fontsize=24)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    st.pyplot(plt.gcf())
    plt.close()
    garis_pembatas()

    # Line Chart: Distribusi video per bulan
    monthly_data = df['month'].value_counts().sort_index()
    plt.figure(figsize=(10, 6))
    line_color = '#7A9E9F'  
    plt.plot(monthly_data.index, monthly_data.values, color=line_color, linewidth=3)
    colors = ["#DCAE96", "#9B90C2", "#8EB6A2", "#7A9E9F", "#B0889B", "#D4A373", "#E3B8A0", "#A19FA6", "#C5B3B3", "#A0AFAE", "#C3B299", "#AD8B73"]
    plt.scatter(monthly_data.index, monthly_data.values, color=colors[:len(monthly_data)], s=100, zorder=5)
    plt.title('Distribusi Video Pilates per Bulan', fontsize=18, fontweight="bold", pad=20)
    plt.xlabel('Bulan', fontsize=15)
    plt.ylabel('Jumlah Video', fontsize=15)
    plt.xticks(rotation=45, fontsize=14)
    plt.yticks(fontsize=14)
    plt.grid(True)
    st.pyplot(plt.gcf())
    plt.close()
    garis_pembatas()

    # WordCloud dari judul video
    titles = df['title'].tolist()
    text = " ".join(titles)
    wordcloud = WordCloud(width=800, height=400, background_color='white', max_font_size=100).generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title("WordCloud Judul Video Pilates", fontsize=18, fontweight="bold", pad=20)
    st.pyplot(plt.gcf())
    plt.close()
    garis_pembatas()

# === HALAMAN UTAMA ===
# === CUSTOM CSS ===
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #f0f0f0;
        }
        .css-1y4p8pa {
            font-size: 22px !important;
            font-weight: bold !important;
        }
        .css-15zrgzn option {
            font-weight: bold;
        }
        .stSelectbox > div {
            border: 2px solid #888 !important;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# === SIDEBAR ===
with st.sidebar:
    st.markdown("# **Pilih Jenis Visualisasi**", unsafe_allow_html=True)
    menu = st.selectbox(label="", options=["Pilates Videos", "Poses"])

if menu == "Poses":
    visualisasi_scraping()
else:
    visualisasi_crawling()
