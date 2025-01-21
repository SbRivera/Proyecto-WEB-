<script lang="ts">
  import Tarjeta from './Tarjeta.svelte';
  import { onMount } from 'svelte';
  import axios from 'axios';

  interface Sitio {
    id: number;
    imagen: string;
    descripcion: string;
    activo: boolean;
  }

  let sitios: Sitio[] = [
    { id: 1, imagen: '/illinizas/img1.jpg', descripcion: '', activo: false },
    { id: 2, imagen: '/illinizas/img2.jpg', descripcion: '', activo: false },
    { id: 3, imagen: '/illinizas/img3.jpg', descripcion: '', activo: false },
    { id: 4, imagen: '/illinizas/img4.jpg', descripcion: '', activo: false },
    { id: 5, imagen: '/illinizas/img5.jpg', descripcion: '', activo: false },
    { id: 6, imagen: '/illinizas/img6.jpg', descripcion: '', activo: false },
  ];

  onMount(async () => {
    try {
      const response = await axios.get('http://localhost:8000/sitios');
      const datosSitios: Array<{ id: number; descripcion: string; activo: boolean }> = response.data;
      sitios = sitios.map(sitio => {
        const datosSitio = datosSitios.find(s => s.id === sitio.id);
        return { ...sitio, descripcion: datosSitio ? datosSitio.descripcion : sitio.descripcion, activo: datosSitio ? datosSitio.activo : sitio.activo };
      });
    } catch (error) {
      console.error("Error al obtener los datos de los sitios:", error);
      alert('Error al cargar los datos de los sitios');
    }
  });
</script>

<style>
  .tarjetas {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1rem;
    padding: 1rem;
    background-color: #eaf0f1;
  }
  .tarjetas a {
    text-decoration: none;
    color: inherit;
  }
  .tarjetas a:hover .tarjeta {
    transform: scale(1.05);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  }
</style>

<main>
  <div class="tarjetas">
    {#each sitios as sitio}
      <a href={`/sitio/${sitio.id}`}>
        <Tarjeta imagen={sitio.imagen} descripcion={sitio.descripcion} />
      </a>
    {/each}
  </div>
</main>
