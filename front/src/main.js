import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// font awesome
// import the fontawesome core 
import { library } from '@fortawesome/fontawesome-svg-core'
// import font awesome icon component 
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
// import specific icons 
import { faBrain } from '@fortawesome/free-solid-svg-icons'
// add icons to the library
library.add(faBrain)

// Vuetify
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as labsComponents from 'vuetify/labs/components'
import * as directives from 'vuetify/directives'

import '@fortawesome/fontawesome-free/css/all.css';
import '@fortawesome/fontawesome-free/js/all.js';

const vuetify = createVuetify({
    components: {
        ...components,
        ...labsComponents,
      },
    directives,
    ssr: true
})

const app = createApp(App)

app.use(router)
app.use(vuetify)
app.component('font-awesome-icon', FontAwesomeIcon)
app.mount('#app')
