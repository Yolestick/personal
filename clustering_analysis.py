import csv
import math
import random
from collections import defaultdict


def load_books(path='Books.csv'):
    books = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            books.append(row)
    return books


def to_int(value):
    return int(value) if value and value.isdigit() else None


def to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def normalize(vals):
    m = min(vals)
    M = max(vals)
    if M == m:
        return [0.0]*len(vals)
    return [(v-m)/(M-m) for v in vals]


def kmeans_cluster(books, k=3, iterations=10):
    samples = []
    for b in books:
        p = to_int(b['pages'])
        r = to_float(b['average_rating']) if b['average_rating'] != 'No rating' else None
        rc = to_int(b['ratings_count'])
        lang = b['language']
        genre = b['genre']
        if None not in (p, r, rc) and lang and genre:
            samples.append({'pages': p, 'rating': r, 'ratings_count': rc, 'language': lang, 'genre': genre})
    if len(samples) < k:
        return []
    langs = {s['language'] for s in samples}
    genres = {s['genre'] for s in samples}
    lang_map = {l: i for i, l in enumerate(sorted(langs))}
    genre_map = {g: i for i, g in enumerate(sorted(genres))}
    for s in samples:
        s['language'] = lang_map[s['language']]
        s['genre'] = genre_map[s['genre']]
    pages_norm = normalize([s['pages'] for s in samples])
    rating_norm = normalize([s['rating'] for s in samples])
    rc_norm = normalize([s['ratings_count'] for s in samples])
    for s, pn, rn, cn in zip(samples, pages_norm, rating_norm, rc_norm):
        s['pages'] = pn
        s['rating'] = rn
        s['ratings_count'] = cn
    centroids = random.sample(samples, k)
    for _ in range(iterations):
        clusters = [[] for _ in range(k)]
        for s in samples:
            distances = [math.dist([s['pages'], s['rating'], s['ratings_count'], s['language'], s['genre']],
                                   [c['pages'], c['rating'], c['ratings_count'], c['language'], c['genre']])
                         for c in centroids]
            idx = distances.index(min(distances))
            clusters[idx].append(s)
        new_centroids = []
        for cluster in clusters:
            if not cluster:
                new_centroids.append(random.choice(samples))
                continue
            mean = {}
            for key in ['pages', 'rating', 'ratings_count', 'language', 'genre']:
                mean[key] = sum(s[key] for s in cluster) / len(cluster)
            new_centroids.append(mean)
        centroids = new_centroids
    return [len(c) for c in clusters]


def main():
    books = load_books()
    print('Cluster sizes:', kmeans_cluster(books, k=3))


if __name__ == '__main__':
    main()
