<script setup>
import axios from 'axios';
import Chart from 'chart.js/auto';
import File from './File.vue';
import CSV from './CSV.vue';
</script>

<script>
    export default{
        data() {
            return{
                parametros:{
                    metrica : '',
                    estandarizacion : ''
                },
                respuesta: null,
                bandera : false,
                file: null,
                columnasNoRequeridas: null,
                headers : null,
                punto1 : null,
                punto2 : null,
                distancia : null,
                col_row : null,
                dimensiones : null
            }
            
        },

        methods: {
            enviandoDatos(){
                const formData = new FormData() ;
                formData.append('file', this.file);
                formData.append( 'metrica', this.parametros.metrica );
                formData.append( 'estandarizacion', this.parametros.estandarizacion );

                if(this.columnasNoRequeridas) {
                    formData.append('columnas_no_requeridas', JSON.stringify(this.columnasNoRequeridas));
                }
                
                axios.post( 'http://127.0.0.1:8000/api/metricas', formData )
                    .then( response => this.guardandoDatos( response ) )
                    .catch( error => console.log( error ) );
            },

            guardandoDatos( res ){
                this.respuesta = res.data.distancias
                this.bandera = true
                const cantidadRegistros = this.respuesta.length;

                // Calcula las opciones para el selector de columnas_renglones
                const opciones = [];
                const division = Math.ceil( cantidadRegistros / 5 ); // Redondea hacia arriba
                for ( let i = 1; i <= 5; i++ ) {
                    opciones.push(( i * division ).toString() );
                }

                // Asigna las opciones al modelo col_row
                this.dimensiones = opciones;

            },

            buscarDistancia(){
                this.distancia = this.respuesta[ this.punto1 ][ this.punto2 ];
            }

            
        }
    }

</script>

<template>
    <h1 class="titulo">Metricas de distancias</h1>
    <form>
        <div class="contenedor">        
            <File @archivoValidado="file => this.file = file" />
            <CSV :file="file" @columnasNoRequeridas="data => this.columnasNoRequeridas = data" />

            <div class="selector">
                <label for=""><strong>Seleccione la metrica de distancia que desea utilizar:</strong></label>
                <br>
                <v-select
                clearable
                hide-details="true"
                label="Selecciona"
                :items="['euclidean', 'chebyshev', 'cityblock', 'minkowski']"
                variant="outlined"
                v-model="parametros.metrica"
                name="metrica" 
                id="metrica"  
                @update:model-value="enviandoDatos"
                class="selector-container"
                ></v-select>

                <label for=""><strong>Seleccione el tipo de estandarización que desea emplear:</strong></label>
                <v-select
                clearable
                hide-details="true"
                label="Selecciona"
                :items="['standardScaler', 'minMaxScaler']"
                variant="outlined"
                v-model="parametros.estandarizacion"
                name="estandarizacion" 
                id="estandarizacion"  
                @update:model-value="enviandoDatos"
                class="selector-container"
                ></v-select>
                <!-- <select name="metrica" id="metrica" v-model="parametros.metrica" @change="enviandoDatos">
                <option value="euclidean">Euclidiana</option>
                <option value="chebyshev">Chebyshev</option>
                <option value="cityblock">City block</option>
                <option value="minkowski">Minkowski</option>
                </select> -->
            </div>
        </div>
    </form>

    <div v-if="bandera">
        <h2>Las distancias obtenidas son las siguientes:</h2>
        <v-text-field 
        label="Punto 1" type="numeric" variant="outlined" clearable hide-details="true"
        v-model="punto1" class="input" @update:model-value="buscarDistancia"
        ></v-text-field>

        <v-text-field 
        label="Punto 2" type="numeric" variant="outlined" clearable hide-details="true"
        v-model="punto2" class="input" @update:model-value="buscarDistancia"
        ></v-text-field>
        <h2 v-if="punto1 && punto2">La distancia entre el punto {{ punto1 }} y el punto {{ punto2 }} es: <es:labe> {{ distancia }} </es:labe></h2>
        <form>
            <div class="contenedor">        
                <div class="selector">
                    <label for=""><strong>Selecciones cuantas columnas y renglones desea ver:</strong></label>
                    <br>
                    <v-select
                    clearable
                    hide-details="true"
                    label="Selecciona"
                    :items="dimensiones"
                    variant="outlined"
                    v-model="col_row"
                    name="columnas_renglones" 
                    id="columnas_renglones"  
                    class="selector-container"
                    ></v-select>
                </div>
            </div>
        </form>
        <!-- <div v-html="tablaHtml" class="contenedor"></div> -->

        <v-table fixed-header height="500px">
            <thead>
            <tr>
                <th></th>
                <th class="text-left" v-for="(res, index) in respuesta.slice(0, col_row)" >{{ index }}</th>
            </tr>
            </thead>
            <tbody>
                <tr v-for="(row, index) in respuesta.slice( 0, col_row)" :key="index">
                    <td>{{ index }}</td>
                    <td v-for="cell in row.slice(0, col_row)">{{ cell.toFixed(3) }}</td>
                </tr>
            </tbody>
        </v-table>

        <!-- <div>
            <v-data-table-server
            :headers="headers"
            :items-per-page="itemsPerPage"
            :total-items="totalItems"
            :server-items-length="serverItemsLength"
            :loading="loading"
            @fetch-data="fetchData"
            ></v-data-table-server>
        </div> -->
    </div>
</template>
  
  <style scoped>
  .titulo {
    color: #d517cb;
    font-size: 40px;
    font-family: Arial, sans-serif;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 50px;
  }
  
  .selector {
    margin-top: 20px;
    text-align: center;
  }

    .select-container {
        display: flex;
        gap: 20px;
        margin: 0 auto;
    }

  .btn-submit {
    margin-top: 20px;
    text-align: center;
}

.titulo {
    color: #d517cb;
    font-size: 40px;
    font-family: Arial, sans-serif;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 50px;
  }
  
  .selector {
    margin-top: 20px;
    text-align: center;
  }

  .btn-submit {
    margin-top: 20px;
    align-self: center;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    text-align: center;
  }

  .table th,
  .table td {
    padding: 8px;
    border: 1px solid #ccc;
  }

  .table th {
    background-color: #f2f2f2;
    text-align: center;
  }

  .table th:first-child,
  .table td:first-child {
    font-weight: bold;
    text-align: center;
  }

  .table td {
    text-align: center;
  }
  </style>
