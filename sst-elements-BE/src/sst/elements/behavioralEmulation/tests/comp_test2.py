Component( "BGQ-core" )
Program( "BGQ-core", "comp_test1.txt" )

Property( "BGQ-core", "app.elementSize", lambda gid, cid, cids, index: 20 )
Property( "BGQ-core", "mpi.commRank", lambda gid, cid, cids, index: cid  )
Property( "BGQ-core", "mpi.commSize", lambda gid, cid, cids, index: cids )

Ordinal( "BGQ-core", "mpi.commRank" )
Relation( "BGQ-core", "BGQ-core", "cpu", "self" )
Attribute( "BGQ-core", "usage", 0.0 )

Component( "BGQ-network" )
Attribute( "BGQ-network", "usage", 0.0 )

Operation( "BGQ-core", "computeA", "computeA.csv", "linear",
           Dawdle( Outputs(0) ))
Operation( "BGQ-core", "computeB", "computeB.csv", "linear",
           Dawdle( Outputs(0) ))
Operation( "BGQ-core", "computeC", "computeC.csv", "linear",
           Dawdle( Outputs(0) ))

Component( "system" )
Offspring( "system", Torus("BGQ-core", "BGQ-network", [1, 2, 2, 2, 2]) )
#Offspring( "system", Torus("BGQ-core", "BGQ-network", [8, 4, 4, 4, 4]) )
Root("system")

