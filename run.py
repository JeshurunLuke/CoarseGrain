from subprocess import call, Popen, PIPE
import os
import numpy as np
LAMMPS_EXEC = os.environ.get('LAMMPS_EXEC')
MOL_EXEC =  os.environ.get('MOL_EXEC')
def main():

    initialize('system.lt')

    equilibrate()

    assembly()
def call_lammps():
    p = Popen(['mpirun','-np', '3', 'lmp_mpi', '-in', 'system.in'])  

    p.wait()
def initialize(file):
    p1 = Popen(['rm', '-r', './movie'], stdout=PIPE)
    p2 = Popen(['rm','-r',  './trajs'], stdout=PIPE)
    p1.wait()
    p2.wait()
    print("Initializing")
    Popen(['mkdir', 'movie'], stdout=PIPE)
    Popen(['mkdir', 'trajs'], stdout=PIPE)
    

#Change box length iteratively 
'''
Possible Variations: Create a .txt file expanding on the terms and equilibrate a run per one
'''
def equilibrate():
    print("Equilibrating")

def assembly():
    print("Assembling")
    epsbb = np.arange(0.059, 0.56, 0.001)

    for i, j in enumerate(epsbb):
        call_lammps()
        update("system.in.settings", j)

        save(i)

def save(i):
    p = Popen(["mv", "./movie.mpg", f'./movie/movie{i}.mpg'], stdout =PIPE)
    p1 = Popen(["mv", "./dump.soft", f'./trajs/dump{i}.soft'], stdout =PIPE)

def update(file, epsbb):
    a_file = open(file, "r") 
    lines = a_file.readlines()
    
    a_file.close()       
    #del lines[-1]
    new_file = open(file, "w+")
    i = 1
    for line in lines:
        if i == 1:
            new_file.write(f"pair_coeff  1  2      {epsbb} 1.0 2.5\n")
            i += 1
        else:
            new_file.write(line)

    new_file.close()
main()