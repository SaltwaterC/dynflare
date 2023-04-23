## About

Dynamic DNS script built on top of the Cloudflare API.

This is the original `dynflare`, now much improved after being rescued from the pit of abandonment.

Features:

 * Cloudflare token (preferred) or email + API key authentication.
 * Cloudflare-based public IP detection (via: https://cloudflare.com/cdn-cgi/trace).
 * Cloudflare DNS-over-HTTPS check for the host value.
 * In memory/network operation only. It doesn't save files to avoid wearing down flash storage on embedded devices.
 * No dependencies. This script can be deployed as it is.
 * Supports optional credential parsing from ACME clients:
   * [Certbot](https://certbot-dns-cloudflare.readthedocs.io/en/stable/)
   * [acme.sh](https://github.com/acmesh-official/acme.sh/wiki/dnsapi#1-cloudflare-option)

The zone record is "upserted" i.e it doesn't have to exist. It is only updated when the public IP address and the stored value in Cloudflare's zone is different. Unless the record needs to be created or updated, dynflare doesn't need to authenticate against Cloudflare as it uses public HTTPS endpoints exclusively. The execution is also very quick as it doesn't need to run slow HTTPS API requests.

Why Python? Because if I could get a shell to a network device running some form of Linux, I could almost always get a Python interpreter, which is the next best thing after native binaries which may be fiddly to cross-compile for whatever native architecture runs on a network device. The glaring exception is OpenWrt, but there's always opkg if space permits.

## Requirements

 * Python 2.7+

dynflare works with Python 3, but it supports Python fallback 2 as some embedded devices may not have Python 3 support.

## Usage

The script has built in help. `./dynflare -h` reveals the mistery.

```bash
$ ./dynflare -h
usage: dynflare [-h] --host HOST --zone-id ZONE_ID [--email EMAIL] [--api-key API_KEY] [--record-type RECORD_TYPE] [--ttl TTL] [--conf-certbot CONF_CERTBOT] [--conf-acmesh CONF_ACMESH]

Dynamic DNS script for updating a record with your machine's public IP address. Supports Cloudflare DNS hosted zones.

options:
  -h, --help            show this help message and exit
  --host HOST           DNS hostname to update.
  --zone-id ZONE_ID     Cloudflare Zone ID
  --email EMAIL         Cloudflare email address. Only required for global API key.
  --api-key API_KEY     Cloudflare API key or API token.
  --record-type RECORD_TYPE
                        Cloudflare DNS zone record type
  --ttl TTL             Cloudflare DNS host record TTL
  --conf-certbot CONF_CERTBOT
                        Configuration file containing email + key or token using same syntax as the Certbot Cloudflare plug-in.
  --conf-acmesh CONF_ACMESH
                        Configuration file containing email + key or token using same syntax as the acme.sh Cloudflare dnsapi.

EMAIL and API_KEY may be read from environment as CLOUDFLARE_EMAIL and CLOUDFLARE_API_KEY. They need to be specified as arguments only when the environment variables are undefined or
when they need to be overridden.
```

This example invocation expects a `python3` executable in `$PATH`. For Python 2 usage, the script needs to be invoked explicitly with `python`/`python2` (depending on OS).

HOST, ZONE_ID, and an API token (via API_KEY) is the minimum configuration necessary. As the authentication token may be parsed from config files or taken from environment, only HOST and ZONE_ID are compulsory CLI arguments.

The TTL value of the record is basically the limiting factor for how often this script may run. The default of 60 is set to match the free Cloudflare accounts, but Pro accounts may reduce this down to 30 seconds.
