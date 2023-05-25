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
                }
            }
        }, 

        mostrandoDatos(res) {
            console.log(res);
            if(this.reglas) {
                this.reglas = null;
            }

            this.reglas = res.data.reglas;

            if(this.chart_frecuencia) {
                this.chart_frecuencia.destroy();
            }
            
            let frecuencia = res.data.frecuencia;
            let x_labels_fre = [];
            let y_labels_fre = [];
            let length = Object.keys(frecuencia).length;
            //console.log(typeof(frecuencia));

            for(let i = 0; i < length; i++) {
                //console.log(frecuencia[i]['frecuencia']);
                x_labels_fre.push(frecuencia[i]['pelicula']);
                y_labels_fre.push(frecuencia[i]['frecuencia'])
            }

            const canvas_frecuencia = document.getElementById('frecuencia');

            this.chart_frecuencia = new Chart(canvas_frecuencia, {
                type: 'bar',
                data: {
                labels: x_labels_fre,
                datasets: [{
                    label: 'Frecuencia',
                    data: y_labels_fre,
                    borderWidth: 10
                }]
                },
                options: {
                    indexAxis: 'y',
                    layout: {
                        padding: 20
                    },
                    // Elements options apply to all of the options unless overridden in a dataset
                    // In this case, we are setting the border of each horizontal bar to be 2px wide
                    elements: {
                        bar: {
                            borderWidth: 2,
                        }
                    },
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'right',
                        },
                        title: {
                            display: true,
                            text: 'Frecuencia de los datos en cada regla de asociacion'
                        }
                    }
                }
            });
        }
    }
}
</script>

<template>
    <div>
        <form class="form" @submit.prevent="enviandoDatos">
            <p>Selecciona un dataset (*extension csv)</p>
            <div class="form-vertical-seccion">
                <label for="dataset">Dataset: </label>
                <input type="file" ref="fileInput" @change="validandoArchivo"/>
                <span v-if="error_archivo.error">
                    {{ error_archivo.mensaje }}
                </span>
            </div>

            <p>Agrega los parametros para aplicar al algoritmo:</p>
            <div class="form-vertical-seccion">
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
            <input type="submit" value="GuardarParametros" class="btn-submit">
        </form>
    </div>

    <div id="graficas">
        <canvas id="frecuencia">

        </canvas>

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

.form .form-vertical-seccion {
  display: flex;
  flex-direction: column;
  gap: 5px;
  width: 70%;
  padding: 10px;
}

.submit-btn {
  align-self: center;
}

</style>