from __future__ import annotations
from enum import unique, Enum, auto
from typing import List


@unique
class RatioGrade(Enum):
    """
    Used to grade ratios.
    """
    UNGRADABLE = auto()
    A_PLUS = auto()
    A = auto()
    A_MINUS = auto()
    B_PLUS = auto()
    B = auto()
    B_MINUS = auto()
    C_PLUS = auto()
    C = auto()
    C_MINUS = auto()
    D_PLUS = auto()
    D = auto()
    D_MINUS = auto()
    F = auto()

    @staticmethod
    def allValidGrades() -> List[RatioGrade]:
        return [RatioGrade.A_PLUS, RatioGrade.A, RatioGrade.A_MINUS, RatioGrade.B_PLUS, RatioGrade.B,
                RatioGrade.B_MINUS, RatioGrade.C_PLUS, RatioGrade.C, RatioGrade.C_MINUS, RatioGrade.D_PLUS,
                RatioGrade.D, RatioGrade.D_MINUS, RatioGrade.F]

    @staticmethod
    def allPassingGrades() -> List[RatioGrade]:
        return [RatioGrade.A_PLUS, RatioGrade.A, RatioGrade.A_MINUS, RatioGrade.B_PLUS, RatioGrade.B,
                RatioGrade.B_MINUS, RatioGrade.C_PLUS, RatioGrade.C, RatioGrade.C_MINUS, RatioGrade.D_PLUS,
                RatioGrade.D, RatioGrade.D_MINUS]
