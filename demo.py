import os

dataset_path = 'Data'
for dirname, j, file_name_list in os.walk(dataset_path):
    print(dirname)
    print(j)
    for file_name in file_name_list:
        print(os.path.join(dirname, file_name))
