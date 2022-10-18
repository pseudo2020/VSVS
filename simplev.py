import random as r
import matplotlib.pyplot as plt


class NoChildError(Warning):
    def __init__(self, arg):
        self.args = arg


class Virus(object):
    """
    Representation of a simple virus (does not model drug effects/resistance)
    """

    def __init__(self, max_birth_prob: float, clear_prob: float):
        """
        Initialises an instance of Virus.

        max_birth_prob: Maximum reproduction probability (a float between 0-1).
        clear_prob: Maximum clearance probability (a float between 0-1).
        """
        self.max_birth_prob: float = max_birth_prob
        self.clear_prob: float = clear_prob

    def does_clear(self) -> bool:
        """
        Determines whether virus is cleared from host.

        returns: Using a random number generator (random.random()), this method
        returns True with probability self.clear_prob
        and otherwise returns False.
        """
        p: float = r.random()
        return p > self.clear_prob

    def reproduce(self, pop_density: float) -> 'Virus':
        """
        Determines whether this virus particle reproduces at a time step.
        Called by the update() method in the simple_patient and
        Patient classes. The virus particle reproduces with probability
        self.max_birth_prob * (1 - pop_density).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring Virus (which has the same max_birth_prob
        and clear_prob values as its parent).

        pop_density: the population density (a float), defined as the current
        virus population divided by the maximum population.

        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        max_birth_prob and clear_prob values as this virus.
        Raises a NoChildError if this virus particle does not reproduce.
        """
        reproduction_prod: float = self.max_birth_prob * (1 - pop_density)
        if reproduction_prod > self.max_birth_prob:
            return Virus(self.max_birth_prob, self.clear_prob)
        raise NoChildError("no virus reproduced")


class Patient(object):
    """
    Representation of a simplified patient.
    The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """

    def __init__(self, viruses: ['Virus'], max_pop: int):
        """
        Initialises an instance of Patient.

        viruses: the list representing the virus population
        (a list of Virus instances)

        max_pop: the maximum virus population for this patient (an integer)

        pop_density: defined as the current virus population
        divided by the maximum population (a float).
        """
        self.viruses: ['Virus'] = viruses
        self.max_pop: int = max_pop
        self.pop_density: float = self.get_total_population() / self.max_pop

    def get_total_population(self) -> int:
        """
        returns: The total virus population (an integer)
        """
        return len(self.viruses)

    def update(self) -> int:
        """
        Update the state of the virus population in this patient for
        a single time step. update() should execute the following
        steps in this order:

        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.

        - The current population density is calculated.
        This population density value is used until the next call to update()

        - Determine whether each virus particle should reproduce and add
        offspring virus particles to the list of viruses in this patient.

        returns: the total virus population after the update (an integer)
        """
        tmp = self.viruses.copy()
        for v in tmp:
            if not v.does_clear():
                self.viruses.remove(v)
        del tmp

        self.pop_density = self.get_total_population() / self.max_pop

        tmp = []
        for v in self.viruses:
            try:
                x = v.reproduce(self.pop_density)
            except NoChildError:
                pass
            else:
                tmp.append(x)
        self.viruses.extend(tmp)
        del tmp
        return self.get_total_population()


class Simulation(object):
    """
    Contains functionality to run simulation of simple virus
    infecting simple person. Uses the Virus class and Person class.
    """

    def __init__(self):
        self.timesteps = 300
        self.results = [None] * self.timesteps
        self.patient = Patient(
            viruses=[Virus(max_birth_prob=0.05, clear_prob=0.01)] * 1000,
            max_pop=10000)

        return

    def run(self):
        for i in range(self.timesteps):
            self.results[i] = self.patient.update()
        return

    def show_results(self):
        for x in self.results:
            print(f"{x}, ", end="")

    def plot(self):
        plt.plot(range(self.timesteps), self.results)
        plt.title("Virus population in patient over time.")
        plt.ylabel('Population')
        plt.xlabel('Time')
        plt.show()
        return
