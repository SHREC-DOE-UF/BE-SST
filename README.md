# BE-SST

BE-SST is a parallel and scalable coarse-grained simulator that employs statistical models to run probabilistic, discrete-event simulation by combining Behavioral Emulation (BE), a coarse-grained modeling approach and Structural Simulation Toolkit (SST), a parallel discrete-event simulation framework from Sandia National Laboratories. BE-SST can be used for application design-space exploration (DSE) where alternate algorithms of an application can be studied on a given architecture; or architectural DSE can be performed for a given application. BE-SST provides a distributed parallel simulation library for Behavioral Emulation through simple interfaces and framework for development of coarse-grained BE models which can be easily extended to model new notional architectures. BE-SST also provides the capability to plug-n-play different subsystems (node, interconnect, memory, etc.), which is necessary to study abstract and notional machines.  
> **_Note:_** Both SST-core and SST-element-BE are provided to you through this repository. You DO NOT have to download the SST-core from the [SST website](www.sst-simulator.org).

## Build and Run

This is a quick start guide for BE-SST. For more detailed and step-by-step instructions on how to build, install and run BE-SST, refer to [DETAILED_BUILD_INSTALL.md](DETAILED_BUILD_INSTALL.md). 

#### Following dependencies are required to build and run BE-SST: 
1. gcc 4.7 and newer  
2. python 2 (anything in 2.7 branch)  
  2.1 numpy package  
  2.2 python-dev
3. GNU make 4.0 or newer  
4. autotools (libtool, autoconf, automake)  
5. [OpenMPI 2.1.3](http://www.open-mpi.org/software/ompi/v2.1/) *(strongly recommended)*   
6. [Boost 1.56](http://sourceforge.net/projects/boost/files/boost/1.56.0/)  

> **_Note:_** OpenMPI 2.1.3 and Boost 1.56 installation steps are listed [DETAILED_BUILD_INSTALL.md](DETAILED_BUILD_INSTALL.md)

### Example Build and Install Directories

These instructions will use the following conventions (the user can adjust these as they see fit):  
- Download directory `$HOME/scratch`  
  - This directory will contain downloaded source code packages for SST and its dependencies.  
  - The following directories should be created on the users machine  
    - `$HOME/scratch`  
    - `$HOME/scratch/src`  
- Download `sst-core-devel` and `SST-elements-BE` from the this GitHub repo inside the `$HOME/scratch/src directory`  
- Installation directory `$HOME/local`
  - This directory will be the installation directory for SST and its dependencies.  
  - The following directories should be created on the users machine:  
    - `$HOME/local`  
    - `$HOME/local/packages`  

### Basic Build and Install

1. Obtain `sst-core-devel` and `sst-elements-BE` from [this](https://github.com/SHREC-DOE-UF/BE-SST) github repo.  
2. Place `sst-core-devel` and `sst-elements-BE` in `$HOME/scratch/src` directory.  
3. Change directory to the SST-Core directory.  
```bash
cd $HOME/scratch/src/sst-core-devel  
```
4. Run the `autogen.sh` script to setup the configure for SST-core  
```bash
./autogen.sh  
```
5. Configure SST-Core.  
```bash
./configure --prefix=$HOME/local/sst-core-devel  
```
6. Compile SST-Core.  
```bash
make all  
```
7. Install SST-Core.  
```bash
make install  
```
8. Change directory to `sst-elements-BE` directory  
```bash
cd $HOME/scratch/src/sst-elements-BE  
```
9. Run the `autogen.sh` script to setup the configure for BE element.  
```bash
./autogen.sh  
```
10. Configure BE element.  
```bash
./configure --prefix=$HOME/local/sst-elements-BE --with-sst-core=$SST_CORE_HOME --with-boost=$BOOST_HOME  
```
11. Compile BE element.  
```bash
make all  
```
12. Install BE element.  
```bash
make install  
```
13. Verify SST Operation with a very simple sanity test **(Note: Path to sst executable must be properly setup.)**  
```bash
sst --version  
```
14. Navigate to the [tests](sst-elements-BE/src/sst/elements/behavioralEmulation/tests/) folder  
```bash
cd src/sst/elements/behavioralEmulation/tests/  
```
15. Running the test script for BE to check its functional correctness  
```bash
./BE_TEST.sh  
```
16. Running a test configuration to obtain a simulated time  
```bash
./BE_RUN.sh -c testConfig.py  
```

---

### Refer to the following papers for more information on BE [1] and BE-SST [2]:  
[1] Kumar N., Pascoe C., Hajas C., Lam H., Stitt G., George A. (2016) Behavioral Emulation for Scalable Design-Space Exploration of Algorithms and Architectures. In: Taufer M., Mohr B., Kunkel J. (eds) High Performance Computing. ISC High Performance 2016. Lecture Notes in Computer Science, vol 9945. Springer, Cham. https://link.springer.com/chapter/10.1007/978-3-319-46079-6_1  
[2] Ajay Ramaswamy, Nalini Kumar, Aravind Neelakantan, Herman Lam, and Greg Stitt. 2018. Scalable Behavioral Emulation of Extreme-Scale Systems Using Structural Simulation Toolkit. In Proceedings of the 47th International Conference on Parallel Processing (ICPP 2018). Association for Computing Machinery, New York, NY, USA, Article 17, 1–11. DOI:https://doi.org/10.1145/3225058.3225124  
*If you consider using this work, please site the above papers.*

For any questions regarding the simulator, contact **Aravind Neelakantan** at aravindneela@ufl.edu
