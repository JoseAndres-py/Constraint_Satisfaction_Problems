# Simple Fuzzy System

El programa se encarga de evaluar un sistema de decisión difusa para la compra de autos basado en dos entradas (precio, kilometraje), un conjunto de reglas y una salida que determina la compra o no-compra del vehículo. 
Entradas: El sistema tiene dos entradas definidas así: 

Precio: Esta entrada tiene un universo de discurso entre 0 y 100 Millones de pesos. 
1. Conjuntos difusos de la entrada:  
    -Barato: Trapezoidal (0, 0, 30, 70)  
    -Estándar: Triangular (25, 60, 85)  
    -Costoso: Trapezoidal (55, 80, 100, 100) 

Kilometraje: Esta entrada tiene un universo de discurso entre 0 y 300 Mil Kilómetros 
1. Conjuntos difusos de la entrada:  
    -Bajo: Trapezoidal (0, 0, 50, 200)  
    -Medio: Trapezoidal (50, 100, 200, 300)  
    -Alto: Triangular (200, 300, 300) 

Salida: La salida tiene un Universo de discurso entre 0 y 1 y dos conjuntos de salida así: 
    -Comprar: Trapezoidal (0, 0, 0.3, 0.8) 
    -No-Comprar: Triangular (0.5, 1, 1) 
    
Base de reglas: Las dos entradas y la salida se encuentran relacionadas mediante 9 reglas definidas en la siguiente matriz de reglas. 


<p align="center">
  <img src="Images/Table.png" width="650" title="hover text">
</p>

Entradas y Salidas del sistema difuso.

<p align="center">
  <img src="Images/Input.png" width="650" title="hover text">
</p>

<p align="center">
  <img src="Images/Ouput.png" width="375" title="hover text">
</p>

