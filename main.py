import random
import math

from datetime import date, timedelta


def generate_publications(publications_count, companies, dates, value_min, value_max, drop_min, drop_max, variation_min,
                          variation_max):
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


def generate_subscriptions(subscriptions_count, fields_frequency, field_equals_frequency, operators, companies, dates,
                           value_min, value_max, drop_min, drop_max, variation_min, variation_max):
    max_subscriptions = subscriptions_count
    # Convert from percentages to values
    for field in fields_frequency.keys():
        fields_frequency[field] = min(1., fields_frequency[field])
        fields_frequency[field] = int(math.floor(subscriptions_count * fields_frequency[field]))
        if field in field_equals_frequency.keys():
            field_equals_frequency[field] = min(1., field_equals_frequency[field])
            field_equals_frequency[field] = int(math.floor(fields_frequency[field] * field_equals_frequency[field]))

    remaining_fields = ['Company', 'Date', 'Value', 'Drop', 'Variation']

    # Generate subscriptions in order to satisfy constraints
    generated_subscriptions = []
    index_sub = 0
    while subscriptions_count > 0:
        subscription = []
        finished_adding = True
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
                finished_adding = False
                if field in field_equals_frequency.keys() and field_equals_frequency[field] > 0:
                    tmp_field = (field, '=', value)
                    field_equals_frequency[field] -= 1
                else:
                    operator = random.choice(operators)
                    tmp_field = (field, operator, value)

                # Insert new fields until we reach max subscription number then append to existing ones
                # checking if fields aren't already present in that subscription
                next_free_index = index_sub
                if len(generated_subscriptions) < max_subscriptions:
                    generated_subscriptions.insert(index_sub, [tmp_field])
                else:
                    collision = True
                    while collision:
                        if any(field in i for i in generated_subscriptions[next_free_index]):
                            next_free_index += 1
                        else:
                            generated_subscriptions[next_free_index].append(tmp_field)
                            collision = False
                # don't skip the subscriptions that got collision
                if next_free_index == index_sub:
                    index_sub += 1
                    index_sub %= max_subscriptions
                fields_frequency[field] -= 1
                if fields_frequency[field] == 0:
                    remaining_fields.remove(field)

        if finished_adding:
            break

        subscriptions_count -= 1

    return generated_subscriptions


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
            'Company': 0.2,
            'Value': 0.2,
            'Variation': 0.2,
            'Drop': 0.2,
            'Date': 0.2
        },
        {
            'Company': 0.9,
            'Value': 0.7,
            'Variation': 0.2,
            'Drop': 0.2,
            'Date': 0.2
        },
        ['>', '<', '=', '>=', '<=', '!='],
        ['Google', 'Microsoft', 'Facebook', 'Twitter', 'Amazon', 'SpaceX', 'Tesla'],
        list(generate_dates_between(date(2015, 6, 22), date(2022, 8, 27))),
        -50., 15.5,
        -40., 3.,
        0.55, 0.67
    ))

    generated_pubs_fields_freq = {
        'Company': 0,
        'Value': 0,
        'Variation': 0,
        'Drop': 0,
        'Date': 0
    }

    generated_subs_fields_freq = {
        'Company': 0,
        'Value': 0,
        'Variation': 0,
        'Drop': 0,
        'Date': 0
    }

    generated_subs_equals_freq = {
        'Company': 0,
        'Value': 0,
        'Variation': 0,
        'Drop': 0,
        'Date': 0
    }

    for tmp_publication in publications:
        for tmp_field in tmp_publication:
            field = tmp_field[0]
            generated_pubs_fields_freq[field] += 1

    for tmp_subscription in subscriptions:
        for tmp_field in tmp_subscription:
            field = tmp_field[0]
            operator = tmp_field[1]
            if operator == '=':
                generated_subs_equals_freq[field] += 1
            generated_subs_fields_freq[field] += 1

    print("==================GENERATED PUBS STATS==================")
    print(generated_pubs_fields_freq)
    print("==================GENERATED SUBS FIELDS FREQUENCY STATS==================")
    print(generated_subs_fields_freq)
    print("==================GENERATED SUBS EQUAL OPERATOR STATS==================")
    print(generated_subs_equals_freq)

    with open('output.txt', 'w') as output_file:
        print(f'Publications: {publications}', file=output_file)
        print(file=output_file)
        print(f'Subscriptions: {subscriptions}', file=output_file)
