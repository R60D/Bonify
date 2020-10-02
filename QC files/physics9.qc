$modelname "Physics\Test9.mdl"
$Scale 100
	$bodygroup "Test"
	{
		studio "9.smd"

	}

	$cdmaterials "models\physics"
	// Freeze at frame 0
	$sequence "Pre" {
		"anims/Action.009.smd"
		fps 24 frame 0 0 
	}
	// Plays the simulation
	$sequence "Action" {
		"anims/Action.009.smd"
		fps 24
	}
	// Freeze at frame 250
	$sequence "Post" {
		"anims/Action.009.smd"
		fps 24 frame 250 250 
	}