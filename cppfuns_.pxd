from libcpp.vector cimport vector
from libcpp cimport bool

cdef extern from "cppfuns.cpp":
    pass

cdef extern from "cppfuns.h":
    void cppcluster_h(int *results_ptr, int *Aindex_ptr, double *Asim_ptr, double *times_ptr, int exptimes, int epoches, int c_true, int vnum, int knn) noexcept nogil