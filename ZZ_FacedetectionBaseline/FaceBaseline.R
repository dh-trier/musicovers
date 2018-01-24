##Einlesen der Datei
f <-read.csv (file="median_full.csv", sep="\t")

#Darstellung der Daten als Tabelle
f 

#Zugriff auf Spaltenwerte mit Variablenname$Spaltenueberschrift
f$faces 

#Wertebereich aller Daten
summary(f$faces)

#Gesamtzahl der Gesichter 
sum(f$faces) 

#Gesamtzahl der Gesichter pro Genre
tapply(f$faces, f$genre, sum)

#Wertebereich der Gesichter pro Genre
tapply(f$faces, f$genre, summary)

#Anzahl Daten pro Genre
table (f$genre)

#Bilden von Teilmengen pro Genre
c1 = subset (f, genre=="country") 
e1 = subset (f, genre=="electronic")
h1 = subset (f, genre=="hip-hop")
p1 = subset (f, genre=="pop") 
r1 = subset (f, genre=="rock")

#Anzahl Gesichter und deren Haeufigkeiten pro Genre
table(c1$faces)
table(e1$faces)
table(h1$faces)
table(p1$faces)
table(r1$faces)



###boxplot###
#svg(filename="boxplot.svg", width=12, height=10, pointsize=12)
farben = c("red", "blue", "green", "orange", "magenta")
plot (f$genre, f$faces, col=farben, ylab="Anzahl Gesichter", xlab="Genre", main="Verteilung der Gesichter")



###Haeufigkeits-Histogramme mit density###
#density ist eine Schaetzung der Dichtefunktion der Verteilung# 
# freq=FALSE fuer relative Haeufigkeiten. Bei TRUE werden die absoluten Haeufigkeiten dargestellt
#hist() plottet das Histogramm.
#mit lines() wird zu einem Histogramm eine beliebige Linie hinzugefuegt. In diesem Fall die
#Dichte-Kurve. Diese basiert immer auf relativen Haeufigkeiten.
#lwd=Linienstaerke
#alles zwischen svg() und dev.off() wird in eine svg-Datei gespeichert.
#mit par(mfrow=c(3,2)) teilt die Ausgabe in eine drei Zeilen und  zwei Spalten auf, sodass
#5 Diagramme in der svg ausgegeben werden

#svg(filename="histogramm.svg", width=12, height=10, pointsize=12)
#old.par <- par(mfrow=c(3, 2))
hist(c1$faces, col="red", axes=TRUE, xlab="Anzahl Gesichter", ylab="rel. Haeufigkeit", main="country", freq=FALSE)
lines(density(c1$faces), lwd=2)

hist(e1$faces, col="blue", axes=TRUE, xlab="Anzahl Gesichter", ylab="rel. Haeufigkeit", main="electronic", freq=FALSE)
lines(density(e1$faces), lwd=2)

hist(h1$faces, col="green", axes=TRUE, xlab="Anzahl Gesichter", ylab="rel. Haeufigkeit", main="hip-hop", freq=FALSE)
lines(density(h1$faces), lwd=2)

hist(p1$faces, col="orange", axes=TRUE, xlab="Anzahl Gesichter", ylab="rel. Haeufigkeit", main="pop",  freq=FALSE)
lines(density(p1$faces), lwd=2)

hist(r1$faces, col="magenta", axes=TRUE, xlab="Anzahl Gesichter", ylab="rel. Haeufigkeit", main="rock",  freq=FALSE, ylim=c(0.0,0.7))
lines(density(r1$faces), lwd=2)

#dev.off()
#par(old.par)




