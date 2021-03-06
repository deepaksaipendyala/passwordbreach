import requests
import hashlib
import passwordgenerate as pg

def newpass():
  return pg.gen()
  
def request_api_data(qchar):
  url = 'https://api.pwnedpasswords.com/range/' + qchar
  res = requests.get(url)
  if res.status_code != 200:
    raise RuntimeError(f' Error fetching : {res.status_code},check the api and try again')
  return res

def get_password_leaks_count(hashes,h_to_check):
  hashes= (line.split(':')for line in hashes.text.splitlines())
  for h,count in hashes:
    if h == h_to_check:
      return count
  return 0

def hashing(password):
  sha1password = hashlib.sha1(password.encode('utf=8')).hexdigest().upper()
  f5char,l5char = sha1password[:5], sha1password[5:]
  response= request_api_data(f5char)
  return get_password_leaks_count(response,l5char)

def check(password):
  count=hashing(password)
  if count:
      print(f'The password "{password}" was found {count} times... its high time to change your password  to for a better security !')
      print(f"New password:{newpass()}\nYou can use the generated password for better security")
  else:
       print(f'The password "{password}" was NOT found. It seems Good to Go!')
  return 'done!'


if __name__=='__main__':
    p=input("Enter your password:")
    check(p)