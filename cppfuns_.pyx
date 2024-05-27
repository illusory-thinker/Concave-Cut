# distutils: language = c++

cimport numpy as np
import numpy as np
np.import_array()

from cython cimport double
from cython cimport boundscheck

from cppfuns_ cimport cppcluster_h

@boundscheck(False)
def cppcluster(int[:, ::1] results, int[:, ::1] Aindex, double[:, ::1] Asim, double[::1] times, int epoches,int c_true):

    cdef:
        int exptimes = results.shape[0]
        int vnum = Aindex.shape[0]
        int knn = Aindex.shape[1]

    cppcluster_h(&results[0, 0], &Aindex[0, 0], &Asim[0, 0], &times[0], exptimes, epoches, c_true, vnum, knn)
