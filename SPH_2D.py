import math

import numpy as np
import matplotlib.pyplot as plt
from sklearn import neighbors
from tqdm import tqdm

MAX_PARTICLES = 125
DOMAIN_WIDTH = 40
DOMAIN_HEIGHT = 80

PARTICLE_MASS = 1
ISOTROPIC_EXPONENT = 20
BASE_DENSITY = 1
SMOOTHING_LENGTH = 5
DYNAMIC_VISCOSITY = 0.5
DAMPING_COEFFICIENT = - 0.9
CONSTANT_FORCE = np.array([[0.0, -0.1]])

TIME_STEP_LENGTH = 0.01
N_TIME_STEPS = 100000
ADD_PARTICLES_EVERY = 50

FIGURE_SIZE = (4, 6)
PLOT_EVERY = 6
SCATTER_DOT_SIZE = 2_000

DOMAIN_X_LIM = np.array([
    SMOOTHING_LENGTH,
    DOMAIN_WIDTH - SMOOTHING_LENGTH
])
DOMAIN_Y_LIM = np.array([
    SMOOTHING_LENGTH,
    DOMAIN_HEIGHT - SMOOTHING_LENGTH
])
# (315 M) / (64 π L⁹)
NORMALIZATION_DENSITY = (
        (315 * PARTICLE_MASS) / (64 * np.pi * SMOOTHING_LENGTH ** 9)
)
# (− (45 M) / (π L⁶))
NORMALIZATION_PRESSURE_FORCE = (
        -(45 * PARTICLE_MASS) / (np.pi * SMOOTHING_LENGTH ** 6)
)
# (45 μ M) / (π L⁶)
NORMALIZATION_VISCOUS_FORCE = (
        (45 * DYNAMIC_VISCOSITY * PARTICLE_MASS) / (np.pi * SMOOTHING_LENGTH ** 6)
)


def main():
    n_particles = 0

    positions = np.zeros((n_particles, 2))
    velocities = np.zeros_like(positions)
    forces = np.zeros_like(positions)

    plt.style.use("dark_background")
    plt.figure(figsize=FIGURE_SIZE, dpi=160)

    for iter in tqdm(range(N_TIME_STEPS)):
        if iter % ADD_PARTICLES_EVERY == 0 and n_particles < MAX_PARTICLES:
            new_positions = np.array([
                [10 + np.random.rand(), DOMAIN_Y_LIM[1]],
                [15 + np.random.rand(), DOMAIN_Y_LIM[1]],
                [20 + np.random.rand(), DOMAIN_Y_LIM[1]],
            ])

            new_velocities = np.array([
                [-3.0, -15.0],
                [-3.0, -15.0],
                [-3.0, -15.0],
            ])

            n_particles += 3

            positions = np.concatenate((positions, new_positions), axis=0)
            velocities = np.concatenate((velocities, new_velocities), axis=0)

        neighbor_ids, distances = neighbors.KDTree(
            positions,
        ).query_radius(
            positions,
            SMOOTHING_LENGTH,
            return_distance=True,
            sort_results=True,
        )

        densities = np.zeros(n_particles)

        for i in range(n_particles):
            for j_in_list, j in enumerate(neighbor_ids[i]):
                densities[i] += NORMALIZATION_DENSITY * (
                        SMOOTHING_LENGTH ** 2 - distances[i][j_in_list] ** 2
                ) ** 3

        pressures = ISOTROPIC_EXPONENT * (densities - BASE_DENSITY)

        forces = np.zeros_like(positions)

        # clear elements
        neighbor_ids = [np.delete(x, 0) for x in neighbor_ids]
        distances = [np.delete(x, 0) for x in distances]

        for i in range(n_particles):
            for j_in_list, j in enumerate(neighbor_ids[i]):
                forces[i] += NORMALIZATION_PRESSURE_FORCE * (
                    - (positions[j] - positions[i])
                ) / distances[i][j_in_list] * (pressures[j] + pressures[i]) / (2 * densities[j]) * (
                                         SMOOTHING_LENGTH - distances[i][j_in_list]) ** 2

                forces[i] += NORMALIZATION_VISCOUS_FORCE * (velocities[j] - velocities[i]) / densities[j] * (
                            SMOOTHING_LENGTH - distances[i][j_in_list])

        forces += CONSTANT_FORCE
        velocities += TIME_STEP_LENGTH * forces / densities[:, np.newaxis]
        positions += TIME_STEP_LENGTH * velocities

        out_of_left_boundary = positions[:, 0] < DOMAIN_X_LIM[0]
        out_of_right_boundary = positions[:, 0] > DOMAIN_X_LIM[1]
        out_of_bottom_boundary = positions[:, 1] < DOMAIN_Y_LIM[0]
        out_of_top_boundary = positions[:, 1] > DOMAIN_Y_LIM[1]

        velocities[out_of_left_boundary, 0] *= DAMPING_COEFFICIENT
        positions[out_of_left_boundary, 0] = DOMAIN_X_LIM[0]

        velocities[out_of_right_boundary, 0] *= DAMPING_COEFFICIENT
        positions[out_of_right_boundary, 0] = DOMAIN_X_LIM[1]

        velocities[out_of_bottom_boundary, 1] *= DAMPING_COEFFICIENT
        positions[out_of_bottom_boundary, 1] = DOMAIN_Y_LIM[0]

        velocities[out_of_top_boundary, 1] *= DAMPING_COEFFICIENT
        positions[out_of_top_boundary, 1] = DOMAIN_Y_LIM[1]

        for force in forces:
            print(math.sqrt(force[0]**2 + force[1]**2))

        if iter & PLOT_EVERY == 0:
            pass
            # print(positions[:, 0], positions[:, 1])
            # plt.scatter(
            #     positions[:, 0],
            #     positions[:, 1],
            #     s=SCATTER_DOT_SIZE,
            #     c=positions[:, 1],
            #     cmap="Wistia_r",
            # )
            # plt.xlim(DOMAIN_X_LIM)
            # plt.ylim(DOMAIN_Y_LIM)
            # plt.xticks([], [])
            # plt.yticks([], [])
            # plt.tight_layout()
            # plt.draw()
            # plt.pause(0.0001)
            # plt.clf()


if __name__ == "__main__":
    main()
