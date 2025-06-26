import csv
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


def avg_pages_by_year(books):
    pages_per_year = defaultdict(list)
    for b in books:
        year = b['published_date'][:4] if b['published_date'] else None
        p = to_int(b['pages'])
        if year and p is not None and year.isdigit():
            pages_per_year[int(year)].append(p)
    return {y: round(sum(v)/len(v), 2) for y, v in pages_per_year.items() if v}


def genre_trends(books, top_n=5):
    counts = defaultdict(lambda: defaultdict(int))
    overall = defaultdict(int)
    for b in books:
        if b['genre']:
            overall[b['genre']] += 1
    top_genres = sorted(overall, key=overall.get, reverse=True)[:top_n]
    for b in books:
        year = b['published_date'][:4] if b['published_date'] else None
        genre = b['genre']
        if year and genre in top_genres and year.isdigit():
            counts[genre][int(year)] += 1
    return {g: dict(years) for g, years in counts.items()}


def main():
    books = load_books()
    print('Average pages by year (sample):', list(avg_pages_by_year(books).items())[:10])
    print('Genre trends (top):', genre_trends(books))


if __name__ == '__main__':
    main()
