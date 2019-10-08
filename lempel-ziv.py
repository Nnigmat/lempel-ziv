from glob import iglob
from os import path, mkdir, chdir, listdir
from tree import Tree

OUT_DIRNAME = 'NikitaNigmatullinOutputs'
INP_DIRNAME = 'dataset'

def create_output_directories(output_dirname, input_dirname):
    # Create output folder
    if not path.exists(output_dirname) or path.isfile(output_dirname):
        mkdir(output_dirname) 

    # Create subfolders (copy subfolders from dataset)
    for fold in get_folder_files(input_dirname):
        if path.isdir(f'{input_dirname}/{fold}') and not path.exists(f'{output_dirname}/{fold}'):
            mkdir(f'{output_dirname}/{fold}')

def encrypt(source_file_path, target_file_path):
    table = {0: (0, 0, 0)}
    prev = 0

    with open(source_file_path, 'rb') as f:
        # Read file as a sequence of numbers
        step =  1

        b = f.read(1)
        while b != b'':
            cur = int(f'{prev}{ord(b)}')
            if cur not in codes:
                substr = codes[prev]
                table[cur] = (step, substr[0], ord(b))
                prev, step = 0, step + 1
            else:
                prev = cur
            b = f.read(1)

    with open(target_file_path, 'w') as f:
        for i in table:
            _, prev_step, char = table[i]
            prev_step = '{0:b}'.format(prev_step)
            prev_step = '0' * (7-len(prev_step) % 7) + prev_step
            tmp = ['0' + prev_step[i:i+7] for i in range(0, len(prev_step), 7)]
            tmp[-1] = '1' + tmp[-1][1:]
            
            f.write(''.join(map(lambda x: chr(int(x, 2)), tmp)) + chr(char))  
        
        if prev != 0:
            _, prev_step, char = table[prev]
            prev_step = '{0:b}'.format(prev_step)
            prev_step = '0' * (7-len(prev_step) % 7) + prev_step
            tmp = ['0' + prev_step[i:i+7] for i in range(0, len(prev_step), 7)]
            tmp[-1] = '1' + tmp[-1][1:]

            f.write(''.join(map(lambda x: chr(int(x, 2)), tmp)) + chr(char))
        # print(codes)


def decrypt(source_file_path, target_file_path):
    table = {0: (-1, '')}

    # with open(source_file_path, 'rb') as f:
    #     step = 1
    #     seq = ''
    #     b = f.read(1)
    #     while b != b'':
    #         seq += b ^ 
    #         if f'{0:b}'.format(b).startswith('1'):
    #             seq += b
    #             b = f.read(1)
    #             table[]

    #         b = f.read(1)

def get_folder_files(input_dirname):
    ### Return dictionary of subdirectories of `input_dirname` and files inside of those subdirectories  
    ### Result example: {'pdf':['file1.pdf', 'file2.pdf'], 'txt':['file1.txt']}
    return {fold:listdir(f'{input_dirname}/{fold}') for fold in listdir(input_dirname)}

if __name__ == "__main__":
    create_output_directories(OUT_DIRNAME, INP_DIRNAME)

    for folder, files in get_folder_files(INP_DIRNAME).items():
        for f in files:
            encrypt(f'{INP_DIRNAME}/{folder}/{f}', f'{OUT_DIRNAME}/{folder}/{f.split(".")[0]}Compressed.{f.split(".")[1]}')
    # print(encrypt('dataset/doc/tmp.txt', 'NikitaNigmatullinOutputs/doc/temp.txt'))
