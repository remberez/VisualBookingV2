<script>
    import { onMount } from 'svelte';
    import { useLocation } from 'svelte-routing';
    import SearchInput from './Routing_lib/searchInput.svelte';
    import Header from '../Header.svelte';
    import { navigate } from 'svelte-routing';
    import axios from 'axios';
    import Object from './Profile/object.svelte';
    import Search from './Main/search.svelte';

    let city = '';
    let adults = '';
    let first_day = '';
    let last_day = '';
    let kids = '';
    let apartments = [];
    let filteredApartments = [];
    let toNavigate = true;

    const location = useLocation();

    async function goHome() {
        navigate(`/`);
    }

    async function fetchCityName(cityId) {
        try {
            const response = await axios.get(`http://localhost:8000/api/city/${cityId}/`);
            return response.data.name; 
        } catch (error) {
            console.error('Ошибка при получении названия города:', error);
            return null; 
        }
    }

    async function fetchObjects() {
        try {
            const response = await axios.get('http://localhost:8000/api/objects/');
            apartments = await Promise.all(response.data.map(async (object) => {
                const cityName = await fetchCityName(object.address.city);
                return {
                    id: object.id,
                    city: cityName || object.address.city,
                    street: object.address.street,
                    house: object.address.house,
                    seaDistance: object.address.sea_distance,
                    title: object.name,
                    description: object.description || "Нет описания",
                    minPrice: object.min_price,
                    type: object.type,
                    images: object.images.length > 0 ? object.images.map(image => image.media) : [],
                    tags: object.tags.map(tag => tag.title),
                };
            }));
            filteredApartments = apartments; // Изначально все квартиры отображаются
        } catch (error) {
            console.error('Ошибка при получении данных:', error);
        }
    }

    function updateFilteredApartments() {
        filteredApartments = apartments.filter(apartment => apartment.city === city);
        if (activeTab === "nerdeSea") {
            filteredApartments.sort((a, b) => a.seaDistance - b.seaDistance);
        }
    }

    onMount(async () => {
        const params = new URLSearchParams(window.location.search);
        city = params.get('city') || '';
        adults = params.get('adults') || '';
        first_day = params.get('first_day') || '';
        last_day = params.get('last_day') || '';
        kids = params.get('kids') || '';

        await fetchObjects();
        updateFilteredApartments();
    });

    let activeTab = "popular";
    let one, two, three;

    const switchTab = (tab) => {
        activeTab = tab;

        one.style.textDecoration = "none";
        two.style.textDecoration = "none";
        three.style.textDecoration = "none";

        if (activeTab === "popular") one.style.textDecoration = "underline";
        if (activeTab === "raiting") two.style.textDecoration = "underline";
        if (activeTab === "nerdeSea") {
            three.style.textDecoration = "underline";
            updateFilteredApartments(); // Обновляем отфильтрованные квартиры при переключении на "ближе к морю"
        }
    };
</script>

<main>
    <Header toNavigate={toNavigate} />
    <div class="block">
        <nav>
            <a href="" on:click={goHome} id="middle">Главная</a> <p> > </p> <p>{city}</p>
        </nav>
        <section>
            <Search
                city={city}
                adults={adults}
                checkInDate={first_day}
                checkOutDate={last_day}
                on:search={() => updateFilteredApartments()} 
            />
        </section>
    </div>

    <div class="block2">
        <div class="blockFilters">
            asads
        </div>

        <div class="blockPage">
            <div class="info">
                <p>Найдено {filteredApartments.length} варианта жилья</p>

                <div class="sort">
                    <a bind:this={one} on:click={() => { switchTab("popular"); updateFilteredApartments(); }}>По популярности</a>
                    <a bind:this={two} on:click={() => { switchTab("raiting"); updateFilteredApartments(); }}>По рейтингу</a>
                    <a bind:this={three} on:click={() => { switchTab("nerdeSea"); updateFilteredApartments(); }}>Ближе к морю</a>
                </div>
            </div>
            <div>
                <div class="blockObjects">
                    {#each filteredApartments as apartment}
                        <Object {apartment} /> 
                    {/each}
                </div>
            </div>
        </div>
    </div>
</main>

<style>
    .blockObjects{
        display: flex;
        flex-direction: column;
        gap: 30px;
    }

    .blockPage{
        display: flex;
        max-width: 817px;
        gap: 30px;
        flex-grow: 1;
        flex-direction: column;
        background: #F5F5F5;
        padding: 25px;
        border: 2px rgba(128, 128, 128, 0.315) solid;
        border-radius: 15px;
    }

    .info{
        display: flex;
        justify-content: space-between;
        color: #959595;
        font-size: 14px;
        font-weight: 300;
        line-height: 16.59px;
    }

    .sort{
        display: flex;
        justify-content: space-between;
        gap: 10px;  
    }

    .block2{
        padding-top: 20px;
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        flex-grow: 1;
        margin: 0 auto;
        width:100%;
    }

    .block{
        margin-top: 50px;
    }
    
    nav{
        display: flex;
        gap: 10px;
        width: 90%;

        padding: 20px 0 20px 5px;
    }

    nav a{
        text-decoration: none;
        color: black;
        transition: all 0.3s ease 0s;
        cursor: cell;
    }

    nav #middle:hover{
        transform: scale(1.2);
        color: gray;
        cursor: pointer;
    }

    section h1{
        color: white;
        font-size: clamp(30px,2vw,50px);
        margin-bottom: 30px;
    }

    section{
        width: 100%;
        background: var(--color);
        padding: 20px 0px 20px 0px;
        margin: 0 auto;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        border-radius: 20px;
    }

    @media(max-width:1498px){
        section{
            border-radius: 0px;
        }
    }
</style>