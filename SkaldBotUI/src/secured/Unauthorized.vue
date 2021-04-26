<template>
    <div id="unauthorized" class="wrapper">
        <p class="centerText">You do not have permission to view this page.</p>
    </div>
</template>

<script>
    import PageMixin from '@/mixins/page-mixin'

    export default {
        name: "unauthorized",

        mixins: [PageMixin],

        beforeMount() {
            this.pageMounting();
        },

        mounted() {
            this.pageMounted().then(() => {
                this.pageReady();
            })
        }
    }
</script>

<style scoped>
</style>