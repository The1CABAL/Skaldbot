<template>
    <div id="ManageForms">
        <VueLoading v-if="!loaded"></VueLoading>
        <div v-if="loaded">
            <div class="flex flex-1">
                <vue-button @click="newForm">New Form</vue-button>
            </div>
            <vue-table-filtered :action-button-options="{Visible: true,Label: 'Edit', EmitValue: 'FormKey'}"
                                showPerPage
                                showSearchField
                                showPagination
                                :items="data"
                                :pages="1"
                                @editClick="handleSelectionChange">
                <vue-table-column v-for="title in titles" :label="title.label" :key="title.prop" is-sortable />
                <vue-table-column label="Is Active" is-sortable />
            </vue-table-filtered>
        </div>
    </div>
</template>

<script>
    import VueLoading from '../../components/VueLoading';
    import PageMixin from '@/mixins/page-mixin.js';
    import vueTableFiltered from '@/components/Tables/vueTableFiltered';
    import vueTableColumn from '@/components/Tables/vueTableColumn';
    import fieldButton from '@/components/CustomFields/fieldButton';

    export default {
        name: "ManageForms",

        mixins: [PageMixin],

        components: {
            VueLoading,
            'vue-table-filtered': vueTableFiltered,
            'vue-table-column': vueTableColumn,
            'vue-button': fieldButton
        },

        data() {
            return {
                loaded: false,
                data: [],
                titles: [
                    {
                        prop: "FormKey",
                        label: "Form Key"
                    },
                    {
                        prop: "FormName",
                        label: "Form Name"
                    }
                ]
            }
        },

        beforeMount() {
            this.pageMounting();
        },

        mounted() {
            this.pageMounted().then(() => {
                if (!this.$store.getters.isMasterAdmin && !this.$store.getters.isAdmin) {
                    this.$router.push('/unauthorized')
                    return;
                }
                this.fetchData();
                this.pageReady();
            });
        },

        methods: {

            fetchData() {
                return this.$store.dispatch('fetchAllForms').then(() => {
                    this.getData();
                });
            },

            getData() {
                this.data = this.$store.getters.getForms
                this.loaded = true;
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