<script lang="ts">
  import axios, { AxiosError } from 'axios';
  import { goto } from '$app/navigation';
  import { userRole, isAuthenticated, usuario } from '$lib/stores';

  let nombre_usuario = '';
  let contrasena = '';
  let errorMessage = '';

  async function iniciarSesion() {
    errorMessage = '';
    try {
      const response = await axios.post('http://localhost:8000/login', { nombre_usuario, contrasena });
      if (response.data.message === 'Login successful') {
        isAuthenticated.set(true);
        userRole.set(response.data.role);
        usuario.set(nombre_usuario);
        goto('/');
      } else {
        errorMessage = response.data.message || 'Error desconocido';
      }
    } catch (error) {
      if (error instanceof AxiosError) {
        errorMessage = error.response?.data?.detail || 'Error desconocido';
      } else {
        errorMessage = 'Error desconocido';
      }
    }
  }
</script>

<main>
  <h1>Inicio de Sesión</h1>
  <form on:submit|preventDefault={iniciarSesion}>
    <div class="form-group">
      <label for="nombre_usuario">Nombre de Usuario:</label>
      <input type="text" id="nombre_usuario" bind:value={nombre_usuario} required>
    </div>
    
    <div class="form-group">
      <label for="contrasena">Contraseña:</label>
      <input type="password" id="contrasena" bind:value={contrasena} required>
    </div>
    
    {#if errorMessage}
      <p class="error">{errorMessage}</p>
    {/if}
    
    <button type="submit">Iniciar Sesión</button>
  </form>
</main>

<style>
  main {
    max-width: 400px;
    margin: auto;
    padding: 1.5rem;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  h1 {
    color: #007bff;
    font-size: 1.5rem;
    margin-bottom: 1rem;
    text-align: center;
  }

  .form-group {
    margin-bottom: 1rem;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: bold;
    color: #333;
  }

  input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
  }

  button {
    display: block;
    width: 100%;
    padding: 0.75rem;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.3s ease, transform 0.3s ease;
  }

  button:hover {
    background-color: #0056b3;
    transform: translateY(-2px);
  }

  .error {
    color: red;
    font-size: 0.875rem;
    margin-top: 0.5rem;
    text-align: center;
  }
</style>
