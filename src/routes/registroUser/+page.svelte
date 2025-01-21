<script lang="ts">
  import axios, { AxiosError } from 'axios';
  import { goto } from '$app/navigation';
  
  let nombre_completo: string = '';
  let nombre_usuario: string = '';
  let contrasena: string = '';
  let correo_electronico: string = '';
  let cedula_identidad: string = '';
  let fecha_nacimiento: string = '';
  let contacto: string = '';
  let nacionalidad: string = '';
  let discapacidades: string = '';

  let errors: { [key: string]: string } = {};

  function calcularEdad(fechaNacimiento: string): number {
    const nacimiento = new Date(fechaNacimiento);
    const hoy = new Date();
    let edad = hoy.getFullYear() - nacimiento.getFullYear();
    const diferenciaMeses = hoy.getMonth() - nacimiento.getMonth();
    if (diferenciaMeses < 0 || (diferenciaMeses === 0 && hoy.getDate() < nacimiento.getDate())) {
      edad--;
    }
    return edad;
  }

  async function verificarUnicidad(campo: string, valor: string): Promise<boolean> {
    try {
      const response = await axios.post(`http://localhost:8000/check_unique`, { field: campo, value: valor });
      return response.data.unique;
    } catch (error) {
      console.error("Error verificando unicidad:", error);
      return false;
    }
  }

  async function validar() {
    errors = {};

    if (!/^[a-zA-Z\s]+$/.test(nombre_completo) || nombre_completo.trim().split(' ').length < 2) {
      errors.nombre_completo = 'Nombre completo debe contener solo letras y al menos un espacio.';
    }

    if (nombre_usuario.length < 4) {
      errors.nombre_usuario = 'Usuario debe tener al menos 4 caracteres.';
    } else if (!(await verificarUnicidad('nombre_usuario', nombre_usuario))) {
      errors.nombre_usuario = 'Este nombre de usuario ya está en uso.';
    }

    if (contrasena.length < 4) {
      errors.contrasena = 'Contraseña debe tener al menos 4 caracteres.';
    }

    if (!/^\d{10}$/.test(cedula_identidad)) {
      errors.cedula_identidad = 'Cédula de Identidad debe contener exactamente 10 números.';
    } else if (!(await verificarUnicidad('cedula_identidad', cedula_identidad))) {
      errors.cedula_identidad = 'Esta cédula de identidad ya está en uso.';
    }

    if (calcularEdad(fecha_nacimiento) < 18) {
      errors.fecha_nacimiento = 'Debe tener al menos 18 años.';
    }

    if (!/^\d{10}$/.test(contacto)) {
      errors.contacto = 'Contacto debe contener exactamente 10 números.';
    }

    if (!/^[a-zA-Z\s]+$/.test(nacionalidad)) {
      errors.nacionalidad = 'Nacionalidad debe contener solo letras y espacios.';
    }

    return Object.keys(errors).length === 0;
  }

  async function registrar() {
    if (!await validar()) {
      return;
    }

    try {
      const response = await axios.post('http://localhost:8000/register', {
        nombre_completo,
        nombre_usuario,
        contrasena,
        correo_electronico,
        cedula_identidad,
        fecha_nacimiento,
        contacto,
        nacionalidad,
        discapacidades
      });
      alert(response.data.message);
      goto('/login');
    } catch (error) {
      if (error instanceof AxiosError) {
        alert(error.response?.data?.detail || 'Error desconocido');
      } else {
        alert('Error desconocido');
      }
    }
  }
</script>

<main>
  <h1>Registro</h1>
  <form on:submit|preventDefault={registrar}>
    <div class="form-group">
      <label for="nombre_completo">Nombre Completo:</label>
      <input type="text" id="nombre_completo" bind:value={nombre_completo} required>
      {#if errors.nombre_completo}<p class="error">{errors.nombre_completo}</p>{/if}
    </div>
    
    <div class="form-group">
      <label for="nombre_usuario">Usuario:</label>
      <input type="text" id="nombre_usuario" bind:value={nombre_usuario} required>
      {#if errors.nombre_usuario}<p class="error">{errors.nombre_usuario}</p>{/if}
    </div>
    
    <div class="form-group">
      <label for="contrasena">Contraseña:</label>
      <input type="password" id="contrasena" bind:value={contrasena} required>
      {#if errors.contrasena}<p class="error">{errors.contrasena}</p>{/if}
    </div>
    
    <div class="form-group">
      <label for="correo_electronico">Correo Electrónico:</label>
      <input type="email" id="correo_electronico" bind:value={correo_electronico} required>
    </div>
    
    <div class="form-group">
      <label for="cedula_identidad">Cédula de Identidad:</label>
      <input type="text" id="cedula_identidad" bind:value={cedula_identidad} required>
      {#if errors.cedula_identidad}<p class="error">{errors.cedula_identidad}</p>{/if}
    </div>
    
    <div class="form-group">
      <label for="fecha_nacimiento">Fecha de Nacimiento:</label>
      <input type="date" id="fecha_nacimiento" bind:value={fecha_nacimiento} required>
      {#if errors.fecha_nacimiento}<p class="error">{errors.fecha_nacimiento}</p>{/if}
    </div>

    <div class="form-group">
      <label for="contacto">Contacto:</label>
      <input type="text" id="contacto" bind:value={contacto}>
      {#if errors.contacto}<p class="error">{errors.contacto}</p>{/if}
    </div>
    
    <div class="form-group">
      <label for="nacionalidad">Nacionalidad:</label>
      <input type="text" id="nacionalidad" bind:value={nacionalidad}>
      {#if errors.nacionalidad}<p class="error">{errors.nacionalidad}</p>{/if}
    </div>
    
    <div class="form-group">
      <label for="discapacidades">Discapacidades:</label>
      <textarea id="discapacidades" bind:value={discapacidades} rows="4"></textarea>
    </div>
    
    <button type="submit">Registrarse</button>
  </form>
</main>

<style>
  main {
    max-width: 600px;
    margin: auto;
    padding: 2rem;
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

  .error {
    color: red;
    font-size: 0.875rem;
    margin-top: 0.5rem;
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
