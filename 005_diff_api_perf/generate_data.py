import json
import os
import random

from faker import Faker
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values


fake = Faker()
load_dotenv()


def get_json_field():
    return json.dumps({
        'name': fake.name(),
        'email': fake.email(),
        'address': fake.address(),
    })


if __name__ == '__main__':
    parents = []
    children = []

    conn = psycopg2.connect(os.getenv('DATABASE_URL'))

    for _ in range(20):
        parents.append((
            fake.text(max_nb_chars=64),
            ''.join(fake.sentences(nb=3)),
            fake.past_datetime(),
            fake.past_datetime(),
        ))

    cursor = conn.cursor()

    execute_values(
        cursor,
        '''INSERT INTO testapp_parent(title, description, created, modified)
        VALUES %s RETURNING id
        ''',
        parents
    )
    parent_ids = tuple(x[0] for x in cursor.fetchall())

    for _ in range(len(parent_ids)*20):
        children.append((
            random.choice(parent_ids),
            fake.text(max_nb_chars=64),
            ''.join(fake.paragraphs(nb=30)),
            get_json_field(),
            fake.past_datetime(),
            fake.past_datetime()
        ))

    execute_values(
        cursor,
        '''
        INSERT INTO testapp_child(parent_id, title, long_text, json_field, created, modified)
        VALUES %s
        ''',
        children
    )
    conn.commit()
    conn.close()
