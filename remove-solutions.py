import json 

import glob

# find all notebooks 
all_notebooks = glob.glob('**/*.ipynb', recursive=True)

if len(all_notebooks)==0:
    exit('No notebooks found')

# iterate over all notebooks
for nb in all_notebooks:

    with open(nb) as f: 
        data = json.load(f)

    student_version = []
    solutionsremoved = 0
    for cell in data['cells']:
        if 'tags' in cell['metadata']:
            if 'solution' not in cell['metadata']['tags']:
                student_version.append(cell)
            else:
                solutionsremoved +=1
        else:
            student_version.append(cell)

    data['cells'] = student_version
    
    print(f'Removed {solutionsremoved} solution cells in {nb}')

    with open(nb, 'w') as outfile:
        json.dump(data, outfile)