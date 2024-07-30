<script lang="ts">
  import axios, { AxiosError } from 'axios';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { usuario } from '$lib/stores';

  let datosUsuario = {
    nombre_usuario: '',
    correo_electronico: '',
    contacto: '',
    discapacidades: '',
    contrasena: ''
  };

  let nombreUsuarioLocal = '';

  usuario.subscribe(value => {
    nombreUsuarioLocal = value;
    datosUsuario.nombre_usuario = value;
  });

  onMount(async () => {
    if (!nombreUsuarioLocal) {
      console.error('El nombre de usuario no está establecido');
      alert('El nombre de usuario no está establecido.');
      return;
    }
    try {
      const response = await axios.get(`http://localhost:8000/usuario/${nombreUsuarioLocal}`);
      datosUsuario = { ...datosUsuario, ...response.data };
    } catch (error) {
      if (error instanceof AxiosError) {
        alert('Error al cargar datos del usuario: ' + (error.response?.data.detail || 'Error desconocido'));
      } else {
        alert('Error al cargar datos del usuario');
      }
    }
  });

  async function actualizarPerfil() {
    if (datosUsuario.contacto && !/^\d{10}$/.test(datosUsuario.contacto)) {
      alert('El contacto debe contener exactamente 10 números.');
      return;
    }

    try {
      const response = await axios.put(`http://localhost:8000/usuario/${nombreUsuarioLocal}`, datosUsuario);
      alert('Perfil actualizado con éxito');

      if (response.data.nuevo_nombre_usuario) {
        usuario.set(response.data.nuevo_nombre_usuario);
      }

      goto('/');
    } catch (error) {
      if (error instanceof AxiosError) {
        alert('Error actualizando el perfil: ' + (error.response?.data.detail || error.message));
      } else {
        alert('Error actualizando el perfil');
      }
    }
  }
</script>

<main>
  <h1>Perfil</h1>
  <form on:submit|preventDefault={actualizarPerfil}>
    <div class="form-group">
      <label for="nombre_usuario">Usuario:</label>
      <input id="nombre_usuario" bind:value={datosUsuario.nombre_usuario} disabled />
    </div>

    <div class="form-group">
      <label for="correo_electronico">Correo Electrónico:</label>
      <input id="correo_electronico" type="email" bind:value={datosUsuario.correo_electronico} />
    </div>

    <div class="form-group">
      <label for="contacto">Contacto:</label>
      <input id="contacto" type="text" bind:value={datosUsuario.contacto} />
    </div>

    <div class="form-group">
      <label for="discapacidades">Discapacidades:</label>
      <textarea id="discapacidades" bind:value={datosUsuario.discapacidades} rows="4"></textarea>
    </div>

    <div class="form-group">
      <label for="contrasena">Nueva Contraseña:</label>
      <input id="contrasena" type="password" bind:value={datosUsuario.contrasena} />
    </div>

    <button type="submit">Actualizar</button>
  </form>
</main>

<style>
  main {
    max-width: 800px;
    margin: auto;
    padding: 1.5rem;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  h1 {
    color: #007bff;
    font-size: 2rem;
    margin-bottom: 1.5rem;
    text-align: center;
  }

  .form-group {
    margin-bottom: 1.5rem;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: bold;
    color: #333;
  }

  input, textarea {
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

</style>
