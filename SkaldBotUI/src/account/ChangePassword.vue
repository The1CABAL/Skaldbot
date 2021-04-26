<template>
    <div id="ChangePassword">
        <Form v-if="!initializing" :formKey="formKey" :passedModel="model" @PasswordSuccess="close" @close="close" showCloseButton />
    </div>
</template>

<script>
    import VueLoading from '../components/VueLoading';
    import Form from '../components/Forms/Form';
    import Vue from 'vue'

    export default {
        name: "ChangePassword",
        components: {
            VueLoading,
            Form
        },

        beforeMount() {
            this.initializing = true;
        },

        mounted() {
            this.assignUserId();
            this.initializing = false;
        },

        data() {
            return {
                initializing: true,
                formKey: 'UpdatePassword',
                model: {
                    userId: '',
                }
            }
        },

        methods: {
            assignUserId() {
                Vue.set(this.model, 'userId', this.$store.getters.userId);
            },

            close() {
                this.$emit('close');
            },
        }
    }
</script>

<style scoped>
</style>