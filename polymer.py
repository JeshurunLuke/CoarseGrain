import numpy as np
from subprocess import call, Popen, PIPE
import os
bondlen = [3.4, 3.4]
nf = 0.025
def main():
    
    polymerize(5, 5)
    boxinit(5, 3, 3)
def boxinit(H,P, NP):
    volpol = NP*(4/3*H*(np.pi*bondlen[0]/2)**2 + 4/3*P*(np.pi*bondlen[1]/2)**2)
    boxvol = (volpol*NP**3)/(nf)*1.2
    len = np.cbrt(boxvol)
    len = 180.0
    print(f"Box paramater: {len}")
    with open("system.lt", "w") as f:
        f.write('import "output_file.lt\"\n')
        f.write('write_once("Data Boundary") {\n')
        f.write(f'\t0 {len} xlo xhi \n\t0 {len}  ylo yhi\n\t0 {len}  zlo zhi\n ')
        f.write('}\n')
        f.write(f'polymers = new Polymer [{NP}].move({len/NP}, 0, 0) \n\t[{NP}].move(0, {len/NP} , 0) \n\t[{NP}].move(0, 0, {len/NP})')
    run()

def run():
    p = Popen('moltemplate.sh system.lt -atomstyle full', shell=True)  
    p.wait()
    Popen(['cp', '../system.in', './'])


def polymerize(H,P):
    polist = []    
    for i in range(0, H):
        polist.append('H')
    for i in range(0, P):
        polist.append('P')

    monlist(polist)
    bondlist(polist)
    filenames = ["polback.txt", "tmpmon.txt", "tmpbond.txt"]

    with open("output_file.lt", "w") as outfile:
        for filename in filenames:
            with open(filename) as infile:
                outfile.write(infile.read())
        outfile.write('}')
        outfile.close()

def monlist(polist):
    with open('tmpmon.txt', 'w') as f:
        for i,mon in enumerate(polist):
            if i < len(polist)-1:
                if polist[i + 1] == 'H':
                    f.write(f'  mon{i} = new {mon}.rot({i%2*180.0}, {i%2*1},0,0).move({i*bondlen[0]},0,0)\n')
                else:
                    f.write(f'  mon{i} = new {mon}.rot({i%2*180.0}, {i%2*1},0,0).move({i*bondlen[1]},0,0)\n')
            else:
                if polist[i - 1] == 'H':
                    f.write(f'  mon{i} = new {mon}.rot({i%2*180.0}, {i%2*1},0,0).move({i*bondlen[0]},0,0)\n')
                else:
                    f.write(f'  mon{i} = new {mon}.rot({i%2*180.0}, {i%2*1},0,0).move({i*bondlen[1]},0,0)\n')

        f.close()

def bondlist(polist):
    with open('tmpbond.txt', 'w') as f:
        f.write('  write("Data Bond List") {\n')
        for i in range(1, len(polist)-1):
            f.write(f'  \t$bond:backbone{i}\t$atom:mon{i}/ca\t$atom:mon{i+1}/ca\n')
        f.write('  }\n')
        f.close()
main()