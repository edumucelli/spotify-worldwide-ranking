# Script for converting a .csv file to .arff
# Usage: Rscript csv_to_arff.r input_file.csv

args <- commandArgs(trailingOnly = TRUE)

input_csv_path <- args[1]
output_arff_path <- paste(tools::file_path_sans_ext(input_csv_path),
                          ".arff",
                          sep="")

cat("Input file: ", input_csv_path, "\n")
cat("Output file: ", output_arff_path, "\n")

library("foreign")
data=read.csv(input_csv_path, header=TRUE)
write.arff(x=data, file=output_arff_path)
cat("-> File sucessfully converted to .arff\n")
