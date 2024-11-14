<script>
    import { onMount } from 'svelte';
    import { useLocation } from 'svelte-routing';
    import SearchInput from './Routing_lib/searchInput.svelte';
    import Header from '../Header.svelte';
    import { navigate } from 'svelte-routing';
    import Page from './page.svelte';
    import axios from 'axios';
    import Object from './Profile/object.svelte';

    let city = '';
    let adults = '';
    let first_day = '';
    let last_day = '';
    let kids = '';
    let apartments = [];
    let filteredApartments = []; // Переменная для отфильтрованных квартир
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
            const fetchedApartments = await Promise.all(response.data.map(async (object) => {
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
                    tags: object.tags.map(tag => tag.title)
                };
            }));

            console.log(apartments, "lfff")

            apartments = fetchedApartments;
            filteredApartments = apartments; // Изначально все квартиры отображаются
        } catch (error) {
            console.error('Ошибка при получении данных:', error);
        }
    }

    // Обновление отфильтрованных квартир
    function updateFilteredApartments() {
        if (city) {
            filteredApartments = apartments.filter(apartment => apartment.city === city);
        } else {
            filteredApartments = apartments; // Если город не выбран, возвращаем все квартиры
        }
    }

    console.log(filteredApartments)

    onMount(async () => {
        const params = new URLSearchParams(window.location.search);

        city = params.get('city') || '';
        adults = params.get('adults') || '';
        first_day = params.get('first_day') || '';
        last_day = params.get('last_day') || '';
        kids = params.get('kids') || '';

        await fetchObjects();
        updateFilteredApartments(); // Обновляем отфильтрованные квартиры
    });

    function correctName(city) {
        if (city === "Саратов" || city === "Екатеринбург" || city === "Санкт-Петербург") {
            city += "e";
        }
        return city;
    }
</script>

<main>
    <Header toNavigate={toNavigate} />
    <div class="block">
        <nav>
            <a href="" on:click={goHome} id="middle">Главная</a> <p> > </p> <p>{city}</p>
        </nav>
        <section>
            <h1>Отдых в {correctName(city)}</h1>
            <SearchInput 
                city={city} 
                adults={adults} 
                first_day={first_day} 
                last_day={last_day} 
                on:search={() => updateFilteredApartments()} 
            />  
        </section>
    </div>

    <div class="block2">
        <div class="blockFilters">
            <h2>Фильтры</h2>
            <label>
                Количество детей:
                <input type="number" bind:value={kids} placeholder="0" />
            </label>
        </div>

        <div class="blockPage">
            <Page {filteredApartments}/>
            <Object {filteredApartments}/>
        </div>
    </div>
</main>

<style>
    .blockPage{
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 30px;
        flex-direction: column;
    }

    .block2{
        padding-top: 20px;
        display: flex;
        justify-content: space-between;
        
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
        background: rgba(9, 18, 121, 0.801);
        background: linear-gradient(90deg, #316bff, #ff1f6b);
        padding: 20px 0px 40px 0px;
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