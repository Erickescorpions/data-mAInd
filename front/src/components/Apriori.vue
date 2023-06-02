<script setup>
import useValidate from '@vuelidate/core';
import { required, numeric } from '@vuelidate/validators';
import axios from 'axios';
import Chart from 'chart.js/auto';
</script>

<script>
export default {
    data() {
        return {
            v$: useValidate(),
            parametros: {
                elevacion: 2,
                confianza: 0.3,
                soporte: 0.01
            },
            error_archivo: {
                error: false,
                mensaje: ""
            },
            chart_frecuencia: null,
            reglas: null
        }
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
        enviandoDatos() {
            
            // obtenemos el dataset proporcionado
            const file = this.$refs.fileInput.files[0];
            
            // validacion del formulario
            this.v$.$validate()

            const formData = new FormData(); 
            formData.append('file', file);

            formData.append('confianza', this.parametros.confianza);
            formData.append('elevacion', this.parametros.elevacion);
            formData.append('soporte', this.parametros.soporte);

            if(!this.v$.$error) {
                axios.post('http://127.0.0.1:8000/api/apriori', formData)
                    .then(response => this.mostrandoDatos(response))
                    .catch(error => console.log(error));
            }
        },

        validandoArchivo(event) {
            const file = event.target.files[0];
            const extensionesPermitidas = ['csv'];

            if(file) {
                const fileExtension = file.name.split('.').pop();
                //console.log(fileExtension);
                if (!extensionesPermitidas.includes(fileExtension)) {
                    // El archivo no tiene la extensión CSV
                    this.error_archivo.error = true;
                    this.error_archivo.mensaje = `El archivo solo puede incluir las siguientes extensiones [${extensionesPermitidas.toString()}]`

                    // limpiamos el input del archivo
                    this.$refs.fileInput.value = '';
                } else {
                    const formData = new FormData(); 
                    formData.append('file', file);

                    axios.post('http://127.0.0.1:8000/api/apriori/frecuencia', formData)
                        .then(response => this.mostrandoFrecuencias(response))
                        .catch(error => console.log(error));
                }
            }
        },


        mostrandoFrecuencias(res) {

            console.log(res);

            if(this.chart_frecuencia) {
                this.chart_frecuencia.destroy();
            }

            if(!res.data.sucess) {
                console.log('Algo fallo');
                return;
            }
            
            let frecuencias = res.data.frecuencias;
            let labels = res.data.labels;

            const canvas_frecuencia = document.getElementById('frecuencia');
            // agregando clase
            document.getElementById('frecuencia-container').style.display = 'block';

            let config  = {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Frecuencia',
                        data: frecuencias
                    }],
                    borderWidth: 1,
                },
                options: {
                    maintainAspectRatio: false,

                    indexAxis: 'y',
                    scales: {
                        y: {
                            beginAtZero: true, // Iniciar el eje Y en 0
                            ticks: {
                                autoSkip: false,
                            },
                            barPercentage: 0.8
                        },
    
                    },

                    tooltips: {
                        enabled: true
                    },

                    plugins: {
                        legend: {
                            position: 'right',
                        },
                        title: {
                            display: true,
                            text: 'Frecuencia de los datos en cada regla de asociacion'

                        },
                    }
                },
            }

            this.chart_frecuencia = new Chart(canvas_frecuencia, config);
        },

        // Función para ocultar/mostrar la gráfica
        toggleChart() {
            let chartContainer = document.getElementById('frecuencia-container');
            if (chartContainer.style.display === 'none') {
                chartContainer.style.display = 'block'; // Mostrar la gráfica
            } else {
                chartContainer.style.display = 'none'; // Esconder la gráfica
            }
        },

        mostrandoDatos(res) {
            console.log(res);
            if(this.reglas) {
                this.reglas = null;
            }

            this.reglas = res.data.reglas;
        }
    }
}
</script>

<template>
    <div class="container">
        
        <p>Selecciona un dataset (*extension csv)</p>
        <div class="container">
            <label for="dataset">Dataset: </label>
            <input type="file" ref="fileInput" @change="validandoArchivo"/>
            <span v-if="error_archivo.error">
                {{ error_archivo.mensaje }}
            </span>
        </div>

        <!-- Seccion de grafica de frecuencia -->
        <button id="toggleButton" v-on:click="toggleChart" v-if="chart_frecuencia">Mostrar/Esconder Gráfica</button>
        <div id="frecuencia-container" class="chart-container">
            <canvas id="frecuencia"> </canvas>
        </div>

        <p>Agrega los parametros para aplicar al algoritmo:</p>
        <div class="container">
            <label for="elevacion">Elevacion:</label>
            <input type="text" name="elevacion" id="elevacion" v-model="parametros.elevacion">
            <span v-if="v$.parametros.elevacion.$error">
                {{ v$.parametros.elevacion.$errors[0].$message }}
            </span>

            <label for="confianza">Confianza:</label>
            <input type="text" name="confianza" id="confianza" v-model="parametros.confianza">
            <span v-if="v$.parametros.confianza.$error">
                {{ v$.parametros.confianza.$errors[0].$message }}
            </span>

            <label for="soporte">Soporte:</label>
            <input type="text" name="soporte" id="soporte" step="any" v-model="parametros.soporte">
            <span v-if="v$.parametros.soporte.$error">
                {{ v$.parametros.soporte.$errors[0].$message }}
            </span>
        </div>
        
        <button class="submit-btn" v-on:click="enviandoDatos">Obtener Reglas</button>
        
        <!-- Seccion tabla de reglas generadas -->
        <div v-if="reglas">
            <table>
                <thead>
                    <tr>
                        <th>Regla</th>
                        <th>Soporte</th>
                        <th>Confianza</th>
                        <th>Elevacion</th>
                    </tr>
                </thead>
                <tbody v-for="regla in reglas">
                    <tr>
                        <th>{{ regla.regla.toString() }}</th>
                        <th>{{ regla.parametros.soporte.toFixed(4) }}</th>
                        <th>{{ regla.parametros.confianza.toFixed(4) }}</th>
                        <th>{{ regla.parametros.elevacion.toFixed(4) }}</th>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>



<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.container {
    display: flex;
    flex-direction: column;
    margin: auto;
    padding: 10px;
}


.submit-btn {
  align-self: center;
}

.chart-container {
    display: none;
    height: 1500px;
}

</style>