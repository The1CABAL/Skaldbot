<template>
    <div class="space-y-4">
        <SelectForm v-on:formKey="onChildChange" :pageId="pageId" @select-forms-loaded="pageReady"/>
        <Form v-if="formKey != ''" :formKey="formKey" v-on:error="error" />
    </div>
</template>

<script>
    import SelectForm from '../components/Forms/SelectForm';
    import Form from '../components/Forms/Form';
    import PageMixin from '@/mixins/page-mixin.js';

    export default {
        name: "Suggestions",

        components: {
            SelectForm,
            Form
        },

        mixins: [PageMixin],

        data() {
            return {
                formKey: '',
                pageId: '1'
            }
        },

        beforeMount() {
            this.pageMounting();
        },

        mounted() {
            this.pageMounted();
        },

        methods: {
            onChildChange(value) {
                if (this.formKey != '') {
                    this.formKey = '';
                }
                this.formKey = value;
            },
            error(value) {
                if (value == true) {
                    this.formKey = '';
                }
            },
        }
    }
</script>

<style scoped>
</style>