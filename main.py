import argparse
from sqlalchemy.exc import SQLAlchemyError
from connect.connect import session
from models.models import Teacher, Student, Group, Subject, Grade

MODELS = {
    'Teacher': Teacher,
    'Student': Student,
    'Group': Group,
    'Subject': Subject,
    'Grade': Grade
}


def create(model_name, **kwargs):
    model = MODELS.get(model_name)
    if not model:
        print(f"Model '{model_name}' is not found.")
        return

    try:
        if model_name == 'Teacher':
            firstname, lastname = kwargs['name'].split(' ')
            instance = model(firstname=firstname, lastname=lastname)
        elif model_name == 'Student':
            firstname, lastname = kwargs['name'].split(' ')
            instance = model(firstname=firstname, lastname=lastname, group_id=kwargs['group_id'])
        elif model_name == 'Group':
            instance = model(gr_name=kwargs['name'])
        elif model_name == 'Subject':
            instance = model(subject=kwargs['name'], teacher_id=kwargs['teacher_id'])
        elif model_name == 'Grade':
            instance = model(student_id=kwargs['student_id'], subject_id=kwargs['subject_id'], grade=kwargs['grade'], date=kwargs['date'])
        else:
            print(f"Model '{model_name}' creation not implemented.")
            return

        session.add(instance)
        session.commit()
        print(f"{model_name} created successfully.")
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()


def update(model_name, id, **kwargs):
    model = MODELS.get(model_name)
    if not model:
        print(f"Model '{model_name}' is not found.")
        return

    try:
        instance = session.query(model).filter(model.id == id).first()
        if not instance:
            print(f"{model_name} with id {id} not found.")
            return

        if model_name == 'Teacher':
            firstname, lastname = kwargs['name'].split(' ')
            instance.firstname = firstname
            instance.lastname = lastname
        elif model_name == 'Student':
            firstname, lastname = kwargs['name'].split(' ')
            instance.firstname = firstname
            instance.lastname = lastname
            instance.group_id = kwargs['group_id']
        elif model_name == 'Group':
            instance.gr_name = kwargs['name']
        elif model_name == 'Subject':
            instance.subject = kwargs['name']
            instance.teacher_id = kwargs['teacher_id']
        elif model_name == 'Grade':
            instance.student_id = kwargs['student_id']
            instance.subject_id = kwargs['subject_id']
            instance.grade = kwargs['grade']
            instance.date = kwargs['date']
        else:
            print(f"Model '{model_name}' update not implemented.")
            return

        session.commit()
        print(f"{model_name} {id} updated successfully.")
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()


def read(model_name):
    model = MODELS.get(model_name)
    if not model:
        print(f"Model '{model_name}' is not found.")
        return

    try:
        instances = session.query(model).all()
        for instance in instances:
            if model_name == 'Teacher':
                print(f"{instance.id}: {instance.firstname} {instance.lastname}")
            elif model_name == 'Student':
                print(f"{instance.id}: {instance.firstname} {instance.lastname}")
            elif model_name == 'Group':
                print(f"{instance.id}: {instance.gr_name}")
            elif model_name == 'Subject':
                print(f"{instance.id}: {instance.subject}")
            elif model_name == 'Grade':
                print(f"{instance.id}: Student ID {instance.student_id}, Subject ID {instance.subject_id}, Grade {instance.grade}, Date {instance.date}")
            else:
                print(instance)
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()


def delete(model_name, id):
    model = MODELS.get(model_name)
    if not model:
        print(f"Model '{model_name}' is not found.")
        return

    try:
        instance = session.query(model).filter(model.id == id).first()
        if not instance:
            print(f"{model_name} with id {id} not found.")
            return

        session.delete(instance)
        session.commit()
        print(f"{model_name} {id} removed successfully.")
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', '-a', required=True, choices=['create', 'list', 'update', 'remove'])
    parser.add_argument('--model', '-m', required=True, choices=['Teacher', 'Student', 'Group', 'Subject', 'Grade'])
    parser.add_argument('--name', '-n')
    parser.add_argument('--id', type=int)
    parser.add_argument('--group_id', '-gr_id')
    parser.add_argument('--teacher_id', '-tr_id')
    parser.add_argument('--student_id', '-st_id')
    parser.add_argument('--subject_id', '-sub_id')
    parser.add_argument('--grade', '-g')
    parser.add_argument('--date', '-d')

    args = parser.parse_args()

    if args.action == 'create':
        create(args.model, name=args.name, group_id=args.group_id, teacher_id=args.teacher_id, student_id=args.student_id, subject_id=args.subject_id, grade=args.grade, date=args.date)
    elif args.action == 'list':
        read(args.model)
    elif args.action == 'update':
        update(args.model, id=args.id, name=args.name, group_id=args.group_id, teacher_id=args.teacher_id, student_id=args.student_id, subject_id=args.subject_id, grade=args.grade, date=args.date)
    elif args.action == 'remove':
        delete(args.model, id=args.id)

    else:
        print(f"Action '{args.action}' is not supported for model '{args.model}' yet.")

if __name__ == '__main__':
    main()