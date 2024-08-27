<script lang="ts">
    import axios from 'axios';
    import { onMount } from 'svelte';
    import { usuario } from '$lib/stores';

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
        estado: string;
    }

    let applications: Application[] = [];
    let localUsername = '';

    usuario.subscribe(value => {
        localUsername = value;
    });

    onMount(async () => {
        await fetchUserApplications();
    });

    async function fetchUserApplications() {
        try {
            const response = await axios.get(`http://localhost:8000/aplicaciones/${localUsername}`);
            applications = response.data;
            applications.reverse();

        } catch (error) {
            console.error('Error fetching user applications:', error);
        }
    }
</script>

<main>
    <h1>Mis Solicitudes</h1>
    <div class="applications-container">
        {#each applications as app (app.id)}
            <div class="application">
                <h3 class="site-name">Solicitud para el sitio {app.nombre_sitio}</h3>
                <p><strong>Contacto de emergencia:</strong> {app.contacto_emergencia}</p>
                <p><strong>Fecha de visita:</strong> {app.fecha_visita}</p>
                <p><strong>Tipo de visita:</strong> {app.tipo_visita}</p>
                <p><strong>Participantes:</strong></p>
                <ul>
                    {#each app.participants as participant}
                        <li>{participant.cedula} - {participant.nombre}</li>
                    {/each}
                </ul>
                <p><strong>Estado:</strong> {app.estado}</p>
            </div>
        {/each}
    </div>
</main>

<style>
    main {
        padding: 1rem;
        max-width: 900px;
        margin: auto;
    }

    .applications-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .application {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        background-color: #f9f9f9;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .application:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }

    .site-name {
        color: #007bff;
    }

    p {
        margin: 0.5rem 0;
        font-size: 1rem;
        color: #333;
    }
</style>
