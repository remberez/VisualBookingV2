<script>
    import { onMount } from 'svelte';
    import { addToFavorites } from '../scripts/favorites'; 
    import Cookies from 'js-cookie';
    import axios from "axios";
    import imghg from '../../../assets/main-photo.png';
    import like from '../../../assets/like.png';

    export let filteredApartments; 
    let isLoggedIn = false;
    let objectTypeName = 'Тип объекта'; // По умолчанию

    async function addToFavoritesHandler(apartment) {
        if (isLoggedIn) {
            try {
                const response = await axios.get(`/api/objects/${apartment.id}/add_to_favorites/`);
                console.log('Добавлено в избранное:', response.data);
            } catch (error) {
                console.error('Ошибка при добавлении в избранное:', error.response ? error.response.data : error.message);
            }
        } else {
            addToFavorites(apartment.id);
            console.log('Сохранено в куки:', apartment.id);
        }
    }

    async function fetchObjectTypeDetails(typeId) {
        try {
            const response = await axios.get(`http://localhost:8000/api/types-of-objects/${typeId}/`);
            objectTypeName = response.data.name; // Сохраняем название типа объекта
            console.log('Данные о типе объекта:', objectTypeName);
        } catch (error) {
            console.error('Ошибка при получении данных о типе объекта:', error.response ? error.response.data : error.message);
        }
    }

    onMount(() => {
        isLoggedIn = !!Cookies.get('token'); 

        if (filteredApartments.length > 0) {
            const typeId = filteredApartments[0].type; // Получаем индекс типа объекта
            fetchObjectTypeDetails(typeId); // Вызываем функцию для получения данных о типе объекта
        }
    });
</script>

<main>
    <div class="photo">
        <img id="middlePhoto" src="{filteredApartments.length > 0 ? filteredApartments[0].images[0] : imghg}" alt="">
    </div>

    <div class="info">
        <div class="blockInfo">
            <div class="nameAdress">
                <h1>
                    {objectTypeName} «{filteredApartments.length > 0 ? filteredApartments[0].title : 'Название объекта'}»
                </h1>
                <p>
                    {filteredApartments.length > 0 ? filteredApartments[0].city : 'Город'}
                    {filteredApartments.length > 0 ? filteredApartments[0].street : 'Адрес'}
                </p>
            </div>
            <img id="like" on:click={() => addToFavoritesHandler(filteredApartments[0])} src="{like}" alt="">
        </div>

        <div class="tags">
            теги
        </div>
    </div>

    <div class="price">
        <h1>От {filteredApartments.length > 0 ? filteredApartments[0].minPrice : 'цена'} руб</h1>
        <p>цена за сутки</p>
    </div>
</main>
<style>
    .price{
        display: flex;
        align-items: center;
        flex-direction: column;
    }

    .info{
        max-width: 300px;
        flex-grow: 1;
        margin-top: 20px;
        margin-bottom: 20px;
        padding-right: 10px;
        border-right: 2px rgba(128, 128, 128, 0.315) solid;
    }

    .blockInfo{
        display: flex;
        width: 100%;
        justify-content: space-between;
        flex-grow: 1;
    }

    .nameAdress h1{
        font-size: 18px;
        font-weight: 400;
        line-height: 21.33px;
        padding-bottom: 10px;
    }

    .nameAdress p{
        font-size: 12px;
        font-weight: 300;
        line-height: 14.22px;
        text-decoration-style: solid;
        text-underline-position: from-font;
        text-decoration-skip-ink: auto;
    }

    main{
        max-width: 768px;
        height: auto;
        border: 1px rgba(128, 128, 128, 0.315) solid;
        border-radius: 10px;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 10px;
    }

    .photo {
        width: 262px; 
        height: 243px;
        overflow: hidden; 
    }

    #like{
        width: 30px;
        height: 27px;
    }

    #middlePhoto{
        width: 100%; 
        height: 100%; 
        border-radius: 10px;
        object-fit: cover; 
    }
</style>