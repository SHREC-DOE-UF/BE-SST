Component( "BGQ-core" )
Program( "BGQ-core", "particles_solver_baseline.txt" )

Property( "BGQ-core", "app.elementSize", lambda gid, cid, cids, index: 15 )
Property( "BGQ-core", "app.elementsPerProcess", lambda gid, cid, cids, index: 4 )
Property( "BGQ-core", "app.alpha", lambda gid, cid, cids, index: 0.1 )

Property( "BGQ-core", "mpi.commRank", lambda gid, cid, cids, index: cid  )
Property( "BGQ-core", "mpi.commSize", lambda gid, cid, cids, index: cids )
Ordinal( "BGQ-core", "mpi.commRank" )
Relation( "BGQ-core", "BGQ-core", "cpu", "self" )
Attribute( "BGQ-core", "usage", 0.0 )
 
Operation( "BGQ-core", "update_particles_location", "vulcan-compute-update_particle_location.csv", "linear",
                 Loiter( "usage", "==", 0.0),
                 Modify( "usage", 1.0 ),
                 Dawdle( AnyOutput() ),
                 Modify( "usage", 0.0 ) )
Operation( "BGQ-core", "update_particles_position", "vulcan-compute-Update_particle_pos.csv", "linear",
                 Loiter( "usage", "==", 0.0),
                 Modify( "usage", 1.0 ),
                 Dawdle( AnyOutput() ),
                 Modify( "usage", 0.0 ) )
Operation( "BGQ-core", "Compute1", "vulcan-compute-compute1.csv", "linear",
                 Loiter( "usage", "==", 0.0),
                 Modify( "usage", 1.0 ),
                 Dawdle( AnyOutput() ),
                 Modify( "usage", 0.0 ) )
Operation( "BGQ-core", "crystal_tuple_sort", "vulcan-compute-crystal_tuple_sort.csv", "linear",
                 Loiter( "usage", "==", 0.0),
                 Modify( "usage", 1.0 ),
                 Dawdle( AnyOutput() ),
                 Modify( "usage", 0.0 ) )
Operation( "BGQ-core", "interp_props_part_location", "vulcan-compute-interp_props_part_location.csv", "linear",
                 Loiter( "usage", "==", 0.0),
                 Modify( "usage", 1.0 ),
                 Dawdle( AnyOutput() ),
                 Modify( "usage", 0.0 ) )
Operation( "BGQ-core", "usr_particles_forces", "vulcan-compute-particles_forces.csv", "linear",
                 Loiter( "usage", "==", 0.0),
                 Modify( "usage", 1.0 ),
                 Dawdle( AnyOutput() ),
                 Modify( "usage", 0.0 ) )
Operation( "BGQ-core", "Compute2", "vulcan-compute-update_vel_and_pos_rk3->Stage1.csv", "linear",
                 Loiter( "usage", "==", 0.0),
                 Modify( "usage", 1.0 ),
                 Dawdle( AnyOutput() ),
                 Modify( "usage", 0.0 ) )
Operation( "BGQ-core", "Compute3", "vulcan-compute-update_vel_and_pos_rk3->Allstages.csv", "linear",
                 Loiter( "usage", "==", 0.0),
                 Modify( "usage", 1.0 ),
                 Dawdle( AnyOutput() ),
                 Modify( "usage", 0.0 ) )
Operation( "BGQ-core", "Compute4", "vulcan-compute-update_vel_and_pos_rk3->Stage3.csv", "linear",
                 Loiter( "usage", "==", 0.0),
                 Modify( "usage", 1.0 ),
                 Dawdle( AnyOutput() ),
                 Modify( "usage", 0.0 ) )

Component( "BGQ-network" )
Attribute( "BGQ-network", "usage", 0.0 )

Component( "system" )
Offspring( "system", Torus( "BGQ-core", "BGQ-network", [ 8, 8, 8, 8, 8 ] ) )
Root("system")
