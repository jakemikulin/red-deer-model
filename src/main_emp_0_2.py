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
        probMale: float = 0.52,
        probFemale: float = 0.48,
        probYoungReproduce: float = 0.1,
        probMatureReproduce: float = 0.9,
    ):
        self.maxCapacityImpact = maxCapacityImpact  # c
        self.capacityCurveSlope = capacityCurveSlope  # a
        self.huntingLimit = huntingLimit  # l
        self.initialIndividuals = initialIndividuals  # i_init
        self.maximumIndividuals = maximumIndividuals  # i_max

        self.probMale = probMale  # p_o,m
        self.probFemale = probFemale  # p_o,f
        self.probYoungReproduce = (
            probYoungReproduce  # Reproduction function, page 18 was 0.3
        )
        self.probMatureReproduce = (
            probMatureReproduce  # Reproduction function, page 18 was 0.9
        )


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

        if deer.age == 1 or deer.age == 2:
            if random.random() < params.probYoungReproduce:
                male = False
                if random.random() < params.probMale:
                    male = True
                newDeer.append(Deer(0, not male, male))

        elif 2 < deer.age < 12:
            if random.random() < params.probMatureReproduce:
                male = False
                if random.random() < params.probMale:
                    male = True
                newDeer.append(Deer(0, not male, male))

    return population + newDeer


def calculateAgeBasedMortality(
    age: int,
) -> float:  # TODO: move some of these into model parameters

    # Calculates the mortality rate (p_{i,d}) based on age (i_a) using the provided formula.

    if 0 <= age <= 2:
        return 0.06  # From Blackmount DMP 6% calf mortality
    elif 2 < age < 16:
        return 0.02 + (0.03 / 14) * (age - 1)  # 0.03 + (0.05 / 14) * (age - 1)
    else:  # age >= 16
        return 0.08 * exp(2.0 * (age - 16))  # 0.08 * exp(2.47 * (age - 16))


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


def get_group(
    population: List[Deer],
    age: int = None,
    min_age: int = None,
    max_age: int = None,
    onlyMale: bool = False,
    onlyFemale: bool = False,
):
    filtered_population = []

    for deer in population:
        # Filter by specific age, if provided
        if age is not None and deer.age != age:
            continue

        # Filter by minimum age (inclusive), if provided
        if min_age is not None and deer.age < min_age:
            continue

        # Filter by maximum age (inclusive), if provided
        if max_age is not None and deer.age > max_age:
            continue

        # Filter by sex
        if onlyMale and not deer.isMale:
            continue
        if onlyFemale and not deer.isFemale:
            continue

        # If all conditions match, include the deer
        filtered_population.append(deer)

    return filtered_population


def hunting(
    population: List[Deer],
    year: int,
    huntingStrategy: HuntingParameters,
    params: ModelParameters,
):
    # Retrieve cull data for the current year
    year_cull = huntingStrategy.culling_data.get(
        year, {"calves": 0, "hinds": 0, "stags": 0}
    )

    # Cull calves
    calves = get_group(population, min_age=0, max_age=2)
    calf_cull_count = min(
        year_cull["calves"], len(calves)
    )  # Ensure we don't remove more than exist
    calves = calves[
        calf_cull_count:
    ]  # Keep only the remaining portion after removing the cull count

    # Cull hinds
    hinds = get_group(population, min_age=3, onlyFemale=True)
    hind_cull_count = min(year_cull["hinds"], len(hinds))
    hinds = hinds[
        hind_cull_count:
    ]  # Keep only the remaining portion after removing the cull count

    # Cull stags
    stags = get_group(population, min_age=3, onlyMale=True)
    stag_cull_count = min(year_cull["stags"], len(stags))
    stags = stags[
        stag_cull_count:
    ]  # Keep only the remaining portion after removing the cull count

    # Rebuild population with remaining deer
    population = calves + hinds + stags

    return population


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
    total_stags = 1800
    total_hinds = 3700
    total_calves = 3700

    # Generate age distributions for stags and hinds (ages 3-15)
    stags_age_distribution = [total_stags // 13] * 13
    hinds_age_distribution = [total_hinds // 13] * 13

    # Initialize the population list
    population: List[Deer] = []

    # Add stags distributed randomly across ages 3-16
    for age, count in enumerate(stags_age_distribution, start=3):
        for _ in range(count):
            population.append(Deer(age, False, True))

    # Add hinds distributed randomly across ages 3-16
    for age, count in enumerate(hinds_age_distribution, start=3):
        for _ in range(count):
            population.append(Deer(age, True, False))

    # Add calves distributed across ages 0, 1, 2 (e.g., equally)
    for age in range(3):  # Ages 0, 1, 2
        for _ in range(total_calves // 6):  # Divide equally between male/female and ages
            population.append(Deer(age, True, False))  # Female calves
            population.append(Deer(age, False, True))  # Male calves


    return population


def runSimulation(
    parameters: ModelParameters,
    huntingStrategy: HuntingParameters,
    samples=100,
    start_year=2005,
    end_year=2018,
):
    population_df = pd.DataFrame(
        columns=[
            "iteration",
            "year",
            "num_individuals",
            "num_stags",
            "num_hinds",
            "num_calves",
            "age_distribution",
        ]
    )

    for i in range(samples):
        population = generateInitialPopulation()

        # print(f"Starting {len(population)}")

        for year in range(start_year, end_year + 1):
            # Annual processes: grow, reproduce, natural death, hunting

            population = grow(population)
            print(f"Year {year}: {len(population)}")
            population = reproduce(population, parameters)
            print(f"Year {year}: {len(population)}")

            num_calves_before, num_stags_before, num_hinds_before = count_population(
                population
            )
            population = naturalDeath(population, parameters)
            num_calves_after, num_stags_after, num_hinds_after = count_population(
                population
            )
            percent_calves_died, percent_stags_died, percent_hinds_died = (
                calculate_death_percentages(
                    num_calves_before,
                    num_stags_before,
                    num_hinds_before,
                    num_calves_after,
                    num_stags_after,
                    num_hinds_after,
                )
            )

            print(f"Year {year}: {len(population)}")

            population = hunting(population, year, huntingStrategy, parameters)

            print(f"Year {year}: {len(population)}")

            num_individuals = len(population)
            num_stags = sum(
                1
                for individual in population
                if individual.isMale and individual.age >= 3
            )
            num_hinds = sum(
                1
                for individual in population
                if individual.isFemale and individual.age >= 3
            )
            num_calves = sum(1 for individual in population if individual.age <= 2)
            age_distribution = [individual.age for individual in population]
            average_age = (
                sum(age_distribution) / len(age_distribution) if age_distribution else 0 # TODO this includes 40% being age 0 calves
            )

            year_data = pd.DataFrame(
                {
                    "iteration": [i],
                    "year": [year],
                    "num_individuals": [num_individuals],
                    "num_stags": [num_stags],
                    "num_hinds": [num_hinds],
                    "num_calves": [num_calves],
                    "age_distribution": [age_distribution],
                    "calves_died_percentage": [percent_calves_died],
                    "stags_died_percentage": [percent_stags_died],
                    "hinds_died_percentage": [percent_hinds_died],
                    "avg_age": [average_age],
                }
            )

            population_df = pd.concat([population_df, year_data], ignore_index=True)

    return population_df


def calculate_death_percentages(
    num_calves_before,
    num_stags_before,
    num_hinds_before,
    num_calves_after,
    num_stags_after,
    num_hinds_after,
):
    percent_calves_died = (
        ((num_calves_before - num_calves_after) / num_calves_before) * 100
        if num_calves_before > 0
        else 0
    )
    percent_stags_died = (
        ((num_stags_before - num_stags_after) / num_stags_before) * 100
        if num_stags_before > 0
        else 0
    )
    percent_hinds_died = (
        ((num_hinds_before - num_hinds_after) / num_hinds_before) * 100
        if num_hinds_before > 0
        else 0
    )

    return percent_calves_died, percent_stags_died, percent_hinds_died


def count_population(population):
    num_calves_before = sum(1 for individual in population if individual.age <= 2)
    num_stags_before = sum(
        1 for individual in population if individual.isMale and individual.age >= 3
    )
    num_hinds_before = sum(
        1 for individual in population if individual.isFemale and individual.age >= 3
    )

    return num_calves_before, num_stags_before, num_hinds_before


def main():
    pass
