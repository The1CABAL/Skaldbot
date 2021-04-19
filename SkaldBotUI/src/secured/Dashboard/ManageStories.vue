<template>
    <div id="ManageStories">
        <VueLoading v-if="!loaded"></VueLoading>
        <Modal v-show="isModalVisible" @close="closeModal" v-bind:modalDisplayTypeId="modalDisplayTypeId" v-bind:lookupId="lookupId"></Modal>
        <div v-if="loaded">
            <vue-table-filtered showPerPage
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
    import Modal from '../../components/ModalComponent';
    import PageMixin from '@/mixins/page-mixin.js';
    import vueTableFiltered from '@/components/Tables/vueTableFiltered';
    import vueTableColumn from '@/components/Tables/vueTableColumn';

    export default {
        name: "ManageStories",

        components: {
            VueLoading,
            Modal,
            'vue-table-filtered': vueTableFiltered,
            'vue-table-column': vueTableColumn,
        },

        mixins: [PageMixin],

        data() {
            return {
                modalDisplayTypeId: 2,
                lookupId: 0,
                loaded: false,
                isModalVisible: false,
                data: [],
                titles: [
                    {
                        prop: "Id",
                        label: "Story Id"
                    },
                    {
                        prop: "Title",
                        label: "Story Title"
                    },
                    {
                        prop: "Story",
                        label: "Story"
                    }
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

                this.getData();
                this.pageReady();
            });
        },

        methods: {
            getData() {
                this.loaded = false;
                this.$store.dispatch('getAllStories').then(() => {
                    this.data = this.$store.getters.getStories;
                    this.loaded = true;
                }).catch(err => {
                    console.log(err);
                    this.$message("There was an error getting all the stories");
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

<style scoped>
</style>