<template>
    <div class="h-full">
        <img class="w-full" :src="background" alt="Skaldbot Home Background">
    </div>
</template>

<script>
    export default {
        name: "HomePage",

        data() {
            return {
                background: require('@/assets/SbBackground.jpg'),
            }
        }
    }
</script>

<style scoped>
</style>