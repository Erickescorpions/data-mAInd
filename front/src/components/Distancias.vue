<script setup>
import axios from 'axios';
import Chart from 'chart.js/auto';
</script>

<script>
    export default{
        data(){
            return{
                parametros:{
                    tipo_distancia : ''
                }
            }
        },

        methods: {
            enviandoDatos(){
                axios.post( 'http://127.0.0.1:8000/api/metricas', this.parametros )
                    .then( response => this.generandoMapa( response ) )
                    .catch( error => console.log( error ) )
            },

            generandoMapa( res ){

            }

        }

    }





</script>

<template>
    <h1 class="titulo">Metricas de distancias</h1>

    <div>
        <select name="metricas_distancias" id="distancias" v-model="tipo_distancia">
            <option value="">Seleccione una opción</option>
            
            <option value="euclidian">Euclidiana</option>
            <option value="chebyshev">Chebyshev</option>
            <option value="cityblock">City block</option>
            <option value="minkowski">Minkowski</option>

        </select>
    </div>

</template>

<style scoped>
    .titulo {
        color: #333;
        font-size: 40px;
        font-family: Arial, sans-serif;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 50px;
    }


</style>