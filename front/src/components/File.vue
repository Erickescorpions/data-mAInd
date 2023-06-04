<script setup>

</script>

<script>
export default {
    data() {
        return {
            error_archivo: {
                error: false,
                mensaje: ""
            },
            fileSelected: null,
        }
    },
    methods: {
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
                    this.error_archivo.error = false;
                    this.error_archivo.mensaje = '';
                    this.$emit('archivoValidado', file);
                }
            }
        },
    }
}
</script>

<template>
    <p>Selecciona un dataset (*extension csv) o escoge entre los archivos predeterminados:</p>
    <div class="file-container">
        <v-file-input 
            clearable label="File input" variant="outlined"
            :disabled="fileSelected ? true : false" hide-details="true"
            ref="fileInput" @change="validandoArchivo" 
        ></v-file-input>
        <v-select
            clearable
            hide-details="true"
            label="Selecciona"
            :items="['California', 'Colorado', 'Florida', 'Georgia', 'Texas', 'Wyoming']"
            variant="outlined"
            v-model="fileSelected"
        ></v-select>
    </div>
    <span v-if="error_archivo.error" class="error-msg">
        {{ error_archivo.mensaje }}
    </span>
</template>

<style scoped>
.file-container {
    display: flex;
    gap: 20px;
    margin: 20px 0px;
}
</style>