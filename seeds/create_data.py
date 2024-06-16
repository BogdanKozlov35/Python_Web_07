import random
from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from connect.connect import session
from models.models import Student, Subject, Teacher, Group, Grade

fake = Faker("uk-UA")

def group_data():
    for _ in range(1, 4):
        group = Group(gr_name=fake.word())
        session.add(group)
    session.commit()

def student_data():
    groups = session.query(Group).all()
    for _ in range(1, 51):
        student = Student(
            firstname=fake.first_name(),
            lastname=fake.last_name(),
            group_id=random.choice(groups).id
        )
        session.add(student)
    session.commit()

def teacher_data():
    for _ in range(1, 6):
        teacher = Teacher(
            firstname=fake.first_name(),
            lastname=fake.last_name()
        )
        session.add(teacher)
    session.commit()

def subject_data():
    teachers = session.query(Teacher).all()
    for _ in range(1, 9):
        subject = Subject(
            subject=fake.word(),
            teacher_id=random.choice(teachers).id
        )
        session.add(subject)
    session.commit()

def grades_data():
    subjects = session.query(Subject).all()
    students = session.query(Student).all()
    for student in students:

        for _ in range(1, 21):
            grade = Grade(
                student_id=student.id,
                subject_id=random.choice(subjects).id,
                date=fake.date(),
                grade=random.randint(1, 100)
            )
            session.add(grade)
    session.commit()

if __name__ == '__main__':
    try:
        group_data()
        student_data()
        teacher_data()
        subject_data()
        grades_data()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()