import csv
import math
from collections import Counter


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


def most_popular_books(books, top_n=10):
    valid = [b for b in books if b['ratings_count'].isdigit()]
    sorted_books = sorted(valid, key=lambda b: int(b['ratings_count']), reverse=True)
    return [(b['title'], int(b['ratings_count'])) for b in sorted_books[:top_n]]


def pages_vs_popularity_corr(books):
    pairs = []
    for b in books:
        pages = to_int(b['pages'])
        rc = to_int(b['ratings_count'])
        if pages is not None and rc is not None:
            pairs.append((pages, rc))
    n = len(pairs)
    if n == 0:
        return None
    mean_x = sum(p for p, _ in pairs) / n
    mean_y = sum(rc for _, rc in pairs) / n
    num = sum((p-mean_x)*(rc-mean_y) for p, rc in pairs)
    den_x = math.sqrt(sum((p-mean_x)**2 for p, _ in pairs))
    den_y = math.sqrt(sum((rc-mean_y)**2 for _, rc in pairs))
    return num / (den_x * den_y) if den_x and den_y else None


def top_rated_books(books, top_n=10):
    valid = []
    for b in books:
        rating = to_float(b['average_rating']) if b['average_rating'] != 'No rating' else None
        if rating is not None:
            valid.append((rating, b['title']))
    valid.sort(reverse=True)
    return [(title, rating) for rating, title in valid[:top_n]]


def main():
    books = load_books()
    print('Most popular books:', most_popular_books(books))
    print('Pages vs popularity correlation:', pages_vs_popularity_corr(books))
    print('Top rated books:', top_rated_books(books))


if __name__ == '__main__':
    main()
