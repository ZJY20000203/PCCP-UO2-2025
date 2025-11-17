import os
import numpy as np
from pylab import *
from ase.io import read, write

cx, cy, cz = 2, 2, 2
npoints = 700

special_points = {
    'G': [0, 0, 0],
    'X': [0.5, 0, 0.5],
    'K': [0.375, 0.375, 0.75],
    'G': [0, 0, 0],
    'L': [0.5, 0.5, 0.5],
    'X': [0.5, 0, 0.5],
    'W': [0.5, 0.25, 0.75],
    'G': [0, 0, 0]
}
points_path = ['GXKGLXWG']

uc = read('POSCAR-unitcell')
struc = uc * (cx, cy, cz)
write("model.xyz", struc)

with open('basis.in', 'w') as f:
    f.write(f"{len(uc)}\n")
    for i, mass in enumerate(uc.get_masses()):
        f.write(f"{i} {mass}\n")
    for _ in range(cx * cy * cz):
        for i in range(len(uc)):
            f.write(f"{i}\n")

npaths = len(points_path)
lengths = [len(path) - 1 for path in points_path]
path_ratio = [float(length / sum(lengths)) for length in lengths]
if npoints % sum(lengths) != 0:
    raise ValueError(f"npoints should be a multiple of {sum(lengths) * 100}")

gpumd_kpts, kpaths, sym_points_list, labels_list = [], [], [], []
for i in range(npaths):
    npts = int(path_ratio[i]*npoints)
    path = uc.cell.bandpath(path=points_path[i], npoints=npts, special_points=special_points)
    kpath, sym_points, labels = path.get_linear_kpoint_axis()
    kpaths.append(kpath)
    sym_points_list.append(sym_points)
    labels_list.append(labels)
    kpts = np.matmul(path.kpts, uc.cell.reciprocal() * 2 * np.pi)
    kpts[np.abs(kpts) < 1e-15] = 0.0
    gpumd_kpts = kpts if i == 0 else np.vstack((gpumd_kpts, kpts))
np.savetxt('kpoints.in', gpumd_kpts, header=str(npoints), comments='', fmt='%g')

whole_kpaths, whole_sym_points = [], []
origin_kpaths, origin_sym_points = 0, 0
for i in range(len(kpaths)):
    if i == 0:
        whole_kpaths.extend(kpaths[i])
        origin_kpaths = kpaths[i][-1]
        whole_sym_points.extend(sym_points_list[i])
        origin_sym_points = sym_points_list[i][-1]
    else:
        adjusted_kpaths = [x + origin_kpaths for x in kpaths[i]]
        whole_kpaths.extend(adjusted_kpaths)
        origin_kpaths += kpaths[i][-1]
        adjusted_sym_points = [x + origin_sym_points for x in sym_points_list[i]]
        whole_sym_points.extend(adjusted_sym_points)
        origin_sym_points += sym_points_list[i][-1]
whole_sym_points = sorted(set(whole_sym_points))

data = np.loadtxt("omega2.out")
for i in range(len(data)):
    for j in range(len(data[0])):
        data[i, j] = np.sqrt(abs(data[i, j])) / (2 * np.pi) * np.sign(data[i, j])
nu = data

figure(figsize=(8.5, 6))
ax = gca()
for spine in ax.spines.values():
    spine.set_linewidth(2)
gca().set_xticks(whole_sym_points)
gca().set_xticklabels([r'$\boldsymbol{\Gamma}$', 'X', 'K', r'$\boldsymbol{\Gamma}$', 'L', 'X', 'W', r'$\boldsymbol{\Gamma}$'][:len(whole_sym_points)], fontsize=20, fontweight='semibold')

if os.path.exists('dft-phon.dat'):
    data_vasp = np.loadtxt('dft-phon.out')
    vasp_path = data_vasp[:, 0] / max(data_vasp[:, 0]) * whole_kpaths[-1]
    scatter(vasp_path, data_vasp[:, 1], marker='o', edgecolors='C1', facecolors='none', linewidths=2, s=30, label='DFT')

for i in range(nu.shape[1]):
    if i == 0:
        plot(whole_kpaths, nu[:, i], color='C0', lw=3.5, label='NEP')
    else:
        plot(whole_kpaths, nu[:, i], color='C0', lw=3.5)

legend(fontsize=17, loc='best',  prop={'size':'17', 'weight': 'semibold'})
xlim([0, whole_kpaths[-1]])
for sym_point in whole_sym_points[1:-1]:
    plt.axvline(sym_point, color='black', linestyle='--', linewidth=2)
ylim([0, 20])
yticks_vals = linspace(0, 20, 5)
ax.set_yticks(yticks_vals)
ytick_objs = ax.set_yticklabels([f'{y:.0f}' for y in yticks_vals], fontsize=25, fontweight='semibold')
ylabel(r'Frequency (THz)', fontsize=20, fontweight='semibold')
tick_params(axis='x', which='both', direction='in', length=6, width=2)
tick_params(axis='y', which='both', direction='in', length=6, width=2, labelsize=15)
savefig('phonon.png', dpi=500, bbox_inches='tight')
#savefig('phonon.pdf', format='pdf', transparent=True)

