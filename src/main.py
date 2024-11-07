from typing import List
from random import random



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


def naturalDeath(population: List[Deer], params: ModelParameters):
    def naturalDeath(population: List[Deer], params: ModelParameters):
    survivors = []
    for deer in population:
        # Determine mortality rate based on the age of the deer
        if deer.age == 0:
            mortality_rate = params.calfMortalityRate  # p_i,d for age 0
        elif 0 < deer.age < 16:
            mortality_rate = params.youngMortalityRate  # p_i,d for age 1 to 15
        else:
            mortality_rate = params.oldMortalityRate  # p_i,d for age 16 and older
        
        # Check if deer survives or dies based on mortality rate
        if random() >= mortality_rate:
            survivors.append(deer)  # Deer survives if random number >= mortality_rate
    
    return survivors


def hunting(population: List[Deer],
            params: ModelParameters, 
            huntingStrategy: HuntingParameters):
    pass


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
            mortalityRateAge0: float,         # Mortality rate for age 0
            mortalityRateAge1to15: float,     # Mortality rate for ages 1 to 15
            mortalityRateAge16Plus: float     # Mortality rate for age 16 and above
                 ):
        self.sampleSpace = sampleSpace,                 # S
        self.maxCapacityImpact = maxCapacityImpact,     # c
        self.capacityCurveSlope = capacityCurveSlope,   # a
        self.huntingLimit = huntingLimit,               # l
        self.initialIndividuals = initialIndividuals,   # i_init
        self.maximumIndividuals = maximumIndividuals    # i_max
        self.mortalityRateAge0 = mortalityRateAge0
        self.mortalityRateAge1to15 = mortalityRateAge1to15
        self.mortalityRateAge16Plus = mortalityRateAge16Plus
       

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
