import numpy as np
from pprint import pprint

class brain :
    def __init__(self, old_weights=None):
        self.reward = 0
        if old_weights is None:
            self.weights = np.random.uniform(-1,1,size=(9,4))
            self.grad_map=np.random.uniform(-1,1,size=(9,4))
            self.dw=np.zeros((9,4))
        else :
            self.weights = old_weights
            self.grad_map=np.random.uniform(-1,1,size=old_weights.shape)
            self.dw=np.zeros(old_weights.shape)

    def good(self) :
        self.reward+=5

    def bad(self):
        self.reward-=5

    def update_gradient(self):
        print(self.reward)
        for i in range(self.weights.shape[0]) :
            for j in range(self.weights.shape[1]):
                self.grad_map[i][j] = (self.reward)/(self.dw[i][j]) + np.random.uniform(-0.001,0.001)

    def update_weights(self):
        for i in range(self.weights.shape[0]) :
            for j in range(self.weights.shape[1]):
                nw= self.grad_map[i][j]
                self.dw[i][j] = nw 
                self.weights[i][j] +=nw

    def decision(self, inputs):
        '''dif = inputs.shape[1] - self.weights.shape[0]
        if dif > 0 :
            tl = list(self.weights)
            gl = list(self.grad_map)
            dl = list(self.energys)
            odl = list(self.oenergys)
            dwl = list(self.dw)
            for _ in range(dif):
                tl.append(np.random.uniform(-5,5,size=(4)))
                gl.append(np.random.uniform(-100,100,size=(4)))
                dl.append(np.array([2000.0,2000.0,2000.0,2000.0]))
                odl.append(np.array([2000.0,2000.0,2000.0,2000.0]))
                dwl.append(np.array([.0,.0,.0,.0]))
            self.weights=np.array(tl)
            self.grad_map=np.array(gl)
            self.energys=np.array(dl)
            self.oenergys=np.array(odl)
            self.dw=np.array(dwl)

        elif dif <0 :
            inputs=list(inputs)
            for _ in range(-dif):
                inputs.append(np.array([0]))
            inputs=np.array(inputs)
        '''
        out=np.matmul(inputs, self.weights)[0]
        print(out)
        return out