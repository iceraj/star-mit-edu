from __future__ import print_function
from time import sleep
import time
import sys
import random
import os
import numpy as np
from mpi4py import MPI
from numpy import linalg as LA
from util import *
from generate_data_helpers import *

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

expi = 2
scenario = 4
N = 42
mi = 6300
ni = 5000
# alpha = 0.1
lr = 0.000000001
c7 = lr/mi
rounds = 300
### overall data set dimensions
stragwrk = [0]*N
lclsize= mi/N

if rank == 0:	
	print ("At master",rank)
	masterComm = comm.Split( 0, rank )
	timecaliter=np.zeros((rounds,1))
	erriter=np.zeros((rounds,1))
	timecalt=np.zeros((rounds,1))
	beta=np.zeros(ni)
	# beta0 = load_data("beta_"+str(case)+"_0.dat")
	beta0 = np.random.normal(0,1,(ni,))
	for i1 in range(rounds):
		print (i1)
		comm.Barrier()
		recvmsg1 = comm.gather(0, root=0)
		# print rank, len(recvmsg1)
		timecaliter[i1]=max(recvmsg1[1:])
		timecalt[i1]=np.sum(timecaliter[0:(i1+1)])
		comm.Irecv([beta, MPI.FLOAT], source=1)

		erriter[i1]=pow((LA.norm(beta-beta0)/LA.norm(beta0)),2)
		print (timecalt[i1])
		print (erriter[i1])

	df=np.matrix(timecalt)
	#np.savetxt('time_uncoded_master.txt',df)
	np.savetxt('AGC_time_%s_%s.txt'%(expi,scenario),df)	  
	
	df=np.matrix(erriter)
	#np.savetxt('time_uncoded_master.txt',df)
	np.savetxt('AGC_error_%s_%s.txt'%(expi,scenario),df)	  

	
else:
	rk=rank
	workerComm = comm.Split( 1, rank )

	strag=stragwrk[rk-1]
	print ("At worker",rk)


	Xi = np.random.normal(0,1,(lclsize,ni))
	yi = np.random.normal(0,1,(lclsize,))

	beta=np.zeros(ni)
	
	for k in range(rounds):
		grad=np.zeros(ni)
		comm.Barrier()
		workerComm.Barrier()
		tst=time.time()
		
		# if rank ==1:
		# 	print(Xi.shape)
		# 	print(yi.shape)
		# 	print(beta.shape)
		gradi=Xi.T.dot(Xi.dot(beta)-yi)

		tr=time.time()-tst
		if strag==1:
			time.sleep(3*tr)
		
		workerComm.Allreduce(gradi,grad,op=MPI.SUM)
		print("worker gradi",gradi,grad)
		beta=beta-c7*grad
		bpt = time.time()


		tlocal=bpt-tst

		recvmsg1 = comm.gather(tlocal, root=0)


		if rk==1:
			sC = comm.Isend([beta, MPI.FLOAT], dest=0)
			sC.wait()
			# print rk,recvmsg1
		
