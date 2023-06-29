from database import Base
from sqlalchemy.orm import Mapped, mapped_column


class History(Base):
    __tablename__ = 'history'
    id: Mapped[int] = mapped_column(primary_key=True)
    left_value: Mapped[float] = mapped_column(nullable=True)
    right_value: Mapped[float] = mapped_column(nullable=True)
    operation: Mapped[str] = mapped_column(nullable=True)
    result: Mapped[float] = mapped_column(nullable=True)
