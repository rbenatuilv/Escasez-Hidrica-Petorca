# Zonas de agua #
install.packages("acnr")
install.packages("R.utils")
install.packages("TTR")
library(acnr)
library(R.utils)
library(TTR)
library(forecast)

# Índices y Serie
NDVI_agua = Petorca_agua_time_series$NDVI
Fechas_agua = Petorca_agua_time_series$date
serie_agua=harmonics_fun(NDVI_agua,as.Date(Fechas_agua),12,as.Date("2015-01-12"))
plot(1:109, serie_agua, type = "l", xlab = "Fecha", ylab = "NDVI zonas de cuerpos de agua", main = "Serie de tiempo de NDVI en zonas de cuerpos de agua")

# Tendencia
for (i in 1:length(NDVI_agua)) {
  if (is.na(NDVI_agua[i])) {
    NDVI_agua[i] <- 0
  }
}

otra_data_agua=data.frame(1:109,NDVI_agua)
otra_data_filtrada_agua <- subset(otra_data_agua, NDVI_agua != 0)

my_reg_time_agua <- lm(NDVI_agua ~ ., data = otra_data_filtrada_agua)
coeficientes_time_agua <- coef(my_reg_time_agua)

tiempo_agua=otra_data_filtrada_agua$X1.109
tendencia_agua <- rep(0, length(tiempo_agua))
for (i in 1:length(tiempo_agua)) {
  # Coeficientes para la regresión con tiempo
  coef_intercep <- coeficientes_time_agua[1]
  coef_t <- coeficientes_time_agua[2]  # Coeficiente para el tiempo
  # Calcula la tendencia lineal
  tendencia_agua[i] <- coef_intercep + coef_t * tiempo_agua[i]
}
reg_tendencia_agua=lm(tendencia_agua  ~ tiempo_agua,otra_data_filtrada_agua)
plot(tendencia_agua, type = "p", ylim = c(0.1086483, 0.1519389), ylab = "Índice", xlab = "Tiempo", main = "Tendencia NDVI zonas de cuerpos de agua")
abline(reg_tendencia_agua,col = "red")

#Análisis de autocorrelación
autocorrelacion_agua=acf(serie_agua)

#Análisis de autocorrelación parcial
autocorr_parcial_agua=pacf(serie_agua)

#Modelo SES
fit_ses_agua<-ses(serie_agua,h=12, initial ="optimal", alpha=0.9)

#Modelo Predictivo
# Nuevo_NDVI(t) = fit_ses_agua$predict[t] + reg_tendendia_agua$Coefficients[2]*(t+total_años_previos)

