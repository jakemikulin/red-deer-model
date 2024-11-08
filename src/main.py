from math import exp, tanh
from random import random
from typing import List

import pandas as pd


class Deer:
    def __init__(
        self,
        age: int,  # i_a
        isFemale: bool,  # i_f
        isMale: bool,  # i_m
    ):
        self.age = age  # i_a
        self.isFemale = isFemale  # i_f
        self.isMale = isMale  # i_m


class ModelParameters:
    def __init__(
        self,
        sampleSpace: int,
        maxCapacityImpact: float,
        capacityCurveSlope: float,
        huntingLimit: int,
        initialIndividuals: int,
        maximumIndividuals: int,
    ):
        self.sampleSpace = sampleSpace  # S
        self.maxCapacityImpact = maxCapacityImpact  # c
        self.capacityCurveSlope = capacityCurveSlope  # a
        self.huntingLimit = huntingLimit  # l
        self.initialIndividuals = initialIndividuals  # i_init
        self.maximumIndividuals = maximumIndividuals  # i_max

        self.probMale = 0.52  # p_o,m
        self.probFemale = 0.48  # p_o,f
        self.probYoungReproduce = 0.3  # Reproduction function, page 18
        self.probMatureReproduce = 0.9  # Reproduction function, page 18


class HuntingParameters:
    def __init__(
        self,
        calves: int,  # h_c
        youngHinds: int,  # h_yh
        youngStags: int,  # h_ys
        matureHinds: int,  # h_h
        matureStags: int,  # h_s
    ):

        self.calves = calves  # h_c
        self.youngHinds = youngHinds  # h_yh
        self.youngStags = youngStags  # h_ys
        self.matureHinds = matureHinds  # h_h
        self.matureStags = matureStags  # h_s


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


def calculateAgeBasedMortality(age: int) -> float:

    # Calculates the mortality rate (p_{i,d}) based on age (i_a) using the provided formula.

    if age == 0:
        return 0.15
    elif 0 < age < 16:
        return 0.03 + (0.05 / 14) * (age - 1)
    else:  # age >= 16
        return 0.08 * exp(2.47 * (age - 16))


def count_group(population, age=None, min_age=None, countMale=True, countFemale=False):
    if age is not None:
        # Count individuals of a specific age
        return [
            ind
            for ind in population
            if ind.age == age
            and (ind.isMale == countMale or ind.isFemale == countFemale)
        ]
    elif min_age is not None:
        # Count individuals older than a certain age
        return [
            ind
            for ind in population
            if ind.age > min_age
            and (ind.isMale == countMale or ind.isFemale == countFemale)
        ]
    return []


def hunting(
    population: List[Deer], params: ModelParameters, huntingStrategy: HuntingParameters
):
    calves = count_group(population, age=0, countMale=True, countFemale=True)
    if len(calves) > params.huntingLimit:
        calves = calves[huntingStrategy.calves :]

    youngHinds = count_group(population, age=1, countMale=False, countFemale=True)
    if len(youngHinds) > params.huntingLimit:
        youngHinds = youngHinds[huntingStrategy.youngHinds :]

    youngStags = count_group(population, age=1, countMale=True, countFemale=False)
    if len(youngStags) > params.huntingLimit:
        youngStags = youngStags[huntingStrategy.youngStags :]

    hinds = count_group(population, min_age=1, countMale=False, countFemale=True)
    if len(hinds) > params.huntingLimit:
        hinds = hinds[huntingStrategy.matureHinds :]

    stags = count_group(population, min_age=1, countMale=True, countFemale=False)
    if len(stags) > params.huntingLimit:
        stags = stags[huntingStrategy.matureStags :]

    population = calves + youngHinds + youngStags + hinds + stags
    return population


def adjustMortalityRate(
    base_mortality: float,
    max_cap_impact: float,
    cap_curve_slope: float,
    inow: int,
    imax: int,
) -> float:
    # Adjust the mortality rate based on carrying capacity
    adjustment = (max_cap_impact / 2) * (1 + tanh(cap_curve_slope * (inow - imax)))
    return base_mortality + adjustment


def naturalDeath(population: List[Deer], params: ModelParameters):
    survivors = []
    inow = len(population)  # Current population size
    imax = params.maximumIndividuals  # Maximum carrying capacity

    for deer in population:
        # Step 1: Calculate the age-based mortality rate using the provided formula
        base_mortality = calculateAgeBasedMortality(deer.age)

        # Step 2: Adjust mortality rate based on carrying capacity (Algorithm 3)
        adjusted_mortality = adjustMortalityRate(
            base_mortality,
            params.maxCapacityImpact,
            params.capacityCurveSlope,
            inow,
            imax,
        )

        # Step 3: Determine if the deer survives based on adjusted mortality rate
        if random() >= adjusted_mortality:
            survivors.append(
                deer
            )  # Deer survives if random number >= adjusted mortality

    return survivors





def main():
    pass
