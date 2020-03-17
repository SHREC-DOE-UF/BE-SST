# BE-SST

BE-SST is a parallel and scalable coarse-grained simulator that employs statistical models to run probabilistic, discrete-event simulation by combining Behavioral Emulation (BE), a coarse-grained modeling approach and Structural Simulation Toolkit (SST), a parallel discrete-event simulation framework from Sandia National Laboratories. BE-SST can be used for application design-space exploration (DSE) where alternate algorithms of an application can be studied on a given architecture; or architectural DSE can be performed for a given application. BE-SST provides a distributed parallel simulation library for Behavioral Emulation through simple interfaces and framework for development of coarse-grained BE models which can be easily extended to model new notional architectures. BE-SST also provides the capability to plug-n-play different subsystems (node, interconnect, memory, etc.), which is necessary to study abstract and notional machines.  
> **_Note:_** Both SST-core and SST-element-BE are provided to you through this repository. You DO NOT have to download the SST-core from the [SST website](www.sst-simulator.org).

## Build and Run

#### Following dependencies are required to build and run BE-SST: 
1. gcc 4.7 and newer  
2. python 2 (anything in 2.7 branch)  
  2.1 numpy package  
  2.2 python-dev
3. GNU make 4.0 or newer  
4. autotools (libtool, autoconf, automake)  
5. [OpenMPI 2.1.3](http://www.open-mpi.org/software/ompi/v2.1/) *(strongly recommended)*   
6. [Boost 1.56](http://sourceforge.net/projects/boost/files/boost/1.56.0/)  
**Note:** OpenMPI 2.1.3 and Boost 1.56 installation steps are listed in BE-SST build and installation document

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

Installation and build process for OpenMPI 2.1.3, Boost 1.56, `sst-core-devel` and `sst-element-BE` are listed in the BE-SST installation and build guide.docx. Refer to this document for detailed step-by-step instruction.

### Testing BE-SST  
Assuming you are in the top directory where `sst-core-devel` and `sst-elements-BE` directories are present:  
\# Navigate to the [tests](sst-elements-BE/src/sst/elements/behavioralEmulation/tests/) folder in `sst-elements-BE`  
cd sst-elements-BE/src/sst/elements/behavioralEmulation/tests/

\# Version -- Simple sanity test  
sst --version

\# Running the test script for BE to check its functioning correctly  
./BE_TEST.sh

\# Running a test configuration to obtain a simulated time   
./BE_RUN.sh -c testConfig.py  

---

### Refer to the following papers for more information on BE [1] and BE-SST [2]:  
[1] Kumar N., Pascoe C., Hajas C., Lam H., Stitt G., George A. (2016) Behavioral Emulation for Scalable Design-Space Exploration of Algorithms and Architectures. In: Taufer M., Mohr B., Kunkel J. (eds) High Performance Computing. ISC High Performance 2016. Lecture Notes in Computer Science, vol 9945. Springer, Cham. https://link.springer.com/chapter/10.1007/978-3-319-46079-6_1  
[2] Ajay Ramaswamy, Nalini Kumar, Aravind Neelakantan, Herman Lam, and Greg Stitt. 2018. Scalable Behavioral Emulation of Extreme-Scale Systems Using Structural Simulation Toolkit. In Proceedings of the 47th International Conference on Parallel Processing (ICPP 2018). Association for Computing Machinery, New York, NY, USA, Article 17, 1–11. DOI:https://doi.org/10.1145/3225058.3225124  
*If you consider using this work, please site the above papers.*

For any questions regarding the simulator, contact **Aravind Neelakantan** at aravindneela@ufl.edu
