### 
# Hiro Antagonist, Jun 29, 2022
# Written for Python 3.9.10
# 
# This script is for reading through big password dumps and sorting out
# all of the garbage, while outputing the valid unames and passwords
# to relevant .txt files, labeled uname.txt and passwd.txt.
# Creates status.txt to make sure files are not repeated.
#
# To operate properly, run this script in a directory, and it 
# will read .txt files for user/pass combos,
# separating credentials to be used for dictionary attacks.
#
# status.txt example:
# foo.txt
# bar.txt
# baz.txt
#
# To do:
## Verbose flag // log file to hold output?
## 
## Terminal and init functions to gracefully stop and pick up again
## Option to skip redundant passwords
#       but how do we do this without taking 200 years?
###

import os

class Cleaner:

    def __init__(self):
        # run at the start to create/load all the necessary files
        # returns handlers for the output files
        ## currently, just creates files! need to make it read instead
        self.input = None
        self.files = []
        dir_list = os.listdir('.')
        #self.files.remove("main.py")


        for fname in dir_list:
            #remove protected files, and non-.txt files
            if fname[0] == "." and fname[1] != '/':
                print ('skipping protected file', fname)
                continue
            elif ".txt" not in fname:
                #try to read subdirectory
                if os.path.isdir(fname):
                    if fname[:2] == "./":
                        for subfile in os.listdir(fname):
                            dir_list.append(fname+'/'+subfile)
                    else:
                        for subfile in os.listdir('./'+fname):
                            dir_list.append('./'+fname+'/'+subfile)

                print ('skipping non-txt file', fname)
                continue
            self.files.append(fname)
        
        #make sure we have support files
        if "status.txt" in self.files:
            self.files.remove("status.txt")
            self.stat = open("status.txt","r+")
        else:
            print("creating status.txt")
            self.stat = open("status.txt","w+")

        if "passwd.txt" in self.files:
            self.files.remove("passwd.txt")
        else:
            print("creating passwd.txt")
        self.passwd = open("passwd.txt","w+")

        if "uname.txt" in self.files:
            self.files.remove("uname.txt")
        else:
            print("creating uname.txt")
        self.uname = open("uname.txt","w+")

        if "log.txt" in self.files:
            self.files.remove("log.txt")
        else:
            print("creating log.txt")
        self.logs = open("log.txt","w+")

    def EOF(self):
        #Run this after we finih a file.
        pass


    def clear(self):
        #this function will clear the status, log, passwd, and uname files upon execution.
        #use at your own risk!
        print("running clear.....")
        self.passwd = open("passwd.txt","w")
        self.passwd.write("")
        self.uname = open("uname.txt","w")
        self.uname.write("")
        self.logs = open("log.txt","w")
        self.logs.write("")
        self.stat = open("status.txt","w")
        self.stat.write("")
        self.stat.close()
        self.stat = open("status.txt","r+")


    def stop(self):
        # just a cleaner func to close file pointers before quitting
        print ("finishing up")
        self.uname.close()
        self.passwd.close()
        self.logs.close()
        self.stat.close()
        #self.input.close()



    def getSeparator(self):
        # figure out the separator between user/pass for the dump
        line = self.input.readline()
        if " " in line:
            #if has space, obviously space is separator
            self.input.seek(0,0)
            return " "
        #else, read through lines and remove separators until there is only one left
        sep = [";",":",",","/","\t"]
        for element in sep:
            if element not in line:
                sep.remove(element)
        while len(sep) > 1:
            line = self.input.readline()
            for element in sep:
                if element not in line:
                    sep.remove(element)
        self.input.seek(0,0)
        if len(sep) == 1:
            return(sep[0])
        else:
            print ("error finding separator for", self.input.name)


    def main(self):
        # set up in while loop for all the files in dir,
        # with graceful stop (include line signature)
        # and also an init that reads where we picked up last

        #read out status info to use later
        if self.stat:
            # cur = self.stat.readline().strip() #current file
            # start_lnum = int(self.stat.readline().strip()) #line number
            
            #build list of fnames which were read already
            complete = [] 
            tmp = self.stat.readline().strip()
            while (tmp) != '':
                complete.append(str(tmp))
                tmp = self.stat.readline().strip()


            #remove files already read
            for fname in complete:
                if fname in self.files:
                    self.files.remove(fname)
            
            # print out dir status
            if len(self.files) < 20:
                print ("To do:", self.files)
            else:
                print (len(self.files), "files to read")
            if len(complete) < 20:
                print ("finished files:", complete)
            else:
                print (len(complete), "finished files")
        
        # Main workhorse loop
        for file in self.files:
            print ("\nOpening", file)
            self.input = open(file,"r")
            try:
                sep = self.getSeparator()
            except:
                print("error finding separator for file")
                continue

            # Parse through input, line-by-line, and handle cases:
            try:
                garbage = False
                for l_num,line in enumerate(self.input):
                    try:
                        splt = line.split(sep)
                        usr = splt[0]
                        pwd =splt[1].strip()
                        if len(usr) > 1:
                            self.uname.write(usr + '\n')
                        if len(pwd) > 1:
                            self.passwd.write(pwd + '\n')
                    except:
                        #garbage line
                        if not garbage:
                            print ("garbage line detected -- see log.txt")
                            garbage = True
                        out = "garbage line "+str(l_num + 1)+" in "+self.input.name+": "+line.strip()+" ...skipping line...\n"
                        self.logs.write(out)
            except UnicodeDecodeError:
                print("unicode decode error in", self.input.name)

            #wrapping up
            self.stat.write(self.input.name + "\n")
            self.input.close()
            
        self.stop()

### start of body ###
cleaner = Cleaner()
#cleaner.clear()
cleaner.main()