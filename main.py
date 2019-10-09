from glob import iglob
from os import path, mkdir, chdir, listdir
from multiprocessing import Process

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

def get_folder_files(input_dirname):
    ### Return dictionary of subdirectories of `input_dirname` and files inside of those subdirectories  
    ### Result example: {'pdf':['file1.pdf', 'file2.pdf'], 'txt':['file1.txt']}
    return {fold:listdir(f'{input_dirname}/{fold}') for fold in listdir(input_dirname)}

def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])

def encrypt(source_file_path, target_file_path):
    table = {-1: (0, 0, 0)}
    prev = -1

    with open(source_file_path, 'rb') as f:
        # Read file as a sequence of numbers
        step =  1

        b = f.read(1)
        while b != b'':
            cur = int(f'{prev}{ord(b)}')
            if cur not in table:
                substr = table[prev]
                table[cur] = (step, substr[0], ord(b))
                prev, step = -1, step + 1
            else:
                prev = cur
            b = f.read(1)

    with open(target_file_path, 'wb') as f:
        table.pop(-1)
        for i in table:
            _, prev_step, char = table[i]
            # Format step and char to binary format and make their lenght divisible by 7 
            prev_step, char = '{0:b}'.format(prev_step), '{0:b}'.format(char)
            prev_step, char = '0' * (7-len(prev_step) % 7) + prev_step, '0' * (8-len(char)) + char 
            tmp = ['0' + prev_step[j:j+7] for j in range(0, len(prev_step), 7)]
            tmp[-1] = '1' + tmp[-1][1:]

            f.write(bitstring_to_bytes(''.join(tmp + [char])))
        
        if prev != 0:
            _, prev_step, char = table[prev]
            # Format step and char to binary format and make their lenght divisible by 7 
            prev_step, char = '{0:b}'.format(prev_step), '{0:b}'.format(char)
            prev_step, char = '0' * (7-len(prev_step) % 7) + prev_step, '0' * (8-len(char)) + char 
            tmp = ['0' + prev_step[j:j+7] for j in range(0, len(prev_step), 7)]
            tmp[-1] = '1' + tmp[-1][1:]

            print(tmp, char)
            f.write(bitstring_to_bytes(''.join(tmp + [char])))
    
    print(f'{source_file_path} encrypted!')


def decrypt(source_file_path, target_file_path):
    table = {0: (-1, b'')}

    with open(source_file_path, 'rb') as f:
        step = 1
        prev_step = ''
        
        b = f.read(1)
        while b != b'':
            tmp = '{0:b}'.format(ord(b))
            tmp = tmp if len(tmp) == 8 else '0' * (8 - len(tmp)) + tmp
            prev_step += tmp[1:]
            if tmp.startswith('1'):
                char = f.read(1)
                table[step] = (int(prev_step, 2), table[int(prev_step, 2)][1] + char)
                print(table[step])

                step += 1
                prev_step = ''
            b = f.read(1)
            
    with open(target_file_path, 'wb') as f:
        table.pop(0)
        for i in table:
            f.write(table[i][1])

    print(f'{source_file_path} decrypted!')


if __name__ == "__main__":
    # create_output_directories(OUT_DIRNAME, INP_DIRNAME)

    # jobs = []
    # for folder, files in get_folder_files(INP_DIRNAME).items():
    #     for f in files:
    #         p = Process(target=encrypt, args=(f'{INP_DIRNAME}/{folder}/{f}', f'{OUT_DIRNAME}/{folder}/{f.split(".")[0]}Compressed.{f.split(".")[1]}', ))
    #         jobs.append(p)
    #         p.start()
    # for j in jobs:
    #     j.join()


    # jobs = []
    # for folder, files in get_folder_files(INP_DIRNAME).items():
    #     for f in files:
    #         p = Process(target=decrypt, args=(f'{OUT_DIRNAME}/{folder}/{f.split(".")[0]}Compressed.{f.split(".")[1]}', f'{OUT_DIRNAME}/{folder}/{f.split(".")[0]}Decompressed.{f.split(".")[1]}', ))
    #         jobs.append(p)
    #         p.start()
    # for j in jobs:
    #     j.join()
    encrypt('dataset/jpg/file1.jpg', 'compressed')
    decrypt('compressed', 'decompressed.jpg')