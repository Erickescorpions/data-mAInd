<script setup>
import { useVuelidate } from '@vuelidate/core';
import { required, numeric } from '@vuelidate/validators';
import axios from 'axios';
import File from './File.vue';
import * as d3 from 'd3';
</script>

<script>
export default {
    data() {
        return {
            parametros: {
                elevacion: 2,
                confianza: 0.3,
                soporte: 0.01
            },
            heatmap: {
                image: null,
                mostrar: false
            },
            columnas: null,
            columnasSeleccionadas: [],

            estandarizacion: 'StandardScaler',
            tipoEstandarizacion: ['StandardScaler', 'MinMaxScaler'],

            metrica: 'euclidean',
            tipoMetrica: ['euclidean', 'chebyshev', 'cityblock', 'minkowski'],

            dendograma: {
                image: null,
                mostrar: false
            },

            numeroClusters: 0,
            centroides: null,
            mostrarCentroides: false
        }
    },

    computed: {
        numeroColumnasSeleccionadas() {
            return this.columnasSeleccionadas.length;
        },
    },

    validations() {
        return {
            parametros: {
                elevacion: { required, numeric },
                confianza: { required, numeric },
                soporte: { required, numeric }
            }
        }
    },

    methods: {
        cargandoArchivo(file) {
            const formData = new FormData();
            formData.append('file', file);
            this.file = file;
            this.heatmap.image = null
            this.heatmap.mostrar = false

            axios.post('http://127.0.0.1:8000/api/clustering/correlaciones', formData)
                .then(response => {
                    this.heatmap.image = response.data.data.image;
                    this.columnas = response.data.data.columnas
                    this.heatmap.mostrar = true;
                })
                .catch(error => console.log(error));
        },

        obteniendoDendograma() {
            const formData = new FormData();
            this.numeroClusters = this.numeroColumnasSeleccionadas;
            formData.append('file', this.file);
            formData.append('metrica', this.metrica);
            formData.append('estandarizacion', this.estandarizacion);
            formData.append('columnas', JSON.stringify(this.columnas));

            axios.post('http://127.0.0.1:8000/api/clustering/jerarquico', formData)
                .then(response => {
                    console.log(response)
                    this.dendograma.image = response.data.data.image;
                    this.dendograma.mostrar = true;
                })
                .catch(error => console.log(error))
        },

        obteniendoClusters() {
            const formData = new FormData();
            formData.append('file', this.file);
            formData.append('metrica', this.metrica);
            formData.append('estandarizacion', this.estandarizacion);
            formData.append('columnas', JSON.stringify(this.columnasSeleccionadas));
            formData.append('numero_clusters', this.numeroClusters);

            axios.post('http://127.0.0.1:8000/api/clustering/jerarquico/centroides', formData)
                .then(response => {
                    console.log(response);
                    this.centroides = JSON.parse(response.data.centroides);
                    this.mostrarCentroides = true;
                })
                .catch(error => console.log(error))
        }
    }
}
</script>

<template>
    <div class="my-container">
        <File @archivoValidado="cargandoArchivo"/>
        <div v-if="heatmap.mostrar">
            <div class="wrapper flex">
                <div class="wrapper">
                    <p>Mapa de calor de las correlaciones de las columnas</p>
                    <div class="img-container">
                        <img :src="heatmap.image" >
                    </div>
                </div>
            </div>
            
            <div class="wrapper">
                <v-select
                    label="Tipo de estandarización"
                    :items="tipoEstandarizacion"
                    variant="outlined"
                    density="compact"
                    v-model="estandarizacion"
                ></v-select>
    
                <v-select
                    label="Metrica distancia"
                    :items="tipoMetrica"
                    variant="outlined"
                    density="compact"
                    v-model="metrica"
                ></v-select>
    
                <v-btn variant="flat" v-on:click="obteniendoDendograma" class="btn">Obtener Dendograma</v-btn>
            </div>

            <div v-if="dendograma.mostrar">
                <div class="flex">
                    <div class="wrapper">
                        <div class="img-container">
                            <img :src="dendograma.image" >
                        </div>
                    </div>
                </div>
                
                <div class="wrapper">
                    <p>Selecciona el numero de clusters</p>
    
                    <input type="range" min="0" max="10" step="1" class="slider" v-model="numeroClusters" @change="() => mostrarCentroides = false">
                    <input type="text" v-model="numeroClusters" class="numero-clusters-container" disabled>

                    <p>Selecciona las columnas mas relevantes:</p>
                    <div class="wrapper">
                        <v-row>
                            <v-col v-for="(item, index) in columnas" cols="3" :key="index">
                                <v-checkbox
                                    v-model="columnasSeleccionadas"
                                    :value="item"
                                    :label="item"
                                    hide-details
                                    class="inline"
                                    @change="() => mostrarCentroides = false"
                                ></v-checkbox>
                            </v-col>
                        </v-row>
                        <p>Nota: minimo se necesitan escoger 4 columnas para ejecutar el algoritmo</p>
                    </div>


                    <v-btn variant="flat" v-on:click="obteniendoClusters" class="btn">Obtener Clusters</v-btn>
                </div>

                <div v-if="mostrarCentroides">
                    <v-table>
                        <thead>
                            <tr>
                                <th class="text-left">
                                    Cluster
                                </th>
                                <th v-for="item in columnasSeleccionadas" class="text-left">
                                    {{ item }}
                                </th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr v-for="(item, index) in centroides" :key="index">
                                <td>{{ index }}</td>
                                <td v-for="val in item">{{ val.toFixed(3) }}</td>
                            </tr>
                        </tbody>
                    </v-table>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.wrapper {
    padding: 10px;
    margin: 20px;
}

.flex {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.inline {
    display: inline;
}

.checbox-container {
    display: block;
}

.img-container {
    width: 80%;
    display: block;
}
.img-container img {
    display: block; /* Coloca la imagen en su propia línea */
    border-radius: 10px;
    max-width: 800px;
    object-fit: scale-down;
}

.slider {
  -webkit-appearance: none;
  width: 80%;
  height: 5px;
  border-radius: 5px;
  background-color: #ddd;
  outline: none;
  display: inline;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  background-color: #4CAF50;
  cursor: pointer;
}

.slider::-moz-range-thumb {
  width: 15px;
  height: 15px;
  border-radius: 50%;
  background-color: #4CAF50;
  cursor: pointer;
}

.numero-clusters-container{
    margin: 20px;
    border: 1px solid rgb(100, 100, 100);
    width: 40px;
    height: 35px;
    text-align: center;
    border-radius: 5px;
    padding: 5px;
}

.btn {
  background-color: var(--main-color);
  color: white;
  margin: auto;
}
</style>