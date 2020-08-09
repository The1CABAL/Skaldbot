<template>
    <div>
        <VueLoading v-if="!loaded"></VueLoading>
        <div v-if="loaded">
            <div style="margin-bottom: 10px">
                <el-row>
                    <el-col :span="6">
                        <el-input placeholder="Search Username" v-model="filters[0].value"></el-input>
                    </el-col>
                </el-row>
            </div>

            <data-tables :data="data" :action-col="actionCol" :filters="filters" @selection-change="handleSelectionChange">
                <el-table-column v-for="title in titles" :prop="title.prop" :label="title.label" :key="title.prop" sortable="custom">
                </el-table-column>
                <el-table-column prop="IsActive" label="User Active">
                    <template slot-scope="scope">
                        <div>{{getBool(scope.row.IsActive)}}</div>
                    </template>
                </el-table-column>
                <el-table-column prop="CreateDate" label="Date Created">
                    <template slot-scope="scope">
                        <div>{{getDate(scope.row.CreateDate)}}</div>
                    </template>
                </el-table-column>
            </data-tables>
        </div>
    </div>
</template>

<script>
    // fake server
    import VueLoading from '../../components/VueLoading';

    export default {
        name: "ManageUsers",
        components: {
            VueLoading
        },
        data() {
            return {
                userId: '',
                loaded: false,
                data: [],
                titles: [
                    {
                        prop: "Id",
                        label: "User Id"
                    },
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
                ],
                filters: [
                    {
                        prop: 'Username',
                        value: ''
                    }
                ],
                actionCol: {
                    props: {
                        label: 'Actions',
                    },
                    buttons: [
                        {
                            props:
                            {
                                type: 'primary'
                            },
                            handler: row => {
                                this.userId = row.Id
                                this.$router.push('/userprofile/' + this.userId)
                            },
                            label: 'Edit'
                        }
                    ]
                },
                selectedRow: []
            }
        },
        mounted: function () {
            if (this.$store.getters.isLoggedIn) {
                this.reloadAuthentication();
            }
            else {
                if (!this.$store.getters.isMasterAdmin && !this.$store.getters.isAdmin) {
                    this.$router.push('/unauthorized')
                }
                else {
                    this.isLoaded = true
                    this.fetchData();
                }
            }
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
                this.selectedRow = val
            },
            getDate(date) {
                let elDate = new Date(date)
                return (elDate.getMonth() + 1) + '-'
                    + elDate.getDate() + '-'
                    + elDate.getFullYear()
            },
            getBool(value) {
                if (value)
                    return "True"
                else
                    return "False"
            },
            reloadAuthentication() {
                this.$store.dispatch('loadRoles').then(() => {
                    if (!this.$store.getters.isMasterAdmin && !this.$store.getters.isAdmin) {
                        this.$router.push('/unauthorized')
                    }
                    else {
                        this.isLoaded = true
                        this.fetchData();
                    }
                });
            }
        }
    }
</script>

<style scoped>
    .el-table{
        background-color: #23272a;
    }
</style>