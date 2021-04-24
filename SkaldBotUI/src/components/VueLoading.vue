<template>
    <div class="flex flex-1 justify-center py-3">
        <svg class="animate-spin -ml-1 mr-3 text-hover" :class="spinnerSize" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
    </div>
</template>

<script>
    export default {
        name: "vue-loading",

        props: {
            size: {
                type: String,
                default: 'small'
            }
        },


        data() {
            return {
                loader: require('@/assets/loading.gif')
            }
        },

        computed: {
            spinnerSize() {
                const propSize = this.size.toLowerCase();

                if (propSize === 'medium') {
                    return 'h-12 w-12';
                }

                if (propSize === 'large') {
                    return 'h-16 w-16';
                }

                return 'h-5 w-5';
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