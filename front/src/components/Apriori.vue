<script setup>
import { useVuelidate } from '@vuelidate/core';
import { required, numeric } from '@vuelidate/validators';
import axios from 'axios';
import Chart from 'chart.js/auto';
import File from './File.vue';
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
            file: null,
            chart_frecuencia: null,
            reglas: null,
            mostrarFrecuencia: true,
            v$: useVuelidate()
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
        cargandoArchivo(file) {
            const formData = new FormData();
            formData.append('file', file);
            this.file = file;

            this.reglas = null;

            axios.post('http://127.0.0.1:8000/api/apriori/frecuencia', formData)
                .then(response => this.mostrandoFrecuencias(response))
                .catch(error => console.log(error));
        },

        mostrandoFrecuencias(res) {
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

        enviandoDatos() {
            // validacion del formulario
            this.v$.$validate() 

            const formData = new FormData(); 
            formData.append('file', this.file);

            formData.append('confianza', this.parametros.confianza);
            formData.append('elevacion', this.parametros.elevacion);
            formData.append('soporte', this.parametros.soporte);

            if(!this.v$.$error) {
                axios.post('http://127.0.0.1:8000/api/apriori', formData)
                    .then(response => this.mostrandoDatos(response))
                    .catch(error => console.log(error));
            }
        },

        // Función para ocultar/mostrar la gráfica
        toggleChart() {
            let chartContainer = document.getElementById('frecuencia-container');
            if (chartContainer.style.display === 'none') {
                chartContainer.style.display = 'block'; // Mostrar la gráfica
                this.mostrarFrecuencia = true;
            } else {
                chartContainer.style.display = 'none'; // Esconder la gráfica
                this.mostrarFrecuencia = false;
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
    <div class="my-container">
        
        <File @archivoValidado="cargandoArchivo"/>

        <!-- Seccion de grafica de frecuencia -->
        <v-btn variant="flat" v-on:click="toggleChart" v-if="chart_frecuencia" class="btn mostrar">
            {{mostrarFrecuencia ? 'Esconder' : 'Mostrar'}} Frecuencia
        </v-btn>

        <div id="frecuencia-container" class="chart-container">
            <canvas id="frecuencia"> </canvas>
        </div>

        <p>Agrega los parametros para aplicar al algoritmo:</p>
        <div class="parametros-container">
            <div class="input-container">
                <v-text-field 
                    label="Elevacion minima" type="numeric" variant="outlined" clearable hide-details="true"
                    v-model="parametros.elevacion" class="input"
                ></v-text-field>
                <span v-if="v$.parametros.elevacion.$error" class="error-msg">
                    {{ v$.parametros.elevacion.$errors[0].$message }}
                </span>
            </div>
            
            <div class="input-container">
                <v-text-field
                    label="Confianza minima" type="numeric" variant="outlined" clearable hide-details="true"
                    v-model="parametros.confianza" class="input"
                ></v-text-field>
                <span v-if="v$.parametros.confianza.$error" class="error-msg">
                    {{ v$.parametros.confianza.$errors[0].$message }}
                </span>
            </div>

            <div class="input-container">
                <v-text-field
                    label="Soporte minimo" type="numeric" variant="outlined" clearable hide-details="true"
                    v-model="parametros.soporte" class="input"
                ></v-text-field>
                <span v-if="v$.parametros.soporte.$error" class="error-msg">
                    {{ v$.parametros.soporte.$errors[0].$message }}
                </span>
            </div>
            
            <v-btn variant="flat" v-on:click="enviandoDatos" class="btn">Obtener Reglas</v-btn>
        </div>
        
        <!-- Seccion tabla de reglas generadas -->
        <div v-if="reglas">
            <v-table>
                <thead>
                <tr>
                    <th class="text-left">No.</th>
                    <th class="text-left">Regla</th>
                    <th class="text-left">Soporte</th>
                    <th class="text-left">Confianza</th>
                    <th class="text-left">Elevacion</th>
                </tr>
                </thead>
                <tbody>
                    <tr v-for="(regla, index) in reglas" :key="index">
                        <td>{{ index }}</td>
                        <td>{{ regla.regla }}</td>
                        <td>{{ regla.soporte.toFixed(4) }}</td>
                        <td>{{ regla.confianza.toFixed(4) }}</td>
                        <td>{{ regla.elevacion.toFixed(4) }}</td>
                    </tr>
                </tbody>
            </v-table>
        </div>
    </div>
</template>

<style scoped>
.chart-container {
    display: none;
    height: 1500px;
}

.parametros-container {
    padding: 30px;
    width: 300px;
    margin: auto;
}

.input-container {
    margin: 20px 0px;
}

.mostrar {
    float: right;
}
</style>