clear all
close all
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
V_s = 10;            %[V]   Fem of the power supply

np = 30;
x = linspace(0.005,0.03,np).';      %[m]
i = linspace(0.001,6,np).';         %[A]

G = mu0*N^2*S;

for countx = 1:30
    for counti = 1:30
        F_input(counti,countx) = -1/4*G*i(counti,1)^2/x(countx,1)^2;  %[N]
        lamda_input(counti,countx) = 1/2*G*i(counti,1)/x(countx,1);%[Wb]
%         l_di(counti,countx) = 1/2*G/x(countx,1);
%         l_dx(counti,countx) = -1/2*G*i(counti,1)/x(countx,1)^2;
    end
end

% Compute the derivatives of lamda
dx = (x(end,1)-x(1,1))/np;
di = (i(end,1)-i(1,1))/np;
[lamda_dx, lamda_di] = gradient(lamda_input, dx,di);
 

[X,Y] = meshgrid(x,i);
figure(1)
surf(X,Y,F_input)
xlabel('i [A]')
ylabel('x [m]')
zlabel('F [N]')
title('Force of the magnetic field')
figure(2)
surf(X,Y,lamda_input)
xlabel('i [A]')
ylabel('x [m]')
zlabel('lamda [Wb]')
title('Magnetic flux')
figure(3)
surf(X,Y,lamda_dx)
xlabel('i [A]')
ylabel('x [m]')
zlabel('dlamda/dx [Wb/m]')
title('Derivative of the magnetic flux with respect the to displacement')
figure(4)
surf(X,Y,lamda_di)
xlabel('i [A]')
ylabel('x [m]')
zlabel('dlamda/di [Wb/A]')
title('Derivative of the magnetic flux with respect the to current')

% Save .csv files
F_col = reshape(F_input,np*np,1);
X_col = reshape(X,np*np,1);
Y_col = reshape(Y,np*np,1);
M_F(:,1) = Y_col;
M_F(:,2) = X_col;
M_F(:,3) = F_col;
csvwrite('F.csv',M_F)

% lamda_di_col = reshape(l_di,np*np,1);
lamda_di_col = reshape(lamda_di,np*np,1);
X_col = reshape(X,np*np,1);
Y_col = reshape(Y,np*np,1);
M_lamda_di(:,1) = Y_col;
M_lamda_di(:,2) = X_col;
M_lamda_di(:,3) = lamda_di_col;
csvwrite('lamda.csv',M_lamda_di)

% lamda_dx_col = reshape(l_dx,np*np,1);
lamda_dx_col = reshape(lamda_dx,np*np,1);
X_col = reshape(X,np*np,1);
Y_col = reshape(Y,np*np,1);
M_lamda_dx(:,1) = Y_col;
M_lamda_dx(:,2) = X_col;
M_lamda_dx(:,3) = lamda_dx_col;
csvwrite('lamda.csv',M_lamda_dx)

% Open and run Simulink
open('ElectromechanicalProblem_Sim_interpolation.slx')
sim('ElectromechanicalProblem_Sim_interpolation.slx')


figure (5)
plot(ans.i_m)
xlabel('t[s]');
ylabel('i [A]');
figure(6)
plot(ans.x_dot)
xlabel('t[s]');
ylabel('dx/dt [m/s]');
figure(7)
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