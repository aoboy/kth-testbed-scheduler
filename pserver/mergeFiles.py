import csv
import os

def append_files(path, mergepath):
    from_dirs    = os.listdir(os.path.abspath(path))
    to_dirs      = os.listdir(os.path.abspath(mergepath))

    from_dirs.sort()
    to_dirs.sort()

    for fdir in from_dirs:
       if os.path.isdir(os.path.join(path,fdir)):
          if fdir.find('Tsch') != -1 or fdir.find('Ch') != -1:
              fdirPath  = path+fdir+'/'
              todirPath = mergepath+fdir+'/'
              fromFiles = os.listdir(os.path.abspath(fdirPath))
              toFiles   = os.listdir(os.path.abspath(todirPath))
              for fname in fromFiles:
                  for mfile in toFiles:
                      if fname == mfile:
                          d2append = open(os.path.join(fdirPath, fname),'rb').read()
                          f2append = open(os.path.join(todirPath, mfile),'a')
                          f2append.write(d2append)
                          #d2append.close()
                          f2append.close()
                          break

if __name__ == '__main__':
    path ='/home/gonga/TSCH/MATLAB/ExperimentalDataLogs/T2Repeat/'
    mergepath = '/home/gonga/TSCH/MATLAB/ExperimentalDataLogs/Merge/'

    append_files(path, mergepath)