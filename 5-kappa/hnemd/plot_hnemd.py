import matplotlib.pyplot as plt
import numpy as np

kappa=np.loadtxt('kappa.out')

M=1000
Ns=kappa.shape[0]//M
t=np.arange(M) # ps
kappa=np.sum(kappa[:,2:4],axis=1)
kappa=kappa.reshape((Ns,M))
kappa_cum=np.zeros((Ns,M))
for ns in range(Ns):
    kappa_cum[ns,:] = np.cumsum(kappa[ns,:])/np.arange(1,M+1)

print('Ns=',Ns)
print('kappa=',np.mean(kappa_cum[:,-1]),'+-',np.std(kappa_cum[:,-1])/np.sqrt(Ns))

mean_kappa = np.mean(kappa_cum[:, -1])
std_error_kappa = np.std(kappa_cum[:, -1]) / np.sqrt(Ns)

plt.figure(figsize=(9, 8))
mean_kappa_curve = np.mean(kappa_cum,axis=0)
plt.plot(2*t, kappa_cum.transpose(), '--', linewidth=1.5)
plt.plot(2*t, mean_kappa_curve, '-', linewidth=4, label='Ave')
plt.plot(2*t, mean_kappa_curve + std_error_kappa, 'k--', linewidth=2.5, label='Err')
plt.plot(2*t, mean_kappa_curve - std_error_kappa, 'k--', linewidth=2.5)
#plt.title('(b)', fontsize=25)
plt.xlabel('Time (ps)', fontsize=30, fontweight='semibold')
plt.ylabel(r'$\boldsymbol{\kappa}$ (W m$^{\boldsymbol{-1}}$ K$^{\boldsymbol{-1}}$)', fontsize=30, fontweight='semibold')
text_str = f'$\\boldsymbol{{\\kappa}} \\boldsymbol{{=}} \\mathbf{{{mean_kappa:.2f}}} \\boldsymbol{{\\pm}} \\mathbf{{{std_error_kappa:.2f}}}$'
plt.text(0.5, 0.05, text_str, transform=plt.gca().transAxes, fontsize=25, verticalalignment='center', horizontalalignment='center')
plt.xticks(fontsize=25, fontweight='semibold')
plt.yticks(fontsize=25, fontweight='semibold')
ax = plt.gca()
ax.spines['bottom'].set_linewidth(2.5)
ax.spines['left'].set_linewidth(2.5)
ax.spines['top'].set_linewidth(2.5)
ax.spines['right'].set_linewidth(2.5)
ax.tick_params(axis='both', which='major', width=2.5, length=8, labelsize=25)
plt.legend(fontsize=25, loc='best',  prop={'size':25, 'weight': 'bold'})
plt.ylim(-0.65,14.75)
plt.tight_layout()
#plt.show()
#plt.savefig('fig-hnemd-500.png')
plt.savefig('fig-hnemd-500.pdf', format='pdf', transparent=True)
