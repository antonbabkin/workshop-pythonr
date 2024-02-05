library(tidyverse)
library(arrow)


#' Estimate regression model for given set of parameters.
estimate_model <- function(yearmin, yearmax, rural_uics) {
  cat(paste("Model parameters:\nfirst year =", yearmin, "\nlast year =", yearmax, "\nrural UICs =", paste(rural_uics, collapse=","), "\n"))
  
  df <- open_dataset("data/bds_county.parquet") |>
    select(year, fips, estabs, emp, net_job_creation_rate, estabs_entry_rate, estabs_exit_rate) |>
    filter(year >= yearmin, year <= yearmax) |>
    collect()
  
  d <- open_dataset("data/uic.parquet") |>
    collect()
  
  df <- left_join(df, d, by = "fips") |>
    mutate(rural = (uic %in% rural_uics))
  
  m <- lm(net_job_creation_rate ~ (estabs_entry_rate + estabs_exit_rate) * rural - 1, data = df)
  return(m)
}

