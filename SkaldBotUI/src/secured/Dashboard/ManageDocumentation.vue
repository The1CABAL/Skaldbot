<template>
    <div>
        <VueLoading v-if="!loaded"></VueLoading>
        <HelpDocumentation v-if="isModalVisible" :HelpContentKey="helpContentKey" @close="closeModal"></HelpDocumentation>
        <div v-if="loaded">

            <vue-table-filtered :action-button-options="{Visible: true,Label: 'Edit', EmitValue: 'HelpContentKey'}"
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
    import HelpDocumentation from '../../components/HelpDocumentation';
    import PageMixin from '@/mixins/page-mixin.js';
    import vueTableFiltered from '@/components/Tables/vueTableFiltered';
    import vueTableColumn from '@/components/Tables/vueTableColumn';

    export default {
        name: "ManageDocumentation",
        components: {
            VueLoading,
            HelpDocumentation,
            'vue-table-filtered': vueTableFiltered,
            'vue-table-column': vueTableColumn
        },

        mixins: [PageMixin],

        data() {
            return {
                helpContentKey: '',
                loaded: false,
                isModalVisible: false,
                data: [],
                titles: [
                    {
                        prop: "HelpContentKey",
                        label: "Help Content Key"
                    },
                    {
                        prop: "HelpTitle",
                        label: "Help Title"
                    },
                    {
                        prop: "HelpContent",
                        label: "Help Content"
                    }
                ]
            }
        },

        beforeMount() {
            this.pageMounting();
        },

        mounted(){
            this.pageMounted().then(() => {
                if (!this.$store.getters.isMasterAdmin && !this.$store.getters.isAdmin) {
                    this.redirectUser('/unauthorized')
                    return;
                }
                this.getData();
                this.pageReady();
            });
        },

        methods: {
            getData() {
                this.loaded = false;

                this.$store.dispatch('getAllDocumentation').then(() => {
                    this.data = this.$store.getters.helpDocumentation
                    this.loaded = true
                }).catch((err) => {
                    console.log(err)
                    this.$message("There was an error getting the help documentations")
                })
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
                this.getData();
            },
        }
    }
</script>