<script lang="ts">
  import axios from 'axios';
  import { onMount } from 'svelte';
  import { usuario } from '$lib/stores';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';

  interface Participante {
    id: string;
    nombre_completo: string;
  }

  let participantes: Participante[] = [];
  let contacto_emergencia = '';
  let fecha_visita = '';
  let tipo_visita = '';
  let id_sitio = '';
  let cedula_identidad_input = '';
  let nombre_usuario_local = '';
  let errorMessage = '';

  $: {
    id_sitio = $page.params.id;
  }

  usuario.subscribe(value => {
    nombre_usuario_local = value;
  });

  onMount(async () => {
    if (!nombre_usuario_local) {
      console.error('El nombre de usuario no está establecido');
      alert('El nombre de usuario no está establecido.');
      return;
    }

    try {
      const response = await axios.get(`http://localhost:8000/info/${nombre_usuario_local}`);
      participantes.push({
        id: response.data.identity_card,
        nombre_completo: response.data.full_name
      });
      participantes = [...participantes];
    } catch (error) {
      console.error('Error al cargar datos del usuario:', error);
      alert('Error al cargar los datos del usuario.');
    }
  });

  function esFechaVisitaValida(fecha: string): boolean {
    const fechaSeleccionada = new Date(fecha);
    const fechaActual = new Date();
    fechaActual.setDate(fechaActual.getDate() + 7);
    return fechaSeleccionada >= fechaActual;
  }

  function agregarParticipante() {
    if (!cedula_identidad_input.match(/^\d{10}$/)) {
      errorMessage = 'La cédula debe tener 10 dígitos';
      return;
    }

    axios.get(`http://localhost:8000/cedula/${cedula_identidad_input}`)
      .then(response => {
        if (participantes.find(p => p.id === cedula_identidad_input)) {
          errorMessage = 'El participante ya está en la lista';
          return;
        }

        participantes = [
          ...participantes,
          {
            id: cedula_identidad_input,
            nombre_completo: response.data.full_name
          }
        ];
        cedula_identidad_input = '';
        errorMessage = '';
      })
      .catch(() => {
        errorMessage = 'Persona no encontrada';
      });
  }

  function eliminarParticipante(index: number) {
    participantes.splice(index, 1);
    participantes = [...participantes];
  }

  async function enviarSolicitud() {
    errorMessage = '';

    if (!contacto_emergencia.match(/^\d{10}$/)) {
      errorMessage = 'El contacto de emergencia debe tener 10 dígitos';
      return;
    }

    if (!esFechaVisitaValida(fecha_visita)) {
      errorMessage = 'La fecha de visita debe ser al menos una semana después de la fecha actual';
      return;
    }

    try {
      await axios.post('http://localhost:8000/aplicaciones', {
        sitio_id: parseInt(id_sitio),
        participant_ids: participantes.map(p => p.id),
        contacto_emergencia,
        fecha_visita,
        tipo_visita,
      });
      alert('Solicitud enviada con éxito');
      goto('/');
    } catch (error) {
      console.error("Error al enviar la solicitud:", error);
      errorMessage = 'Error al enviar la solicitud';
    }
  }
</script>

<main>
  <h1>Datos del visitante</h1>
  <form on:submit|preventDefault={enviarSolicitud}>
    <label for="cedula_identidad">Participantes:</label>
    <div>
      <input type="text" id="cedula_identidad" bind:value={cedula_identidad_input} />
      <button type="button" on:click={agregarParticipante}>Agregar</button>
    </div>
    
    {#if errorMessage}
      <p class="error">{errorMessage}</p>
    {/if}
    
    <ul>
      {#each participantes as participante, index}
        <li>
          {participante.nombre_completo} - Cédula: {participante.id}
          <button type="button" on:click={() => eliminarParticipante(index)}>Eliminar</button>
        </li>
      {/each}
    </ul>
    
    <label for="fecha_visita">Fecha de visita:</label>
    <input type="date" id="fecha_visita" bind:value={fecha_visita} />
    
    <h3>Tipo de visita:</h3>
    <div>
      <input type="radio" id="tipo_visita_particular" name="tipo_visita" value="particular" bind:group={tipo_visita} />
      <label for="tipo_visita_particular">Particular</label>
    </div>
    <div>
      <input type="radio" id="tipo_visita_grupo" name="tipo_visita" value="grupo organizado" bind:group={tipo_visita} />
      <label for="tipo_visita_grupo">Grupo Organizado</label>
    </div>
    <div>
      <input type="radio" id="tipo_visita_operadoras" name="tipo_visita" value="operadoras" bind:group={tipo_visita} />
      <label for="tipo_visita_operadoras">Operadoras</label>
    </div>
    
    <label for="contacto_emergencia">Contacto de emergencia:</label>
    <input type="text" id="contacto_emergencia" bind:value={contacto_emergencia} />
    
    <button type="submit">Enviar Solicitud</button>
  </form>
</main>

<style>
  main {
    max-width: 800px;
    margin: auto;
    padding: 1rem;
    background-color: #f9f9f9;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
  h1 {
    font-size: 2rem;
    color: #2c3e50;
    text-align: center;
    margin-bottom: 1.5rem;
  }
  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: bold;
    color: #34495e;
  }
  input[type="text"], input[type="date"] {
    width: calc(100% - 1rem);
    margin-bottom: 1rem;
    padding: 0.75rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 1rem;
  }
  button {
    display: block;
    width: 100%;
    padding: 0.75rem;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  button:hover {
    background-color: #2980b9;
  }
  ul {
    list-style-type: none;
    padding: 0;
    margin-bottom: 1rem;
  }
  li {
    margin-bottom: 0.75rem;
    padding: 0.75rem;
    background-color: #ecf0f1;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  li button {
    background-color: #e74c3c;
    margin-left: 1rem;
  }
  li button:hover {
    background-color: #c0392b;
  }
  .error {
    color: red;
    font-size: 0.875rem;
    margin-bottom: 1rem;
    text-align: center;
  }
  div {
    margin-bottom: 1rem;
  }
  h3 {
    color: #2c3e50;
    margin-bottom: 0.5rem;
  }
</style>
