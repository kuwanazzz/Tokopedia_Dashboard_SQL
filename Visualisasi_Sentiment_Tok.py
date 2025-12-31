import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# 1. Load Data Hasil Sentiment & Word Cloud
df_sentiment = pd.read_csv('tokopedia_sentiment_results.csv')
df_keywords = pd.read_csv('top_negative_keywords.csv')

# Set Tema Visualisasi
sns.set_theme(style="whitegrid")
fig = plt.figure(figsize=(15, 10))

# --- GRAFIK 1: Donut Chart (Total Sentiment) ---
plt.subplot(2, 2, 1)
sentiment_counts = df_sentiment['sentiment'].value_counts()
colors = ['#42B549', '#FFC107', '#FF5252'] # Hijau, Kuning, Merah
plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', 
        startangle=140, colors=colors, pctdistance=0.85, explode=(0.05, 0, 0))

# Buat lubang di tengah agar jadi Donut
centre_circle = plt.Circle((0,0), 0.70, fc='white')
fig.gca().add_artist(centre_circle)
plt.title('Overall Market Sentiment', fontsize=14, fontweight='bold')

# --- GRAFIK 2: Bar Chart (Sentiment by Category) ---
plt.subplot(2, 2, 2)
# Ambil top 5 kategori saja biar tidak penuh
top_categories = df_sentiment['category'].value_counts().nlargest(5).index
df_top_cat = df_sentiment[df_sentiment['category'].isin(top_categories)]

sns.countplot(data=df_top_cat, y='category', hue='sentiment', 
              palette={'Positive': '#42B549', 'Neutral': '#FFC107', 'Negative': '#FF5252'})
plt.title('Sentiment by Top 5 Categories', fontsize=14, fontweight='bold')
plt.legend(title='Sentiment', loc='lower right')

# --- GRAFIK 3: Word Cloud (Negative Pain Points) ---
plt.subplot(2, 1, 2)
# Mengubah dataframe keyword menjadi dictionary untuk WordCloud
word_freq = dict(zip(df_keywords['word'], df_keywords['frequency']))

wordcloud = WordCloud(width=1000, height=400, background_color='white', 
                      colormap='Reds').generate_from_frequencies(word_freq)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Top Negative Keywords (Pain Points)', fontsize=16, fontweight='bold', pad=20)

# Atur Layout agar tidak tumpang tindih
plt.tight_layout()
plt.show()


fig.savefig('tokopedia_sentiment_dashboard.png', dpi=300)
print("Dashboard berhasil disimpan sebagai 'tokopedia_sentiment_dashboard.png'")