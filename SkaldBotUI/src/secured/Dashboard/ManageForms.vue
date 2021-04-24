<template>
    <div id="ManageForms">
        <VueLoading v-if="!loaded"></VueLoading>
        <div v-show="loaded">
            <div class="flex flex-1">
                <vue-button @click="newForm">New Form</vue-button>
            </div>
            <vue-table-filtered :action-button-options="{Visible: true,Label: 'Edit', EmitValue: 'FormKey'}"
                                showPerPage
                                showSearchField
                                showPagination
                                :columns="titles"
                                :searchFunction="fetchData"
                                @editClick="handleSelectionChange">
            </vue-table-filtered>
        </div>
    </div>
</template>

<script>
    import VueLoading from '../../components/VueLoading';
    import PageMixin from '@/mixins/page-mixin.js';
    import vueTableFiltered from '@/components/Tables/vueTableFiltered';
    import fieldButton from '@/components/CustomFields/fieldButton';

    export default {
        name: "ManageForms",

        mixins: [PageMixin],

        components: {
            VueLoading,
            'vue-table-filtered': vueTableFiltered,
            'vue-button': fieldButton
        },

        data() {
            return {
                loaded: false,
                data: [],
                titles: [
                    {
                        prop: "FormKey",
                        label: "Form Key",
                        sortable: true
                    },
                    {
                        prop: "FormName",
                        label: "Form Name",
                        sortable: true
                    },
                    {
                        prop: "IsActive",
                        label: "Is Active",
                        sortable: true
                    }
                ]
            }
        },

        beforeMount() {
            this.pageMounting();
        },

        mounted() {
            this.pageMounted().then(() => {
                if (!this.masterAdmin && !this.admin) {
                    this.redirectUser('/unauthorized')
                    return;
                }
                
                this.pageReady();
            });
        },

        methods: {
            async fetchData(model) {
                this.loaded = false;

                await this.$store.dispatch('fetchAllForms', model);

                this.loaded = true;

                return this.$store.getters.getForms;
            },

            handleSelectionChange(val) {
                this.redirectUser(`/modifyform/${val}`)
            },

            newForm() {
                this.redirectUser('/modifyform')
            }
        }
    }
</script>