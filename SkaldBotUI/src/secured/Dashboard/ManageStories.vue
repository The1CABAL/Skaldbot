<template>
    <div id="ManageStories" class="h-full overflow-x-auto">
        <VueLoading v-if="!loaded"></VueLoading>
        <Modal v-show="isModalVisible" @close="closeModal" v-bind:modalDisplayTypeId="modalDisplayTypeId" v-bind:lookupId="lookupId"></Modal>
        <div v-show="loaded">
            <vue-table-filtered showPerPage
                                showSearchField
                                showPagination
                                :searchFunction="getData"
                                :columns="titles"
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
        name: "ManageStories",

        components: {
            VueLoading,
            Modal,
            'vue-table-filtered': vueTableFiltered,
        },

        mixins: [PageMixin],

        data() {
            return {
                modalDisplayTypeId: 2,
                lookupId: 0,
                loaded: false,
                isModalVisible: false,
                refreshData: false,
                data: [],
                titles: [
                    {
                        prop: "Id",
                        label: "Story Id",
                        sortable: false
                    },
                    {
                        prop: "Title",
                        label: "Story Title",
                        sortable: true
                    },
                    {
                        prop: "Story",
                        label: "Story",
                        sortable: true
                    },
                    {
                        prop: "IsActive",
                        label: "Is Active",
                        sortable: true
                    },
                ],
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

                this.pageReady();
            });
        },

        methods: {
            async getData(model) {
                this.loaded = false;

                await this.$store.dispatch('getAllStories', model);

                this.loaded = true;
                return this.$store.getters.getStories;
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

<style scoped>
</style>