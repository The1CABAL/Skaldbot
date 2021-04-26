<template>
    <div id="ManageWisdoms" class="h-full overflow-x-auto">
        <VueLoading v-if="!loaded"></VueLoading>
        <Modal v-show="isModalVisible" @close="closeModal" v-bind:modalDisplayTypeId="modalDisplayTypeId" v-bind:lookupId="lookupId"></Modal>
        <div v-show="loaded">
            <vue-table-filtered showPerPage
                                showSearchField
                                showPagination
                                :columns="titles"
                                :searchFunction="getData"
                                @editClick="handleSelectionChange"
                                :forceRefresh="refreshData"
                                @data-reset="resetDataVariable">
            </vue-table-filtered>
        </div>
    </div>
</template>

<script>
    import VueLoading from '../../components/VueLoading';
    import Modal from '../../components/ModalComponent';
    import PageMixin from '@/mixins/page-mixin.js';
    import vueTableFiltered from '@/components/Tables/vueTableFiltered';

    export default {
        name: "ManageWisdoms",

        components: {
            VueLoading,
            Modal,
            'vue-table-filtered': vueTableFiltered
        },

        mixins: [PageMixin],

        data() {
            return {
                modalDisplayTypeId: 3,
                lookupId: 0,
                loaded: false,
                isModalVisible: false,
                refreshData: false,
                titles: [
                    {
                        prop: "Id",
                        label: "Wisdom Id",
                        sortable: false
                    },
                    {
                        prop: "Wisdom",
                        label: "Wisdom",
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
        mounted() {
            this.pageMounted().then(() => {
                if (!this.masterAdmin && !this.admin) {
                    this.$router.push('/unauthorized')
                    return;
                }

                this.pageReady();
            })
                
        },
        methods: {
            async getData(model) {
                this.loaded = false;

                await this.$store.dispatch('getAllWisdoms', model);

                this.loaded = true
                return this.$store.getters.getWisdoms;
            },

            handleSelectionChange(val) {
                this.lookupId = val
                this.showModal();
            },

            showModal() {
                this.isModalVisible = true
            },

            closeModal() {
                this.isModalVisible = false;
                this.lookupId = 0;
                this.refreshData = true;
            },

            resetDataVariable() {
                this.refreshData = false;
            }
        }
    }
</script>