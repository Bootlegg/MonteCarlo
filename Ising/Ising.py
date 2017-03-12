import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


nx = 30
ny = 30
N = nx*ny
#x = np.linspace(0,10,nx)
#y = np.linspace(0,10,ny)
T = 0.5
dT = 0.15
Nt = 30
J = 1# J > 0 gives ferromagnetism
ntest = 10

#indices = [i for i in range(nx)]

#X,Y = np.meshgrid(x,y)

#Z = np.random.random_integers(-1,1, size=(10, 10))

S = np.zeros((ny,nx),dtype=int)+1

def randomS(S):
	#Start with random initial spin
	for i in range(nx):
		for j in range(ny):
			val = np.random.rand()
			if val > 0.5:
				S[j,i] = 1
			else:
				S[j,i] = -1
randomS(S)
print(S)

M = np.sum(S)


def CalcH(S):
	
	H = 0
	
	H2 = 0

	#Jeg bør bruge nogle pointers, så jeg ikke double count.. fx "S12*S11" eksisterer, så "S11*S12" skal ikke 
	#tilføjes til H... Så måske først lave pairs, og derefter sum dem up..
	#Eller, divide by 4
	#Pairs = []
	for i in range(nx):
		for j in range(ny):

			#Nearest neighbor? Ingen diagonal neighbors?
			#PDE, periodic boundary conditions
			if j == 0:
				H += -J*S[nx-1,i]*S[j,i]
				H += -J*S[1,i]*S[j,i]
				
				#H2 += np.abs(-J*S[nx-1,i]*S[j,i])
				#H2 += np.abs(-J*S[1,i]*S[j,i])
			elif j == nx-1:
				H += -J*S[0,i]*S[j,i]
				H += -J*S[nx-2,i]*S[j,i]
				
				#H2 += np.abs(-J*S[0,i]*S[j,i])
				#H2 += np.abs(-J*S[nx-2,i]*S[j,i])
			else:
				H += -J*S[j-1,i]*S[j,i]
				H += -J*S[j+1,i]*S[j,i]
				
				H2 += np.abs(-J*S[j-1,i]*S[j,i])
				H2 += np.abs(-J*S[j+1,i]*S[j,i])
				
			
			if i == 0:
				H += -J*S[j,ny-1]*S[j,i]
				H += -J*S[j,1]*S[j,i]
				
				#H2 += np.abs(-J*S[j,ny-1]*S[j,i])
				#H2 += np.abs(-J*S[j,1]*S[j,i])
				
			elif i == ny-1:
				H += -J*S[j,0]*S[j,i]
				H += -J*S[j,ny-2]*S[j,i]
				
				#H2 += np.abs(-J*S[j,0]*S[j,i])
				#H2 += np.abs(-J*S[j,ny-2]*S[j,i])
			else:
				H += -J*S[j,i+1]*S[j,i]
				H += -J*S[j,i-1]*S[j,i]
				
				#H2 += np.abs(-J*S[j,i+1]*S[j,i])
				#H2 += np.abs(-J*S[j,i-1]*S[j,i])
	
	#Noget med at jeg skal calculate probabilities, right? Eller, nej, måske ikke, men man KUNNE godt...
	#Men der vil være 10^10 mulige permutations så hvis jeg tænker rigtigt...
	#Hvis man vil brute force probabilities...


	H = H/2

	#H2 = H2/2 #How many times does it count the same? Gotta try it 4x4 grid maybe
	#Energien burde være integer så vidt jeg kan se, men lige nu får jeg 190.5 etc... de der 0.5
	#Kan jo prøve med grid i full +1, så bør den give en easy analytical expression for energy som
	#jeg kan compare...
	#Jeg tror dog højest det bliver double counted, ikke 4x counted...
	return H

def Esiteflip(S,j,i):
	
	E2 = 0
	
	#Outcommented J, we work with natural units anyway
	#Should see if this energy is correct
	
	if j == 0:
		E2 += -S[nx-1,i]#*(-1)
		E2 += -S[1,i]#*(-1)
	elif j == nx-1:
		E2 += -S[0,i]#*(-1)
		E2 += -S[nx-2,i]#*(-1)
	else:
		E2 += -S[j-1,i]#*(-1)
		E2 += -S[j+1,i]#*(-1)
		

	if i == 0:
		E2 += -S[j,ny-1]#*(-1)
		E2 += -S[j,1]#*(-1)
	elif i == ny-1:
		E2 += -S[j,0]#*(-1)
		E2 += -S[j,ny-2]#*(-1)
	else:
		E2 += -S[j,i+1]#*(-1)
		E2 += -S[j,i-1]#*(-1)
	
	#Da summen bliver J*(term+term+term+term), så får vi 4J, men vi kan gå fra -8 til 8, right?
	#Så jeg skal calculate 16 exponentials? Eller 17, med 0...
	#Så hvis vi siger at PreCalcExp[8] = np.exp(0
	#Eller er det noget med at dE altid er et lige tal? Dette vil gøre tingene mere simple
	#Ja, det er jo altid lige tal, forid vi har faktor 2... så jeg kan fjerne nogle af precalc
	#exponentials, men, whatever...
	return 2*E2*S[j,i]*(-1)
	

H1 = CalcH(S)

#Anyway, nu skal vi flip spin af en random thingy right?
randi = np.random.randint(0,nx)
randj = np.random.randint(0,nx)
print("row,column")
print(randj,randi)
print(S)
print("Next")
Stry = S.copy()
Stry[randj,randi] = -1*Stry[randj,randi]
print(Stry)

H2 = CalcH(Stry)

dH = H2-H1
print("Change in energy")
print(dH)

if dH < 0:
	S[randj,randi] *= -1
else:
	x = np.random.uniform(0,1)
	P = np.exp(-dH/T)
	if x <= P:
		S[randj,randi] *= -1



#Precalculated exponentials
PreCalcExp = [np.exp(-(i-8.0)/T) for i in range(17)]
#exp(-(0-8)/T)
#exp(-(1-8)/T)
#exp(-(2-8)/T)
#exp(-(3-8)/T)
#exp(-(4-8)/T)
#exp(-(5-8)/T)
#exp(-(6-8)/T)
#exp(-(7-8)/T)
#exp(-(8-8)/T)
#exp(-(9-8)/T)
#exp(-(10-8)/T)
#exp(-(11-8)/T)
#exp(-(12-8)/T)
#exp(-(13-8)/T)
#exp(-(14-8)/T)
#exp(-(15-8)/T)
#exp(-(16-8)/T)
#print(PreCalcExp[0])
#print(PreCalcExp)


#################################################
#Make (T,M) graph
Ms = []
Es = []
XTs = []
Cvs = []
Ts = []



for nt in range(Nt):
	
	
	Eavg = 0
	Mavg = 0
	M2avg = 0
	
	#Denner her er speshul
	E2avg = 0
	
	#Precalculated exponenstial, for every T, for more efficiency
	#Der er noget i vejen emd disse, heldigvis, så er det til at fix ftw
	PreCalcExp = [np.exp(-(i-8.0)/T) for i in range(17)]
	
	#Fordi noget med at bad initial conditions kan give local minim..
	#ntest is the number of times i run the simulation at the SAME temperature, to average results
	for navg in range(ntest):
	
		#randomS(S)
		if T < 2.2:
			S = np.ones((ny,nx))
		else:
			#If val of index = 0, then we go to -1, if val of index = 2, then we get 1.
			S = 2*np.random.randint(0,2,(ny,nx))-1
		#print(S)
		
		#Lige her bør jeg faktisk lave en endnu en loop
		
		
		
		#100*N = 100*625 = 62500
		#E2calcavg = 0
		for n in range(150*N):
			randi = np.random.randint(0,nx)
			randj = np.random.randint(0,nx)


			dE = Esiteflip(S,randj,randi)
		
			if dE < 0:
				S[randj,randi] *= -1
			else:
				x = np.random.uniform(0,1)
				
				#P = np.exp(-dE/T) #PreCalcExp[dH-8]# #Cant use precalculated that well, since we are increasing T
				P = PreCalcExp[int(dE)+8]
				#Hvis dH=0, så tager vi PreCalcExp[8]
				#P = np.exp(-dH/T)
				if x <= P:
					S[randj,randi] *= -1
					
			#if n >= 150*N-20:
			#	Etotalavg = CalcH(S)
				
			#	E2calcavg = E2calcavg + Etotalavg*Etotalavg
				
		#E2calcavg *= (1.0/20.0)
		#Calculate Magnetization
		#I want it to be absolute value, and an average, pr site, i think.
		#I want to to be absolute especially if I'm gonna run the test multiple times and average it.
		
		Mtotal = np.abs(np.sum(S))
		
		
		Mavg = Mavg + Mtotal
		

		#Calculate Energies, jeg venter med at divide med N til sidst, pga E2avg
		Etotal = CalcH(S)
		
		Eavg = Eavg + Etotal
		
		E2avg = E2avg + Etotal*Etotal
		
		#Inklusiv intra-avg:
		#E2avg = E2avg + E2calcavg

		
		#Used for isothermal susceptibility, skal måske her divide med N**2?
		#Skal måske også lave den til M*M ligesom Etotal*Etotal...
		#I (<M2>-<M>**2) så vil <M>**2 have faktor 1/N**2, mens <M2> kun har faktor 1/N
		#Så det skal nok være faktor 1/N**2 også på M2
		
		#M2avg = M2avg + Mtotal*Mtotal
		
		M2avg = M2avg + np.abs(np.sum(S**2))
	
	
	
	
	E = Eavg/ntest
	M = Mavg/ntest
	M2 = M2avg/ntest
	E2 = E2avg/ntest
	
	#Calculate Isothermal susceptibility
	#Det er egentlig XT pr site, pga N**2... men det er pr site squared, virker ikke helt rigtigt
	XT = (1/T)*(M2**2-M**2)/N**2
	
	#Calculate specific heat
	#Kan også prøve at sammenligne med finite differences
	#Dette er egentlig Cv pr mass/site
	#Hvilke values af Cv får de andre?
	
	
	#Lad os køre specific heat uden N... det er jo <E**2>-<E>**2, men IKKE PR SPIN.
	Cv = (1/T**2)*(E2-E**2)/N
	#Det kan godt være, at i stedet for np.abs(), skal det være ( )**2
	
	
	
	E = E/N
	M = M/N
	
	
	
	#2-dimensional_ising_model
	#XT i ranges 0-100
	#Cv i range 0-0.6
	#ENergy pr link 0-(-1)
	
	#advancedlab1_Part1
	#E per site 0-(-2)
	#Cv specific 0-0.12
	#X 0-0.3
	#Nok kun E som er pr site?
	
	
	#AsherIsingModelReport
	#E pr site 0-(-2)
	#X 0-0.4
	#Cv 0-0.2
	
	
	#Chap12_Ising_Model_v04
	#E pr site 0-(-2)
	#Cv/N 0-4
	
	
	#Ising (1)
	#C/N 0-3
	#E/N 0-(-2)
	
	
	#Ising Model 1
	#E 0-(-1)
	#Cv 0-10
	#XT 0-300
	
	
	#ising_Model
	#E pr spin 0-(-4)
	#Cv 0-5000
	#XT pr spin 0-0.18
	
	
	#lecture6-stat_mech
	#Cv pr spin 0-2
	#
	
	#SCALAS2013_04_16-17
	#Cv 0-1.5
	
	#Student Ising Swarthmore
	#E fra 0-(-2)
	#Cv 0-0.2
	#X 0-0.1
	
	
	
	#Save figure
	fig = plt.figure()
	ax = fig.gca()
	plt.imshow(S, interpolation=None,vmin = -1, vmax = 1,cmap = "jet")
	ax.set_title('Ising model, Metropolis algorithm')
	fig.savefig('Ising{0:0.3}.png'.format(T), bbox_inches='tight')
	plt.close()
	
	#Append to lists for plotting later
	Ms.append(M)
	Es.append(E)
	XTs.append(XT)
	Ts.append(T)
	Cvs.append(Cv)
	T += dT

	
	
fig2 = plt.figure(2)
plt.plot(Ts,Ms)
plt.xlabel("T")
plt.ylabel("m")
plt.title("Magnetization")
fig2.savefig('Magnetization.png', bbox_inches='tight')
plt.show()

fig3 = plt.figure(3)
plt.plot(Ts,Es)
plt.xlabel("T")
plt.ylabel("E")
plt.title("Energy pr spin site")
fig3.savefig('Energy.png', bbox_inches='tight')
plt.show()

fig4 = plt.figure(4)
plt.plot(Ts,XTs)
plt.xlabel("T")
plt.ylabel("XT")
plt.title("Isothermal Susceptibility")
fig4.savefig('Susceptibility', bbox_inches='tight')
plt.show()


fig5 = plt.figure(5)
plt.plot(Ts,Cvs)
plt.xlabel("T")
plt.ylabel("Cv")
plt.title("Specific heat")
fig5.savefig('Specificheat.png', bbox_inches='tight')
plt.show()


print(Ms)
print(Ts)
#Lige nu der går den til M = +-625... 



fig = plt.figure()
ax = fig.gca()
plt.imshow(S, interpolation=None,vmin = -1, vmax = 1,cmap = "jet")
ax.set_title('Ising model, Metropolis algorithm')
fig.savefig('Ising.png', bbox_inches='tight')
#plt.colorbar()
def animate(i): #i increment with 1 each step

	ax.clear()
	ax.set_title('Ising model, Metropolis algorithm')
	
	#Vi skal update den gamle energy til den nye energy, right? som x=xold
	#H1 = CalcH(S)
	#M = np.sum(S)
	#print("E = {} M = {}".format(H1,M))
	
	
	randi = np.random.randint(0,nx)
	randj = np.random.randint(0,nx)
	#print("row,column")
	#print(randj,randi)
	#print(S)
	#print("Next")
	#E1 = Esite(S,randi,randj)
	E2 = Esiteflip(S,randj,randi)
	#print(E2)
	
	#Stry = S.copy()
	#Stry[randj,randi] = -1*Stry[randj,randi]
	#print(Stry)

	#H2 = CalcH(Stry)

	#dH = H2-H1
	#print("Change in energy")
	#print(dH)
	
	dH = E2#-E1
	
	if dH < 0:
		S[randj,randi] = -1*S[randj,randi]
	else:
		x = np.random.uniform(0,1)
		
		P = PreCalcExp[dH-8]#
		#Hvis dH=0, så tager vi PreCalcExp[8]
		#P = np.exp(-dH/T)
		if x <= P:
			S[randj,randi] = -1*S[randj,randi]

	
	


	plt.imshow(S, interpolation=None,vmin = -1, vmax = 1,cmap = "jet")
	#plt.colorbar()
	return None
#anim = animation.FuncAnimation(fig, animate, frames=10, interval=100)

plt.show()
####################################
#jeg kan prøve at se med 3x3 case og se om den calculate det samme som jeg gør på paper, og måske