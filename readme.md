# Supplementary Material

## Files and Directory Introduction

File FERET.mat is the dataset.

Files demo.py and plot_demo.py are the python files to show the results and figures of the dataset in our paper.

File requirements.txt lists all the required python libraries and their version.

Files cppfuns$\_$.pyx and cppfuns$\_$.pyd are the cython files to communicate between cpp and python.

Files cppfuns.cpp, cppfuns.h are the cpp related files used to accelerate Half-Cut and directory eigen3 is  a C++ template library for linear algebra: matrices, vectors, numerical solvers, and related algorithms.

## Run Files

We use Anaconda as our IDE, you can use others instead. We sincerely advise that these files should run on a Linux operating system. It's completely different  to compile these c++ files on Windows. After you finish installing python and its environment according to requirements.txt, you can run the python files by following the instructions below:

### 1.Run demo.py

You should compile the c++ files by the command below:

```
python build setup.py build_ext --inplace
```

After compiling the C++ files, you can run demo.py by the command below to get the result of Half-Cut on FERET in TABLE III:
```
python demo.py
```
### 2.Run plot_demo.py

you can run plot_demo.py by the command below to get the figure of FERET in Fig. 3:

```
python plot_demo.py
```

