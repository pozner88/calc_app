from database import get_db
from fastapi import APIRouter, HTTPException, Depends
from schema import Result
from service import value_to_db, select_history, select_result

router = APIRouter(
    prefix='/calc',
    tags=['calc']
)


@router.post('/leftValue')
def get_left_value(left_value: float, session=Depends(get_db)):
    result = value_to_db(session, left_value=left_value)
    if result.rowcount > 0:
        return {'left_value': left_value}
    else:
        raise HTTPException(status_code=400, detail='operation failed')


@router.post('/rightValue')
def get_right_value(right_value: float, session=Depends(get_db)):
    result = value_to_db(session, right_value=right_value)
    if result.rowcount > 0:
        return {"right_value": right_value}
    else:
        raise HTTPException(status_code=400, detail='operation failed')


@router.post('/operation')
def get_operation(operation, session=Depends(get_db)):
    if len(operation) == 1 and operation in ['+', '-', '*', '/']:
        result = value_to_db(session, operation=operation)
        if result.rowcount > 0:
            return {"operation": operation}
        else:
            raise HTTPException(status_code=400, detail='operation failed')
    else:
        raise HTTPException(status_code=400, detail='Unsupported operation')


@router.get('/history', response_model=list[Result])
def get_history(page: int = 1, limit: int = 20, session=Depends(get_db)):
    return select_history(page, limit, session)


@router.get('/getResult', response_model=Result)
def get_result(session=Depends(get_db)):
    calc = select_result(session)
    if calc['right_value'] is None:
        raise HTTPException(status_code=400, detail='right value is not set')
    elif calc['left_value'] is None:
        raise HTTPException(status_code=400, detail='left value is not set and no calculated results')
    elif calc['operation'] is None:
        raise HTTPException(status_code=400, detail='operation not selected')
    try:
        result = eval(f"{calc['right_value']} {calc['operation']} {calc['left_value']}")
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid operation")
    value_to_db(session, result=result)
    calc['result'] = result
    return calc
