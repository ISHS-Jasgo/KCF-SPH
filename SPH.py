"""
Simulates the free-surface flow of "pouring a beer" using Smoothed Particle
Hydrodynamics (SPH). Uses the super-simple approch of Matthias Müller:
https://matthias-research.github.io/pages/publications/sca03.pdf

Simulates the Navier-Stokes Momentum in Lagrangian Form

    ρ Du/Dt = − ∇p + μ ∇²u + g

u : velocity
ρ : density
p : pressure
μ : dynamics viscosity
g : gravity

Du/Dt : Lagrangian temporal derivative (=Material Derivative)
∇p    : Pressure Gradient
∇²u   : Velocity Laplacian (=collection of second derivatives)

IMPORTANT: The simulated fluid is not incompressible.

-------

Scenario

        +-------------------------+
        |      /  /  /            |
        |     /  /  /             |
        |    ↙  ↙  ↙              |
        |                         |
        |                         |
        |                         |
        |                         |
        |                         |
        |                         |
        |                         |
        |                         |
        |                         |
        |                         |
        |                         |
        +-------------------------+

-> A vertical Rectangular domain with all walls

-> New Particles enter the domain slightly below the top with a velocity
directed to the bottom left (like pouring in the beer)

----------

Solution Strategy:

Discretize the fluid by N particles (i=0, 1, ..., N-1) that smooth
their properties radially with some smoothing kernels. Then the Momentum
Equation discretizes to

Duᵢ/Dt = Pᵢ + Vᵢ + G

with

uᵢ : The velocity of the i-th smoothed particle
Pᵢ : The pressure forces acting on the i-th smoothed particle
Vᵢ : The viscosity forces acting on the i-th smoothed particle
G  : The gravity forces (acting equally on all particles)

This yields a set of N ODEs each for the two velocity components (in case
of 2D) of the particles. These can be solved using a (simpletic) integrator
to advance the position of the particles.


Let xᵢ be the 2D position of each smoothed particle.

Let L be the smoothing length of each smoothed particle.

Let M be the mass of each smoothed particle.

------

Algorithm

(for details on the chosen smoothing kernels, see the paper mentioned above)

1. Compute the rhs for each particle Fᵢ

    1.1 Compute the distances between all particle positions

        dᵢⱼ = || xᵢ − xⱼ ||₂

    1.2 Compute the density at each particle's position

        ρᵢ = (315 M) / (64 π L⁹) ∑ⱼ (L² − dᵢⱼ²)³

    1.3 Compute the pressure at each particle's position (κ is the isentropic
        exponent, ρ₀ is a base density)

        pᵢ = κ * (ρ − ρ₀)

    1.4 Compute the pressure force of each particle

        Pᵢ = (− (45 M) / (π L⁶)) ∑ⱼ − (xⱼ − xᵢ) / (dᵢⱼ) (pⱼ + pᵢ) / (2 ρⱼ) (L − dᵢⱼ)²

    1.5 Compute the viscosity force of each particle

        Vᵢ = (45 μ M) / (π L⁶) ∑ⱼ (uⱼ − uᵢ) / (ρⱼ) (L − dᵢⱼ)

    1.6 Add up the RHS

        Fᵢ = Pᵢ + Vᵢ + G

2. Integrate the Ordinary Differential Equation  "ρ Duᵢ/Dt = Fᵢ" with a
   Δt timestep

    2.1 Update the particles' velocities

        uᵢ ← uᵢ + Δt Fᵢ / ρᵢ

    2.2 Update the particles' positions

        xᵢ ← xᵢ + Δt uᵢ

3. Enforce the wall Boundary Conditions. If a particle leaves the
   domain then:

    3.1 Set its position to the Boundary

    3.2 Inverse its velocity component perpendicular to the wall

    3.3 Multiply the velocity component perpendicular to the
        wall with a damping factor

-------

Computational Considerations.

1. The steps on computing density, pressure force and viscosity force
   involve the computation of the various smoothing kernels. Those
   always consist of a constant part that is due to the normalization
   which can be precomputed.

2. When applying summations in the distance calculations and when
   applying the smothing kernels in density, pressure force and
   viscosity force calculations only OTHER PARTICLES IN THE
   SMOOTHING LENGTH OF THE CONSIDERED PARTICLE ARE RELEVANT. Hence,
   we can use efficient neighbor computation routines.

-------

Take care that the ODE integration can become instable when using too
large time steps.
"""