<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import axios from 'axios';
  import { goto } from '$app/navigation';
  import { isAuthenticated } from '$lib/stores';

  let sitioId: string;
  let datosSitio: {
    titulo: string;
    descripcion: string;
    requisitos: string;
    vestimenta: string;
    restricciones: string;
    disponibilidad: number;
    activo: boolean;
  } = {
    titulo: '',
    descripcion: '',
    requisitos: '',
    vestimenta: '',
    restricciones: '',
    disponibilidad: 0,
    activo: false
  };

  let imagenSitio: string = '';
  let autenticado: boolean;

  $: sitioId = $page.params.id;

  $: isAuthenticated.subscribe(value => {
    autenticado = value;
  });

  onMount(async () => {
    if (sitioId) {
      try {
        const response = await axios.get(`http://localhost:8000/sitio/${sitioId}`);
        datosSitio = response.data;
        setImagenSitio(sitioId);
      } catch (error) {
        console.error("Error al obtener los datos del sitio:", error);
        alert('Error al cargar los datos del sitio');
      }
    } else {
      console.error("El ID del sitio no está establecido");
    }
  });

  function setImagenSitio(id: string) {
    const imagenes: { [key: string]: string } = {
      '1': '/illinizas/img1.jpg',
      '2': '/illinizas/img2.jpg',
      '3': '/illinizas/img3.jpg',
      '4': '/illinizas/img4.jpg',
      '5': '/illinizas/img5.jpg',
      '6': '/illinizas/img6.jpg',
    };
    imagenSitio = imagenes[id] || '/illinizas/ilinisas.png';
  }

  function aplicar() {
    goto(`/apply/${sitioId}`);
  }
</script>

<main>
  <h1 class="site-title">{datosSitio.titulo}</h1>
  <div class="image-container">
    <img src={imagenSitio} alt="Imagen del sitio">
  </div>
  <div class="info-section">
    <h2>Descripción</h2>
    <p>{datosSitio.descripcion}</p>
  </div>
  <div class="info-section">
    <h2>Requisitos</h2>
    <p>{datosSitio.requisitos}</p>
  </div>
  <div class="info-section">
    <h2>Vestimenta</h2>
    <p>{datosSitio.vestimenta}</p>
  </div>
  <div class="info-section">
    <h2>Restricciones</h2>
    <p>{datosSitio.restricciones}</p>
  </div>
  <div class="info-section">
    <h2>Disponibilidad</h2>
    <p>Disponible: {datosSitio.disponibilidad}</p>
  </div>
  <button on:click={aplicar} disabled={!datosSitio.activo || !autenticado}>Llenar solicitud</button>
</main>

<style>
  main {
    max-width: 800px;
    margin: auto;
    padding: 1rem;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .site-title {
    color: #007bff;
    font-size: 2rem;
    margin-bottom: 1rem;
  }

  .image-container {
    margin-bottom: 1.5rem;
  }

  img {
    width: 100%;
    height: auto;
    border-radius: 8px;
    border: 1px solid #ddd;
  }

  .info-section {
    margin-bottom: 1.5rem;
    padding: 1rem;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }

  h2 {
    color: #333;
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
  }

  p {
    color: #666;
    line-height: 1.6;
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

  button:disabled {
    background-color: #d3d3d3;
    cursor: not-allowed;
  }

  button:hover:enabled {
    background-color: #0056b3;
    transform: translateY(-2px);
  }
</style>
