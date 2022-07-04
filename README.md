## About

IPv4 Dynamic DNS script built on top of the Cloudflare API. It only supports a handful of configuration options and [Certbot's configuration file syntax](https://certbot-dns-cloudflare.readthedocs.io/en/stable/) which makes it very easy to configure and use.

Uses DNS based public IPv4 detection by querying `myip.opendns.com` on `resolver1.opendns.com`.

The zone record is "upserted" i.e it doesn't have to exist. It is only updated when the public IP address and the stored value in Cloudflare's zone is different.

## Requirements

 * Python 2.7+
 * dnslib
 * publicsuffix2
 * cloudflare

Works with Python 3, but it supports Python fallback 2 as some embedded devices may not have Python 3 support.

## How to

Install dependencies with (may require sudo):

```bash
# may be 2 or 3 depending on system
pip install -r requirements.txt
# alternatives, depending on system
pip2 install -r requirements.txt
pip3 install -r requirements.txt
```

The script has built in help. `./dynflare -h` reveals the mistery. This example invocation expects a `python` executable in `$PATH`, whether 2 or 3. A symlink or alias may be needed where the included shebang is not necessary or specify the desired Python binary in the command line invocation.

Using a properly scoped (bearer) API token is preferable to a general access email and API key as that API key gives access to the whole Cloudflare account.
