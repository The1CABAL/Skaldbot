<template>
    <div class="h-full overflow-x-auto">
        <VueLoading v-if="!loaded"></VueLoading>
        <div v-show="loaded">
            <vue-table-filtered :hidden-columns="['Id']"
                                showPerPage
                                showSearchField
                                showPagination
                                :model="model"
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
    import UtilMixin from '@/mixins/util-mixin.js';
    import vueTableFiltered from '@/components/Tables/vueTableFiltered';

    export default {
        name: "ManageUsers",

        components: {
            VueLoading,
            'vue-table-filtered': vueTableFiltered
        },

        mixins: [PageMixin, UtilMixin],

        data() {
            return {
                userId: '',
                loaded: false,
                titles: [
                    {
                        prop: "Username",
                        label: "Username",
                        sortable: true
                    },
                    {
                        prop: "FirstName",
                        label: "First Name",
                        sortable: true
                    },
                    {
                        prop: "LastName",
                        label: "Last Name",
                        sortable: true
                    },
                    {
                        prop: "IsActive",
                        label: "Is Active",
                        sortable: true
                    },
                    {
                        prop: "CreateDate",
                        label: "Date Created",
                        sortable: true
                    },
                ],
                model: {
                    isMaster: true
                }
            }
        },

        beforeMount() {
            this.pageMounting();
        },

        mounted() {
            this.pageMounted().then(() => {
                if (!this.$store.getters.isMasterAdmin && !this.$store.getters.isAdmin) {
                    this.$router.push('/unauthorized')
                }

                this.pageReady();
            })
        },

        methods: {
            async fetchData(model) {
                this.loaded = false;

                await this.$store.dispatch('getAllUsers', model);

                this.loaded = true;

                return this.$store.getters.getUsers
            },

            handleSelectionChange(val) {
                this.redirectUser(`/userprofile/${val}`)
            },
        }
    }
</script>

<style scoped>
    .el-table {
        background-color: #23272a;
    }
</style>