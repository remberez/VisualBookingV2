<script>
    import { onMount } from 'svelte';
    import { addToFavorites } from '../scripts/favorites'; 
    import Cookies from 'js-cookie';
    import axios from "axios";
    import imghg from '../../../assets/main-photo.png';
    import like from '../../../assets/like.png';

    export let apartment; // Измените пропс на отдельную квартиру
    let isLoggedIn = false;
    let objectTypeName = 'Тип объекта';
    let seaDistance = 0; 

    async function addToFavoritesHandler() {
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
            objectTypeName = response.data.name;
            console.log('Данные о типе объекта:', objectTypeName);
        } catch (error) {
            console.error('Ошибка при получении данных о типе объекта:', error.response ? error.response.data : error.message);
        }
    }

    onMount(() => {
        isLoggedIn = !!Cookies.get('token'); 
        seaDistance = apartment.seaDistance; 
        fetchObjectTypeDetails(apartment.type); 
    });
</script>

{#if apartment}
<main>
    <div class="photo">
        <img id="middlePhoto" src="{apartment.images.length > 0 ? apartment.images[0] : imghg}" alt="">
    </div>

    <div class="info">
        <div class="blockInfo">
            <div class="nameAdress">
                <h1>
                    {objectTypeName} «{apartment.title}»
                </h1>
                <p>
                    {apartment.city}, {apartment.street}
                </p>

                <p>Море - {seaDistance > 999 ? (seaDistance / 1000).toFixed(1) + " км" : seaDistance + " м"}</p>
            </div>
            <img id="like" on:click={addToFavoritesHandler} src="{like}" alt="">
        </div>
        <div class="block">
            <div class="tags">
                <div class="fullTags">
                    {#if apartment.tags.length > 0}
                        {#each apartment.tags.slice(0, 6) as tag}
                            {tag}
                        {/each}
                    {:else}
                        <p>Нет тегов</p>
                    {/if}
                </div>
                <div class="raiting">
                    <p>
                        <span>5.0</span> 33 отзыва
                    </p>  
                </div>
            </div>
        </div>
    </div>

    <div class="price">
        <h1>От { Math.floor(apartment.minPrice) } руб</h1>
        <p>цена за сутки</p>

        <section>
            <button id="blueButton">Подробнее</button>
        </section>
    </div>
</main>
{:else}
    <p>Нет доступных квартир</p>
{/if}
<style>
    .block{
        height: 70%;
        display: flex;
        align-items: end;
    }

    .price h1{
        font-size: 17px;
        font-weight: 400;
        line-height: 20.15px;
        align-self: flex-start;
    }

    .price p{
        font-size: 12px;
        font-weight: 300;
        line-height: 14.22px;
        align-self: flex-start;
    }

    #blueButton{
        width: 102px;
        height: 27px;
        border-radius: 5px;
        background-color: var(--color);
        color: white;
        font-family: Rubik;
        font-size: 12px;
        font-weight: 400;
        line-height: 14.22px;
    }

    section{
        display: flex;
        justify-content: center;
        align-items: end;
        height: 80%;
    }

    .raiting span{
        background: #00C12A;
        font-family: Rubik;
        font-size: 12px;
        font-weight: 300;
        line-height: 14.22px;
        color: white;
        padding: 0 5px 0 5px;
        border-radius: 10px;
    }

    .raiting p{
        font-family: Rubik;
        font-size: 12px;
        font-weight: 300;
        line-height: 14.22px;
    }

    .price{
        display: flex;
        padding: 0 10px 0 10px;
        align-items: center;
        margin: 20px 0 20px 0;
        height: auto;
        flex-direction: column;
        border-left: 2px rgba(128, 128, 128, 0.315) solid;
    }

    .fullTags{
        display: flex;
        gap: 10px;
        font-size: 12px;
        font-weight: 300;
        line-height: 14.22px;
        margin-bottom: 10px;
    }

    .info{
        max-width: 400px;
        flex-grow: 1;
        margin-top: 20px;
        margin-bottom: 20px;
        flex-direction: column;
        height: auto;
        margin-left: 10px;
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