# Zonas de plantaciones #
install.packages("acnr")
install.packages("R.utils")
install.packages("TTR")
library(acnr)
library(R.utils)
library(TTR)
library(forecast)

# Índices y Serie
NDVI_rios = Petorca_rios_time_series$NDVI
Fechas_rios = Petorca_rios_time_series$date
serie_rios=harmonics_fun(NDVI_rios,as.Date(Fechas_rios),12,as.Date("2015-01-12"))
plot(1:109, serie_rios, type = "l", xlab = "Fecha", ylab = "NDVI zonas de rios", main = "Serie de tiempo de NDVI en zonas de rios")

#Tendencia
for (i in 1:length(NDVI_rios)) {
  if (is.na(NDVI_rios[i])) {
    NDVI_rios[i] <- 0
  }
}

otra_data_rios=data.frame(1:109,NDVI_rios)
otra_data_filtrada_rios <- subset(otra_data_rios, NDVI_rios != 0)

my_reg_time_rios <- lm(NDVI_rios ~ ., data = otra_data_filtrada_rios)
coeficientes_time_rios <- coef(my_reg_time_rios)

tiempo_rios=otra_data_filtrada_rios$X1.109
tendencia_rios <- rep(0, length(tiempo_rios))
for (i in 1:length(tiempo_rios)) {
  # Coeficientes para la regresión con tiempo
  coef_intercep <- coeficientes_time_rios[1]
  coef_t <- coeficientes_time_rios[2]  # Coeficiente para el tiempo
  # Calcula la tendencia lineal
  tendencia_rios[i] <- coef_intercep + coef_t * tiempo_rios[i]
}
reg_tendencia_rios=lm(tendencia_rios  ~ tiempo_rios,otra_data_filtrada_rios)
plot(tendencia_rios, type = "p", ylim = c(0.1, 0.5), ylab = "Índice", xlab = "Tiempo", main = "Tendencia NDVI zonas de rios")
abline(reg_tendencia_rios,col = "red") #baja

#Análisis de autocorrelación
autocorrelacion_rios=acf(serie_rios) # Patrón no estacional 

#Análisis de autocorrelación parcial
autocorr_parcial_rios=pacf(serie_rios) #Relación estacional

#Modelo SES
fit_ses_rios<-ses(serie_rios,h=12, initial ="optimal", alpha=0.2)

#Modelo Predictivo
# Nuevo_NDVI(t) = fit_ses_{zona}$predict[t] + reg_tendendia_{zona}$Coefficients[2]*(t+total_años_previos)

