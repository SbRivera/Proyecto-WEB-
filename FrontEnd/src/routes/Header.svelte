<script>
  import { isAuthenticated, userRole } from '$lib/stores';
  import { goto } from '$app/navigation';
  
  function logout() {
    isAuthenticated.set(false);
    userRole.set('guest');
    goto('/login'); 
  }
</script>
  
<style>
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background-color: #f8f9fa;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  .logo {
    display: flex;
    align-items: center;
    cursor: pointer;
  }
  .logo img {
    height: 50px;
    margin-right: 1rem;
  }
  .centro h1 {
    font-size: 1.5rem;
    color: #2c3e50;
    margin: 0;
  }
  .botones {
    display: flex;
    gap: 1rem;
  }
  .botones button {
    padding: 0.5rem 1rem;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  .botones button:hover {
    background-color: #2980b9;
  }
  .logout {
    margin-left: auto;
  }
  @media (max-width: 768px) {
    .botones button {
      padding: 0.5rem;
    }
  }
</style>
  
<header>
  <div class="logo">
    <a href="/">
      <img src="/illinizas/ilinisas.png" alt="Logo">
    </a>
  </div>
  <div class="centro">
    <h1>RESERVA ECOLOGICA LOS ILINIZAS</h1>
  </div>
  <div class="botones">
    {#if $isAuthenticated}
      <button on:click={() => goto('/profile')}>Perfil</button>
      {#if $userRole === 'admin'}
        <button on:click={() => goto('/admin/solicitudes')}>Gestionar Solicitudes</button>
        <button on:click={() => goto('/visitor/solicitudes')}>Ver Solicitudes</button>
      {/if}
      {#if $userRole === 'visitor'}
        <button on:click={() => goto('/visitor/solicitudes')}>Solicitudes</button>
      {/if}
      <button on:click={logout} class="logout">Cerrar sesión</button>
    {:else}
      <button on:click={() => goto('/login')}>Inicio de Sesión</button>
      <button on:click={() => goto('/registroUser')}>Registro</button>
    {/if}
  </div>
</header>
