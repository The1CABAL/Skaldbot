<template>
    <div class="space-y-4">
        <SelectForm v-on:formKey="onChildChange" :pageId="pageId" @select-forms-loaded="pageReady" />
        <Form v-if="formKey != ''" :formKey="formKey" v-on:error="error" />
        <vue-button varient="secondary" type="button" v-on:click="openHelp" class="btn-button">Help</vue-button>
        <HelpDocumentation v-if="showHelp" :HelpContentKey="helpContentKey" @close="closeHelp"></HelpDocumentation>
    </div>
</template>

<script>
    import SelectForm from '../components/Forms/SelectForm';
    import Form from '../components/Forms/Form';
    import PageMixin from '@/mixins/page-mixin.js';
    import HelpDocumentation from '../components/HelpDocumentation'
    import fieldButton from '@/components/CustomFields/fieldButton'

    export default {
        name: "Suggestions",

        components: {
            SelectForm,
            Form,
            HelpDocumentation,
            'vue-button': fieldButton
        },

        mixins: [PageMixin],

        data() {
            return {
                formKey: '',
                pageId: '1',
                helpContentKey: 'SuggestionHelp',
                showHelp: false,
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
</style>