# Zonas de plantaciones #
install.packages("acnr")
install.packages("R.utils")
install.packages("TTR")
library(acnr)
library(R.utils)
library(TTR)
library(forecast)

# Índices y Serie
NDVI_plant = Petorca_plant_time_series$NDVI
Fechas_plant = Petorca_plant_time_series$date
serie_plant=harmonics_fun(NDVI_plant,as.Date(Fechas_plant),12,as.Date("2015-01-12"))
plot(1:109, serie_plant, type = "l", xlab = "Fecha", ylab = "NDVI zonas de plantaciones", main = "Serie de tiempo de NDVI en zonas de plantaciones")

#Tendencia
for (i in 1:length(NDVI_plant)) {
  if (is.na(NDVI_plant[i])) {
    NDVI_plant[i] <- 0
  }
}

otra_data_plant=data.frame(1:109,NDVI_plant)
otra_data_filtrada_plant <- subset(otra_data_plant, NDVI_plant != 0)

my_reg_time_plant <- lm(NDVI_plant ~ ., data = otra_data_filtrada_plant)
coeficientes_time_plant <- coef(my_reg_time_plant)

tiempo_plant=otra_data_filtrada_plant$X1.109
tendencia_plant <- rep(0, length(tiempo_plant))
for (i in 1:length(tiempo_plant)) {
  # Coeficientes para la regresión con tiempo
  coef_intercep <- coeficientes_time_plant[1]
  coef_t <- coeficientes_time_plant[2]  # Coeficiente para el tiempo
  # Calcula la tendencia lineal
  tendencia_plant[i] <- coef_intercep + coef_t * tiempo_plant[i]
}
reg_tendencia_plant=lm(tendencia_plant  ~ tiempo_plant,otra_data_filtrada_plant)
plot(tendencia_plant, type = "p", ylim = c(0.1, 0.5), ylab = "Índice", xlab = "Tiempo", main = "Tendencia NDVI zonas de plantaciones")
abline(reg_tendencia_plant,col = "red") #Casi estático (leve baja)

#Análisis de autocorrelación
autocorrelacion_plant=acf(serie_plant) # Patrón no estacional 

#Análisis de autocorrelación parcial
autocorr_parcial_plant=pacf(serie_agua) #Relación estacional

#Modelo SES
fit_ses_plant<-ses(serie_plant,h=12, initial ="optimal", alpha=0.2)

#Modelo Predictivo
# Nuevo_NDVI(t) = fit_ses_{zona}$predict[t] + reg_tendendia_{zona}$Coefficients[2]*(t+total_años_previos)

