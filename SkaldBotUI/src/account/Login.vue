<template>
    <div id="login">
        <div>
            <Form :formKey="formKey" @LoginSuccess="login" />
            <router-link to="/register" class="min-w-32 max-w-xs w-auto pr-2 pl-2 mb-2 p-2 h-32 rounded-md text-white bg-hover hover:bg-secondary">Register</router-link>
        </div>
    </div>
</template>

<script>
    import Form from '../components/Forms/Form';
    import PageMixin from '@/mixins/page-mixin';
    export default {
        name: 'Login',

        components: {
            Form
        },

        mixins: [PageMixin],

        data() {
            return {
                formKey: 'LoginForm'
            }
        },

        beforeMount() {
            this.pageMounting();
        },

        mounted() {
            this.pageMounted().then(() => {
                this.pageReady();
            })
        },

        methods: {
            login() {
                this.redirectUser('/')
            }
        }
    }
</script>