import random
from math import exp, tanh
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
        maxCapacityImpact: float,
        capacityCurveSlope: float,
        huntingLimit: int,
        initialIndividuals: int,
        maximumIndividuals: int,
    ):
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

    return population


def reproduce(population: List[Deer], params: ModelParameters):
    newDeer = []

    hasMale = any([deer.isMale and deer.age >= 1 for deer in population])

    if not hasMale:
        return population

    for deer in population:
        if not deer.isFemale:
            continue

        if deer.age == 1:
            if random.random() < params.probYoungReproduce:
                male = False
                if random.random() < params.probMale:
                    male = True
                newDeer.append(Deer(0, not male, male))

        elif 1 < deer.age < 12:
            if random.random() < params.probMatureReproduce:
                male = False
                if random.random() < params.probMale:
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


def get_group(population, age=None, min_age=None, onlyMale=False, onlyFemale=False):
    if age is not None:
        return [
            deer
            for deer in population
            if deer.age == age
            and (
                (onlyMale == onlyFemale)
                or (deer.isMale and onlyMale)
                or (deer.isFemale and onlyFemale)
            )
        ]
    elif min_age is not None:
        return [
            deer
            for deer in population
            if deer.age > min_age
            and (
                (onlyMale == onlyFemale)
                or (deer.isMale and onlyMale)
                or (deer.isFemale and onlyFemale)
            )
        ]
    return []


def hunting(
    population: List[Deer], params: ModelParameters, huntingStrategy: HuntingParameters
):
    calves = get_group(population, age=0, onlyMale=False, onlyFemale=False)
    if len(calves) > params.huntingLimit:
        calves = calves[huntingStrategy.calves :]

    youngHinds = get_group(population, age=1, onlyMale=False, onlyFemale=True)
    if len(youngHinds) > params.huntingLimit:
        youngHinds = youngHinds[huntingStrategy.youngHinds :]

    youngStags = get_group(population, age=1, onlyMale=True, onlyFemale=False)
    if len(youngStags) > params.huntingLimit:
        youngStags = youngStags[huntingStrategy.youngStags :]

    hinds = get_group(population, min_age=1, onlyMale=False, onlyFemale=True)
    if len(hinds) > params.huntingLimit:
        hinds = hinds[huntingStrategy.matureHinds :]

    stags = get_group(population, min_age=1, onlyMale=True, onlyFemale=False)
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
        if random.random() >= adjusted_mortality:
            survivors.append(
                deer
            )  # Deer survives if random number >= adjusted mortality

    return survivors


def generate_random_list(size, total):
    numbers = []
    current_sum = 0
    for _ in range(size - 1):
        remaining = total - current_sum
        value = random.randint(0, min(10, remaining))
        numbers.append(value)
        current_sum += value
    numbers.append(total - current_sum)
    return numbers


def generateInitialPopulation():
    """
    Creates the same population as in the paper (Figure 3.2)
    """

    stags = [5, 4, 3, 0, 4, 9, 0, 3, 3, 5, 1, 7, 0, 3, 3]
    hinds = [9, 4, 2, 3, 5, 1, 2, 4, 1, 1, 3, 4, 2, 1, 6, 2]

    stags = generate_random_list(15, 100)
    hinds = generate_random_list(15, 100)

    population: List[Deer] = []

    for age, count in enumerate(stags):
        for _ in range(count):
            population.append(Deer(age, False, True))
    for age, count in enumerate(hinds):
        for _ in range(count):
            population.append(Deer(age, True, False))

    return population


def runSimulation(
    parameters: ModelParameters,
    huntingStrategy: HuntingParameters,
    samples=100,
    years=100,
):

    population_df = pd.DataFrame(
        columns=[
            "iteration",
            "year",
            "num_individuals",
            "num_stags",
            "num_hinds",
            "age_distribution",
        ]
    )

    for i in range(samples):
        population = generateInitialPopulation()
        for t in range(years):
            population = grow(population)
            population = reproduce(population, parameters)
            population = naturalDeath(population, parameters)
            population = hunting(population, parameters, huntingStrategy)

            num_individuals = len(population)
            num_stags = sum(1 for individual in population if individual.isMale)
            num_hinds = sum(1 for individual in population if individual.isFemale)
            age_distribution = [individual.age for individual in population]

            year_data = pd.DataFrame(
                {
                    "iteration": [i],
                    "year": [t],
                    "num_individuals": [num_individuals],
                    "num_stags": [num_stags],
                    "num_hinds": [num_hinds],
                    "age_distribution": [age_distribution],
                }
            )

            population_df = pd.concat([population_df, year_data], ignore_index=True)

    return population_df


def main():
    pass
