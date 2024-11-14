<script>
  import Card from "./card.svelte";
  import axios from "axios";

  let activeButton = null;
  let cards = []; 
  let filteredCards = [];

  // Категории и их идентификаторы
  const categories = {
    GUEST_HOUSES: 1,
    PRIVATE_SECTOR: 2,
    RECREATION_BASES: 3,
    APARTMENTS: 4
  };

  // Устанавливаем активную категорию по умолчанию
  activeButton = categories.GUEST_HOUSES;

  function setActive(buttonNumber) {
    if (activeButton !== buttonNumber) {
      activeButton = buttonNumber;
      filterCardsByCategory(buttonNumber);
    }
  }

  async function fetchObjects() {
    try {
      const response = await axios.get('http://localhost:8000/api/objects/');

      console.log(response.data);
      cards = response.data.map((object) => ({
        city: object.address.city, 
        street: object.address.street, 
        house: object.address.house, 
        seaDistance: object.address.sea_distance, 
        nameObject: object.name, 
        minPrice: object.min_price, 
        type: object.type, 
        images: object.images.length > 0 ? object.images[0].media : null, 
        tags: object.tags.map(tag => tag.title) 
      }));

      console.log(cards);
      filterCardsByCategory(activeButton);
    } catch (error) {
      console.error('Ошибка при получении данных:', error);
    }
  }

  function filterCardsByCategory(categoryId) {
    if (categoryId) {
      filteredCards = cards.filter(card => card.type.id === categoryId);
    } else {
      filteredCards = cards;
    }
  }

  fetchObjects();
</script>

<main>
  <h1 class="animate__animated wow animate__fadeInDown">Объекты с лучшим рейтингом</h1>
  
  <section class="animate__animated wow animate__fadeInDown">
    <button class={activeButton === categories.GUEST_HOUSES ? 'active' : ''} on:click={() => setActive(categories.GUEST_HOUSES)} id="b1">
      Гостевые дома
    </button>

    <button class={activeButton === categories.PRIVATE_SECTOR ? 'active' : ''} on:click={() => setActive(categories.PRIVATE_SECTOR)} id="b2">
      Частный сектор
    </button>

    <button class={activeButton === categories.RECREATION_BASES ? 'active' : ''} on:click={() => setActive(categories.RECREATION_BASES)} id="b3">
      Базы отдыха
    </button>

    <button class={activeButton === categories.APARTMENTS ? 'active' : ''} on:click={() => setActive(categories.APARTMENTS)} id="b4">
      Квартиры посуточно
    </button>
  </section>
  
  <nav>
    {#each filteredCards as card}
      <Card 
        city={card.city} 
        distans={card.seaDistance}
        nameObject={card.nameObject} 
        sale={card.minPrice}
        hrefs={card.images} 
        tegs={card.tags} 
      />
    {/each}
  </nav>

  <div class="block animate__animated wow animate__fadeInUp">
    <a id="more-variants" href="">Смотреть еще 120 вариантов</a>
  </div>
  <br><br>
</main>


<style>
  nav {
    margin-top: 20px;
    display: flex;
    width: clamp(320px, 100%, 1500px);
    flex-wrap: wrap;
    gap: 20px;
  }

  #more-variants {
    background-color: var(--color);
    padding: 9px 19px;
    color: white;
    text-decoration: none;
    border-radius: 10px;
    font-size: 20px;
    transition: 0.3s;
  }

  #more-variants:hover{
    background-color: var(--colorHover);
  }

  .block {
    margin-top: 100px;
    text-align: start;
    width: clamp(320px, 100%, 1300px);
  }

  .active {
    color: var(--color);
  }

  #gorizontal-line {
    width: 100%;
    display: none;
    margin-top: 50px;
  }

  main {
    display: flex;
    justify-content: center;
    flex-direction: column;
    margin: 0 auto;
    width: clamp(320px, 100%, 1500px);
  }

  h1 {
    font-weight: 500;
    font-size: 32px; 
  }

  button {
    background-color: transparent;
    color: #777777;
    border: none;
    cursor: pointer;
    text-wrap: nowrap;
    transition: all 0.3s ease;
    font-size: 20px;
    font-weight: 400;
    line-height: 23.7px;
    text-align: left;
    text-underline-position: from-font;
    text-decoration-skip-ink: none;

  }

  section {
    display: flex;
    margin-top: 30px;
    gap: 20px;
    overflow-x: scroll;
    padding-bottom: 20px;
  }

  section::-webkit-scrollbar {
    height: 4px;    
  }

  section::-webkit-scrollbar-thumb {
    background-color: #77777773; 
    border-radius: 10px; 
  }
  section::-webkit-scrollbar-track {
    background: transparent;
  }

  @media(max-width:716px){
    h1{
      text-align: center;
    }
  }

  @media(max-width:1200px){
    nav{
      align-items: center;
      justify-content: center;
    }
  }
</style>