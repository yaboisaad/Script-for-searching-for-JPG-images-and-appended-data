'''
Author: Mohammad Saad
G01026444
CFRS 510
Homework 3
'''

import os
import hashlib
import datetime
import base64


def sha256HashFunc(file_directory):
    fd = open(file_directory, 'rb')
    file_data = fd.read()
    hash_of_file = hashlib.sha256(file_data).hexdigest()
    return hash_of_file


def main():
    '''
    This first part of the function will ask the user for the directories to check. It will loop on and on until 
    the user is satisfied with the directories entered and enters 'no'
    '''
    try:
        import os
    except ImportError as error1:
        print("Module error. Please install: ", error1)
    try:
        import hashlib
    except ImportError as error2:
        print("Module error. Please install: ", error2)
    try: 
        import json
    except ImportError as error3:
        print("Module error. Please install: ", error3)
    try: 
        import datetime
    except ImportError as error4:
        print("Module error. Please install: ", error4)
    try:
        import base64
    except ImportError as error5:
        print("Module error. Please install: ", error5)
    x = 0
    paths = []
    try:
        folder = input("Please enter the directory path you want to investigate: ")   
       # paths.append(folder)
    except:
        paths = None
    '''
    The if-statements below check for errors. If these erorrs are raised, it may be the user's fault.
    '''
    if(folder == ''):
        raise ValueError("You entered nothing. Please enter a directory next time.")
    folder_check = os.path.isfile(folder)
    if(folder_check == True):
        raise ValueError("You entered a file name instead of a directory/path. Please enter a directory.\n")
    just_file_names = []
    for root, dirs, files in os.walk(folder):
        for filename5 in files:
            just_file_names.append(filename5)
            filename5 = root + "/" + filename5
            paths.append(filename5)
    w = 0                                              #Counter variable
    file_name_array = []
    length_of_paths = len(paths)
    '''
    This while-loop's purpose is to collect all of the file's entire directory paths to easily open it up later. Example: (/File2Check/JPGs/jpg01)
    '''
    list_of_files = len(file_name_array)
    if not just_file_names:
        raise ValueError("You may have entered an incorrect directory or it is empty. Please check.")
    #If  the list "just_file_names is empty, that means something went wrong."
    
    u = 0                                              #Counter variable
    file_LIST = []
    '''
    #This for-loop is used to collect ONLY the file's names. Example: (jpg01)
    '''
    for j in paths:
        for p in file_name_array:
            for n in p:
                temp = j + '/' + n
                file_checker2 = os.path.isfile(temp)
                if(file_checker2 == True):
                    file_LIST.append(temp)
                    just_file_names.append(n)
    '''Creating arrays to store all of the files' information.'''
    list_of_hashes = []
    creation = []
    modification = []   
    access = []
    v = len(paths)
    jpg_string = b"\xff\xd8\xff"
    ''' Above is the header signature in hex of a JPG image. I use it to splice a file's header to check if a file is a JPG or not.'''
    jpg_files = []
    ONLY_JPG_NAMES = []
    y = 0
    '''
    This while-loop is used to read the first 20 bytes of each files' header information.
    If the JPG header signature is inside of the header, then it is considered a JPG file.
    If it is a JPG, then all of the access, modification, and creation times for each
    file is collected and stored in an array. 
    Also, if the file is a JPG, the SHA256 hash is taken of that file and stored. 
    '''
    while(y < v):
        header_data = open(paths[y], 'rb').read(20)
        if(jpg_string in header_data):
            hash_data = sha256HashFunc((paths[y]))
            a_time = os.path.getatime(paths[y])
            m_time = os.path.getmtime(paths[y])
            c_time = os.path.getctime(paths[y])
            if(just_file_names[y] in paths[y]):
                ONLY_JPG_NAMES.append(just_file_names[y])
            list_of_hashes.append(hash_data)
            access.append(a_time)
            modification.append(m_time)
            creation.append(c_time)
            jpg_files.append(paths[y])
            y += 1
        else:
            y += 1
    '''
    A text file is created which stores the dictionary's contents. It will also store any appended data if a file has it.
    Each file will be checked with the hw64decode() function.
    '''
    txtfile = open('SaadOutput.txt', 'w')
    hashes_with_no_appdata, decoded_message_main, names_with_app = hw64decode(jpg_files, ONLY_JPG_NAMES)
    file_info_dict = {}
    file_info_dict["File names(Only JPG files)"] = str(ONLY_JPG_NAMES)
    #file_info_dict["Hashes"] = list_of_hashes
    file_info_dict["Creation times:"] = str(creation)
    file_info_dict["Access times:"] = str(access)
    file_info_dict["Modification times:"] = str(modification)
    file_info_dict["Hashes of files with no appended data:"] = str(hashes_with_no_appdata)
    for key,values in file_info_dict.items():
        txtfile.write(key)
        txtfile.write(values)
        txtfile.write("\n")
    b = 0
    length_of_decoding = len(decoded_message_main)
    '''
    Thie while-loop writes all decoded appended data from each file into the textfile. Along with the file's name.
    '''
    while(b < length_of_decoding):
        txtfile.write("\nFile name: ")
        txtfile.write(names_with_app[b])
        txtfile.write("\nThe decoded appended data: ")
        txtfile.write(decoded_message_main[b])
        b += 1
    directory1 = os.getcwd()
    print("\nThe JPG files' names, hashes, and timestamps are all saved to")
    print("a textfile in the same directory that this script was run in. That directory is this: ", directory1)
    print("The dictionary's contents will be listed as this: ")
    print("File names, hashes, creation times, access times, and modificaton times.")
    print("They are all lined up respectively to one another.")
    print("(First element in each type of info match up to the same file.)")
    time_exec = datetime.datetime.now()
    date_time_exec = time_exec.strftime("%m/%d/%y, %H:%M:%S")
    print("The script finished executing at: ", date_time_exec)


def hw64decode(jpg_files, ONLY_JPG_NAMES):
    '''
    This function will take in an array of file names that are strictly JPG only.
    It will also take in the same array with just a different naming convention. 
    '''
    jpg_footer = b"\xff\xd9"
    x = 0
    message_decoded_array = []
    filenames_with_appended_data = []
    hash_of_files_with_no_appdata = []
    length_of_jpgfiles = len(jpg_files)
    '''
    This loop will check every single JPG file's bytes to see if
    it contains any data after the footer ends. If it does, then 

    '''
    while(x < length_of_jpgfiles):
        file_footer = open(jpg_files[x], 'rb').read()
        base64_content = file_footer.split(b"\xff\xd9")
        temp = base64_content[1]
        if not temp:
            file_footer2 = hashlib.sha256(file_footer).hexdigest()
            hash_of_files_with_no_appdata.append(file_footer2)
            x += 1
        else:
            decoded_utf = temp.decode('utf-8')
            message_64 = base64.b64decode(decoded_utf)
            message_decoded = message_64.decode('ascii')
            file_info_no64 = hashlib.sha256(file_footer).hexdigest()
            message_decoded_array.append(message_decoded)
            hash_of_files_with_no_appdata.append(file_info_no64)
            filenames_with_appended_data.append(ONLY_JPG_NAMES[x])
            x += 1
    return hash_of_files_with_no_appdata, message_decoded_array, filenames_with_appended_data



if __name__ == '__main__':
    main()

