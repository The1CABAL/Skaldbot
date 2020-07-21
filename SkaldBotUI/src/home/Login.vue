<template>
    <div id="login">
        <Form v-if="formKey != ''" :formKey="formKey" @LoginSuccess="login"/>
    </div>
</template>

<script>
    import Form from '../components/Forms/Form';
    export default {
        name: 'Login',
        components: {
            Form
        },
        data() {
            return {
                formKey: 'LoginForm'
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
</style>