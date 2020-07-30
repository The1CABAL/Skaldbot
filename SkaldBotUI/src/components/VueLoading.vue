<template>
    <div>
        <img :src="loader" alt="loadingGif" class="loadingImg" />
    </div>
</template>

<script>
    export default {
        name: "vue-loading",
        data() {
            return {
                loader: require('@/assets/loading.gif')
            }
        }
    }
</script>

<style scoped>
    .loadingImg {
        display: block;
        margin: 0 auto;
        height: 2%;
        width: 2%;
    }
</style>