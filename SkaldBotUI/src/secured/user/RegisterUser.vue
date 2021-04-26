<template>
    <div id="RegisterUser">
        <vue-button @click="goBack">Go Back</vue-button>
        <Form :formKey="formKey" :accountId="accountId" @RegisterSuccess="alert" />
        <vue-button @click="openHelp" varient="secondary">Help</vue-button>
        <HelpDocumentation v-if="showHelp" :HelpContentKey="helpContentKey" @close="closeHelp"></HelpDocumentation>
    </div>
</template>

<script>
    import Form from '../../components/Forms/Form';
    import HelpDocumentation from '../../components/HelpDocumentation'
    import fieldButton from '../../components/CustomFields/fieldButton'

    export default {
        name: 'RegisterUser',
        props: {
            accountId: {
                type: String,
                required: true
            }
        },
        components: {
            Form,
            HelpDocumentation,
            'vue-button': fieldButton
        },
        beforeRouteEnter(to, from, next) {
            next((vm) => {
                vm.prevRoute = from
            })
        },
        data() {
            return {
                formKey: 'RegisterUserForm',
                helpContentKey: 'RegisterHelp',
                showHelp: false,
            }
        },
        methods: {
            alert() {
                this.$emit('registerUserSuccess', true)
            },
            goBack() {
                this.$router.push(this.prevRoute.path)
            },
            openHelp() {
                this.showHelp = true;
            },
            closeHelp() {
                this.showHelp = false;
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