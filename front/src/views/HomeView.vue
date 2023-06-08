<script setup>

</script>

<script>

</script>

<template>
  <main class="container">
    <section id="inicio">
      <div class="container">
        <div class="container-inicio">
          <div class="title-container">
            <h1 id="title">
              Data MAInd tu herramienta web para interactuar con el funcionamiento <br> de algoritmos de machine learning
            </h1>
            <p class="cuerpo">Proporciona tus dataseet y nosotros te damos el analisis</p>
          </div>
          <div class="image-slider">
            <button class="arrow-button" @click="prevImage">←</button>
            <img :src="currentImage" class="slider-image">
            <button class="arrow-button" @click="nextImage">→</button>
          </div>
        </div>
      </div> 
    </section>
    
    <div class="algoritmos-container">

      <section class="card apriori-card">
        <div class="container">
          <div class="apriori-image">
            <img src="" alt="Imagen de apriori">
          </div>
          <div class="container-apriori">
            <div class="title-apriori">
              <h1 class="apriori-title">Apriori</h1>
              <p class="cuerpo-apriori">
                El algoritmo Apriori es un algoritmo de minería de datos utilizado en el campo 
                del aprendizaje automático y la extracción de reglas de asociación. Su objetivo 
                principal es descubrir patrones frecuentes en conjuntos de datos transaccionales 
                o de mercado. Se utiliza comúnmente en sistemas de recomendación, análisis de 
                cesta de compras, detección de fraudes y otras aplicaciones donde es importante 
                descubrir relaciones y asociaciones entre elementos. consta de dos etapas 
                principales: generación de conjuntos de elementos frecuentes y generación de 
                reglas de asociación. En la primera etapa, se generan y exploran diferentes 
                conjuntos de elementos candidatos para encontrar aquellos que cumplen con un 
                umbral de frecuencia mínimo establecido por el usuario. En la segunda etapa, se 
                generan reglas de asociación a partir de los conjuntos de elementos frecuentes 
                encontrados en la etapa anterior. Las reglas de asociación resultantes del 
                algoritmo Apriori son declaraciones del tipo "si ocurre A, entonces también 
                ocurre B con una cierta probabilidad". Estas reglas pueden ser utilizadas para 
                realizar recomendaciones, tomar decisiones o comprender mejor los patrones y 
                comportamientos en los datos.
              </p>
              <!-- <a href="/apriori" class="card-link">Probar algoritmo</a> -->
            </div>
          </div>
        </div>
      </section>

      <section class="card metricas-card">
        <div class="container">
          <div class="container-metricas">
            <div class="title-metricas">
              <h1 class="metricas-title">Metricas de distancias</h1>
              <p class="cuerpo-metricas">
                Los algoritmos de métricas de distancias son técnicas utilizadas en el campo de 
                la minería de datos y el aprendizaje automático para medir la similitud o la 
                diferencia entre dos objetos o conjuntos de datos. Estas métricas permiten 
                cuantificar la distancia o la proximidad entre elementos y son fundamentales en 
                diversas aplicaciones, como la clasificación, el agrupamiento y la recuperación 
                de información. Estos algoritmos se basan en cálculos matemáticos que determinan 
                la distancia entre dos puntos en un espacio multidimensional. Algunas de las 
                métricas de distancias más comunes incluyen la distancia Euclidiana, la 
                distancia de Manhattan, la distancia de Chebyshev y la distancia de Hamming, 
                entre otras. Cada métrica tiene su propia fórmula y se utiliza en diferentes 
                contextos según las características y la naturaleza de los datos. Estas métricas 
                de distancias permiten comparar objetos en función de sus atributos o 
                características, lo que proporciona información sobre su similitud o 
                disimilitud. Esto es útil en tareas como la clasificación de imágenes, el 
                agrupamiento de documentos, la recomendación de productos y la búsqueda de 
                información relevante.
              </p>
              <!-- <a href="/distancias" class="card-link">Probar algoritmo</a> -->
            </div>
          </div>
        </div>
      </section>

      <section class="card clustering-card">
        <div class="container">
          <div class="container-clustering">
            <div class="title-clustering">
              <h1 class="clustering-title">Clustering</h1>
              <p class="cuerpo-clustering">
                El algoritmo de clustering es una técnica de aprendizaje automático no 
                supervisado que se utiliza para agrupar un conjunto de datos en diferentes 
                grupos o clústeres. El objetivo principal del clustering es encontrar patrones 
                intrínsecos en los datos y organizarlos en grupos basados en la similitud entre 
                ellos. El algoritmo de clustering analiza las características y la estructura de
                los datos sin conocer ninguna información previa sobre las clases o etiquetas a 
                las que pertenecen los elementos. Utiliza medidas de similitud o distancia para 
                determinar qué elementos son más similares entre sí y deben agruparse en el 
                mismo clúster. Existen varios algoritmos de clustering, como el algoritmo 
                K-means, el algoritmo de agrupamiento jerárquico, el algoritmo DBSCAN, 
                entre otros. Cada algoritmo tiene sus propias características y suposiciones, y 
                la elección del algoritmo depende del tipo de datos y del objetivo del análisis.
                El clustering tiene una amplia gama de aplicaciones en diferentes campos, como 
                la segmentación de clientes, la detección de anomalías, la exploración de datos, 
                la bioinformática y la imagenología, entre otros. Permite descubrir patrones 
                ocultos, identificar grupos similares y comprender la estructura subyacente de 
                los datos, lo que puede proporcionar información valiosa para la toma de 
                decisiones y la generación de conocimiento.
              </p>
              <!-- <a href="/" class="card-link">Probar algoritmo</a> -->
            </div>
          </div>
        </div>
      </section>

      <section class="card arboles-card">
        <div class="container">
          <div class="container-arboles">
            <div class="title-arboles">
              <h1 class="arboles-title">Arboles de decisión</h1>
              <p class="cuerpo-arboles">
                Los árboles de decisión son un tipo de algoritmo de aprendizaje automático 
                utilizado para modelar y predecir resultados basados en reglas de decisión. 
                Este algoritmo se basa en la estructura de un árbol, donde cada nodo representa 
                una característica o atributo, las ramas representan las posibles salidas o 
                resultados, y las hojas representan las decisiones o predicciones finales. El 
                proceso de construcción de un árbol de decisiones implica dividir el conjunto de 
                datos en función de diferentes atributos y criterios de división, de manera que 
                se maximice la homogeneidad de las muestras dentro de cada subconjunto 
                resultante. Esto se hace evaluando diferentes métricas de impureza o ganancia de 
                información, como la entropía o el índice de Gini. Una vez construido el árbol, 
                se puede utilizar para realizar predicciones sobre nuevos datos. Para ello, se 
                sigue el camino desde el nodo raíz hasta una hoja, siguiendo las reglas de 
                decisión en cada nodo. Cada hoja representa una clase o categoría a la que 
                pertenece la muestra. Los árboles de decisión son ampliamente utilizados debido 
                a su capacidad para manejar datos numéricos y categóricos, su interpretabilidad 
                y su capacidad para manejar conjuntos de datos grandes. Además, pueden ser 
                utilizados tanto en problemas de clasificación como en problemas de regresión.
              </p>
              <!-- <a href="/" class="card-link">Probar algoritmo</a> -->
            </div>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<style scoped>

#inicio {
    padding-top: 55px;
    padding-bottom: 75px;
    background-color: #000000;
    background-image: url(https://f.odnos.app/f/644abd716219a7vpgeoRLtNtriangles14301051280.webp);
    color: #ffffff;
    box-shadow: 0 0 10px rgba(222, 21, 205, 0.5);
    margin-top: -38px;
    margin-left: -33px;
    margin-right: -33px;
    background-size: cover;
    background-position: center;
    box-shadow: #de15cd;
    opacity: 1;
}

.title-container{
  margin-top: 1.25rem;
  margin-bottom: 1.25rem;
  text-align: center;
  width: 50%;
  
}


.container-inicio{
  display: flex;
  flex-wrap: wrap;
  align-items: center;
}

.container {
  margin-top: 120px;
}

.container-apriori{
  display: flex;
  align-items: center;
  flex-direction: row-reverse;
}

.title-apriori{
  color: #000000;
  margin-top: 1.25rem;
  margin-bottom: 1.25rem;
  text-align: center;
  width: 50%;  
}

.cuerpo-apriori {
  font-size: 16px;
  color: hwb(0 0% 100%);
  margin-bottom: 20px;
}

.algoritmos-container {
  display: flex;
  flex-wrap: wrap;
  margin-left: -37px;
  margin-right: -37px;
}

.apriori-card {
  margin-top: 10px;
  width: 100%;
  padding-top: 55px;
  padding-bottom: 75px;
  border: none;

}

.apriori-title {
  font-size: 100px;
  font-weight: bolder;
  color: #18367c;
}

.apriori-image{
  width: 10px;
  height: 100px; 
  background-color: #f0f0f0; 
  position: relative; 

}

.metricas-card {
  background-color:rgba(235, 233, 233, 0.492);
  width: 100%;
  border: none;
}

.metricas-title {
  font-size: 100px;
  font-weight: bolder;
  color: #18367c;
}

.title-metricas{
  color: #000000;
  margin-top: 1.25rem;
  margin-bottom: 1.25rem;
  text-align: center;
  width: 50%;  
}

.container-metricas{
  display: flex;
  flex-wrap: wrap;
  align-items: center;
}
.cuerpo-metricas {
  font-size: 16px;
  color: hwb(0 0% 100%);
  margin-bottom: 20px;
}

.clustering-card {
  background-color: #ffffff39;
  width: 100%;
  border: none;
}

.container-clustering{
  display: flex;
  align-items: center;
  flex-direction: row-reverse;
}

.title-clustering{
  color: #000000;
  margin-top: 1.25rem;
  margin-bottom: 1.25rem;
  text-align: center;
  width: 50%;  
}

.cuerpo-clustering {
  font-size: 16px;
  color: hwb(0 0% 100%);
  margin-bottom: 20px;
}

.clustering-title {
  font-size: 100px;
  font-weight: bolder;
  color: #18367c;
}

.arboles-card {
  background-color: #00000097;
  width: 100%;
  border: none;
}

.arboles-title {
  font-size: 100px;
  font-weight: bolder;
  color: #18367c;
}

.title-arboles{
  color: #000000;
  margin-top: 1.25rem;
  margin-bottom: 1.25rem;
  text-align: center;
  width: 50%;  
}

.container-arboles{
  display: flex;
  flex-wrap: wrap;
  align-items: center;
}
.cuerpo-arboles {
  font-size: 16px;
  color: hwb(0 100% 0% / 0.759);
  margin-bottom: 20px;
}
.card {
  margin: 0;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgb(255, 255, 255);
  text-align: center;
  color: #fff;
  flex: 0 0 100%;
  max-width: 100%;
  padding-left: 15px;
  padding-right: 15px;
}

.card h3 {
  font-size: 24px;
  margin: 0;
}

.card p {
  font-size: 16px;
  margin-bottom: 20px;
}
.image-slider {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  margin-top: 20px;
}

.slider-image {
  width: 200px;
  height: 200px;
  object-fit: cover;
  
}

.arrow-button {
  background: transparent;
  border: none;
  font-size: 24px;
  color: #fff;
  cursor: pointer;
  padding: 5px;
  margin: 0 10px;
}
</style>
