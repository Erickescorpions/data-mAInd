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
            }
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
            this.v$.$validate()

            if(!this.v$.$error) {
                axios.post('http://127.0.0.1:8000/api/apriori', this.parametros)
                    .then(response => this.generandoGraficas(response))
                    .catch(error => console.log(error))
            }
        },

        generandoGraficas(res) {
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

            new Chart(canvas_frecuencia, {
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
        <p>Selecciona los parametros para aplicar al algoritmo:</p>   
        <form class="form" @submit.prevent="enviandoDatos">
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
            <input type="submit" value="GuardarParametros" class="btn-submit">
        </form>
    </div>

    <div id="graficas">
        <canvas id="frecuencia">

        </canvas>

        <canvas id="reglas">

        </canvas>
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

.form {
  display: flex;
  flex-direction: column;
  gap: 5px;
  width: 70%;
  border: 3px white solid;
  border-radius: 15px;
  padding: 10px;
}

.submit-btn {
  align-self: center;
}

</style>