% Run DATA INITIALIZATION code first before plotting anything
%%%%%%%%%%%%%%%%%%%%%%%
% DATA INITIALIZATION %
%%%%%%%%%%%%%%%%%%%%%%%

fileID=fopen('EEE158_Week5_InputData_SOMBRITO_SYZ1.txt')
data=fscanf(fileID,'%f', [4 22])

% prepare the different datasets
data1 = data(1,:)
data2 = data(2,:)
data3 = data(3,:)
data4 = data(4,:)

% set time period and input
time=[0:21]
input = stepDataOptions('InputOffset',0,'StepAmplitude', 4.36)

%%%%%%%%%%%%%%%%%%%%%%%
% STEP RESPONSE PLOTS %
%%%%%%%%%%%%%%%%%%%%%%%

% sys1
sys1 = tf([928.89908 456.77981],[1500 571])
[y1,t] = step(sys1, input, 21)
plot(t, y1)
hold on							
plot(time, data1, '-o')
grid on
xlabel('Time (min)')
ylabel('Vtemp (V)')
title('Vtemp when Gc(s) = 1')
legend('Model Vtemp', 'Actual Vtemp')

% sys2
sys2 = tf([464.44954 363.88990],[750 421])
[y2,t] = step(sys2, input, 21)
plot(t, y2)
hold on							
plot(time, data2, '-o')
grid on
xlabel('Time (min)')
ylabel('Vtemp (V)')
title('Vtemp when Gc(s) = 2')
legend('Model Vtemp', 'Actual Vtemp')

% sys3
sys3 = tf([185.77981 308.15596],[300 331])
[y3,t] = step(sys3, input, 21)
plot(t, y3)
hold on							
plot(time, data3, '-o')
grid on
xlabel('Time (min)')
ylabel('Vtemp (V)')
title('Vtemp when Gc(s) = 5')
legend('Model Vtemp', 'Actual Vtemp')
	
% sys4
sys4 = tf([928.89 185.778 271],[1500 300 271])
[y4,t] = step(sys4, input, 21)
plot(t,y4)
hold on							
plot(time, data4, '-o')
grid on
xlabel('Time (min)')
ylabel('Vtemp (V)')
title('Vtemp when Gc(s) = 1/s')
legend('Model Vtemp', 'Actual Vtemp')

%%%%%%%%%%%%%%%%%%%%%
% TEMPERATURE PLOTS %
%%%%%%%%%%%%%%%%%%%%%

% sys1
plot(time, data1 * 10)
grid on
xlabel('Time (min)')
ylabel('Temp (°C)')
title('Temp when Gc(s) = 1')

% sys2
plot(time, data2 * 10)
grid on
xlabel('Time (min)')
ylabel('Temp (°C)')
title('Temp when Gc(s) = 2')

% sys3
plot(time, data3 * 10)
grid on
xlabel('Time (min)')
ylabel('Temp (°C)')
title('Temp when Gc(s) = 5')

% sys4
plot(time, data4 * 10)
grid on
xlabel('Time (min)')
ylabel('Temp (°C)')
title('Temp when Gc(s) = 1/s')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%      ΔTEMPERATURE PLOTS      %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% sys1
plot(time, data1 * 10 - 27)
grid on
xlabel('Time (min)')
ylabel('Temp (°C)')
title('ΔTemp when Gc(s) = 1')

% sys2
plot(time, data2 * 10 - 27)
grid on
xlabel('Time (min)')
ylabel('Temp (°C)')
title('ΔTemp when Gc(s) = 2')

% sys3
plot(time, data3 * 10 - 27)
grid on
xlabel('Time (min)')
ylabel('Temp (°C)')
title('ΔTemp when Gc(s) = 5')

% sys4
plot(time, data4 * 10 - 27)
grid on
xlabel('Time (min)')
ylabel('Temp (°C)')
title('ΔTemp when Gc(s) = 1/s')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% PROPORTIONAL CONTROLLER ERROR PLOTS %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

plot(time, 4.36 - data1)
hold on	

plot(time, 4.36 - data2)
hold on	

plot(time, 4.36 - data3)

title('Proportional Controllers Error Plot')
legend('Controller Gc(s) = 1 Error', 'Controller Gc(s) = 2 Error', 'Controller Gc(s) = 5 Error')
xlabel('Time (min)')
ylabel('Error (V)')
grid on

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% INTEGRAL CONTROLLER ERROR PLOTS %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

t = [0:0.1:50]
theoretical_error = 1.66 * exp(-0.1*t) .* cos(0.413118 * t) + 0.4018220 * exp(-0.1 * t) .* sin(0.413118 * t) 
plot(t, theoretical_error)
hold on

plot(time, 4.36 - data4, '-o')

legend('Theoretical Error Response', 'Actual Dataset Error Response')
title('Integral Controller Error')
xlabel('Time (min)')
ylabel('Error (V)')
grid on

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%          ROOT LOCUS          %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

rlocus(tf([271], [1500 300]))
title('Root Locus of Proportional Controller')

rlocus(tf([271], [1500 300 0]))
title('Root Locus of Proportional Controller')