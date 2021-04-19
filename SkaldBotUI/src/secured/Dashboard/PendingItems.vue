<template>
    <div>
        <VueLoading v-if="!loaded"></VueLoading>
        <Modal v-show="isModalVisible" @close="closeModal" v-bind:modalDisplayTypeId="modalDisplayTypeId" v-bind:lookupId="lookupId"></Modal>
        <div v-if="loaded">
            <vue-table-filtered :hidden-columns="['Id']"
                                showPerPage
                                showSearchField
                                showPagination
                                :items="data"
                                :pages="1"
                                @editClick="handleSelectionChange">
                <vue-table-column v-for="title in titles" :label="title.label" :key="title.prop" is-sortable />
                <vue-table-column label="Is Approved" is-sortable />
                <vue-table-column label="Is Reviewed" is-sortable />
                <vue-table-column label="Date Created" is-sortable />
            </vue-table-filtered>
        </div>
    </div>
</template>

<script>
    import VueLoading from '../../components/VueLoading';
    import Modal from '../../components/ModalComponent';
    import PageMixin from '@/mixins/page-mixin.js';
    import vueTableFiltered from '@/components/Tables/vueTableFiltered';
    import vueTableColumn from '@/components/Tables/vueTableColumn';

    export default {
        name: "PendingItems",

        mixins: [PageMixin],

        components: {
            VueLoading,
            Modal,
            'vue-table-filtered': vueTableFiltered,
            'vue-table-column': vueTableColumn
        },

        data() {
            return {
                modalDisplayTypeId: 1,
                lookupId: 0,
                loaded: false,
                isModalVisible: false,
                data: [],
                titles: [
                    {
                        prop: "ItemType",
                        label: "Submitted Item Type"
                    },
                    {
                        prop: "Title",
                        label: "Title"
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
                this.getData();
                this.pageReady();
            })
        },
        methods: {
            getData() {
                this.loaded = false;

                this.$store.dispatch('getSuggestions').then(() => {
                    if (this.$store.getters.getSubmittedItems.length > 0) {
                        this.data = this.$store.getters.getSubmittedItems
                        for (var i = 0; i < this.data.length; i++) {
                            this.data[i].ItemType = this.data[i].luIT[0].ActualItemType
                        }
                    }
                    this.loaded = true;
                }).catch(err => {
                    console.log(err);
                    this.$message("There was an error getting the submitted items");
                })
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
                this.getData();
            },
        }
    }
</script>