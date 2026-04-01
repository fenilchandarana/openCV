import csv

input_file = "mapping.csv"   # change path if needed
output_file = "mapping.h"

physical = []
electrical = []

with open(input_file, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        physical.append(int(row["physical"].strip()))
        electrical.append(int(row["electrical"].strip()))

count = len(physical)

with open(output_file, "w") as f:
    f.write("#pragma once\n\n")
    f.write(f"#define MAPPING_SIZE {count}\n\n")
    f.write("const int physical[MAPPING_SIZE] = {\n  ")
    f.write(",\n  ".join(str(v) for v in physical))
    f.write("\n};\n\n")
    f.write("const int electrical[MAPPING_SIZE] = {\n  ")
    f.write(",\n  ".join(str(v) for v in electrical))
    f.write("\n};\n")

print(f"Done! Generated {output_file} with {count} pairs.")