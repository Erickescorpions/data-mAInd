<script setup>
import { RouterLink } from 'vue-router'
</script>


<template>
    <header class="header-seguidor">
        <div class="title-container">
            <h1 class="page-title">
                Data MAInd 
                <font-awesome-icon icon="fa-solid fa-brain" style="color: white;" />
            </h1>
        </div>
        <nav>
            <RouterLink to="/">Home</RouterLink>
            <RouterLink to="/distancias">Distancias</RouterLink>
            <RouterLink to="/apriori">Apriori</RouterLink>
            <RouterLink to="/clustering">Clustering</RouterLink>
        </nav>
    </header>
</template>

<style scoped>
header {
  line-height: .1;
  max-height: 100vh;
  text-align: center;
}

.header-seguidor {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 999;
}

.hide {
    transform: translateY(-100%);
    transition: transform 0.3s ease-in-out;
  }

nav {
  width: 100%;
  font-size: 16px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--secondary-color);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

.page-title {
  color: white;
  font-family: 'Architects Daughter', cursive;
}

</style>
