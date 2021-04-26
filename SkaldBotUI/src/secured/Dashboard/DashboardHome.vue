<template>
    <div id="DashboardHome" class="h-full overflow-x-auto">
        <p>Welcome to the admin dashboard. Select one of the options in the navigation pane to the left to start managing the application!</p>
    </div>
</template>

<script>
    import PageMixin from '@/mixins/page-mixin'

    export default {
        name: "DashboardHome",

        mixins: [PageMixin],

        beforeMount() {
            this.pageMounting();
        },

        mounted() {
            this.pageMounted().then(() => {
                if (!this.masterAdmin && !this.admin) {
                    this.redirectUser('/unauthorized');
                    return;
                }

                this.pageReady();
            });
        }
    }
</script>

<style scoped>
</style>