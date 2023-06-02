<script setup>
import axios from 'axios';
import Chart from 'chart.js/auto';
</script>

<script>
    export default{
        data(){
            return{
                parametros:{
                    metrica : ''
                },

                error_archivo: {
                    error: false,
                    mensaje: ""
                },

                respuesta: null,
                col_row : 0,
                bandera : false
            }
            
        },

        computed:{
            tablaHtml(){
                return this.generandoTabla( this.respuesta )
            }
        },

        methods: {
            enviandoDatos(){
                 // obtenemos el dataset proporcionado
                const file = this.$refs.fileInput.files[0]

                const formData = new FormData() 
                formData.append('file', file)

                formData.append( 'metrica', this.parametros.metrica )
                axios.post( 'http://127.0.0.1:8000/api/metricas', formData )
                    .then( response => this.guardandoDatos( response ) )
                    .catch( error => console.log( error ) )
            },

            mostrarCSV(){
                const file = this.$refs.fileInput.files[0];
                const reader = new FileReader();
                
                reader.onload = () => {
                    const csvString = reader.result;
                    // Procesar csvString como lo necesites
                    const jsonArray = csvtojson().fromString(csvString);
                    this.guardandoDatos(jsonArray);
                    this.mostrarContenido = true; // Mostrar el contenido del archivo automáticamente
                };

                reader.readAsText(file);
            },

            validandoArchivo(event) {
                const file = event.target.files[0];
                const extensionesPermitidas = ['csv'];

                if(file) {
                    const fileExtension = file.name.split('.').pop();
                    // console.log(fileExtension);
                    if (!extensionesPermitidas.includes(fileExtension)) {
                        // El archivo no tiene la extensión CSV
                        this.error_archivo.error = true;
                        this.error_archivo.mensaje = `El archivo solo puede incluir las siguientes extensiones [${extensionesPermitidas.toString()}]`

                        // limpiamos el input del archivo
                        this.$refs.fileInput.value = '';
                    }
                    this.mostrarCSV();

                }
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
            <p>Selecciona un dataset (*extension csv)</p>
            <div class="slector">
                <label for="dataset">Dataset: </label>
                <input type="file" ref="fileInput" @change="validandoArchivo"/>
                <span v-if="error_archivo.error">
                    {{ error_archivo.mensaje }}
                </span>
                <table class="table">
                    <!-- Encabezados de columna -->
                    <thead>
                    <tr>
                        <th></th>
                        <th v-for="(value, index) in respuesta[0]" :key="index">{{ index }}</th>
                    </tr>
                    </thead>
                    <!-- Contenido del archivo CSV -->
                    <tbody>
                    <tr v-for="(row, rowIndex) in respuesta" :key="rowIndex">
                        <td><strong>{{ rowIndex }}</strong></td>
                        <td v-for="(value, key) in row" :key="key">{{ value }}</td>
                    </tr>
                    </tbody>
                </table>
            </div>

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
        <div v-html="tablaHtml" class="contenedor"></div>
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
