import glob
import numpy as np 
from numpy import array,mat,sin,cos,dot,eye
from numpy.linalg import norm
from numpy import * 
import glob
from scipy.io import savemat
from IPython.core.debugger import Tracer

def rodrigues(r):
    def S(n):
        Sn = array([[0,-n[2],n[1]],[n[2],0,-n[0]],[-n[1],n[0],0]])
        return Sn
    theta = norm(r)
    if theta > 1e-30:
        n = r/theta
        Sn = S(n)
        R = eye(3) + sin(theta)*Sn + (1-cos(theta))*dot(Sn,Sn)
    else:
        Sr = S(r)
        theta2 = theta**2
        R = eye(3) + (1-theta2/6.)*Sr + (.5-theta2/24.)*dot(Sr,Sr)
    return mat(R)


def process_a_set(set_name):

    data = np.load(set_name)

    rvecs = data['rvecs']
    tvecs = data['tvecs']

    Trans_Mat = []

    for i in range(0,rvecs.shape[0]):

        t_mat = np.zeros([4,4])
        t_mat[:3,:3] = rodrigues(rvecs[i])
        t_mat[:3,3:] = tvecs[i]
        t_mat[3,3]   = 1

        Trans_Mat.append(t_mat)

    return Trans_Mat



if __name__ == '__main__':

    to_do_list = sorted(glob.glob('./*.npz'))
    set_Mats   = []

    for name in to_do_list:
        T_M = process_a_set(name)
        set_Mats.append(T_M)

    savemat('set_trans_mats',{'set_Mats':set_Mats})
    np.save('set_trans_mats',set_Mats)
