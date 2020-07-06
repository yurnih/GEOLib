from typing import List
from enum import IntEnum
from pydantic import constr, confloat
from geolib.models.dseries_parser import DSeriesUnmappedNameProperties
from geolib.models.internal import Bool
from geolib.utils import csv_as_namedtuples
import logging
from pathlib import Path


class SoilType(IntEnum):
    GRAVEL = 0
    SAND = 1
    LOAM = 2
    CLAY = 3
    PEAT = 4
    SANDYLOAM = 5


class MaxConeResistType(IntEnum):
    STANDARD = 0
    MANUAL = 1


class Soil(DSeriesUnmappedNameProperties):
    name: constr(min_length=1, max_length=25)
    soilcolor: int = 10871211  # could be color
    soilsoiltype: SoilType = SoilType.SAND
    soilbelgiansoiltype: SoilType = SoilType.SAND
    soilgamdry: confloat(ge=0.0, le=100) = 20.00
    soilgamwet: confloat(ge=0.0, le=100) = 20.00
    soilinitialvoidratio: confloat(ge=0.0, le=20.0) = 0.001001
    soildiameterd50: confloat(ge=0.0, le=1000.0) = 0.20000
    soilminvoidratio: confloat(ge=0.0, le=1.0) = 0.400
    soilmaxvoidratio: confloat(ge=0.0, le=1.0) = 0.800
    soilcohesion: confloat(ge=0.0, le=1000.0) = 30.00
    soilphi: confloat(ge=0.0, le=89.0)
    soilcu: confloat(ge=0.0, le=1000.0)
    soilmaxconeresisttype: MaxConeResistType = MaxConeResistType.STANDARD
    soilmaxconeresist: confloat(ge=0.0, le=1000000.0) = 0.00
    soilusetension: Bool = Bool.TRUE
    soilca: confloat(ge=0.0, le=10.0) = 0.0040000
    soilccindex: confloat(ge=0.0, le=20.0) = 0.1260000

    def __init__(self, *args, **kwargs):
        if "name" not in kwargs:
            name = None
            for key, value in kwargs.items():
                if key not in self.__fields__:
                    name = key + value
                    break
            if name:
                kwargs["name"] = name
                kwargs.pop(key)
        super().__init__(*args, **kwargs)

    class Config:
        arbitrary_types_allowed = True
        validate_assignment = True

    @classmethod
    def default_soils(cls, model: str = "BEARING_PILES") -> List["Soil"]:
        currentfolder = Path(__file__).parent
        name = model.lower()
        filename = currentfolder / f"soil_csv/{name}_soils.csv"
        if not filename.exists():
            logging.warning(f"No default soils supported for {model}")
            return []

        soils = [
            Soil(
                name=name,
                soilsoiltype=soilsoiltype,
                soilgamdry=soilgamdry,
                soilgamwet=soilgamwet,
                soilphi=soilphi,
                soilcohesion=soilcohesion,
                soilcu=soilcu,
                soilccindex=soilccindex,
                soilca=soilca,
                soilinitialvoidratio=soilinitialvoidratio,
                soilcolor=soilcolor,
            )
            for name, soilsoiltype, soilgamdry, soilgamwet, soilphi, soilcohesion, soilcu, soilccindex, soilca, soilinitialvoidratio, soilcolor in csv_as_namedtuples(
                filename
            )
        ]
        return soils
