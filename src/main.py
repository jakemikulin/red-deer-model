from typing import List
from random import random
from math import tanh


def grow(population: List[Deer]):
    for deer in population:
        deer.age += 1


def reproduce(population: List[Deer], params: ModelParameters):
    newDeer = []

    hasMale = any([deer.isMale and deer.age >= 1 for deer in population])

    if hasMale:
        return population

    for deer in population:
        if not deer.isFemale:
            continue

        if deer.age == 1:
            if random() < params.probYoungReproduce:
                male = False
                if random() < params.probMale:
                    male = True
                newDeer.append(Deer(0, not male, male))

        elif 1 < deer.age < 12:
            if random() < params.probMatureReproduce:
                male = False
                if random() < params.probMale:
                    male = True
                newDeer.append(Deer(0, not male, male))

    return population + newDeer

def adjustMortalityRate(base_mortality: float, max_cap_impact: float, cap_curve_slope: float, inow: int, imax: int) -> float:
    # Adjust the mortality rate based on carrying capacity
    adjustment = (max_cap_impact / 2) * (1 + tanh(cap_curve_slope * (inow - imax)))
    return base_mortality + adjustment

def naturalDeath(population: List[Deer], params: ModelParameters):
    pass


def naturalDeath(population: List[Deer], params: ModelParameters):
    survivors = []
    inow = len(population)  # Current population size
    imax = params.maximumIndividuals  # Maximum carrying capacity

    for deer in population:
        # Determine base mortality rate based on age
        if deer.age == 0:
            base_mortality = 0.2  # Base mortality rate for age 0
        elif 0 < deer.age < 16:
            base_mortality = 0.05  # Base mortality rate for ages 1 to 15
        else:
            base_mortality = 0.4  # Base mortality rate for age 16 and above
        
        # Adjust mortality rate based on carrying capacity
        adjusted_mortality = adjustMortalityRate(
            base_mortality,
            params.maxCapacityImpact,
            params.capacityCurveSlope,
            inow,
            imax
        )
        
        # Determine if the deer survives
        if random() >= adjusted_mortality:
            survivors.append(deer)  # Deer survives if random number >= adjusted mortality
    
    return survivors


class Deer():
    def __init__(
            self,
            age: int,       # i_a
            isFemale: bool, # i_f
            isMale: bool,   # i_m
            ):
        self.age = age,           # i_a
        self.isFemale = isFemale, # i_f
        self.isMale = isMale,     # i_m


class ModelParameters():
    def __init__(
            self,
            sampleSpace: int,
            maxCapacityImpact: float,
            capacityCurveSlope: float,
            huntingLimit: int,
            initialIndividuals: int,
            maximumIndividuals: int
                 ):
        self.sampleSpace = sampleSpace,                 # S
        self.maxCapacityImpact = maxCapacityImpact,     # c
        self.capacityCurveSlope = capacityCurveSlope,   # a
        self.huntingLimit = huntingLimit,               # l
        self.initialIndividuals = initialIndividuals,   # i_init
        self.maximumIndividuals = maximumIndividuals    # i_max
       

class HuntingParameters():
    def __init__(
            self,
            calves: int,            # h_c
            youngHinds: int,        # h_yh
            youngStags: int,        # h_ys
            matureHinds: int,       # h_h
            matureStags: int,       # h_s
                 ):

        self.calves = calves,             # h_c
        self.youngHinds = youngHinds,     # h_yh
        self.youngStags = youngStags,     # h_ys
        self.matureHinds = matureHinds,   # h_h
        self.matureStags = matureStags    # h_s


def runSimulation(parameters: ModelParameters, huntingStrategy: HuntingParameters):
    pass


def main():
    pass
