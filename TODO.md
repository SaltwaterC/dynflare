## TODO

 * Pre-fill the zone ID for the host to save on Cloudflare API calls via arg (no `zone_id` calls).
 * Support checking the host value via DNS to save on Cloudflare API calls (no `record_info` calls unless `NXDOMAIN`).
