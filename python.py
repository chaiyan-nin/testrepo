import numpy as np
import math
import statistics 

# Start T
Test = []
T = []
P = []
C = []
Ch_P = [];
Ch_C = [];
filepath = 'test.csv'
with open(filepath) as fp:
	line = fp.readline()
	cnt = 0
	while line:
		if cnt>0:
			#print("Line {}: {}".format(cnt, line.strip()))
			parts = line.split(',')
			P.append(float(parts[2]));
			C.append(float(parts[3]));
			if cnt>1:
				Ch_P.append((P[cnt-2]-P[cnt-1])/P[cnt-1]);
				Ch_C.append((C[cnt-2]-C[cnt-1])/C[cnt-1]);
		line = fp.readline()
		cnt += 1
fp.close();
Test.append(P);
Test.append(C);

T.append(Ch_P);
T.append(Ch_C);
#print(T)
# End T

# Start A
P = []
C = []
filepath = 'train.csv'
with open(filepath) as fp:
	line = fp.readline()
	cnt = 0
	while line:
		if cnt>0:
			#print("Line {}: {}".format(cnt, line.strip()))
			parts = line.split(',')
			P.append(float(parts[2]));
			C.append(float(parts[3]));
		line = fp.readline()
		cnt += 1
fp.close();
#print(P[0]);
num_prices = len(P)
#num_loop = math.floor(num_prices/11);
#fraction = num_prices%11;
#num_loop = (num_loop+1) if (fraction>0) else num_loop;
D = []

Changes = []
Selected_P = []
Selected_C = []
Selected_D = []
Stds = [1000,1000,1000]
Stds_i = [-1,-1,-1]
D_bars = []
for i in range(1, num_prices-12):
	A = []
	Diff_P = []
	Diff_C = []
	for j in range(i, i+10):
		Diff_P.append((P[j]-P[j-1])/P[j-1]);
		Diff_C.append((C[j]-C[j-1])/C[j-1]);
	A.append(Diff_P);
	A.append(Diff_C);
	Dx = np.subtract(T, A)
	D = Dx[0]+Dx[1];
	std = statistics.stdev(D)
	D_bar = statistics.mean(D);

	D_bars.append(D_bar);
	if std<Stds[0]:
		Stds[0] = std;
		Stds_i[0] = i;
		Selected_D.append(Dx);
		Selected_P.append(P[i:10]);
		Selected_C.append(C[i:10]);
		Changes.append(A);
	elif std>Stds[0] and std<Stds[1]:
		Stds[1] = std;
		Stds_i[1] = i;
		Selected_D.append(Dx);
		Selected_P.append(P[i:10]);
		Selected_C.append(C[i:10]);
		Changes.append(A);
	elif std>Stds[1] and std<Stds[2]:
		Stds[2] = std;
		Stds_i[2] = i;
		Selected_D.append(Dx);
		Selected_P.append(P[i:10]);
		Selected_C.append(C[i:10]);
		Changes.append(A);
	#print(T);
	#print("---");
	#print(A);
	#print("---");
	#print(D);
	#print("---");
	#print(Std,Std_i);
	#break;	
#print(Std, Std_i);


Pds = [[[],[]],[[],[]],[[],[]]]
for i in range(0, 5):
	#print(Changes[0][0][i]);
	ft_p = (Changes[0][0][i]+1)*(1+D_bars[Stds_i[0]-1])
	ft_c = (Changes[0][1][i]+1)*(1+D_bars[Stds_i[0]-1])
	Pds[0][0].append(P[len(P)-1]*ft_p);
	Pds[0][1].append(C[len(C)-1]*ft_c);

	ft_p = (Changes[1][0][i]+1)*(1+D_bars[Stds_i[1]-1])
	ft_c = (Changes[1][1][i]+1)*(1+D_bars[Stds_i[1]-1])
	Pds[1][0].append(P[len(P)-1]*ft_p);
	Pds[1][1].append(C[len(C)-1]*ft_c);

	ft_p = (Changes[2][0][i]+1)*(1+D_bars[Stds_i[2]-1])
	ft_c = (Changes[2][1][i]+1)*(1+D_bars[Stds_i[2]-1])
	Pds[2][0].append(P[len(P)-1]*ft_p);
	Pds[2][1].append(C[len(C)-1]*ft_c);

print("[Tested Data]");
print(Test);
print("[T Data]");
print(T);
print("-----------");
print("[Model D 1] (index:"+str(Stds_i[0])+")");
print(Selected_D[0]);
print("D Bar 1")
print(D_bars[Stds_i[0]-1])
print("[Standard diviation 1]");
print(Stds[0]);
print("[Predicted Data 1]");
print(Pds[0]);
print("-----------");
print("[Model D 2] (index:"+str(Stds_i[1])+")");
print(Selected_D[1]);
print("D Bar 1")
print(D_bars[Stds_i[1]-1])
print("[Standard diviation 2]");
print(Stds[1]);
print("[Predicted Data 2]");
print(Pds[1]);
print("-----------");
print("[Model D 3] (index:"+str(Stds_i[0])+")");
print(Selected_D[2]);
print("D Bar 1")
print(D_bars[Stds_i[2]-1])
print("[Standard diviation 3]");
print(Stds[2]);
print("[Predicted Data 3]");
print(Pds[2]);