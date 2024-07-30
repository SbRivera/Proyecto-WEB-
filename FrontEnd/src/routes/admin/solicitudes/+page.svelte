<script lang="ts">
    import axios from 'axios';
    import { onMount } from 'svelte';
  
    interface Application {
      id: string;
      sitio_id: number;
      nombre_sitio: string;
      participants: string[];
      contacto_emergencia: string;
      fecha_visita: string;
      tipo_visita: string;
      grupo_id: string;
      estado?: string;
    }

    let applications: Application[] = [];
    let filteredApplications: Application[] = [];
    let selectedDate = '';
  
    onMount(async () => {
      await fetchApplications();
    });
  
    async function fetchApplications() {
      try {
        const response = await axios.get('http://localhost:8000/aplicaciones');
        console.log('Fetched applications:', response.data);
        applications = response.data;
        filteredApplications = applications; 
      } catch (error) {
        console.error('Error fetching applications:', error);
      }
    }
  
    function filterApplications() {
      if (selectedDate) {
        filteredApplications = applications.filter(app => app.fecha_visita === selectedDate);
      } else {
        filteredApplications = applications;
      }
    }
  
    function resetFilter() {
      filteredApplications = applications;
      selectedDate = '';
    }
  
    async function updateStatus(grupo_id: string, estado: string) {
      try {
        console.log("Sending update request with group_id:", grupo_id);
        console.log("Status:", estado);
        await axios.put('http://localhost:8000/aplicaciones/estado', { grupo_id, estado });
        applications = applications.map(app => app.grupo_id === grupo_id ? { ...app, estado } : app);
        filterApplications();
      } catch (error) {
        console.error('Error updating status:', error);
      }
    }
  </script>
  
  <main>
    <h1>Solicitudes</h1>
    <label for="filterDate">Filtrar por fecha:</label>
    <input type="date" id="filterDate" bind:value={selectedDate} />
    <button on:click={filterApplications}>Filtrar</button>
    <button on:click={resetFilter}>Desfiltrar</button>
  
    <div>
      {#each filteredApplications as app (app.id)}
        <div class="application">
          <h3>Solicitud para el sitio {app.nombre_sitio}</h3>
          <p>Contacto de emergencia: {app.contacto_emergencia}</p>
          <p>Fecha de visita: {app.fecha_visita}</p>
          <p>Tipo de visita: {app.tipo_visita}</p>
          <p>Participantes:</p>
          <ul>
            {#each app.participants as participant}
              <li>{participant}</li>
            {/each}
          </ul>
          {#if !app.estado}
            <button on:click={() => updateStatus(app.grupo_id, 'accepted')}>Aceptar</button>
            <button on:click={() => updateStatus(app.grupo_id, 'rejected')}>Rechazar</button>
          {:else}
            <p>Estado: {app.estado}</p>
          {/if}
        </div>
      {/each}
    </div>
  </main>
  
  <style>
    .application {
      border: 1px solid #ccc;
      padding: 1rem;
      margin: 1rem 0;
    }
    button {
      margin-right: 1rem;
    }
  </style>
  