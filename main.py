import random
import math

from datetime import date, timedelta


def generate_publications(publications_count, companies, dates, value_min, value_max, drop_min, drop_max, variation_min, variation_max):
    for _ in range(publications_count):
        company = random.choice(companies)
        date = random.choice(dates)
        value = random.uniform(value_min, value_max)
        drop = random.uniform(drop_min, drop_max)
        variation = random.uniform(variation_min, variation_max)

        publication = (
            ('Company', company),
            ('Date', date),
            ('Value', value),
            ('Drop', drop),
            ('Variation', variation)
        )
        yield publication

def generate_subscriptions(subscriptions_count, fields_frequency, field_equals_frequency, operators, companies, dates, value_min, value_max, drop_min, drop_max, variation_min, variation_max):
    # Convert from percentages to values
    for field in fields_frequency.keys():
        if field in field_equals_frequency.keys():
            field_equals_frequency[field] = min(1., field_equals_frequency[field])
            fields_frequency[field] = max(fields_frequency[field], field_equals_frequency[field])
            field_equals_frequency[field] = int(math.ceil(subscriptions_count * field_equals_frequency[field]))
        fields_frequency[field] = min(1., fields_frequency[field])
        fields_frequency[field] = int(math.ceil(subscriptions_count * fields_frequency[field]))

    # Generate subscriptions in order to satisfy constraints
    while subscriptions_count > 0:
        subscription = []

        for field in fields_frequency.keys():
            value = None
            if field == 'Company':
                value = random.choice(companies)
            elif field == 'Date':
                value = random.choice(dates)
            elif field == 'Value':
                value = random.uniform(value_min, value_max)
            elif field == 'Drop':
                value = random.uniform(drop_min, drop_max)
            elif field == 'Variation':
                value = random.uniform(variation_min, variation_max)
            if value is None:
                continue

            if fields_frequency[field] > 0:
                if field in field_equals_frequency.keys() and field_equals_frequency[field] > 0:
                    subscription.append((field, '=', value))
                    field_equals_frequency[field] -= 1
                else:
                    operator = random.choice(operators)
                    subscription.append((field, operator, value))
                fields_frequency[field] -= 1

        if len(subscription) == 0:
            break
        
        yield tuple(subscription)

        subscriptions_count -= 1

    fields = ['Company', 'Date', 'Value', 'Drop', 'Variation']

    # Generate the other required subscriptions
    for _ in range(subscriptions_count):
        sampled_fields = []
        for __ in range(random.randrange(1, len(fields))):
            sampled_field = random.choice(fields)
            sampled_fields.append(sampled_field)
        sampled_fields = set(sampled_fields)

        subscription = []
        
        for field in sampled_fields:
            value = None
            if field == 'Company':
                value = random.choice(companies)
            elif field == 'Date':
                value = random.choice(dates)
            elif field == 'Value':
                value = random.uniform(value_min, value_max)
            elif field == 'Drop':
                value = random.uniform(drop_min, drop_max)
            elif field == 'Variation':
                value = random.uniform(variation_min, variation_max)
            if value is None:
                raise Exception('Logic exception')

            operator = random.choice(operators)
            subscription.append((field, operator, value))

        yield tuple(subscription)


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

    subscriptions = list(generate_subscriptions(
        50,
        {},
        {},
        ['>', '<', '=', '>=', '<=', '!='],
        ['Google', 'Microsoft', 'Facebook', 'Twitter', 'Amazon'],
        list(generate_dates_between(date(2010, 1, 15), date(2022, 1, 15))),
        -30., 30.,
        -10., 10.,
        0., 1.
    ))
    
    print(publications)
    print(subscriptions)
