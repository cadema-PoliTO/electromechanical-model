close all
clear all
clc

mu0 =  4*pi*10^(-7); %[H/m] Vacuum magnetic permeability
S = 0.001;           %[m^2] Section of the ferromagnet
x0 = 0.02;           %[m]   Initial displacement
N = 1000;            %[-]   Number of windings
k = 10000;            %[N/m] Elastic constant
c = 0.5;             %[Ns/m]Mechanical damper
m = 2;               %[kg]  Mass
R_m = 1.8833;        %[Ohm] Resistance of the magnetic circuit
R_s = 0;             %[Ohm] Resistance of the power supply
L_s = 0;             %[H]   Inductance of the power supply
V_s = 10;        %[V]   Fem of the power supply
open('ElectromechanicalProblem_Sim.slx')
sim('ElectromechanicalProblem_Sim.slx')
figure (1)
plot(ans.i_m)
xlabel('t[s]');
ylabel('i [A]');
figure(2)
plot(ans.x_dot)
xlabel('t[s]');
ylabel('dx/dt [m/s]');
figure(3)
plot(ans.x)
xlabel('t[s]');
ylabel('x [m]');

% figure (1)
% plot(a.times,a.iA)
% figure(2)
% plot(a.times,a.xdotms)
% x=-a.f_elN/10000;
% figure(3)
% plot(a.times,x)