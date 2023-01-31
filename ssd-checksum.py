import os
import sys
import random
import hashlib

def random_file(size):
  # grab size from /dev/urandom
  return os.urandom(size)

def get_hash(data):
  # get md5 hash of data
  return hashlib.md5(data).hexdigest()

def write_random_file(path, size):
  contents = random_file(size)
  hash = get_hash(contents)
  filename = path + '/ssdcheck' + hash + '.dat'
  with open(filename, 'wb') as f:
    f.write(contents)

def verify_file(path, filename):
  with open(path + '/' + filename, 'rb') as f:
    data = f.read()
    hash = get_hash(data)
    if hash != filename[8:-4]:
      return False
    else:
      return True

def write_files_until_full(path, size):
  print("\nWRITING FILES")
  try:
    i = 0
    while True:
      print(i, end=" ", flush=True)
      i += 1
      write_random_file(path, size)
  except:
    print("\n\nDONE WRITING FILES. NOW VERIFYING...")

def verify_all_files(path, size):
  files = os.listdir(path)
  random.shuffle(files)

  i = 0
  for filename in files:
    if not filename.startswith('ssdcheck'):
      continue
    # skip incomplete files
    if os.path.getsize(path + '/' + filename) < size:
      continue
    print(i, end=" ", flush=True)
    i += 1
    if not verify_file(path, filename):
      print("\nERROR: file %s is corrupt\n" % filename)
      sys.exit(1)

  print("\n\nDONE. ALL FILES VERIFIED OK.")
  print("Verified capacity: %d GB" % (i * 100 / 1024))

def main():
  print("ssd-checksum: fills SSD with random files, and then verifies that they can be read back correctly.")
  if len(sys.argv) != 2:
    print('usage: python capacity.py <path_to_ssd>')
    sys.exit(1)

  path = sys.argv[1]
  size = 100 * 1024 * 1024 # 100 MB file chunks

  write_files_until_full(path, size)
  verify_all_files(path, size)

if __name__ == '__main__':
  main()
