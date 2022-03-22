import random

from datetime import date, timedelta


def generate_publications(publications_count, companies, dates, value_min, value_max, drop_min, drop_max, variation_min, variation_max):
    for _ in range(publications_count):
        company = random.choice(companies)
        date = random.choice(dates)
        value = random.uniform(value_min, value_max)
        drop = random.uniform(drop_min, drop_max)
        variation = random.uniform(variation_min, variation_max)

        publication = {
            'Company': company,
            'Date': date,
            'Value': value,
            'Drop': drop,
            'Variation': variation
        }
        yield publication

def generate_dates_between(start_date, end_date):
    delta = end_date - start_date

    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        yield str(day)


if __name__ == '__main__':
    publications = list(generate_publications(
        10,
        ['Google', 'Microsoft', 'Facebook', 'Twitter', 'Amazon'],
        list(generate_dates_between(date(2010, 1, 15), date(2022, 1, 15))),
        -30., 30.,
        -10., 10.,
        0., 1.
    ))
    print(publications)