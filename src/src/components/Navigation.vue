<template>
  <nav
      class="navbar is-fixed-top is-warning"
      role="navigation"
      aria-label="main navigation"
  >
    <div class="navbar-brand">
      <a class="navbar-item" href="https://bulma.io">
        <img src="https://bulma.io/images/bulma-logo.png" width="112" height="28">
      </a>

      <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>
    <div class="navbar-start">
  <RouterLink to="/" class="navbar-item">Domů</RouterLink>
  <RouterLink to="/practicing" class="navbar-item">Procvičování</RouterLink>
  <RouterLink to="/learning" class="navbar-item">Učení</RouterLink>
    </div>
    <div class="navbar-end">
      <div class="navbar-item">
        <div class="buttons">
          <a class="button is-primary">
            <strong>Sign up</strong>
          </a>
          <a class="button is-light">
            Log in
          </a>
        </div>
      </div>
    </div>

  </nav>






</template>

<script lang="ts">

import { defineComponent } from "vue";

export default defineComponent({
  name: "Navigation"
})
</script>


<style scoped>

</style>