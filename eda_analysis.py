import csv
from collections import Counter
import statistics


def load_books(path='Books.csv'):
    books = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            books.append(row)
    return books


def to_int(value):
    return int(value) if value and value.isdigit() else None


def page_distribution(books):
    pages = [to_int(b['pages']) for b in books if to_int(b['pages']) is not None]
    if not pages:
        return {}
    stats = {
        'count': len(pages),
        'min': min(pages),
        'max': max(pages),
        'mean': round(statistics.mean(pages), 2),
        'median': statistics.median(pages)
    }
    return stats


def distribution_by_field(books, field, top_n=10):
    counter = Counter(b[field] for b in books if b[field])
    return counter.most_common(top_n)


def publication_year_distribution(books):
    years = []
    for b in books:
        date = b['published_date']
        if date:
            year = date.split('-')[0]
            if year.isdigit():
                years.append(int(year))
    return Counter(years)


def main():
    books = load_books()
    print('Page distribution:', page_distribution(books))
    print('Top genres:', distribution_by_field(books, 'genre'))
    print('Top languages:', distribution_by_field(books, 'language'))
    print('Top publishers:', distribution_by_field(books, 'publisher'))
    years = publication_year_distribution(books)
    print('Publication years sample:', list(years.items())[:10])


if __name__ == '__main__':
    main()
