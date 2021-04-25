<template>
    <div id="app" class="bg-primary text-white">
        <nav-bar v-if="contentReady" />
        <alerts />
        <header v-if="contentReady">
            <div class="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
                <h1 class="text-2xl font-bold border-b-2 border-gray-200 pb-2">
                    {{currentPage}}
                </h1>
            </div>
        </header>
        <main>
            <div class="max-w-7xl mx-auto py-3 sm:px-6 lg:px-8">
                <div class="flex justify-center items-center h-screen" v-if="!contentReady">
                    <div class="text-center text-2xl">
                        <loader size="large" />
                    </div>
                </div>
                <div class="min-h-screen h-full">
                    <router-view v-show="contentReady" />
                </div>
            </div>
        </main>
    </div>
</template>

<script>
    import navBar from './components/Nav/navBar.vue';
    import PageMixin from '@/mixins/page-mixin.js'
    import VueLoading from '@/components/VueLoading'
    import VueAlerts from '@/components/Alerts/VueAlerts'

    export default {
        name: "app",

        data() {
            return {
                currentPage: 'Home',
                contentReady: false
            }
        },

        mixins: [PageMixin],

        components: {
            'nav-bar': navBar,
            'loader': VueLoading,
            'alerts': VueAlerts
        },

        mounted() {
            this.currentPage = this.$route.name.toUpperCase();
        },

        created: function () {
            this.$http.interceptors.response.use(undefined, function (err) {
                return new Promise(function (resolve, reject) {
                    if (err.status == 401 && err.config && !err.config__isRetryRequest) {
                        this.$store.dispatch(logout)
                    }
                    throw err;
                });
            });
        },

        watch: {
            '$route.name'(newVal, oldVal) {
                if (newVal !== oldVal) {
                    this.currentPage = newVal.toUpperCase();
                }
            },
            '$store.state.page.loading'(newVal, oldVal) {
                if (newVal !== oldVal) {
                    this.contentReady = !newVal;
                }
            }
        }
    }
</script>