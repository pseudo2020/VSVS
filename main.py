import simplev as v
import matplotlib.pyplot as plt


def main():
    sim = v.Simulation()
    sim.run()
    plot_sim_results(sim.results, sim.timesteps)
    return


def plot_sim_results(results: [int], timesteps: int):
    plt.plot(range(timesteps), results)
    plt.title("Virus population in patient over time.")
    plt.ylabel('Population')
    plt.xlabel('Time')
    plt.show()
    return


if __name__ == '__main__':
    main()
