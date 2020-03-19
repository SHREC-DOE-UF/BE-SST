# Detailed Build Instructions for BE-SST

BE-SST is a combination of Behavioral Emulation (BE) modeling approach and the parallel discrete-event simulation framework from Sandia National Labs called Structural Simulation Toolkit (SST).  
Majority of the installation instruction has been taken from the [SST documentation](http://sst-simulator.org/SSTPages/SSTBuildAndInstall9dot0dot0SeriesDetailedBuildInstructions/) and it has been modified to cater to the setup (installation and build) of BE-SST. 

## Build and Run

BE-SST has been tested on LINUX systems and the below mentioned instructions are for linux systems only. We currently do not have build and installation instructions for other operating systems.

#### Following dependencies are required to build and run BE-SST: 
1. gcc 4.7 and newer  
2. python 2 (anything in 2.7 branch)  
  2.1. numpy package  
  2.2. python-dev
3. GNU make 4.0 or newer  
4. autotools (libtool, autoconf, automake)  
5. [OpenMPI 2.1.3](http://www.open-mpi.org/software/ompi/v2.1/) *(strongly recommended)*   
6. [Boost 1.56](http://sourceforge.net/projects/boost/files/boost/1.56.0/)  

> **Note:** OpenMPI 2.1.3 and Boost 1.56 installation steps are listed below under External Dependent Component.

---

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

---

### External Dependent Component   

**OpenMPI 2.1.3 *(Strongly recommended)***  
Download OpenMPI from [link](http://www.open-mpi.org/software/ompi/v2.1/)  
`1.` Download the OpneMPI archive file `openmpi-2.1.3.tar.gz` to `$HOME/scratch/src`
`2.` Unarchive the compressed tar file  
```bash
cd $HOME/scratch/src  
tar xfz openmpi-2.1.3.tar.gz  
cd openmpi-2.1.3  
```
`3.` Decide on an installation location. For this example: `$HOME/local/packages/OpenMPI-2.1.3`. Note this location will contain `bin`, `lib`, `include`, and other directories for use of OpenMPI.  
`4.` Set the home directory environment variable of the OpenMPI installation.  
```bash
export MPIHOME=$HOME/local/packages/OpenMPI-2.1.3  
```
`5.` Configure OpenMPI to be installed in `$MPIHOME`  
```bash
./configure --prefix=$MPIHOME  
```
`6.` Build and install OpenMPI 
```bash
make all install  
```
`7.` Update your `PATH` environment variable so that it contains the bin directory of the OpenMPI installation location. Also set the `MPICC` and `MPICXX` variables to point to the correct MPI compiler options, initialization file.  
```bash
export PATH=$MPIHOME/bin:$PATH  
export MPICC=mpicc  
export MPICXX=mpicxx  
```
`8.` OPTIONAL - In some cases, it may be necessary to specify the location of the OpenMPI library files for proper operation of SST.  
```bash
export LD_LIBRARY_PATH=$MPIHOME/lib:$LD_LIBRARY_PATH  
export DYLD_LIBRARY_PATH=$MPIHOME/lib:$DYLD_LIBRARY_PATH  
export MANPATH=$MPIHOME/share/man:$DYLD_LIBRARY_PATH  
```
`9.` To make the changes to the environment variables a permanent change, it may require editing of your login shell’s initialization file.  

**Boost 1.56 *(Required for BE)***  
BE requires Boost library to be installed and build. Boost 1.56 can be obtained [online](http://sourceforge.net/projects/boost/files/boost/1.56.0/)  
`1.` Download Boost archive file `boost_1_56_0.tar.gz` to `$HOME/scratch/src`  
`2.` Unarchive the compressed tar file  
```bash
cd $HOME/scratch/src  
tar xfz boost_1_56_0.tar.gz  
cd $HOME/scratch/src/boost_1_56_0  
```
`3.` Decide on an installation location. For this example: `$HOME/local/packages/boost-1.56`. Note this location will contain `lib`, `include`, and other directories for use of Boost.  
`4.` Set the home directory environment variable of the Boost installation.  
```bash
export BOOST_HOME=$HOME/local/packages/boost-1.56  
```
`5.` Configure Boost to be installed in `$BOOST_HOME`  
```bash
./bootstrap.sh --prefix=$BOOST_HOME  
```
`6.` Build and install Boost 1.56 in `$BOOST_HOME`  
```bash
./b2 install  
```
`7.` OPTIONAL - In some cases, it may be necessary to specify the location of the Boost library files for proper operation of SST.  
```bash
export LD_LIBRARY_PATH=$BOOST_HOME/lib:$LD_LIBRARY_PATH  
export DYLD_LIBRARY_PATH=$BOOST_HOME/lib:$DYLD_LIBRARY_PATH  
```
`8.` To make the changes to the environment variables a permanent change, it may require editing of your login shell’s initialization file.  

---

### SST CORE Build and Installation  

After the prerequisite Components (OpenMPI and boost) have been successfully installed, the SST-Core can then be built and installed.  
`1.` Navigate to SST-Core directory in `$HOME/scratch/src`.  
```bash
cd $HOME/scratch/src/sst-core-devel  
```
`2.` Set the home directory environment variable to the SST-Core installation (i.e. where you want the SST-Core files installed).  
```bash
export SST_CORE_HOME=$HOME/local/sst-core-devel  
```
`3.` Run the `autogen.sh` script to setup the configure for SST-core  
```bash
./autogen.sh  
```
`4.` Configure SST-Core, being sure to make `configure` reference the location of SST-Core’s local prerequisite packages.  
```bash
./configure --prefix=$SST_CORE_HOME  
```
`5.` Build and install SST-CORE  
```bash
make all  
make install  
```
`6.` Update your `PATH` environment variable so that it contains the bin directory of the SST-CORE installation location.  
```bash
export PATH=$SST_CORE_HOME/bin:$PATH  
```
`7.` Test your sst-core install  
```bash
which sst  
sst --version  
sst-info  
```
`8.` To make the changes to the environment variables a permanent change, it may require editing of your login shell’s initialization file.  

---

### SST ELEMENT (BE) Build and Installation  

After SST-Core has been successfully installed, Behavioral Emulation (BE) can then be built and installed.  
`1.` Navigate to the SST-element-BE directory in `$HOME/scratch/src`.  
```bash
cd $HOME/scratch/src/sst  
```
`2.` Set the home directory environment variable to the SST-Elements installation (i.e. where you want the SST-Elements files installed).  
```bash
export SST_ELEMENTS_HOME=$HOME/local/sstelements-devel  
```
`3.` Run the `autogen.sh` script to setup the configure for BE  
```bash
./autogen.sh  
```
`4.` Configure SST-Elements, being sure to make `configure` reference the location of SST-Element-BE’s local prerequisite packages.  
```bash
./configure --prefix=$SST_ELEMENTS_HOME --with-sst-core=$SST_CORE_HOME –-with-boost=$BOOST_HOME  
```
`5.` Build and install SST-ELEMENTS (This will register SST-Elements with the SST-Core)  
```bash
make all  
make install  
```
`6.` Update your PATH environment variable so that it contains the bin directory of the SST-ELEMENTS installation location.  
```bash
export PATH=$SST_ELEMENTS_HOME/bin:$PATH  
```
`7.` To make the changes to the environment variables a permanent change, it may require editing of your login shell’s initialization file.

---

### Testing BE-SST  
Assuming you are in the `sst-elements-BE` directory:  
```bash
# Navigate to the tests folder  
cd src/sst/elements/behavioralEmulation/tests/

# Version -- Simple sanity test  
sst --version

# Running the test script for BE to check its functional correctness  
./BE_TEST.sh

# Running a test configuration to obtain a simulated time   
./BE_RUN.sh -c testConfig.py  
```

---
