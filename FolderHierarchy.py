from os import makedirs

dirs = ['train/', 'test/']
for subdir in dirs:
	label_dirs = ['dogs/', 'cats/']
	for label_dir in label_dirs:
		new_dir = "dataset/" + subdir + label_dir
		makedirs(new_dir, exist_ok=True)