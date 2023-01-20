import random

from functools import reduce

class Product:

    def __init__(self, name: str, area: float, price:float):
        """
        Class to define a product.

        Attributes:
        -----------
        name: str
            product name

        area: float
            product size

        price: float
            product price
        """

        self.name = name
        self.area = area
        self.price = price

class Individual:

    def __init__(self, areas: list[float], prices: list[float], max_area: float = 3.0, gen: int = 0):
        """
        Class to define an individual.

        Attributes:
        -----------
        areas: list[float]
            products size

        prices: list[float]
            product prices

        max_area: float
            max area to travel

        gen: int
            index of generation
        """

        self.areas = areas
        self.prices = prices
        self.max_area = max_area
        self.gen = gen
        self.rate = 0
        self.chromosome = []
        self.used_area = 0

        # initialize chromosomes
        for i in range(len(areas)):
            self.chromosome.append(0 if random.random() < 0.5 else 1)

    def evaluate(self):
        """
        Method to evaluate individual.

        Parameters:
        -----------
        No parameters.

        Raises:
        -----------
        No raises.
        """

        rate = 0
        used_area = 0

        for i in range(len(self.chromosome)):
            if self.chromosome[i] == 1:
                rate = rate + self.prices[i]
                used_area = used_area + self.areas[i]

        # reset rate ir exced max area (penalty)
        if used_area > self.max_area:
            rate = 1

        self.rate = rate
        self.used_area = used_area

    def crossover(self, another):
        """
        Method to calculate genetic crossover

        Parameters:
        -----------
        another: Individual
            Individual to make crossover

        Raises:
        -----------
        No raises.
        """

        cut_off = round(random.random() * (len(self.chromosome) - 1))

        child_0 = another.chromosome[0:cut_off] + self.chromosome[cut_off::]
        child_1 = self.chromosome[0:cut_off] + another.chromosome[cut_off::]

        children = [
            Individual(areas=self.areas, prices=self.prices, gen=self.gen + 1),
            Individual(areas=self.areas, prices=self.prices, gen=self.gen + 1)
        ]

        children[0].chromosome = child_0
        children[1].chromosome = child_1

        return children

    def mutation(self, mutation_rate: float = 0.02):
        """
        Method to make mutation. It's necessary to don't have overfitting.

        Parameters:
        -----------
        mutation_rate: float
            Diversity rate.

        Raises:
        -----------
        No raises.
        """

        for i in range(len(self.chromosome)):
            # invert chromosome value
            if random.random() < mutation_rate:
                self.chromosome[i] = 0 if self.chromosome[i] == 1 else 1

        return self

class GA:

    def __init__(self, population_size: int, areas: list[float], prices: list[float], max_area: float = 3.0):
        """
        Class to define genetic algorithm.

        Attributes:
        -----------
        population_size: int
            Size of population.

        areas: list[float]
            products size

        prices: list[float]
            product prices

        max_area: float
            max area to travel
        """

        self.population_size = population_size
        self.areas = areas
        self.prices = prices
        self.max_area = max_area
        self.population = []
        self.gen = 0
        self.best = 0

    def init_population(self):
        """
        Initialize population with random sample.

        Parameters:
        -----------
        No parameters.

        Raises:
        -----------
        No raises.
        """

        for i in range(self.population_size):
            self.population.append(Individual(areas=self.areas, prices=self.prices, max_area=self.max_area))

        self.best = self.population[0]

    def sort(self):
        """
        Sort values in desc order.

        Parameters:
        -----------
        No parameters.

        Raises:
        -----------
        No raises.

        """

        self.population = sorted(self.population, key=lambda individual : individual.rate, reverse=True)

    def set_best(self, individual: Individual):
        """
        Compare two individuals and get best

        Parameters:
        -----------
        individual: Individual
            Individual to comparey myself.

        Raises:
        -----------
        No raises.

        """

        if individual.rate > self.best.rate:
            self.best = individual

    def get_parent(self):
        """
        Returns the individual with the highest probatility.

        Parameters:
        -----------
        No parameters.

        Raises:
        -----------
        No raises.

        """

        indexes = list(range(len(self.population)))
        rates = [individual.rate for individual in self.population]

        # sum total value
        total = reduce(lambda x, y : x + y, rates)

        # probatilities
        probas = [rate * 100 / total for rate in rates]

        return random.choices(population=indexes, weights=probas)[0]

    def solve(self, gen: int = 100, mutation_rate: float = 0.02):
        """
        Solve optimisation.

        Parameters:
        -----------
        gen: int
            Number of generations.

        mutation_rate: float
            Diversity rate.

        Raises:
        -----------
        No raises.

        """

        self.init_population()

        for g in range(gen):

            for individual in self.population:
                individual.evaluate()

            self.sort()

            # best individual
            best = self.population[0]
            self.set_best(best)

            new_population = []

            for individual in range(self.population_size // 2):
                p1 = self.get_parent()
                p2 = self.get_parent()

                children = self.population[p1].crossover(self.population[p2])
                new_population.append(children[0].mutation(mutation_rate=mutation_rate))
                new_population.append(children[1].mutation(mutation_rate=mutation_rate))

            self.population = list(new_population)

        return self.best

if __name__ == '__main__':
    products = []

    products.append(Product(name='Geladeira Dako', area=0.751, price=999.90))
    products.append(Product(name='iPhone 6', area=0.0000899, price=2911.12))
    products.append(Product(name='TV 55', area=0.400, price=4346.99))
    products.append(Product(name='TV 50', area=0.290, price=3999.90))
    products.append(Product(name='TV 42', area=0.200, price=2999.00))
    products.append(Product(name='Notebook Dell', area=0.00350, price=2499.90))
    products.append(Product(name='Ventilador Panasonic', area=0.496, price=199.90))
    products.append(Product(name='Microondas Eletrolux', area=0.0424, price=308.66))
    products.append(Product(name='Microondas LG', area=0.0544, price=429.90))
    products.append(Product(name='Microondas Panasonic', area=0.0319, price=299.29))
    products.append(Product(name='Geladeira Brastemp', area=0.635, price=899.00))
    products.append(Product(name='Geladeira Consul', area=0.870, price=1199.89))
    products.append(Product(name='Notebook Lenovo', area=0.498, price=1999.90))
    products.append(Product(name='Notebook Asus', area=0.527, price=3999.00))

    a, p = zip(*[(p.area, p.price) for p in products])

    ga = GA(population_size=20, areas=a, prices=p)

    result = ga.solve(gen=500, mutation_rate=0.02)

    print('Solved -> Gen: {}, Price: {}, Used Area: {}, Chromosome: {}'.format(result.gen, result.rate, result.used_area, result.chromosome))
