import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createVuetify } from 'vuetify'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'

import App from './App.vue'
import EmployeeList from './components/DummyEmployeeList.vue'
import EmployeeForm from './components/DummyEmployeeForm.vue'

const routes = [
  { path: '/', component: EmployeeList },
  { path: '/employees', component: EmployeeList },
  { path: '/employees/create', component: EmployeeForm },
  { path: '/employees/edit/:id', component: EmployeeForm, props: true }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const vuetify = createVuetify({
  theme: {
    defaultTheme: 'light'
  }
})

const app = createApp(App)
app.use(router)
app.use(vuetify)
app.mount('#app')
