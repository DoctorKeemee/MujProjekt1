import { createRouter, createWebHistory } from "vue-router";

import Practicing from "./components/Practicing.vue";
import Learning from "./components/Learning.vue";
import Home from "./views/Home.vue";

const  routes  = [
    {
        path: '/',
        name: 'Domů',
        component: Home
    },
    {
        path: '/learning',
        name: 'Učení',
        component: Learning
    },
    {
        path: '/practicing',
        name: 'Opakování',
        component: Practicing
    },
    //pridani dalsich cest
]

const  router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
})

export default router;