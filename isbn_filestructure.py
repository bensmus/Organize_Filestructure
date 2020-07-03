import PyPDF2
import os
import shutil  
from tabulate import tabulate  # for pretty printing

# this program goes through a filetree and (a) renames the files according to ISBN-13 Convention, (b) moves them all to one directory

### workflow ### 
# Copy entire filetree from ftp server to local computer and rename it to ftpfiles_original.
# Make a directory called ftpfiles_formatted in the same directory as ftpfiles_original (NECESSARY).
# Run this program, which should populate ftpfiles_formatted with files in the correct format.
# The program will ask you for a filename, which will be the filename of a file that contains the old and new filenames (effectively shows you what the prgram did).
# This file is used for the companion program xml_write_v4.py, which uses that file to make an ONIX file.
# Lastly the program also creates two .txt files for problematic pdf's (the program creates three .txt files in total)

# also note that you may see 'file' being syntax highlighted specially
# but that is just due to it being the name of a builtin function in python2 (depreciated)
def extract_isbn(filepath):
    '''Returns the proper filename for the PDF using ISBN13.'''
    
    with open(filepath, 'rb') as f:
        reader = PyPDF2.PdfFileReader(f)

        string = ''
        for i in range(7):  
            page = reader.getPage(i)
            string += page.extractText()

    start = string.find('ISBN')  # returns -1 if no ISBN found
    if start == -1:
        return 

    string = string[start:]
    
    isbn = ''
    for char in string:
        if len(isbn) == 13:
            break
        if char.isdigit():
            isbn += char

    if len(isbn) == 13:
        return isbn + '.pdf'


failed_isbn = []  # cannot find ISBN inside pdf
failed_open = []  # failed to open pdf
successes = 0  # number of successfuly copied files
failures = 0  # number of failed files

# Check that the directory is found on the system  
rootdir = r'C:\Users\Ben Smus\Evident_Point\FTP\Carnegie_Clone\ftpfiles_original'
if not os.path.exists(rootdir):
    raise OSError(f'Directory {rootdir} does not exist on your computer')

# where we will be moving all of the files 
targetdir = r'C:\Users\Ben Smus\Evident_Point\FTP\Carnegie_Clone\ftpfiles_formatted'

# finding the total number of files so that we can include in the progress log
total = 0
for folder, subs, files in os.walk(rootdir):
    for f in files:
        total += 1

# used for creating ONIX script in another program
text_filename = input('Output filename (use extension .txt)? ')

# file for storing old (descriptive) and new (ISBN13) names
with open(text_filename, 'a') as namefile:

    # searching all supdirectories of rootdir
    for folder, subs, files in os.walk(rootdir):
        
        for name in files:   
            full_name = os.path.join(folder, name)  # e.g C:\Users\foo.pdf

            try:
                new_name = extract_isbn(full_name)
                
                if new_name != None:
                    new_full_name = os.path.join(targetdir, new_name)

                    # copy the file to the new location
                    shutil.copy(full_name, new_full_name)

                    namefile.write(new_name + ' ')
                    namefile.write(name + '\n')
                    
                    successes += 1
                    

                else:
                    failures += 1
                    failed_isbn.append(full_name)
            
            except OSError as e:
                failures += 1
                failed_open.append(full_name)

            # unicode check and crosses for success and failure
            # using tabulate to get a nice output
            table = [[successes, failures, total]]
            print(tabulate(table, headers=[u'\u2713', u'\u2717', 'total']))

#   ✓    ✗    total
# 119   15      134

with open('failed.txt', 'a') as f:

    f.write('FAILED TO OPEN\n')
    for name in failed_open:
        f.write(name + '\n')
    f.write('\n')
    f.write('FAILED TO LOCATE ISBN\n')
    for name in failed_isbn:
        f.write(name + '\n')
    


    

