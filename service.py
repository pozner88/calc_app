# from database import session
from models import History
from sqlalchemy import insert, update


def value_to_db(session, **kwargs):
    if not session.query(History).all():
        add_new_record(session)
    if 'right_value' in kwargs:
        stmt = update(History).values(right_value=kwargs['right_value'])
    elif 'left_value' in kwargs:
        stmt = update(History).values(left_value=kwargs['left_value'])
    elif 'operation' in kwargs:
        stmt = update(History).values(operation=kwargs['operation'])
    elif 'result' in kwargs:
        stmt = update(History).values(result=kwargs['result'])
        add_new_record(session)
    else:
        return

    ids = session.query(History.id).order_by(History.id.desc()).limit(1).scalar()
    stmt = stmt.filter(History.id == ids) if 'result' not in kwargs else stmt.filter(History.id == ids - 1)
    res = session.execute(stmt)
    session.commit()

    return res


def add_new_record(session):
    stmt = insert(History)
    session.execute(stmt)
    session.commit()


def select_history(page, limit, session):
    return session.query(History).filter(History.left_value.isnot(None)).offset((page - 1) * limit).limit(limit).all()


def select_result(session):
    res = session.query(History).filter().order_by(History.id.desc()).all()
    right_value = res[0].right_value
    if res[0].left_value is None:
        left_value = session.query(History.result).filter(History.result.isnot(None)).order_by(History.id.desc()). \
            limit(1).scalar()
        value_to_db(left_value=left_value)
    else:
        left_value = res[0].left_value

    operation = res[0].operation

    return {'right_value': right_value, 'left_value': left_value, 'operation': operation}
