#ifndef _CPPFUNS_H
#define _CPPFUNS_H

// #define _USE_MATH_DEFINES
// #define EIGEN_USE_MKL_ALL
#define EIGEN_USE_BLAS
// #define EIGEN_DONT_PARALLELIZE 
#include <iostream>
#include <algorithm>
#include <fstream>
#include <stdlib.h>
#include <cmath>
#include <vector>
#include <numeric>
#include <limits>
#include <functional>
#include <set>
#include <unordered_map>
#include <ctime>
#include <chrono>
#include <eigen3/Eigen/Dense>
#include <eigen3/Eigen/Sparse>
#include <eigen3/Eigen/Core>

using std::chrono::steady_clock;

using Eigen::MatrixXd;
using Eigen::MatrixXi;

using Eigen::ArrayXd;
using Eigen::ArrayXi;

using Eigen::VectorXd;
using Eigen::VectorXi;

using Eigen::RowVectorXd;
using namespace std;

typedef Eigen::Triplet<double> Tri;
typedef Eigen::SparseMatrix<double, Eigen::RowMajor> spMatdr; 

typedef Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> Matdr;
typedef Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::ColMajor> Matdc;

typedef Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> Matir;
typedef Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::ColMajor> Matic;

typedef Eigen::Matrix<bool,   Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> Matbr;
typedef Eigen::Matrix<bool,   Eigen::Dynamic, Eigen::Dynamic, Eigen::ColMajor> Matbc;

typedef Eigen::Array<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> Arrdr;
typedef Eigen::Array<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::ColMajor> Arrdc;

typedef Eigen::Array<int, Eigen::Dynamic, 1, Eigen::ColMajor> Arr1ic;
typedef Eigen::Array<int, 1, Eigen::Dynamic, Eigen::RowMajor> Arr1ir;

typedef Eigen::Array<double, Eigen::Dynamic, 1, Eigen::ColMajor> Arr1dc;
typedef Eigen::Array<double, 1, Eigen::Dynamic, Eigen::RowMajor> Arr1dr;

typedef RowVectorXd Vecdr;
typedef VectorXd Vecdc;

void cppcluster_h(int *results_ptr, int *Aindex_ptr, double *Asim_ptr, int exptimes, int epoches, int c_true, int vnum, int knn);
void cppcluster_c(int *results_ptr, int *Aindex_ptr, double *Asim_ptr, double *times_ptr, int epoch, int c_true, int vnum, int knn);

#endif