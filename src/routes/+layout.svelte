<script lang="ts">
  import Header from './Header.svelte';
  import PieDePagina from './PieDePagina.svelte';
  import { onMount } from 'svelte';
  import { isAuthenticated, userRole, usuario } from '$lib/stores';

  onMount(() => {
    isAuthenticated.useLocalStorage();
    userRole.useLocalStorage();
    usuario.useLocalStorage();
  });
</script>

<style>
  main {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }
  .contenido {
    flex: 1;
  }
</style>

<main>
  <Header />
  <div class="contenido">
    <slot />
  </div>
  <PieDePagina />
</main>
