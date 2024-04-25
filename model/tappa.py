from dataclasses import dataclass
from datetime import date

from model.situazione import Situazione


@dataclass
class Tappa(Situazione):
    costo: int


if __name__ == '__main__':
    tappa = Tappa('Torino', date(1, 1, 1), 20, 120)


