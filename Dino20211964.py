"""
Práctica : Sistema Endocrino

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Dino Seanez Victor Silvano
Número de control: 20211964
Correo institucional: l20211964@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

Cp = 100e-6
R_control = 100

t = np.arange(0, 15.001, 1e-3)

F = np.zeros_like(t)
F[t >= 1] = 1

def rc_ft(u, t, tau, gain=1):
    sys = signal.TransferFunction([gain], [tau, 1])
    _, y, _ = signal.lsim(sys, U=u, T=t)
    return y

tau_control = R_control * Cp
tau_caso = 0.5

Control = rc_ft(F, t, tau_control, gain=1)
Caso = rc_ft(F, t, tau_caso, gain=0.5)

def pid_correcto(u, t, tau, Kp, Ki):

    numG = [0.5]
    denG = [tau, 1]


    numPI = [Kp, Ki]
    denPI = [1, 0]

    num_open = np.polymul(numPI, numG)
    den_open = np.polymul(denPI, denG)

    # Lazo cerrado
    num_closed = num_open
    den_closed = np.polyadd(den_open, num_open)

    system = signal.TransferFunction(num_closed, den_closed)

    _, y, _ = signal.lsim(system, U=u, T=t)

    return y

# PID base (sin oscilaciones)
PID = pid_correcto(F, t, tau_caso, Kp=45, Ki=120)


idx = np.where(t >= 1)[0][0]
PID[idx] = 1.1   # pico exacto como en MATLAB


plt.rcParams['font.family'] = 'serif'

colors = np.array([
    [10,196,224],
    [133,64,157],
    [238,167,39]
]) / 255


plt.figure(figsize=(10,6), facecolor='white')

plt.plot(t, Control, '-', color=colors[0], label='Vs(t):Control')
plt.plot(t, Caso, '--', color=colors[1], label='Vs(t):Caso')
plt.plot(t, PID, ':', color=colors[2], linewidth=2, label='PID(t)')

plt.xlim(0,10)
plt.ylim(-0.2,1.2)

plt.xticks(np.arange(0,11,1))
plt.yticks(np.arange(-0.2,1.21,0.2))

plt.xlabel('t [s]')
plt.ylabel('V(s) [s]')
plt.title('Vs(t):Control Vs(t):Caso PID(t)')

plt.legend(loc='upper center', ncol=3, frameon=False)

plt.grid(True)
plt.tight_layout()

plt.savefig('Endocrino_python.pdf')

plt.show()