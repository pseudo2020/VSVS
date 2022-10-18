import random as r
import matplotlib.pyplot as plt


class NoChildError(Warning):
    def __init__(self, arg):
        self.args = arg


class Virus(object):
    def __init__(self, max_birth_prob: float, clear_prob: float):
        self.max_birth_prob: float = max_birth_prob
        self.clear_prob: float = clear_prob

    def does_clear(self) -> bool:
        p: float = r.random()
        return p > self.clear_prob

    def reproduce(self, pop_density: float) -> 'Virus':
        reproduction_prod: float = self.max_birth_prob * (1 - pop_density)
        if reproduction_prod > self.max_birth_prob:
            return Virus(self.max_birth_prob, self.clear_prob)
        raise NoChildError("no virus reproduced")


class Patient(object):
    def __init__(self, viruses: ['Virus'], max_pop: int):
        self.viruses: ['Virus'] = viruses
        self.max_pop: int = max_pop
        self.pop_density: float = self.get_total_population() / self.max_pop

    def get_total_population(self) -> int:
        return len(self.viruses)

    def update(self) -> int:
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
