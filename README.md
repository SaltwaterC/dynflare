## About

Dynamic DNS script built on top of the Cloudflare API.

This is the original `dynflare`, now much improved after being rescued from the pit of abandonment.

Features:

 * Cloudflare token (preferred) or email + API key authentication.
 * DNS-based public IP detection.
 * DNS-based check for the host value.
 * In memory/network operation only. It doesn't save files to avoid wearing down flash storage on embedded devices.
 * Supports optional credential parsing from ACME clients:
   * [Certbot](https://certbot-dns-cloudflare.readthedocs.io/en/stable/)
   * [acme.sh](https://github.com/acmesh-official/acme.sh/wiki/dnsapi#1-cloudflare-option)

The zone record is "upserted" i.e it doesn't have to exist. It is only updated when the public IP address and the stored value in Cloudflare's zone is different. Unless the record needs to be created or updated, dynflare doesn't need to authenticate against Cloudflare as it uses DNS queries exclusively. The execution is also very quick as it doesn't need to run slow HTTPS API requests.

Why Python? Because if I could get a shell to a network device running some form of Linux, I could almost always get a Python interpreter, which is the next best thing after native binaries which may be fiddly to cross-compile for whatever native architecture runs on a network device. The glaring exception is OpenWrt, but there's always opkg if space permits.

## Requirements

 * Python 2.7+
 * dnslib
 * cloudflare

dynflare works with Python 3, but it supports Python fallback 2 as some embedded devices may not have Python 3 support.

## Installation

Install dependencies with (may require sudo):

```bash
# may be 2 or 3 depending on system
pip install -r requirements.txt
# alternatives, depending on system
pip2 install -r requirements.txt
pip3 install -r requirements.txt
```

## Usage

The script has built in help. `./dynflare -h` reveals the mistery.

```bash
$ ./dynflare -h
usage: dynflare [-h] --host HOST --zone-id ZONE_ID [--email EMAIL]
                [--api-key API_KEY] [--record-type RECORD_TYPE] [--ttl TTL]
                [--conf-certbot CONF_CERTBOT] [--conf-acmesh CONF_ACMESH]
                [--dns-ip-host DNS_IP_HOST]
                [--dns-ip-resolvers DNS_IP_RESOLVERS]
                [--dns-ip-type DNS_IP_TYPE]

Dynamic DNS script for updating a record with your machine's public IP
address. Supports Cloudflare DNS hosted zones.

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           DNS hostname to update.
  --zone-id ZONE_ID     Cloudflare Zone ID
  --email EMAIL         Cloudflare email address. Only required for global API
                        key.
  --api-key API_KEY     Cloudflare API key or API token.
  --record-type RECORD_TYPE
                        Cloudflare DNS zone record type
  --ttl TTL             Cloudflare DNS host record TTL
  --conf-certbot CONF_CERTBOT
                        Configuration file containing email + key or token
                        using same syntax as the Certbot Cloudflare plug-in.
  --conf-acmesh CONF_ACMESH
                        Configuration file containing email + key or token
                        using same syntax as the acme.sh Cloudflare dnsapi.
  --dns-ip-host DNS_IP_HOST
                        The host value used for DNS based public IP detection
  --dns-ip-resolvers DNS_IP_RESOLVERS
                        The comma separated list of resolvers used for DNS
                        based public IP detection
  --dns-ip-type DNS_IP_TYPE
                        The DNS record type to resolve the public IP

EMAIL and API_KEY may be read from environment as CLOUDFLARE_EMAIL and
CLOUDFLARE_API_KEY. They need to be specified as arguments only when the
environment variables are undefined or when they need to be overridden.
```

This example invocation expects a `python` executable in `$PATH`, whether 2 or 3. A symlink or alias may be needed where the included shebang is not necessary or specify the desired Python binary in the command line invocation.

HOST, ZONE_ID, and an API token (via API_KEY) is the minimum configuration necessary. As the authentication token may be parsed from config files or taken from environment, only HOST and ZONE_ID are compulsory CLI arguments.

The TTL value of the record is basically the limiting factor for how often this script may run. The default of 120 is set to match the free Cloudflare accounts, but Pro accounts may reduce this down to 30 seconds.

## Advanced usage

The DNS-based public IP detection has the following defaults for `--dns-ip-host`, `--dns-ip-resolvers`, `--dns-ip-type`:

 * host: myip.opendns.com
 * resolvers: 208.67.222.222,208.67.220.220,208.67.222.220,208.67.220.222 # aka resolver1.opendns.com, resolver2.opendns.com, resolver3.opendns.com, resolver4.opendns.com
 * type: A

For OpenDNS, you can obtain an IPv6 value by passing `--dns-ip-type AAAA`. However, to set this value to Cloudflare, you must also override the record type for HOST via `--record-type AAAA`.

Google offers the same kind of DNS-based public IP detection:

 * host: o-o.myaddr.l.google.com
 * resolvers: 216.239.32.10,216.239.34.10,216.239.36.10,216.239.38.10 # aka ns1.google.com, ns2.google.com, ns3.google.com, ns4.google.com
 * type: TXT

Google's version needs to be manually matched with `--record-type` on Cloudflare's side i.e `A` (default, IPv4) or `AAAA` (IPv6). The TXT record result returns IPv4 or IPv6 depending on the protocol used to query the resolver.
