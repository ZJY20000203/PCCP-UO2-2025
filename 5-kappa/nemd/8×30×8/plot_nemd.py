import matplotlib.pyplot as plt
import numpy as np

M = 1000
data = np.loadtxt('compute.out')
dEdt1 = data[-1, -1] / 2000  # eV/ps
dEdt2 = -data[-1, -2] / 2000  # eV/ps
A = 4.297984 ** 2  # nm^2
dT = np.mean(data[500:, 1]) - np.mean(data[500:, 12])  # K
G = np.array((1.602177e+2 * dEdt1 / A / dT, 1.602177e+2 * dEdt2 / A / dT))

print('G =', np.mean(G), '+-', np.std(G) / np.sqrt(2))

fig, axs = plt.subplots(1, 2, figsize=(12, 6))

for ax in axs:
    ax.spines['top'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)

def set_tick_labels(ax, fontsize=18, fontweight='550'):
    for tick_label in ax.get_xticklabels() + ax.get_yticklabels():
        tick_label.set_fontsize(fontsize)
        tick_label.set_fontweight(fontweight)

for ax in axs:
    set_tick_labels(ax)

axs[0].plot(np.arange(1, 13), np.mean(data[500:, 1:13], axis=0), '-o', linewidth=3)
#axs[0].set_title('(a)', fontsize=25, fontweight='550')
axs[0].set_xlabel('Group index', fontsize=25, fontweight='550')
axs[0].set_ylabel('Temperature (K)', fontsize=25, fontweight='550')
axs[0].tick_params(axis='both', labelsize=18, width=2.5, length=5)
axs[0].set_xticks(np.arange(1, 13))

axs[1].plot(2*np.arange(M), data[:, -2]/1000, '-', linewidth=3, label='Heat Source')
axs[1].plot(2*np.arange(M), data[:, -1]/1000, '--', linewidth=3, label='Cold Sink')
#axs[1].set_title('(b)', fontsize=25, fontweight='550')
axs[1].set_xlabel('Time (ps)', fontsize=25, fontweight='550')
axs[1].set_ylabel(r'Energy (×10$^{\boldsymbol{3}}$ eV)', fontsize=25, fontweight='550')
axs[1].tick_params(axis='both', labelsize=18, width=2.5, length=5)
axs[1].legend(prop={'size': 18, 'weight': 'bold'})

plt.tight_layout()
plt.savefig('fig-500-nemd.jpg', format='jpg', dpi=500)
plt.show()
