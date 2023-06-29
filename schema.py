from pydantic import BaseModel


class CalcInput(BaseModel):
    left_value: float | None
    right_value: float | None
    operation: str | None

    class Config:
        orm_mode = True


class Result(CalcInput):
    result: float | None
