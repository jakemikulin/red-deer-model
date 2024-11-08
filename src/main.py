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
    pass

def count_group(population, age=None, min_age=None, countMale=True, countFemale=False):
    if age is not None:
        # Count individuals of a specific age
        return [ind for ind in population if ind.age == age and (ind.isMale==countMale or ind.isFemale==countFemale)]
    elif min_age is not None:
        # Count individuals older than a certain age
        return [ind for ind in population if ind.age > min_age and (ind.isMale==countMale or ind.isFemale==countFemale)]
    return []

def hunting(population: List[Deer],
            params: ModelParameters, 
            huntingStrategy: HuntingParameters):
    calves=count_group(population, age= 0, countMale=True, countFemale=True)
    if len(calves)>params.huntingLimit:
        calves=calves[huntingStrategy.calves:]

    youngHinds=count_group(population, age= 1, countMale=False, countFemale=True)
    if len(youngHinds)>params.huntingLimit:
        youngHinds=youngHinds[huntingStrategy.youngHinds:]

    youngStags=count_group(population, age= 1, countMale=True, countFemale=False)
    if len(youngStags)>params.huntingLimit:
        youngStags=youngStags[huntingStrategy.youngStags:]

    hinds=count_group(population, min_age= 1, countMale=False, countFemale=True)
    if len(hinds)>params.huntingLimit:
        hinds=hinds[huntingStrategy.matureHinds:]

    stags=count_group(population, min_age= 1, countMale=True, countFemale=False)
    if len(stags)>params.huntingLimit:
        stags=stags[huntingStrategy.matureStags:]
    
    population=calves+youngHinds+youngStags+hinds+stags
    return population

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
