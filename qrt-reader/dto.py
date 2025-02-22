from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional

class Base (DeclarativeBase):
    pass

class S05010201 (Base):
    __tablename__ = 'S05010201'
    Company: Mapped[str] = mapped_column(primary_key=True)
    Year: Mapped[int] = mapped_column(primary_key=True)
    LoB: Mapped[str] = mapped_column(primary_key=True)
    R0110: Mapped[Optional[int]]
    R0120: Mapped[Optional[int]]
    R0130: Mapped[Optional[int]]
    R0140: Mapped[Optional[int]]
    R0200: Mapped[Optional[int]]
    R0210: Mapped[Optional[int]]
    R0220: Mapped[Optional[int]]
    R0230: Mapped[Optional[int]]
    R0240: Mapped[Optional[int]]
    R0300: Mapped[Optional[int]]
    R0310: Mapped[Optional[int]]
    R0320: Mapped[Optional[int]]
    R0330: Mapped[Optional[int]]
    R0340: Mapped[Optional[int]]
    R0400: Mapped[Optional[int]]
    R0410: Mapped[Optional[int]]
    R0420: Mapped[Optional[int]]
    R0430: Mapped[Optional[int]]
    R0440: Mapped[Optional[int]]
    R0500: Mapped[Optional[int]]
    R0550: Mapped[Optional[int]]
    R1210: Mapped[Optional[int]]
    R1300: Mapped[Optional[int]]

class S17010201 (Base):
    __tablename__ = 'S17010201'
    Company: Mapped[str] = mapped_column(primary_key=True)
    Year: Mapped[int] = mapped_column(primary_key=True)
    LoB: Mapped[str] = mapped_column(primary_key=True)
    R0010: Mapped[Optional[int]]
    R0050: Mapped[Optional[int]]
    R0060: Mapped[Optional[int]]
    R0140: Mapped[Optional[int]]
    R0150: Mapped[Optional[int]]
    R0160: Mapped[Optional[int]]
    R0240: Mapped[Optional[int]]
    R0250: Mapped[Optional[int]]
    R0260: Mapped[Optional[int]]
    R0270: Mapped[Optional[int]]
    R0280: Mapped[Optional[int]]
    R0320: Mapped[Optional[int]]
    R0330: Mapped[Optional[int]]
    R0340: Mapped[Optional[int]]

class Account (Base):
    __tablename__ = 'Account'
    Code: Mapped[str] = mapped_column(primary_key=True)
    Label: Mapped[str]

class LoB (Base):
    __tablename__ = 'LoB'
    Code: Mapped[str] = mapped_column(primary_key=True)
    Label: Mapped[str]