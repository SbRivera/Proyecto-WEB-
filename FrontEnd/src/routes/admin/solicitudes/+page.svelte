<script lang="ts">
    import axios from 'axios';
    import { onMount } from 'svelte';
  
    interface Participant {
      cedula: string;
      nombre: string;
    }

    interface Application {
      id: string;
      sitio_id: number;
      nombre_sitio: string;
      participants: Participant[];
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
        
        applications = response.data.map((app: any) => ({
          ...app,
          participants: app.participants.map((participant: any) => ({
            cedula: participant.cedula,
            nombre: participant.nombre
          }))
        }));
        
        applications.reverse();

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
    <button class="reset-filter" on:click={resetFilter}>Desfiltrar</button>
  
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
              <li>{participant.cedula} - {participant.nombre}</li>
            {/each}
          </ul>
          {#if !app.estado}
            <button on:click={() => updateStatus(app.grupo_id, 'Aceptado')}>Aceptar</button>
            <button class="reset-filter" on:click={() => updateStatus(app.grupo_id, 'Rechazado')}>Rechazar</button>
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
    .reset-filter {
      background-color: #e74c3c; 
      color: white;
    }

    .reset-filter:hover {
      background-color: #c0392b; 
    }

  </style>
  