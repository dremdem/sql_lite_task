import sqlite3

from faker import Faker

CREATE_USERS_STATEMENTS = """
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR2(50)
    );

"""

CREATE_COURSES_STATEMENTS = """
CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    name VARCHAR2(50)
    );

"""

CREATE_SAVES_STATEMENTS = """
CREATE TABLE saves (
    id INTEGER PRIMARY KEY,
    user_id INTEGER, 
    course_id INTEGER, 
    lesson_no INTEGER, 
    exercise_no INTEGER,
    data varchar2(250),
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(course_id) REFERENCES courses(id)
    );

"""


def create_all_tables(connection: sqlite3.Connection) -> None:
    """
    Create all tables
    """

    c = connection.cursor()

    # check if tables exists
    c.execute(
        "SELECT count(name) FROM sqlite_master WHERE type='table' AND name in ('users', 'courses', 'saves')")
    if c.fetchone()[0] < 3:
        c.execute(CREATE_USERS_STATEMENTS)
        c.execute(CREATE_COURSES_STATEMENTS)
        c.execute(CREATE_SAVES_STATEMENTS)


def populate_tables(connection: sqlite3.Connection) -> None:
    """
    Populate DB with fake data
    """
    fake = Faker()
    Faker.seed(0)

    c = conn.cursor()

    number_of_courses = fake.pyint(min_value=5, max_value=20)

    for _ in range(number_of_courses):
        course_name = fake.word()

        insert_statement = f'insert into courses (name) values ("{course_name}");'
        c.execute(insert_statement)

    connection.commit()

    number_of_users = fake.pyint(min_value=1, max_value=23)

    Faker.seed()

    for _ in range(number_of_users):

        if fake.pybool():
            user_name = f'{fake.first_name_female()} {fake.last_name_female()}'
        else:
            user_name = f'{fake.first_name()} {fake.last_name()}'

        insert_statement = f'insert into users (name) values ("{user_name}");'
        c.execute(insert_statement)

    connection.commit()

    for _ in range(50000):
        Faker.seed()

        random_user_id = fake.pyint(1, number_of_users)
        random_course_id = fake.pyint(1, number_of_courses)
        Faker.seed()
        random_lesson_no = fake.pyint(3, 12)
        Faker.seed()
        random_exercise_no = fake.pyint(1, 50)
        random_data = fake.sentence()

        insert_statement = f"""insert into saves (user_id, course_id, lesson_no, exercise_no,data) 
                               values ({random_user_id}, {random_course_id}, {random_lesson_no}, 
                               {random_exercise_no}, '{random_data}');"""
        c.execute(insert_statement)

    connection.commit()


def get_users_with_finished_courses(connection: sqlite3.Connection) -> list:
    """
    Get all users and quantity of finished courses
    """
    select_statement = """
        select
            u.name as user_name, count(*)
        from
            (
                select user_id, course_id, count(*)
                from (select distinct user_id, course_id, lesson_no, exercise_no
                from saves) unique_saves
                group by user_id, course_id having count(*) > 100
            ) finished_courses, users u
        where
            1=1
            and finished_courses.user_id = u.id
        group by u.name;"""

    rows = connection.execute(select_statement)

    return list(rows)


if __name__ == '__main__':
    conn = sqlite3.connect(':memory:')
    create_all_tables(conn)
    populate_tables(conn)
    print(get_users_with_finished_courses(conn))
