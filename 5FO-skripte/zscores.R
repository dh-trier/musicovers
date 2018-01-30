##Normalisierung von Gesichtern: Z-Score-Transformation

#Einlesen der Datei
f <-read.csv (file="4FE-009.csv", sep=",")

#Darstellung der Daten als Tabelle
f 

# Normalisierung: Z-score-Transformation
# auf 4 Stellen runden
zscore = round((f$faces- mean(f$faces))/(sd(f$faces)),4)
zscore

#zscore zu Tabelle hinzufuegen
f$zscore_faces =  zscore 

#csv-Datei speichern
write.table(f, file = "6FO-011.csv",row.names=FALSE,col.names=TRUE, sep=",", dec=".")
