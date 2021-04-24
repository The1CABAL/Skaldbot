<template>
    <div>
        <vue-select :items="getForms" :value-key="valueKey" :name-key="nameKey" v-on:change="onChange"/>
    </div>
</template>

<script>
    import { mapActions } from "vuex";
    import fieldSelect from '../CustomFields/fieldSelect'

    export default {
        name: "SelectForm",

        props: {
            pageId: {
                type: Number | String,
                required: false,
                default: 0
            }
        },

        components: {
            'vue-select': fieldSelect
        },

        data() {
            return {
                thePageId: { ...this.pageId },
                valueKey: 'FormKey',
                nameKey: 'FormName'
            }
        },

        methods: {
            ...mapActions(["fetchAllForms", "fetchAllFormsByPageId"]),
            onChange(e) {
                if (typeof e === 'object') {
                    this.$emit('formKey', e[this.valueKey])
                    return;
                }

                this.$emit('formKey', e)
            }
        },

        computed: {
            getForms() {
                return this.$store.getters.getForms;
            },
        },

        mounted() {
            if (this.pageId == 0 || this.pageId == undefined)
                this.fetchAllForms();
            else {
                this.fetchAllFormsByPageId(this.pageId);
            }

            this.$emit('select-forms-loaded')
        }
    }
</script>

<style scoped>
</style>