import numpy as np
import matplotlib.pyplot as plt

C = [
0.47856 ,
0.497646,
0.590201,
0.643329,
0.637732,
0.604732,
0.707489,
0.794551,
0.851778,
0.90159 ,
1.02255 ,
1.13577 ,
1.10085 ,
1.27833
]

D= [
4.15806 ,
4.35715 ,
5.06848 ,
5.45879 ,
5.52364 ,
5.14211 ,
5.51497 ,
5.80232 ,
6.01414 ,
6.2786  ,
6.74906 ,
7.14743 ,
7.14173 ,
8.1337
]

c = 0.493569
d = 4.18239

for i in range(len(C)):
    C[i] = c/C[i]
    D[i] = d/D[i]

X = np.array(range(1,15))

plt.plot(X, C)
plt.title("automate, calculus")
plt.xlabel("coeurs")
plt.xticks(X)
plt.ylabel("speed up")
plt.savefig('speedUp_automate_calculus.png', bbox_inches='tight')
plt.show()

plt.plot(X, D)
plt.title("automate, display")
plt.xlabel("coeurs")
plt.xticks(X)
plt.ylabel("speed up")
plt.savefig('speedUp_automate_display.png', bbox_inches='tight')
plt.show()