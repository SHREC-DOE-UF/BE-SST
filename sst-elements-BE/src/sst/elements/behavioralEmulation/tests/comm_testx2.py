Component( "BGQ-core" )
Program( "BGQ-core", "comm_testx2.txt" )

Property( "BGQ-core", "app.transferSize", lambda gid, cid, cids, index: 128 )
Property( "BGQ-core", "app.elementPerProcessor", lambda gid, cid, cids, index: 64 )
Property( "BGQ-core", "app.elementSize", lambda gid, cid, cids, index: 9 )
Property( "BGQ-core", "app.particleCount", lambda gid, cid, cids, index: 10 )

Property( "BGQ-core", "mpi.commRank", lambda gid, cid, cids, index: cid  )
Property( "BGQ-core", "mpi.commSize", lambda gid, cid, cids, index: cids )

Ordinal( "BGQ-core", "mpi.commRank" )
Relation( "BGQ-core", "BGQ-core", "cpu", "self" )
Attribute( "BGQ-core", "usage", 0.0 )

Operation( "BGQ-core", "wait", NoLookup, None,
           RecvWait(True))
Operation( "BGQ-core", "unwait", NoLookup, None,
           Recv(True))

Mailbox( "BGQ-core", "unwait", lambda source, target, size, tag: [source],
         OnTarget )

e1="testPart3.txt"
Operation( "BGQ-core", "computeA", "testPart3.txt", "Equation",
           Dawdle( e1 ))

Component( "BGQ-network" )
Attribute( "BGQ-network", "usage", 0.0 )
Operation( "BGQ-network", "transfer", "comm_test1.csv", "linear",
           Dawdle( Outputs(0) ))

Mailbox( "BGQ-network", "transfer", lambda source, target, size, tag: [size],
         OnAll )

Component( "system" )
Offspring( "system", Mesh("BGQ-core", "BGQ-network", [2, 2, 2]) )
Root("system")

