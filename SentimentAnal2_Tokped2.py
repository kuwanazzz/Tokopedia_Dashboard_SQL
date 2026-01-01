import pandas as pd
import ast
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


file_path = 'tokopedia_products_with_review.csv'
print(f"Memuat data {file_path}...")
df = pd.read_csv(file_path)


def parse_list(x):
    try:
        return ast.literal_eval(x) if isinstance(x, str) else []
    except:
        return []

df['message'] = df['message'].apply(parse_list)
df_exploded = df[['product_id', 'category', 'message']].explode('message').dropna(subset=['message'])


analyzer = SentimentIntensityAnalyzer()
new_words = {
    'aman': 2.0, 'cepat': 1.5, 'puas': 2.0, 'original': 2.0, 'ori': 2.0,
    'kecewa': -2.0, 'rusak': -2.5, 'palsu': -3.0, 'lama': -1.5, 'jelek': -2.0
}
analyzer.lexicon.update(new_words)

def get_vader_sentiment(text):
    score = analyzer.polarity_scores(str(text))['compound']
    if score >= 0.05:
        return 'Positive'
    elif score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'


print("Menganalisis sentimen menggunakan VADER Library...")
df_exploded['sentiment'] = df_exploded['message'].apply(get_vader_sentiment)


print("Menyimpan hasil...")
df_exploded.to_csv('tokopedia_sentiment_results.csv', index=False)
print("Selesai! Sekarang datanya jauh lebih akurat.")