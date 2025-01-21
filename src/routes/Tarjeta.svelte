<script>
  export let imagen;
  export let descripcion;
</script>
  
<style>
  .tarjeta {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    margin: 1rem;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  .tarjeta:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  }
  .tarjeta img {
    max-width: 100%;
    border-bottom: 1px solid #ddd;
    padding-bottom: 1rem;
    border-radius: 10px 10px 0 0;
  }
  .tarjeta p {
    margin-top: 1rem;
    font-size: 1.1rem;
    color: #2c3e50;
  }
</style>
  
<div class="tarjeta">
  <img src={imagen} alt="Imagen del sitio">
  <p>{descripcion}</p>
</div>
