# Zonas rubanas #
install.packages("acnr")
install.packages("R.utils")
install.packages("TTR")
library(acnr)
library(R.utils)
library(TTR)
library(forecast)

# Índices y Serie
NDVI_urban = Petorca_urban_time_series$NDVI
Fechas_urban = Petorca_urban_time_series$date
serie_urban=harmonics_fun(NDVI_urban,as.Date(Fechas_urban),12,as.Date("2015-01-12"))
plot(1:109, serie_urban, type = "l", xlab = "Fecha", ylab = "NDVI zonas urbanas", main = "Serie de tiempo de NDVI en zonas urbanas")

#Tendencia
for (i in 1:length(NDVI_urban)) {
  if (is.na(NDVI_urban[i])) {
    NDVI_urban[i] <- 0
  }
}

otra_data_urban=data.frame(1:109,NDVI_urban)
otra_data_filtrada_urban <- subset(otra_data_urban, NDVI_urban != 0)

my_reg_time_urban <- lm(NDVI_urban ~ ., data = otra_data_filtrada_urban)
coeficientes_time_urban <- coef(my_reg_time_urban)

tiempo_urban=otra_data_filtrada_urban$X1.109
tendencia_urban <- rep(0, length(tiempo_urban))
for (i in 1:length(tiempo_urban)) {
  # Coeficientes para la regresión con tiempo
  coef_intercep <- coeficientes_time_urban[1]
  coef_t <- coeficientes_time_urban[2]  # Coeficiente para el tiempo
  # Calcula la tendencia lineal
  tendencia_urban[i] <- coef_intercep + coef_t * tiempo_urban[i]
}
reg_tendencia_urban=lm(tendencia_urban  ~ tiempo_urban,otra_data_filtrada_urban)
plot(tendencia_urban, type = "p", ylim = c(0.1, 0.5), ylab = "Índice", xlab = "Tiempo", main = "Tendencia NDVI zonas urbanas")
abline(reg_tendencia_urban,col = "red") #baja

#Análisis de autocorrelación
autocorrelacion_urban=acf(serie_urban) # Patrón no estacional 

#Análisis de autocorrelación parcial
autocorr_parcial_urban=pacf(serie_urban) #Relación estacional

#Modelo SES
fit_ses_urban<-ses(serie_urban,h=12, initial ="optimal", alpha=0.2)

#Modelo Predictivo
# Nuevo_NDVI(t) = fit_ses_{zona}$predict[t] + reg_tendendia_{zona}$Coefficients[2]*(t+total_años_previos)

