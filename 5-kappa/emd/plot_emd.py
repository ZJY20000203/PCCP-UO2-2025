import matplotlib.pyplot as plt
import numpy as np

hac=np.loadtxt('hac.out')

M=500
Ns=hac.shape[0]//M
t=hac[0:M,0] # ps
kappa=np.sum(hac[:,6:],axis=1)/3
kappa=kappa.reshape((Ns,M))

print('Ns=',Ns)
print('kappa=',np.mean(kappa[:,-1]),'+-',np.std(kappa[:,-1])/np.sqrt(Ns))

mean_kappa = np.mean(kappa[:, -1])
std_error_kappa = np.std(kappa[:, -1]) / np.sqrt(Ns)

plt.figure(figsize=(9, 8))
plt.plot(t, kappa.transpose(), '--',color=(0.7,0.7,0.7), linewidth=1.5)
mean_kappa_curve = np.mean(kappa,axis=0)
plt.plot(t, mean_kappa_curve, '-', linewidth=4, label='Ave')
plt.plot(t, mean_kappa_curve + std_error_kappa, 'k--', linewidth=2.5, label='Err')
plt.plot(t, mean_kappa_curve - std_error_kappa, 'k--', linewidth=2.5)
plt.xlabel('Correlation time (ps)', fontsize=30, fontweight='semibold')
plt.ylabel(r'$\boldsymbol{\kappa}$ (W m$^{\boldsymbol{-1}}$ K$^{\boldsymbol{-1}}$)', fontsize=30, fontweight='semibold')
plt.xticks(fontsize=25, fontweight='semibold')
plt.yticks(fontsize=25, fontweight='semibold')
text_str = f'$\\boldsymbol{{\\kappa}} \\boldsymbol{{=}} \\mathbf{{{mean_kappa:.2f}}} \\boldsymbol{{\\pm}} \\mathbf{{{std_error_kappa:.2f}}}$'
plt.text(0.5, 0.05, text_str, transform=plt.gca().transAxes, fontsize=25, verticalalignment='center', horizontalalignment='center')
plt.legend(fontsize=25, loc='best',  prop={'size':25, 'weight': 'bold'})
ax = plt.gca()
ax.spines['bottom'].set_linewidth(2.5)
ax.spines['left'].set_linewidth(2.5)
ax.spines['top'].set_linewidth(2.5)
ax.spines['right'].set_linewidth(2.5)
ax.tick_params(axis='both', which='major', width=2.5, length=8, labelsize=25)
plt.tight_layout()
#plt.show()
plt.savefig('fig-emd-500.pdf', format='pdf', transparent=True)

