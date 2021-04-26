<template>
    <div class="h-full overflow-x-auto">
        <VueLoading v-if="!loaded"></VueLoading>
        <Modal v-show="isModalVisible" @close="closeModal" v-bind:modalDisplayTypeId="modalDisplayTypeId" v-bind:lookupId="lookupId"></Modal>
        <div v-show="loaded">
            <vue-table-filtered :hidden-columns="['Id', 'ItemType']"
                                showPerPage
                                showSearchField
                                showPagination
                                :columns="titles"
                                :forceRefresh="refreshData"
                                :searchFunction="getData"
                                @editClick="handleSelectionChange"
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
        name: "PendingItems",

        mixins: [PageMixin],

        components: {
            VueLoading,
            Modal,
            'vue-table-filtered': vueTableFiltered,
        },

        data() {
            return {
                modalDisplayTypeId: 1,
                lookupId: 0,
                loaded: false,
                isModalVisible: false,
                refreshData: false,
                titles: [
                    {
                        prop: "ActualItemType",
                        label: "Submitted Item Type",
                        sortable: true
                    },
                    {
                        prop: "Title",
                        label: "Title",
                        sortable: true
                    },
                    {
                        prop: "ItemText",
                        label: "Content",
                        sortable: false
                    },
                    {
                        prop: "DiscordUserId",
                        label: "Discord User Id",
                        sortable: false
                    },
                    {
                        prop: "CreateDate",
                        label: "Date Created",
                        sortable: true
                    },
                    {
                        prop: "IsApproved",
                        label: "Is Approved",
                        sortable: true
                    },
                    {
                        prop: "IsReviewed",
                        label: "Is Reviewed",
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
                if (!this.$store.getters.isMasterAdmin && !this.$store.getters.isAdmin) {
                    this.$router.push('/unauthorized')
                    return;
                }
                
                this.pageReady();
            })
        },
        methods: {
            async getData(model) {
                this.loaded = false;

                await this.$store.dispatch('getSuggestions', model);

                let data = this.$store.getters.getSubmittedItems

                this.loaded = true;

                return data;
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