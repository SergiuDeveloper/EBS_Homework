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
        fields_frequency[field] = min(1., fields_frequency[field])
        fields_frequency[field] = int(math.floor(subscriptions_count * fields_frequency[field]))
        if field in field_equals_frequency.keys():
            field_equals_frequency[field] = min(1., field_equals_frequency[field])
            field_equals_frequency[field] = int(math.floor(fields_frequency[field] * field_equals_frequency[field]))

    remaining_fields = ['Company', 'Date', 'Value', 'Drop', 'Variation']

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
                if fields_frequency[field] == 0:
                    remaining_fields.remove(field)

        if len(subscription) == 0:
            break
        
        yield tuple(subscription)

        subscriptions_count -= 1

    fields = remaining_fields
    if len(remaining_fields) == 0:
        return

    # Generate the other required subscriptions
    for _ in range(subscriptions_count):
        sampled_fields = []
        for __ in range(random.randrange(1, len(fields) + 1)):
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
        100,
        ['Google', 'Microsoft', 'Facebook', 'Twitter', 'Amazon', 'Uber', 'Glovo'],
        list(generate_dates_between(date(2010, 4, 12), date(2018, 1, 1))),
        -30., 30.,
        -10., 10.,
        0.1, 0.8
    ))

    subscriptions = list(generate_subscriptions(
        10,
        {
            'Company': 0.7,
            'Value': 0.3,
            'Variation': 0.2
        },
        {
            'Company': 0.9,
            'Value': 0.7
        },
        ['>', '<', '=', '>=', '<=', '!='],
        ['Google', 'Microsoft', 'Facebook', 'Twitter', 'Amazon', 'SpaceX', 'Tesla'],
        list(generate_dates_between(date(2015, 6, 22), date(2022, 8, 27))),
        -50., 15.5,
        -40., 3.,
        0.55, 0.67
    ))
    
    with open('output.txt', 'w') as output_file:
        print(f'Publications: {publications}', file=output_file)
        print(file=output_file)
        print(f'Subscriptions: {subscriptions}', file=output_file)
