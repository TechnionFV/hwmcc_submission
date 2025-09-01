# hwmcc24_submission

Our submission for HWMCC25

# Pavy Script

## How to Run the Script

To execute the script, use the following command:

```bash
./pavy.bash <benchmark> <certificate.sat> <certificate.unsat>

```

The script will launch multiple engines, each with a different configuration. Before completing, it will display the result status (`UNSAT` (instead of SAFE), `SAT` (instead of UNSAFE), or `UNDETERMINED`). Moreover, the counterexample and certificate will be written to <certificate.sat> and <certificate.unsat> respictevlity as required.

# Submitters

* Prof. Arie Gurfinkel, Waterloo University
* Basel Khouri, Technion
* Andrew Luka, Technion
* Dr. Yakir Vizel, Technion
