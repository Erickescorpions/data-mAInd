<script setup>
import axios from 'axios';
</script>

<script>
export default {
    props: ['file'],

    data() {
        return {
            columnas: null,
            data: null,
            headers: null,
            mostrar : false
        }
    },

    methods: {
        obteniendoDatos() {
            const formData = new FormData();
            formData.append('file', this.file);

            if(this.columnas) {
                let columnasNoRequeridas = [];
                let length = this.columnas.length;
                for(let i = 0; i < length; i++) {
                    if(!this.columnas[i].requerida) {
                        columnasNoRequeridas.push(this.columnas[i].columna);
                    } 
                }

                this.$emit('columnasNoRequeridas', columnasNoRequeridas);
                formData.append('columnas_no_requeridas', JSON.stringify(columnasNoRequeridas));
            }

            axios.post('http://127.0.0.1:8000/api/csv', formData)
                .then(response => {
                    console.log(response);
                    this.columnas = response.data.columnas;

                    let length = this.columnas.length;
                    let headers = [];
                    for(let i = 0; i < length; i++) {
                        if(this.columnas[i].requerida) {
                            headers.push(this.columnas[i].columna);
                        }
                    }
                    this.headers = headers;

                    this.data = JSON.parse(response.data.data);
                    console.log(this.data);
                })
                .catch(error => console.log(error));
        },

        mostrarDatos(){
            this.mostrar = !this.mostrar;
            if ( this.mostrar == true ){
                this.obteniendoDatos();
            }
        },
    }
}
</script>

<template>
    <div>
        <v-btn variant="flat" v-if="file" v-on:click="mostrarDatos" class="btn" >
            Mostrar Datos
        </v-btn>

        <v-row v-if="mostrar">
            <v-col v-for="(item, index) in columnas" cols="4">
                <v-checkbox
                    :label="item.columna"
                    v-model="item.requerida"
                    hide-details
                    @change="obteniendoDatos"
                ></v-checkbox>
            </v-col>
        </v-row>

        <!-- Se muestra un modal -->
        <v-table fixed-header height="500px" v-if="mostrar">
            <thead>
            <tr>
                <th class="text-left" v-for="head in headers">{{ head }}</th>
            </tr>
            </thead>
            <tbody>
                <tr v-for="(row, index) in data" :key="index">
                    <td v-for="cell in row">{{ cell }}</td>
                </tr>
            </tbody>
        </v-table>
        
    </div>
</template>

<style scoped>
.btn {
    background-color: var(--main-color);
    color: white;
    margin: auto;
}
</style>