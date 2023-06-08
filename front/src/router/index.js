import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },

    {
      path: '/apriori',
      name: 'apriori',
      component: () => import('../views/AprioriView.vue')
    },

    {
      path: '/distancias',
      name : 'distancias',
      component: () => import( '../views/DistanciasView.vue' )
    },
    {
      path: '/clustering',
      name: 'clustering',
      component: () => import('../views/ClusteringView.vue')
    }
  ]
})

export default router
