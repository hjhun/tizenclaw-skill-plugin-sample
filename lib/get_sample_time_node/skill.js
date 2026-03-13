#!/usr/bin/env node
/**
 * get_sample_time_node skill
 * Returns system time information using Node.js.
 * Reads CLAW_ARGS from environment for parameters.
 */

function main() {
  const now = new Date();
  const result = {
    iso_timestamp: now.toISOString(),
    unix_timestamp: Math.floor(now.getTime() / 1000),
    timezone_offset: now.getTimezoneOffset(),
    locale_string: now.toLocaleString(),
    node_version: process.version,
  };

  // Output exactly one JSON line to stdout
  console.log(JSON.stringify(result));
}

main();
