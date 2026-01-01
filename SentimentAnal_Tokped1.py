import pandas as pd
import ast



print("Sedang memuat data...")
df = pd.read_csv('tokopedia_products_with_review.csv')


def parse_list(x):
    try:
        return ast.literal_eval(x) if isinstance(x, str) else []
    except:
        return []

print("Parsing data review (ini mungkin agak lama karena 1jt+ data)...")
df['message'] = df['message'].apply(parse_list)
df['review_rating'] = df['review_rating'].apply(parse_list)


print("Transforming data ke format long...")
df_exploded = df[['product_id', 'category', 'message', 'review_rating']].explode(['message', 'review_rating'])


df_exploded = df_exploded.dropna(subset=['message'])

def analyze_sentiment(text):
    text = str(text).lower()
    

    pos_words = {'bagus', 'mantap', 'puas', 'cepat', 'original', 'ori', 'rapi', 'sesuai', 'recomended', 'aman'}
    neg_words = {'kecewa', 'jelek', 'rusak', 'palsu', 'lama', 'lambat', 'kurang', 'pecah', 'penipu', 'lelet'}
    
    words = text.split()
    pos_score = sum(1 for w in words if w in pos_words)
    neg_score = sum(1 for w in words if w in neg_words)
    
    if pos_score > neg_score:
        return 'Positive'
    elif neg_score > pos_score:
        return 'Negative'
    else:
        return 'Neutral'

print("Menganalisis sentimen...")
df_exploded['sentiment'] = df_exploded['message'].apply(analyze_sentiment)


print("Menyimpan hasil ke CSV...")
df_exploded.to_csv('tokopedia_sentiment_results.csv', index=False)
print("Selesai! File 'tokopedia_sentiment_results.csv' siap digunakan.")