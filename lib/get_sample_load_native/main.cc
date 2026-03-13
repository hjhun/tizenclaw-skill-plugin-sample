/*
 * get_sample_load_native — A native C++ TizenClaw skill.
 *
 * Reads system load averages from /proc/loadavg and prints
 * a JSON result to stdout. Uses CLAW_ARGS env for parameters
 * (unused here).
 *
 * Compile (cross-compile for ARM):
 *   arm-linux-gnueabi-g++ -static -o get_sample_load_native main.cc
 */

#include <cstdio>
#include <cstdlib>
#include <cstring>

int main() {
  double load1 = 0.0, load5 = 0.0, load15 = 0.0;
  FILE* fp = fopen("/proc/loadavg", "r");
  if (fp) {
    if (fscanf(fp, "%lf %lf %lf", &load1, &load5, &load15) < 3) {
      load1 = load5 = load15 = 0.0;
    }
    fclose(fp);
  }

  // Read uptime from /proc/uptime
  double uptime_sec = 0.0;
  fp = fopen("/proc/uptime", "r");
  if (fp) {
    if (fscanf(fp, "%lf", &uptime_sec) < 1) {
      uptime_sec = 0.0;
    }
    fclose(fp);
  }

  int hours = (int)(uptime_sec / 3600);
  int minutes = (int)((uptime_sec - hours * 3600) / 60);

  printf("{\"load_1min\": %.2f, \"load_5min\": %.2f, "
         "\"load_15min\": %.2f, \"uptime\": \"%dh %dm\"}\n",
         load1, load5, load15, hours, minutes);

  return 0;
}
