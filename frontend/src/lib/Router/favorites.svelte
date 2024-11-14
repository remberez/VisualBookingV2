<script>
    import { onMount } from 'svelte';
    import { getFavorites, clearFavorites } from './scripts/favorites'; 
    import Cookies from 'js-cookie';
    import axios from "axios";
  
    let favorites = [];
    let isLoggedIn = false;
  
    onMount(() => {
        isLoggedIn = !!Cookies.get('token');
        if (isLoggedIn) {
            fetchFavorites();
        } else {
            favorites = getFavorites();
        }
    });
  
    async function fetchFavorites() {
        try {
            const response = await axios.get('http://localhost:8000/api/objects/1/add_to_favorites/', {
                headers: {
                    Authorization: `Bearer ${Cookies.get('token')}`
                }
            });
            favorites = response.data;
        } catch (error) {
            console.error('Ошибка при получении избранных:', error);
        }
    }
  
    async function removeFavorite(favoriteId) {
        try {
            await axios.delete(`http://localhost:8000/api/favorites/${favoriteId}/`, {
                headers: {
                    Authorization: `Bearer ${Cookies.get('token')}`
                }
            });
            favorites = favorites.filter(favorite => favorite.id !== favoriteId);
        } catch (error) {
            console.error('Ошибка при удалении избранного:', error);
        }
    }
  </script>
  
  {#if favorites.length > 0}
    <h1>Ваши избранные объекты</h1>
    <div class="favorites-container">
        {#each favorites as favorite}
        <div class="favorite-item">
            <img src={favorite.image} alt={favorite.title} />
            <h2>{favorite.title}</h2>
            <p>{favorite.description}</p>
            <p>Цена: {favorite.minPrice} руб. в сутки</p>
            <button on:click={() => removeFavorite(favorite.id)}>Удалить из избранного</button>
        </div>
        {/each}
    </div>
  {:else}
    <p>У вас нет избранных объектов.</p>
  {/if}
  
  <style>
    .favorites-container {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
    }
    .favorite-item {
        border: 1px solid #ccc;
        padding: 10px;
        border-radius: 5px;
        width: calc(33.33% - 20px);
    }
    img {
        max-width: 100%;
        height: auto;
        border-radius: 5px;
    }
  </style>