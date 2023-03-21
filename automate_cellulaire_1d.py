import numpy as np
import time
import matplotlib.pyplot as plt
import sys

# initialization of MPI communication
from mpi4py import MPI

comm = MPI.COMM_WORLD
process = MPI.COMM_WORLD.Get_rank()
numProcess = MPI.COMM_WORLD.Get_size()
# command to run on terminal
# mpirun -n 8 /bin/python3 /home/tr0fin0/Downloads/tmp_OS202/setup.py

nombre_cas: int = 256
nb_cellules: int = 360  # Cellules fantomes
nb_iterations: int = 360

compute_time = 0.
display_time = 0.


# add "./images/" to saving path to store all images separately from the main code.
def save_as_md(cells, symbols='⬜⬛'):
    res = np.empty(shape=cells.shape, dtype='<U')
    res[cells == 0] = symbols[0]
    res[cells == 1] = symbols[1]
    np.savetxt(f'./images/resultat_{num_config:03d}.md',
               res,
               fmt='%s',
               delimiter='',
               header=f'Config #{num_config}',
               encoding='utf-8')


def save_as_png(cells):
    fig = plt.figure(figsize=(nb_iterations / 10., nb_cellules / 10.))
    ax = plt.axes()
    ax.set_axis_off()
    ax.imshow(cells[:, 1:-1], interpolation='none', cmap='RdPu')
    plt.savefig(f"./images/resultat_{num_config:03d}.png",
                dpi=100,
                bbox_inches='tight')
    plt.close()

# creating buffers to save variables between the communication
sendbufC = np.zeros(1)  # buffer saving local Calculs time
sendbufD = np.zeros(1)  # buffer saving local Display time
recvbufC = np.zeros(1)  # buffer saving global Calculs time by Reduce function
recvbufD = np.zeros(1)  # buffer saving global Display time by Reduce function


# on this approach each process will receive a part of the "nombre_cas"
# in function of it's rank and size of MPI in such a manner that each 
# process will receive an almost equal sized number of possibilites to calcule.

startRange = int(process * nombre_cas // numProcess)
endRange = int((process + 1) * nombre_cas // numProcess - 1)

for num_config in range(startRange, endRange):
# for num_config in range(nombre_cas):
    t1 = time.time()
    cells = np.zeros((nb_iterations, nb_cellules + 2), dtype=np.int16)
    cells[0, (nb_cellules + 2) // 2] = 1
    for iter in range(1, nb_iterations):
        vals = np.left_shift(
            1, 4 * cells[iter - 1, 0:-2] + 2 * cells[iter - 1, 1:-1] +
            cells[iter - 1, 2:])
        cells[iter, 1:-1] = np.logical_and(np.bitwise_and(vals, num_config), 1)
    t2 = time.time()
    # compute_time += t2 - t1
    sendbufC[0] += t2 - t1

    t1 = time.time()
    save_as_md(cells)  # save quicker
    # save_as_png(cells)  # save longer
    t2 = time.time()
    # display_time += t2 - t1
    sendbufD[0] += t2 - t1

# prints were removed to improve usability of the output of code.
# print(f'{process}/{numProcess}')
# print(f"Temps calcul des generations de cellules : {compute_time:.6g} s")
# print(f"Temps d'affichage des resultats : {display_time:.6g} s")

# after the calculation the times of calculation and display were reduce, in other words summed,
# into the same variable.
comm.Reduce(sendbufC, recvbufC, op=MPI.SUM, root=0)
comm.Reduce(sendbufD, recvbufD, op=MPI.SUM, root=0)


if process == 0:
    print(f"| MPI 1 [{numProcess}] | {recvbufC[0]:.6g} | {recvbufD[0]:.6g} |")
