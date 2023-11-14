/// <reference types="vite/client" />

import { ComponentCustomProperties } from 'vue';

module '*.vue' {
    import { defineComponent } from 'vue';
    const component: ReturnType<typeof defineComponent>;
    export default component;
}
interface ComponentCustomProperties {
    $router: any; // Add this line if you're using the Vue Router
}