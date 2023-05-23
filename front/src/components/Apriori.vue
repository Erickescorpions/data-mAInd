<script>
import { required } from '@vuelidate/core'
import { useVualidate } from '@vuelidate/validators'

export default {

  setup() {
    return { v$: useVualidate() }
  },

  data() {
      return {
        elevacion: 0,
        confianza: 0,
        soporte: 0
      }
  },

  // vuelidate para validar 
  validations() {
    return {
      elevacion: { required },
      confianza: { required },
      soporte: { required }
    }
  }, 
  methods: {

  }
}
</script>

<template>
  <div>
    <div>
      <p>Selecciona los parametros para aplicar al algoritmo:</p>
      <form action="" class="form" method="post" @submit="validar">
        <div :class="{ error: v$.elevacion.$errors.length }">
          <label for="elevacion">Elevacion:</label>
          <input type="text" name="elevacion" id="elevacion" v-model="elevacion">
          <div class="input-errors" v-for="error of v$.elevacion.$errors" :key="error.$uid">
            <div class="error-msg">{{ error.$message }}</div>
          </div>
        </div>

        <div :class="{ error: v$.confianza.$errors.length }">
          <label for="confianza">Confianza:</label>
          <input type="text" name="confianza" id="confianza" v-model="confianza">
          <div class="input-errors" v-for="error of v$.confianza.$errors" :key="error.$uid">
            <div class="error-msg">{{ error.$message }}</div>
          </div>
        </div>

        <div :class="{ error: v$.soporte.$errors.length }">
          <label for="soporte">Soporte:</label>
          <input type="text" name="soporte" id="soporte" step="any" v-model="soporte">
          <div class="input-errors" v-for="error of v$.soporte.$errors" :key="error.$uid">
            <div class="error-msg">{{ error.$message }}</div>
          </div>
        </div>

        <input type="submit" value="Guardar Parametros" class="submit-btn">
      </form>
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

.form {
  display: flex;
  flex-direction: column;
  gap: 5px;
  width: 30%;
  border: 3px white solid;
  border-radius: 15px;
  padding: 10px;
}

.submit-btn {
  max-width: 50%;
  align-self: center;
}

</style>