from sqlalchemy import func, desc, select, and_

from models.models import Grade, Teacher, Student, Group, Subject
from connect.connect import session
from sqlalchemy.exc import SQLAlchemyError


def select_01():

    result = (
        session.query(
            Student.id,
            Student.fullname,
            func.round(func.avg(Grade.grade), 2).label('average_grade')
        )
        .select_from(Student)
        .join(Grade).group_by(Student.id)
        .order_by(desc('average_grade'))
        .limit(5).all())
    return result


def select_02():
    random_subject = session.query(Subject.id).order_by(func.random()).limit(1).scalar()

    result = (
        session.query(
            Student.id,
            Student.fullname,
            func.round(func.avg(Grade.grade), 2).label('average_grade')
        )
        .join(Grade, Grade.student_id == Student.id)
        .filter(Grade.subject_id == random_subject)
        .group_by(Student.id)
        .order_by(desc('average_grade'))
        .limit(1).all()
        )
    return result


def select_03():

    result = (
        session.query(
            Subject.subject,
            Group.gr_name,
            func.round(func.avg(Grade.grade), 2)
            .label('average_grade')
        )
        .join(Grade, Grade.subject_id == Subject.id)
        .join(Student, Grade.student_id == Student.id)
        .join(Group, Student.group_id == Group.id)
        .group_by(Subject.subject, Group.gr_name).all())
    return result


def select_04():

    result = (
        session.query(
            Group.gr_name,
            func.round(func.avg(Grade.grade), 2)
            .label('average_grade')
        )
        .join(Student, Grade.student_id == Student.id)
        .join(Group, Student.group_id == Group.id)
        .group_by(Group.gr_name)
        .order_by(desc('average_grade'))
        .all())
    return result


def select_05():

    result = (
        session.query(
            Teacher.fullname,
            Subject.subject
        )
        .join(Subject, Subject.teacher_id == Teacher.id)
        .group_by(Teacher.fullname, Subject.subject)
        .all())
    return result


def select_06():

    result = (
        session.query(
            Group.gr_name,
            Student.fullname
        )
        .join(Group, Student.group_id == Group.id)
        .order_by(Group.gr_name)
        .all())
    return result


def select_07():
    random_subject = session.query(Subject.id).order_by(func.random()).limit(1).scalar()
    random_group = session.query(Group.id).order_by(func.random()).limit(1).scalar()

    result = (
        session.query(
            Student.fullname,
            Subject.subject,
            Group.gr_name,
            func.round(func.avg(Grade.grade), 2)
            .label('average_grade')
        )
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Grade.subject_id == Subject.id)
        .join(Group, Student.group_id == Group.id)
        .filter(and_(Grade.subject_id == random_subject, Student.group_id == random_group))
        .group_by(Student.fullname, Subject.subject, Group.gr_name)
        .order_by(desc('average_grade'))
        .all())
    return result


def select_08():

    result = (
        session.query(
            Teacher.fullname,
            Subject.subject,
            func.round(func.avg(Grade.grade), 2)
            .label('average_grade')
        )
        .join(Subject, Subject.teacher_id==Teacher.id)
        .join(Grade, Grade.subject_id == Subject.id)
        .group_by(Teacher.fullname, Subject.subject)
        .order_by(desc('average_grade'))
        .all())
    return result


def select_09():
    result = (
        session.query(
            Student.fullname,
            Subject.subject,
        )
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Grade.subject_id == Subject.id)
        .group_by(Student.fullname, Subject.subject)
        .all())
    return result


def select_10():
    result = (
        session.query(
            Student.fullname,
            Teacher.fullname,
            Subject.subject,
        )
        .join(Grade, Grade.subject_id == Subject.id)
        .join(Student, Grade.student_id == Student.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .group_by(Student.fullname, Teacher.fullname, Subject.subject)
        .distinct()
        .all())
    return result


def select_12():

    subquery = (select(func.max(Grade.grade_date)).join(Student).filter(and_(
        Grade.subjects_id == 2, Student.group_id == 3
    ))).scalar_subquery()

    result = session.query(Student.id, Student.fullname, Grade.grade, Grade.grade_date) \
        .select_from(Grade) \
        .join(Student) \
        .filter(and_(Grade.subjects_id == 2, Student.group_id == 3, Grade.grade_date == subquery)).all()

    return result


if __name__ == '__main__':
    try:
        print(select_01())
        # print(select_02())
        # print(select_03())
        # print(select_04())
        # print(select_05())
        # print(select_06())
        # print(select_07())
        # print(select_08())
        # print(select_09())
        # print(select_10())

        # print(select_12())
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()

