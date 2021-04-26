<template>
    <div class="h-full">
        <img class="w-full" :src="background" alt="Skaldbot Home Background">
    </div>
</template>

<script>
    import PageMixin from '@/mixins/page-mixin.js';

    export default {
        name: "HomePage",

        mixins: [PageMixin],

        data() {
            return {
                background: require('@/assets/SbBackground.jpg'),
            }
        },

        beforeMount() {
            this.pageMounting();
        },

        mounted() {
            this.pageMounted().then(() => {
                this.pageReady();
            });;

        }
    }
</script>