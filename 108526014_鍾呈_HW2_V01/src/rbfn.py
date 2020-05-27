import numpy as np
import random
import sys

# rbfn Net
class rbfNet(object):
    # set rbfn variable
    def __init__(self, thegma, weight, m, theta):

        self.theta = theta
        self.thegma = thegma
        self.m = m
        self.weight = weight

    # compute rbfn outpuy
    def output (self, x):
        fx = self.add_thegma(0)
        for i in range(np.size(self.m, 0)):
            m = self.m[i:i+1, ]
            g = self.gaussan(x, i, m)
            w = self.mul_weight(g, i)
            fx  = fx + w

        return fx

    # add thegma
    def add_thegma(self, n):
        n = n + self.thegma[0][0]
        return n

    # compute gaussan value
    def gaussan(self, x, i, m):
        theta = self.theta[0][i]
        n =  np.exp(-((np.sum(np.square(x-m)) / (2 * np.square(theta)))))

        return n

    # multiple by weight
    def mul_weight(self, n, i):
        weight = self.weight[0][i]
        # print('weight = ', weight, n.shape)
        n = n * weight
        return n

# PSO optimizier 
class psoOptimaizer(object):
    # set initial variable
    def __init__(self, swarm, j, dim):
        self.x = swarm
        self.j = j
        self.dim = dim
        self.theta1 = 0.3
        self.theta2 = 0.3

        print('self.swarm size , ', np.shape(swarm)[0])
        self.vt0 = np.zeros(( np.shape(swarm)[0] , dim))

        self.pi = swarm
        self.pg = np.full((1, 1), 100)

    def computev(self, err_rate):
        print('err_rate', err_rate)
        y = np.argsort(err_rate , axis=0)
        print('y', y, y[0][0])
        int_i = int(y[0][0])
        print('x', self.x)
        self.pg = self.x[int_i: int_i + 1, :]
        print('pg ', self.pg)
        
        vt1 = self.vt0 + self.theta1 * (self.pi - self.x) 
        


# geneticOptimizer
class geneticOptimizer(object):
    # set initial variable
    def __init__(self, swarm, err_rate, j ,dim):
        self.swarm = swarm
        self.err_rate = abs(err_rate)
        
        self.cro_rate = 0.9
        self.mut_rate = 0.9

        self.cro_theta = 0.01
        self.mut_s = 1

        self.j = j
        self.dim = dim
        
    # output genatic optimizer swarm
    def genatic_opt(self):
        self.reproduction()
        self.crossover()
        self.mutation()
        
        return self.swarm

    # reproducation select top 5 swarm to reproduction
    def reproduction(self):
        y = np.argsort(self.err_rate , axis=0) 

        k = 0
        for i in (y): 
            int_i = int(i[0])
            a = self.swarm[int_i: int_i + 1, :]
            if(k == 0):
                for i in range (10):
                    if(i == 0 ):
                        b = a 
                    else :
                        b = np.append(b, a, axis=0)
            else :
                 for i in range (10):
                     b = np.append(b, a, axis=0)
            k = k + 1
            if(k == np.size(self.err_rate, 0)/10):

                break
        self.swarm = b
    
    #  crossover 
    def crossover (self):
        for i in range (np.size(self.err_rate, 0)):
            # make random number
            size = (1, 1)
            rand_num = np.random.uniform(0, 1, size)
            
            # choose to crossover or not
            if(rand_num < self.cro_rate):
                # choose witch swarm to crossover
                b = random.randint(0, np.size(self.err_rate, 0) - 1 )
                # crossover by 250 point
                for j in range (200):
                    #choose random point to crossover
                    n= random.randint(0, np.size(self.swarm[0], 0) - 1 )
                  
                    b0 = self.swarm[i][n]
                    b1 = self.swarm[b][n]
                    
                    bs0 = self.swarm[i][n] + (b1 - b0) *  self.cro_theta
                    bs1 =self.swarm[b][n] -  (b1 - b0) *  self.cro_theta 
                   
                    # thata can't be negative 
                    if(n >= self.dim - self.j ):
                        if(bs0 >= 0):
                            self.swarm[i][n] = bs0
                        
                        if(bs1 >= 0):
                            self.swarm[b][n] = bs1

                    else :
                        self.swarm[i][n] = bs0
                        self.swarm[b][n] = bs1
                    
   # mutation 
    def mutation (self):
        for i in range (np.size(self.err_rate, 0)):
            # make random number
            size = (1, 1)
            rand_num = np.random.uniform(0, 1, size)

            # choose to crossover or not
            if(rand_num < self.mut_rate):
                
                # mutation by 50 point
                for j in range (40):
                    # choose random point to mutation
                    n= random.randint(0, np.size(self.swarm[i], 0) - 1)
                    size = (1, 1)
                    noisy = np.random.uniform(-1, 1, size)

                    mut_n = self.swarm[i][n] + noisy * self.mut_s

                    # theta can't be negative
                    if(n >= self.dim - self.j ):
                   
                        if(mut_n >= 0):
                            self.swarm[i][n] = mut_n
                    else :
                        self.swarm[i][n] = mut_n


def main():
    # set initial data 
    j =  1
    swarm_num = 10
    epoch_num = 1

 
    dataset = '4d'
    print('dataset = ', dataset)
    
    dim = 1 + j + 3*j + j
    print('j, dim = ', j, dim)

    #get training data
    f = open(r'train4d_All.txt')
    i = 0
    for line in f:
        s = line.split(" ")
        d = float(s[0])
        ld = float(s[1])
        rd = float(s[2])
        car_angle = float(s[3].split('\n')[0])
        if(i == 0):
            xx = np.array([[d, ld, rd]])
            yy = np.array([[car_angle]])
        else :
            xx = np.append(xx, np.array([[d, ld, rd]]), axis=0)
            yy = np.append(yy, np.array([[car_angle]]), axis=0)

        i = i + 1
            

  
    print('i = ', i)
    print('shpae of xx , yy = ', xx.shape, yy.shape)
    
    # initialize swarm
    size = (swarm_num, dim)
    g_data = np.random.uniform( -40, 40, size)
    
    # variable to calculate the network
    num_x = i 
    best_err = 100
    best_var = 100
    for epoch  in range (epoch_num):
            print('e = ', epoch)
            for i in range(swarm_num):
                # get varible for rbfn in swarm
                g_data[i:i+1, dim-j: dim] = abs(g_data[i:i+1, dim-j: dim])
                # print('e, i = ', e, i)
                thegma = g_data[i:i+1, 0:1]
                # print('thegma = ', thegma.shape)
                weight = g_data[i:i+1, 1: j+1]
                # print('weight = ', weight.shape)
                theta = g_data[i:i+1, dim-j: dim]
                # print('theta = ', theta)
                m = g_data[i: i+1, j+1: j+1+(3* j )]
                m = np.reshape(m, (j, 3))
                # print('m = ', m.shape)

                # set the variable
                net = rbfNet(thegma, weight, m, theta)

                # check totaal error rate
                for k in range  (num_x):
                    f_total = net.output(xx[k:k+1, : ])
                    f_total= np.array([[f_total]])

                    if(k == 0):
                        fout = np.array(f_total)
                    else :
                        fout = np.append(fout, np.array(f_total), axis=0)


                # compute error for fitness function 
                
                error = np.sum(np.square(fout-yy))/2
                if(i == 0):
                    err_rate = np.array([[error]])
                else :
                    err_rate = np.append(err_rate, np.array([[error]]), axis=0)
                
                # compute error for the network caculate
                error_total = np.sum(abs(fout-yy))/num_x
                if(error_total < best_err):
                    best_err  = error_total
                    best_var = g_data[i]
                    pre_angle = fout
                    best_epoch = epoch
                
                

            # # put swarm data and error rate in geneticOptimizer 
            # g_opt = geneticOptimizer(g_data, err_rate, j,  dim)
            # # update variable 
            # g_data = g_opt.genatic_opt()

            # put swarm data and error rate in geneticOptimizer 
            g_opt = psoOptimaizer(g_data, j,  dim)
            # update variable 
            g_opt.computev(err_rate)
           
            # print out the network information in epoch
            print('epoch best --> ', repr(best_var), pre_angle, pre_angle.shape, j, dim, best_err, best_epoch, epoch)

    # print out the total netowrok information
    print('global best --> ', repr(best_var), pre_angle, best_epoch, best_err)

    

if __name__ == "__main__":
    main()