<template>
    <div class="h-full overflow-x-auto">
        <VueLoading v-if="!loaded"></VueLoading>
        <HelpDocumentation v-if="isModalVisible" :HelpContentKey="helpContentKey" @close="closeModal"></HelpDocumentation>
        <div v-show="loaded">

            <vue-table-filtered :action-button-options="{Visible: true,Label: 'Edit', EmitValue: 'HelpContentKey'}"
                                showPerPage
                                showSearchField
                                showPagination
                                :columns="titles"
                                :searchFunction="getData"
                                @editClick="handleSelectionChange">
            </vue-table-filtered>
        </div>
    </div>
</template>

<script>
    import VueLoading from '../../components/VueLoading';
    import HelpDocumentation from '../../components/HelpDocumentation';
    import PageMixin from '@/mixins/page-mixin.js';
    import vueTableFiltered from '@/components/Tables/vueTableFiltered';

    export default {
        name: "ManageDocumentation",
        components: {
            VueLoading,
            HelpDocumentation,
            'vue-table-filtered': vueTableFiltered
        },

        mixins: [PageMixin],

        data() {
            return {
                helpContentKey: '',
                loaded: false,
                isModalVisible: false,
                titles: [
                    {
                        prop: "HelpContentKey",
                        label: "Help Content Key",
                        sortable: true
                    },
                    {
                        prop: "HelpTitle",
                        label: "Help Title",
                        sortable: true
                    },
                    {
                        prop: "HelpContent",
                        label: "Help Content",
                        sortable: true
                    },
                    {
                        prop: "IsActive",
                        label: "Is Active",
                        sortable: true
                    },
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
            async getData(model) {
                this.loaded = false;

                await this.$store.dispatch('getAllDocumentation', model);

                this.loaded = true

                return this.$store.getters.helpDocumentation
            },

            handleSelectionChange(val) {
                this.helpContentKey = val
                this.showModal();
            },

            showModal() {
                this.isModalVisible = true
            },

            closeModal() {
                this.isModalVisible = false;
                this.helpContentKey = '';
            },
        }
    }
</script>