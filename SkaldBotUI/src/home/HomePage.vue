<template>
    <div>
        <div class="image">
        </div>
    </div>
</template>

<script>
    export default {
        name: "HomePage"
    }
</script>

<style scoped>
    .image {
        width: 100%;
        height: 100%;
        min-height: 600px;
        background: url(../assets/SbBackground.jpg) no-repeat center center fixed;
        -webkit-background-size: cover;
        -moz-background-size: cover;
        -o-background-size: cover;
        background-size: cover;
        filter: drop-shadow(5px 10px 4px #060c1c);
        color: white;
    }
</style>