# import the module
from bs4 import BeautifulSoup
import urllib2
import time, re, sys

# this module handles the job of connecting to the mail server
from smtplib import SMTP_SSL as SMTP
# this module helps us to construct email objects and set their properties
from email.mime.text import MIMEText

def get_url(taxid):
  return 'http://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Info&id=' + str(taxid) + '&lvl=3&lin=f&keep=1&srchmode=1&unlock'

def get_counts(taxid):
  url = get_url(taxid)
  page = urllib2.urlopen(url).read()

  soup = BeautifulSoup(page)
  
  info={}
  for row in soup.find_all('tr'):
    columns = row.find_all('td')
    td_count = len(columns)
    if td_count == 3:
      dbname, subtree, dlink = columns
      if dbname.string == 'Nucleotide':
        info['nucleotide'] = str(subtree.string)
      elif dbname.string == 'Protein':
        info['protein'] = str(subtree.string)
      elif dbname.string == 'Genome':
        info['genome'] = str(subtree.string)
    info['name'] = str(soup.find_all('h2')[0].string)

  return info

def send_mail(taxids = [6656, 9779], email_address = 'real.address@popucui.me'):
  dicts = []
  for taxid in taxids:
    counts_dict = get_counts(taxid)
    dicts.append(counts_dict)

  time.sleep(3)
  SMTPserver = 'smtp.163.com'
  # your email address goes here
  sender = "real.address@163.com"
  destination = email_address

  USERNAME = "username"
  PASSWORD = "pa$$w0rd"
  content = """
  hello cui, this is your result:
  """ + str(dicts) + time.ctime() 
  subject = "daily counts update"
  try:
    # create a new message object and store it in the variable msg
    msg = MIMEText(content, 'plain')
    # set the subject and the from address
    msg['Subject']= subject
    msg['From'] = sender
    # connect to the server, set the debug level so that we can see some messages, and login
    conn = SMTP(SMTPserver)
    conn.set_debuglevel(1)
    conn.login(USERNAME, PASSWORD)
    # now do the actual send
    try:
        conn.sendmail(sender, destination, msg.as_string())
    finally:
        conn.close()
# if there's an error then it will show up here
  except:
    sys.exit( "mail failed!")

def mail_man():
  with open('address.txt') as f:
    for line in f.readlines():
      email = re.search(r'\S+@\S+', line)
      email_address = email.group()
      taxids = re.findall(r'\d+', line)
      send_mail(taxids, email_address)
if __name__ == '__main__':
  mail_man()
