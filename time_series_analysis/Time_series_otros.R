# Zonas otras #
install.packages("acnr")
install.packages("R.utils")
install.packages("TTR")
library(acnr)
library(R.utils)
library(TTR)
library(forecast)

# Índices y Serie
NDVI_otros = Petorca_otros_time_series$NDVI
Fechas_otros = Petorca_otros_time_series$date
serie_otros=harmonics_fun(NDVI_otros,as.Date(Fechas_otros),12,as.Date("2015-01-12"))
plot(1:109, serie_otros, type = "l", xlab = "Fecha", ylab = "NDVI zonas no etiquetadas", main = "Serie de tiempo de NDVI en zonas no etiquetadas")

# Tendencia
for (i in 1:length(NDVI_otros)) {
  if (is.na(NDVI_otros[i])) {
    NDVI_otros[i] <- 0
  }
}

otra_data_otros=data.frame(1:109,NDVI_otros)
otra_data_filtrada_otros <- subset(otra_data_otros, NDVI_otros != 0)

my_reg_time_otros <- lm(NDVI_otros ~ ., data = otra_data_filtrada_otros)
coeficientes_time_otros <- coef(my_reg_time_otros)

tiempo_otros=otra_data_filtrada_otros$X1.109
tendencia_otros <- rep(0, length(tiempo_otros))
for (i in 1:length(tiempo_otros)) {
  # Coeficientes para la regresión con tiempo
  coef_intercep <- coeficientes_time_otros[1]
  coef_t <- coeficientes_time_otros[2]  # Coeficiente para el tiempo
  # Calcula la tendencia lineal
  tendencia_otros[i] <- coef_intercep + coef_t * tiempo_otros[i]
}
reg_tendencia_otros=lm(tendencia_otros ~ tiempo_otros,otra_data_filtrada_otros)
plot(tendencia_otros, type = "p", ylim = c(0.1, 0.3), ylab = "Índice", xlab = "Tiempo", main = "Tendencia NDVI zonas no etiquetadas")
abline(reg_tendencia_otros,col = "red")

#Análisis de autocorrelación
autocorrelacion_otros=acf(serie_otros) # Patrón estacional 

#Análisis de autocorrelación parcial
autocorr_parcial_otros=pacf(serie_otros) # Relacion estacional

#Modelo SES
fit_ses_otros<-ses(serie_otros,h=12, initial ="optimal", alpha=0.7)

#Modelo Predictivo
# Nuevo_NDVI(t) = fit_ses_agua$predict[t] + reg_tendendia_agua$Coefficients[2]*(t+total_años_previos)
