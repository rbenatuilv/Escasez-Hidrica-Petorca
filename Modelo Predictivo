install.packages("acnr")
install.packages("R.utils")
library(acnr)
library(R.utils)
install.packages("TTR")
library(TTR)
library(forecast)

# Extración datos 
fechas  <- c("2013-03-18", "2013-03-23", "2013-06-22", "2013-07-08", "2013-07-24",
                                    "2013-08-09", "2013-08-25", "2013-09-10", "2013-09-26", "2013-10-28",
                                    "2013-11-13", "2013-11-29", "2013-12-15", "2013-12-31", "2014-01-16",
                                    "2014-02-01", "2014-02-17", "2014-03-05", "2014-03-21", "2014-04-06",
                                    "2014-05-08", "2014-05-24", "2014-06-09", "2014-06-25", "2014-07-11",
                                    "2014-08-28", "2014-09-29", "2014-10-15", "2014-11-16", "2014-12-18",
                                    "2015-01-19", "2015-02-04", "2015-02-20", "2015-03-08", "2015-03-24",
                                    "2015-04-09", "2015-05-11", "2015-05-27", "2015-06-12", "2015-06-28",
                                    "2015-07-14", "2015-07-30", "2015-08-15", "2015-08-31", "2015-09-16",
                                    "2015-10-18", "2015-11-03", "2015-11-19", "2015-12-05", "2016-01-06",
                                    "2016-02-07", "2016-02-23", "2016-03-10", "2016-03-26", "2016-04-11",
                                    "2016-04-27", "2016-05-13", "2016-06-14", "2016-06-30", "2016-07-16",
                                    "2016-08-01", "2016-08-17", "2016-09-02", "2016-09-18", "2016-10-04",
                                    "2016-10-20", "2016-11-05", "2016-11-21", "2016-12-07", "2016-12-23",
                                    "2017-01-08", "2017-01-24", "2017-02-09", "2017-02-25", "2017-03-13",
                                    "2017-03-29", "2017-04-14", "2017-04-30", "2017-05-16", "2017-06-01",
                                    "2017-06-17", "2017-07-03", "2017-07-19", "2017-08-04", "2017-08-20",
                                    "2017-09-05", "2017-09-21", "2017-10-07", "2017-11-24", "2017-12-10",
                                    "2017-12-26", "2018-01-27", "2018-03-16", "2018-04-01", "2018-04-17",
                                    "2018-05-03", "2018-06-04", "2018-06-20", "2018-07-06", "2018-08-07",
                                    "2018-08-23", "2018-09-08", "2018-11-11", "2018-11-27", "2018-12-29",
                                    "2019-01-30", "2019-02-15", "2019-03-19", "2019-04-04", "2019-04-20",
                                    "2019-05-06", "2019-05-22", "2019-06-23", "2019-07-09", "2019-07-25",
                                    "2019-08-10", "2019-08-26", "2019-09-11", "2019-09-27", "2019-10-13",
                                    "2019-10-29", "2019-11-14", "2019-12-16", "2020-01-01", "2020-01-17",
                                    "2020-02-02", "2020-02-18", "2020-03-05", "2020-03-21", "2020-04-06",
                                    "2020-04-22", "2020-05-24", "2020-06-09", "2020-06-25", "2020-07-11",
                                    "2020-07-27", "2020-08-12", "2020-08-28", "2020-09-13", "2020-10-15",
                                    "2020-10-31", "2020-11-16", "2020-12-02", "2020-12-18", "2021-01-19",
                                    "2021-02-04", "2021-02-20", "2021-03-08", "2021-03-24", "2021-04-09",
                                    "2021-04-25", "2021-05-11", "2021-05-27", "2021-06-28", "2021-07-14",
                                    "2021-07-30", "2021-09-16", "2021-10-02", "2021-10-18", "2021-11-03",
                                    "2021-11-19", "2021-12-05", "2021-12-21")

datos = ee.chart$NDVI
# Iterar sobre la columna 'datos' y reemplazar NA con 0
for (i in 1:length(datos)) {
  if (is.na(datos[i])) {
    datos[i] <- 0
  }
}
data=data.frame(fechas,datos)
datos_filtrados <- subset(data, datos != 0)

otra_data=data.frame(1:163,datos)
otra_data_filtrada <- subset(otra_data, datos != 0)

#Time Series

# from Jan 2009 to Dec 2014 as a time series object
myts <- ts(otra_data_filtrada[,2], start=1, end=68, frequency=1)

# plot series
plot(myts)

NDVI=datos_filtrados$datos
fechas_interes=datos_filtrados$fechas

# Análisis Armónico
harmonics_fun <- function(user_vals, user_dates, harmonic_deg, ref_date){
  
  ### For every missing output parameter set the default ###
  
  if (missing(user_vals)){
    stop("Values must be provided.")
  }
  if (missing(user_dates)){
    stop("Dates must be provided.")
  }
  # Check if dates are in "Date"-format
  if (class(user_dates) != "Date"){
    stop("Dates must be provided as 'Date' objects.")
  }
  if (missing(harmonic_deg)){
    stop("Harmonic degree must be provided.")
  }
  if (missing(ref_date)){
    ref_date <- as.Date("1970-01-01")
  } else if (class(ref_date) != "Date"){
    stop("Reference date must be provided as a 'Date' object.")
  }
  
  # If user vals are only NA, output is same as input
  
  if (all(is.na(user_vals))) {
    print("User values consist of NA values only. Output is same as input")
    return(user_vals)
    
    # Otherwise apply harmonic analysis
  } else {
    
    ### Calculate difference to ref_date in radians ###
    
    # Start for loop
    for (i in 1:length(user_dates)){
      current_date <- user_dates[i]
      # Calculate the difference in days
      current_diff_days <- as.numeric(difftime(current_date, ref_date), units="days")
      # Convert to years
      current_diff_years <- current_diff_days/365.25
      # Convert to radians
      current_diff_radians <- current_diff_years * 2 * pi
      if (i == 1){
        my_radians <- current_diff_radians
      } else {
        my_radians <- c(my_radians, current_diff_radians)
      }
      rm(i, current_date, current_diff_days, current_diff_years, current_diff_radians)
    }
    
    ### Caculate sines and cosines ###
    
    # Define constant
    my_cons <- rep(1, times = length(my_radians))
    # Create sines and cosines data frames with one column for each harmonic
    my_sin <- data.frame(matrix(nrow = length(my_radians), ncol = harmonic_deg))
    my_cos <- data.frame(matrix(nrow = length(my_radians), ncol = harmonic_deg))
    # Create names for df
    sin_names <- rep("sin_", times=harmonic_deg)
    cos_names <- rep("cos_", times=harmonic_deg)
    my_seq <- as.character(seq(1,harmonic_deg, by=1))
    sin_names <- paste(sin_names, my_seq, sep="")
    cos_names <- paste(cos_names, my_seq, sep="")
    # Add names to df
    names(my_sin) <- sin_names
    names(my_cos) <- cos_names
    # Calculate sines and cosines for each harmonic
    for (j in 1:harmonic_deg){
      # Calculate current sines and cosines by multiplying the radians with the current
      # degree of harmonic and then apply the sine/cosine function
      current_sines <- sin(my_radians * j)
      current_cosines <- cos(my_radians * j)
      # Fill data frames with values
      my_sin[,j] <- current_sines
      my_cos[,j] <- current_cosines
      # remove redundant variables
      rm(j, current_cosines, current_sines)
    }
    # Create df from the dependent and all independent variables
    df_for_reg <- cbind(user_vals, my_cons, my_radians, my_sin, my_cos)
    
    ### Apply Ordinary Least Squares Regression ###
    
    # Ordinary Least Squares Regression
    my_reg <- stats::lm(formula = user_vals ~ ., data = df_for_reg)
    # Get coefficients (constant is intercept value)
    # For coefficient and radians it's easy ...
    cons_coef <- my_reg$coefficients[1]
    t_coef <- my_reg$coefficients[3]
    # ... for the sines and cosines selecting the right columns is a little more complicated
    # Start with 4 because the first three values are the ndvi, my_cons and my_radians
    # First define the start and stop column for the sines and cosines ...
    sin_start <- 4
    sin_end <- 4 + harmonic_deg - 1
    cos_start <- 4 + harmonic_deg
    cos_end <- 4 + harmonic_deg + harmonic_deg -1
    # ... and then subset the data accordingly
    sin_coef <- my_reg$coefficients[c(sin_start:sin_end)]
    cos_coef <- my_reg$coefficients[c(cos_start:cos_end)]
    
    ### Calculate fitted values ###
    
    # multiply independent variables with the coefficients
    df_for_reg[,2] <- df_for_reg[,2] * cons_coef
    df_for_reg[,3] <- df_for_reg[,3] * t_coef
    # for loop multiplying the factor for each harmonic degree
    for (k in 1:harmonic_deg){
      # for the sines define i + 3 because the first sine column is at the 4th position
      df_for_reg[,k + 3] <- df_for_reg[,k + 3] * sin_coef[k]
      # for the cosines define i + 3 + harmonic_deg to get to the first cosine column
      df_for_reg[,k + 3 + harmonic_deg] <- df_for_reg[,k + 3 + harmonic_deg] * cos_coef[k]
      # remove reduntant variables
      rm(k)
    }
    # calculate sum (fitted value) of the multplied independent variables
    fitted <- rowSums(df_for_reg[,c(2:ncol(df_for_reg))], na.rm = TRUE)
    # return fitted values
    return(fitted)
  }
}

### ANÁLISIS DE SERIES DE TIENPO ###
serie=harmonics_fun(ee.chart$NDVI,as.Date(fechas),12,as.Date("2013-06-22"))
summary(serie)
# Visualización de la serie de tiempo
plot(1:163, serie, type = "l", xlab = "Fecha", ylab = "NDVI", main = "Serie de tiempo de NDVI")

# Ajuste del modelo de regresión sin tiempo
my_reg_nontime <- lm(NDVI ~ ., data = ee.chart)
# Ajuste del modelo de regresión con tiempo
my_reg_time <- lm(NDVI ~ ., data = otra_data_filtrada)

# Coeficientes para la regresión sin tiempo
coeficientes_nontime <- coef(my_reg_nontime)
# Coeficientes para la regresión con tiempo
coeficientes_time <- coef(my_reg_time)

# Coeficientes armónicos
ajuste_armonico = lm(ee.chart$NDVI ~ serie) 
coeficientes_armonicos <- coef(summary(ajuste_armonico))
significativos <- coeficientes_armonicos[, 4] < 0.05  # Coeficientes significativos (p < 0.05)
coeficientes_significativos <- coeficientes_armonicos[significativos, ]

#Tendendcia
tiempo=otra_data_filtrada$X1.163
tendencia1 <- rep(0, length(tiempo))
for (i in 1:length(tiempo)) {
  # Coeficientes para la regresión con tiempo
  coef_intercep <- coeficientes_time[1]
  coef_t <- coeficientes_time[2]  # Coeficiente para el tiempo
  # Calcula la tendencia lineal
  tendencia1[i] <- coef_intercep + coef_t * tiempo[i]
}
plot(tendencia, type = "p", ylim = c(7.326465e-17, 7.632739e-17), ylab = "Índice", xlab = "Tiempo", main = "Tendencia")

# Otro análisis
#Análisis de autocorrelación
acf(serie)
#Análisis de autocorrelación parcial
pacf(serie)
#Modelo Arima
auto.arima(serie)
