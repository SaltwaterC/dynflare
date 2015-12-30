#!/usr/bin/env python

import argparse, os, sys, json
from dnslib import DNSRecord
from publicsuffix import PublicSuffixList
from cfpy import CFapi

# functions
def my_ip():
  hostname = "myip.opendns.com"
  server = "resolver1.opendns.com"
  
  question = DNSRecord.question(hostname).send(server)
  return DNSRecord.parse(question).short()

def zone_id(cf, domain):
  zone_info = cf.list_zones(name = domain)
  return json.loads(zone_info)[0]["id"]

def record_info(cf, zid, host):
  record_info = cf.list_dns_records(zid, type = "A", name = host)
  return json.loads(record_info)[0]

def upsert_record(psl, cf, host):
  ip = my_ip()
  domain = psl.get_public_suffix(host)
  zid = zone_id(cf, domain)
  
  try:
    rinf = record_info(cf, zid, host)
    if rinf["content"] != ip:
      # cfpy doesn't have this implemented, yet
      # cf.update_dns_record()
      path = "/zones/" + zid + "/dns_records/" + rinf["id"]
      data = {
        "type": "A",
        "name": host,
        "content": ip,
        "ttl": 120
      }
      cf.api_request(path, data = data, method = "PUT")
      print "Updated " + host + " with content " + ip
    else:
      print "Host " + host + " is already up to date with " + ip
  except IndexError:
    cf.create_dns_record(zid, "A", host, ip, 120)
    print "Created " + host + " with content " + ip

# arguments
parser = argparse.ArgumentParser(
  description = '''
    Dynamic DNS script for updating a record with machine's public IP address.
    Supports CloudFlare DNS hosted zones.
  ''',
  epilog = '''
    EMAIL and TKN may be read from environment as CF_EMAIL and CF_TKN. They need
    to be specified as arguments only when the environment variables are
    undefined or when they need to be overridden.
  '''
)
parser.add_argument(
  "--host",
  dest = "host",
  type = str,
  help = "DNS hostname to update",
  required = True
)
parser.add_argument(
  "--email",
  dest = "email",
  type = str,
  help = "CloudFlare email address"
)
parser.add_argument(
  "--tkn",
  dest = "tkn",
  type = str,
  help = "CloudFlare API token / key"
)
args = parser.parse_args()

# implementation
email = os.environ.get("CF_EMAIL")
email = args.email if type(args.email) is not type(None) else email
if type(email) is type(None):
  sys.exit("Fatal: EMAIL is required!")

tkn = os.environ.get("CF_TKN")
tkn = args.tkn if type(args.tkn) is not type(None) else tkn
if type(tkn) is type(None):
  sys.exit("Fatal: TKN is required!")

psl = PublicSuffixList()
cf = CFapi(email, tkn)
upsert_record(psl, cf, args.host)
