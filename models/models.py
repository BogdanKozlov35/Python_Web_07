from sqlalchemy import Column, Integer, String, Date, ForeignKey, text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.exc import SQLAlchemyError

from connect.connect import session, engine

Base = declarative_base()

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    gr_name = Column(String(50), nullable=False)



class Student(Base):
    __tablename__ ='students'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)
    group = relationship('Group', backref='students', cascade="all, delete")

    @hybrid_property
    def fullname(self):
        return self.firstname + " " + self.lastname



class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(120), nullable=False)
    lastname = Column(String(120), nullable=False)

    @hybrid_property
    def fullname(self):
        return self.firstname + " " + self.lastname



class Subject(Base):
    __tablename__ ='subjects'
    id = Column(Integer, primary_key=True)
    subject = Column(String(50), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='CASCADE'), nullable=False)
    teacher = relationship('Teacher', backref='subjects', cascade="all, delete")



class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    date = Column(Date, nullable=False)
    grade = Column(Integer, nullable=False)
    student = relationship('Student', backref='grades', cascade="all, delete")
    subject = relationship('Subject', backref='grades', cascade="all, delete")



if __name__ == '__main__':
    try:
        with engine.connect() as connection:
            connection.execute(text("DROP TABLE IF EXISTS grades"))
            connection.execute(text("DROP TABLE IF EXISTS subjects"))
            connection.execute(text("DROP TABLE IF EXISTS students"))
            connection.execute(text("DROP TABLE IF EXISTS teachers"))
            connection.execute(text("DROP TABLE IF EXISTS groups"))

        Base.metadata.create_all(engine)
        Base.metadata.bind = engine

        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()