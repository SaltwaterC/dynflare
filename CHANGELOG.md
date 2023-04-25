## v0.3

 * Rewrite without using any dependencies.
 * The DNS verifications have been replaced with HTTPS endpoints to avoid implementing the DNS wire format against DoH servers.
 * Dropped the customer resolver feature as the host public IP detection is now done against a Cloudflare endpoint. There were a few reasons:
   * Cloudflare's JSON API for their DoH implementation doesn't support specifying a class, so querying `CH TXT whoami.cloudflare` does not work without implementing the DNS wire format.
   * Google supports the same style of JSON API for their DoH, but they don't support their `o-o.myaddr.l.google.com` host as the nameservers are different.
   * OpenDNS doesn't support a JSON API for their DoH at all, so there's no easy way of querying `myip.opendns.com`.

## v0.2

 * Rewrite using cloudflare in place of cfpy.
 * Supports Python 3 with Python 2 fallback.
 * Supports Cloudflare (scoped bearer) API tokens.
 * Adds output timestamps.
 * Add required ZONE_ID argument to reduce API calls and remove publicsuffix2 dependency.
 * Add support for acme.sh config file.
 * Add support for DNS verification of target host record.

## v0.1

 * Initial release built on top of cfpy, dnslib, and publicsuffix2.
