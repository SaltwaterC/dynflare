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
