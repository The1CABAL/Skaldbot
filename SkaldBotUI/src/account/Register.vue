<template>
    <div id="Register">
        <Form v-if="formKey != ''" :formKey="formKey" @RegisterSuccess="login" />
        <router-link to="/login" class="link">Login</router-link>
    </div>
</template>

<script>
    import Form from '../components/Forms/Form';
    export default {
        name: 'Register',
        components: {
            Form
        },
        data() {
            return {
                formKey: 'RegisterForm'
            }
        },
        methods: {
            login() {
                console.log("Logging in...")
                this.$emit("authenticated", true)
            }
        }
    }
</script>

<style scoped>
    .link {
        margin-left: 1%;
        display: inline-block;
        color: #444;
        border: 1px solid #CCC;
        background: #DDD;
        box-shadow: 0 0 5px -1px rgba(0,0,0,0.2);
        cursor: pointer;
        vertical-align: middle;
        max-width: 100px;
        padding: 5px;
        text-align: center;
        text-decoration: none;
    }

        .link:hover {
            background: #B8B8B8;
        }
</style>