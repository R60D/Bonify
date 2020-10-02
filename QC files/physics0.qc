$modelname "Physics\Test0.mdl"
$Scale 100
	$bodygroup "Test"
	{
		studio "0.smd"

	}

	$cdmaterials "models\physics"
	// Freeze at frame 0
	$sequence "Pre" {
		"anims/Action.smd"
		fps 24 frame 0 0 
	}
	// Plays the simulation
	$sequence "Action" {
		"anims/Action.smd"
		fps 24
	}
	// Freeze at frame 250
	$sequence "Post" {
		"anims/Action.smd"
		fps 24 frame 120 120
	}