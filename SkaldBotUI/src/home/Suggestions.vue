<template>
    <div class="suggestions">
        <SelectForm v-on:formKey="onChildChange" :pageId="pageId" />
        <Form v-if="formKey != ''" :formKey="formKey" v-on:error="error" />
    </div>
</template>

<script>
    import SelectForm from '../components/Forms/SelectForm';
    import Form from '../components/Forms/Form';

    export default {
        name: "Suggestions",
        components: {
            SelectForm,
            Form
        },
        data() {
            return {
                formKey: '',
                pageId: '1'
            }
        },
        methods: {
            onChildChange(value) {
                //console.log('Parent function called');
                if (this.formKey != '') {
                    this.formKey = '';
                }
                this.formKey = value;
            },
            error(value) {
                if (value == true) {
                    this.formKey = '';
                }
            }
        }
    }
</script>

<style scoped>
</style>