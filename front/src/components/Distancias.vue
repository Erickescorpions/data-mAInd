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
                    metrica : ''
                },
                respuesta: null,
                col_row : 0,
                bandera : false,
                file: null,
                columnasNoRequeridas: null
            }
            
        },

        computed:{
            tablaHtml(){
                return this.generandoTabla( this.respuesta )
            }
        },

        methods: {
            enviandoDatos(){
                const formData = new FormData() ;
                formData.append('file', this.file);
                formData.append( 'metrica', this.parametros.metrica );

                if(this.columnasNoRequeridas) {
                    formData.append('columnas_no_requeridas', JSON.stringify(this.columnasNoRequeridas));
                }
                
                axios.post( 'http://127.0.0.1:8000/api/metricas', formData )
                    .then( response => this.guardandoDatos( response ) )
                    .catch( error => console.log( error ) );
            },

            guardandoDatos( res ){
                this.respuesta = res.data.distancias
                this.col_row = 5
                this.bandera = true
            },

            generandoTabla( data ){
                if ( Array.isArray( data ) ) {

                    const colRow = parseInt( this.col_row ); // Convertir a entero

                    // Formatear los datos en una tabla HTML
                    let tabla = '<table>';
                    tabla += '<thead><tr>';

                    // Agregar encabezado de columnas
                    tabla += '<th></th>';
                    for ( let i = 0; i < colRow; i++ ) {
                        tabla += `<th>${i}</th>`;
                    }

                    tabla += '</tr></thead>';
                    tabla += '<tbody>';

                    for ( let i = 0; i < colRow; i++ ) {
                        tabla += '<tr>';
                        tabla += `<td><strong>${ i }</strong></td>`; // Agregar encabezado de fila
                        for (let j = 0; j < colRow; j++) {
                            tabla += `<td>${ data[i][j] }</td>`;
                        }

                        tabla += '</tr>';
                    }

                    tabla += '</tbody>';
                    tabla += '</table>';

                    return tabla;
                }

                return '';   
            }
        }
    }

</script>

<template>
    <h1 class="titulo">Metricas de distancias</h1>
    <form @submit.prevent="enviandoDatos">
        <div class="contenedor">        
            <File @archivoValidado="file => this.file = file" />
            <CSV :file="file" @columnasNoRequeridas="data => this.columnasNoRequeridas = data" />

            <div class="selector">
                <label for=""><strong>Seleccione la metrica de distancia que desea utilizar:</strong></label>
                <br>
                <select name="metrica" id="metrica" v-model="parametros.metrica">
                <option value="euclidean">Euclidiana</option>
                <option value="chebyshev">Chebyshev</option>
                <option value="cityblock">City block</option>
                <option value="minkowski">Minkowski</option>
                </select>
            </div>
            <div class="btn-submit">
                <button type="submit" class="btn-submit">Enviar</button>
            </div>
        </div>
    </form>

    <div v-if="csv">
        <h2>Contenido del archivo:</h2>
        <table>
            <thead>
                <tr>
                    <th></th>
                    <th v-for="(value, index) in respuesta[0]" :key="index">{{ index }}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(row, rowIndex) in respuesta" :key="rowIndex">
                    <td>{{ rowIndex }}</td>
                    <td v-for="(value, key) in row" :key="key">{{ value }}</td>
                </tr>
            </tbody>
        </table>
    </div>




    <!-- <div>
        <h2>Respuesta del servidor:</h2>
        <pre>{{ respuesta }}</pre>
    </div> -->

    <div v-if="bandera">
        <h2>Las distancias obtenidas son las siguientes:</h2>
        <form>
            <div class="contenedor">        
                <div class="selector">
                    <label for=""><strong>Selecciones cuantas columnas y renglones desea ver:</strong></label>
                    <br>
                    <select name="col_row" id="" v-model="col_row">
                    <option value="5">5</option>
                    <option value="20">20</option>
                    <option value="50">50</option>
                    <option value="200">200</option>
                    </select>
                </div>
            </div>
        </form>
        <!-- <div v-html="tablaHtml" class="contenedor"></div> -->

        <v-table fixed-header height="500px">
            <thead>
            <tr>
                <th></th>
                <th class="text-left" v-for="(res, index) in respuesta[0]">{{ index }}</th>
            </tr>
            </thead>
            <tbody>
                <tr v-for="(row, index) in respuesta" :key="index">
                    <td>{{ index }}</td>
                    <td v-for="cell in row">{{ cell.toFixed(3) }}</td>
                </tr>
            </tbody>
        </v-table>
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
