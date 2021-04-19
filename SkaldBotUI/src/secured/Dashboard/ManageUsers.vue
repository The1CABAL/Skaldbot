<template>
    <div>
        <VueLoading v-if="!loaded"></VueLoading>
        <div v-if="loaded">
            <vue-table-filtered :hidden-columns="['Id']"
                                showPerPage
                                showSearchField
                                showPagination
                                :items="data"
                                :pages="1"
                                @editClick="handleSelectionChange">
                <vue-table-column v-for="title in titles" :label="title.label" :key="title.prop" is-sortable />
                <vue-table-column label="User Active" is-sortable />
                <vue-table-column prop="CreateDate" label="Date Created" is-sortable />
            </vue-table-filtered>
        </div>
    </div>
</template>

<script>
    import VueLoading from '../../components/VueLoading';
    import PageMixin from '@/mixins/page-mixin.js';
    import vueTableFiltered from '@/components/Tables/vueTableFiltered';
    import vueTableColumn from '@/components/Tables/vueTableColumn';

    export default {
        name: "ManageUsers",

        components: {
            VueLoading,
            'vue-table-filtered': vueTableFiltered,
            'vue-table-column': vueTableColumn
        },

        mixins: [PageMixin],

        data() {
            return {
                userId: '',
                loaded: false,
                data: [],
                titles: [
                    {
                        prop: "Username",
                        label: "Username"
                    },
                    {
                        prop: "FirstName",
                        label: "First Name"
                    },
                    {
                        prop: "LastName",
                        label: "Last Name"
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
                }

                this.fetchData();
                this.pageReady();
            })
        },

        methods: {
            fetchData() {
                this.loaded = false;
                var isMaster = this.$store.getters.isMasterAdmin;

                this.$store.dispatch('getAllUsers', isMaster).then(() => {
                    this.data = this.$store.getters.getUsers;
                    this.loaded = true
                }).catch(err => {
                    console.log(err);
                    this.$emit('error', true);
                })
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