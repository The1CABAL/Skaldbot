<template>
    <div id="app" class="bg-primary text-white">
        <div v-if="!loading">
            <nav-bar />
            <header>
                <div class="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
                    <h1 class="text-2xl font-bold border-b-2 border-gray-200 pb-2">
                        {{currentPage}}
                    </h1>
                </div>
            </header>
            <main>
                <div class="max-w-7xl mx-auto py-3 sm:px-6 lg:px-8 min-h-screen h-full">
                    <router-view />
                </div>
            </main>

        </div>
    </div>
</template>

<script>
    import navBar from './components/Nav/navBar.vue';
    import PageMixin from '@/mixins/page-mixin.js'
    import fieldButton from '@/components/CustomFields/fieldButton'
    export default {
        name: "app",

        data() {
            return {
                currentPage: 'Home'
            }
        },

        mixins: [PageMixin],

        components: {
            'nav-bar': navBar,
            'vue-button': fieldButton
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
            }
        }
    }
</script>