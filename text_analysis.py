import csv
import math
import random
from collections import Counter, defaultdict

POSITIVE = {'good','great','excellent','amazing','wonderful','love','loved','like','masterpiece','outstanding'}
NEGATIVE = {'bad','poor','terrible','awful','boring','hate','hated','dislike','mediocre','worst'}


def load_books(path='Books.csv'):
    books = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            books.append(row)
    return books


def words_from_description(text):
    return [w.strip('.,;!?:"\'()').lower() for w in text.split() if w]


def word_frequencies_by_genre(books, top_n=20):
    genre_words = defaultdict(Counter)
    for b in books:
        genre = b['genre'] or 'Unknown'
        if b['description']:
            words = words_from_description(b['description'])
            genre_words[genre].update(words)
    top = {g: words.most_common(top_n) for g, words in genre_words.items()}
    return top


def sentiment_by_genre(books):
    scores = defaultdict(list)
    for b in books:
        genre = b['genre'] or 'Unknown'
        if b['description']:
            words = words_from_description(b['description'])
            pos = sum(w in POSITIVE for w in words)
            neg = sum(w in NEGATIVE for w in words)
            scores[genre].append(pos - neg)
    avg = {g: round(sum(vals)/len(vals), 3) for g, vals in scores.items() if vals}
    return avg


def simple_genre_classifier(books, train_ratio=0.8):
    random.shuffle(books)
    split = int(len(books)*train_ratio)
    train, test = books[:split], books[split:]
    word_counts = defaultdict(lambda: defaultdict(int))
    genre_totals = Counter()
    vocab = set()
    for b in train:
        genre = b['genre']
        if not genre or not b['description']:
            continue
        words = words_from_description(b['description'])
        genre_totals[genre] += 1
        for w in words:
            word_counts[genre][w] += 1
            vocab.add(w)
    genre_probs = {g: genre_totals[g]/sum(genre_totals.values()) for g in genre_totals}
    def predict(desc):
        words = words_from_description(desc)
        scores = {}
        for g in genre_totals:
            total_words = sum(word_counts[g].values()) + len(vocab)
            log_prob = math.log(genre_probs[g])
            for w in words:
                log_prob += math.log((word_counts[g][w] + 1) / total_words)
            scores[g] = log_prob
        return max(scores, key=scores.get)
    correct = 0
    total = 0
    for b in test:
        if not b['genre'] or not b['description']:
            continue
        pred = predict(b['description'])
        if pred == b['genre']:
            correct += 1
        total += 1
    accuracy = correct/total if total else None
    return accuracy


def main():
    books = load_books()
    freqs = word_frequencies_by_genre(books)
    print('Word frequencies by genre (sample):', {g: words[:5] for g, words in freqs.items()})
    print('Sentiment by genre:', sentiment_by_genre(books))
    print('Genre classifier accuracy:', simple_genre_classifier(books))


if __name__ == '__main__':
    main()
