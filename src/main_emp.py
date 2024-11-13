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
    def __init__(self, culling_data: dict):
        """
        culling_data: dict with year as key and a sub-dict of 'calves', 'matureHinds', 'matureStags' cull numbers
        Example:
            culling_data = {
                2005: {'calves': 160, 'matureHinds': 570, 'matureStags': 420},
                2006: {'calves': 200, 'matureHinds': 500, 'matureStags': 520},
                ...
            }
        """
        self.culling_data = culling_data



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


def hunting(population: List[Deer], year: int, huntingStrategy: HuntingParameters):
    # Retrieve yearly cull numbers from hunting strategy
    year_cull = huntingStrategy.culling_data.get(year, {'calves': 0, 'matureHinds': 0, 'matureStags': 0})
    
    calves = get_group(population, age=0)
    if len(calves) > year_cull['calves']:
        calves = calves[year_cull['calves']:]

    hinds = get_group(population, min_age=1, onlyFemale=True)
    if len(hinds) > year_cull['hinds']:
        hinds = hinds[year_cull['hinds']:]

    stags = get_group(population, min_age=1, onlyMale=True)
    if len(stags) > year_cull['stags']:
        stags = stags[year_cull['stags']:]

    # Rebuild population with remaining (surviving) deer after culling
    population = calves + hinds + stags
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
    Initializes the population based on empirical data for 2005:
    2000 stags, 4100 hinds, and 4100 calves.
    Distributes non-calves (stags and hinds) across ages 1-16 randomly,
    while calves are set to age 0.
    """
    total_stags = 2000
    total_hinds = 4100
    total_calves = 4100

    # Generate age distributions for stags and hinds (ages 1-16)
    stags_age_distribution = generate_random_list(16, total_stags)
    hinds_age_distribution = generate_random_list(16, total_hinds)

    # Initialize the population list
    population: List[Deer] = []

    # Add stags distributed randomly across ages 1-16
    for age, count in enumerate(stags_age_distribution, start=1):
        for _ in range(count):
            population.append(Deer(age, False, True))

    # Add hinds distributed randomly across ages 1-16
    for age, count in enumerate(hinds_age_distribution, start=1):
        for _ in range(count):
            population.append(Deer(age, True, False))

    # Add calves with age 0 (assuming a roughly equal male/female distribution)
    population.extend([Deer(0, True, False) for _ in range(total_calves // 2)])
    population.extend([Deer(0, False, True) for _ in range(total_calves // 2)])

    return population


def runSimulation(parameters: ModelParameters, huntingStrategy: HuntingParameters, samples=100, start_year=2005, end_year=2018):
    population_df = pd.DataFrame(columns=[
        "iteration", "year", "num_individuals", "num_stags", "num_hinds", "num_calves", "age_distribution"
    ])

    for i in range(samples):
        population = generateInitialPopulation()

        for year in range(start_year, end_year + 1):
            # Annual processes: grow, reproduce, natural death, hunting
            population = grow(population)
            population = reproduce(population, parameters)
            population = naturalDeath(population, parameters)
            population = hunting(population, year, huntingStrategy)

            # Collect statistics for the current population
            num_individuals = len(population)
            num_stags = sum(1 for individual in population if individual.isMale and individual.age > 0)
            num_hinds = sum(1 for individual in population if individual.isFemale and individual.age > 0)
            num_calves = sum(1 for individual in population if individual.age == 0)
            age_distribution = [individual.age for individual in population]

            year_data = pd.DataFrame({
                "iteration": [i],
                "year": [year],
                "num_individuals": [num_individuals],
                "num_stags": [num_stags],
                "num_hinds": [num_hinds],
                "num_calves": [num_calves],
                "age_distribution": [age_distribution],
            })

            population_df = pd.concat([population_df, year_data], ignore_index=True)

    return population_df



def main():
    pass
