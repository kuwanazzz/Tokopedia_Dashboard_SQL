import pandas as pd
import ast

# 1. Load Data
# Pastikan file 'tokopedia_products_with_review.csv' ada di folder yang sama
print("Sedang memuat data...")
df = pd.read_csv('tokopedia_products_with_review.csv')

# 2. Parsing Kolom List
# Karena di CSV kolom 'message' dan 'review_rating' terbaca sebagai string "[...]", 
# kita ubah balik jadi list Python beneran.
def parse_list(x):
    try:
        return ast.literal_eval(x) if isinstance(x, str) else []
    except:
        return []

print("Parsing data review (ini mungkin agak lama karena 1jt+ data)...")
df['message'] = df['message'].apply(parse_list)
df['review_rating'] = df['review_rating'].apply(parse_list)

# 3. Explode Data
# Kita pecah list review agar setiap review punya barisnya sendiri (long format)
print("Transforming data ke format long...")
df_exploded = df[['product_id', 'category', 'message', 'review_rating']].explode(['message', 'review_rating'])

# Hapus data yang tidak punya review
df_exploded = df_exploded.dropna(subset=['message'])

# 4. Sentiment Analysis Sederhana (Lexicon-Based)
def analyze_sentiment(text):
    text = str(text).lower()
    
    # Kamus sederhana bahasa Indonesia
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

# 5. Export Hasil
# Kita simpan hasil akhir untuk ditarik ke Tableau
print("Menyimpan hasil ke CSV...")
df_exploded.to_csv('tokopedia_sentiment_results.csv', index=False)
print("Selesai! File 'tokopedia_sentiment_results.csv' siap digunakan.")