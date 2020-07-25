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
    import VueLoading from '../components/VueLoading';
    import axios from 'axios';

    export default {
        name: "ManageUsers",
        components: {
            VueLoading
        },
        data() {
            return {
                selectedUserId: '',
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
                                this.selectedUserId = row.Id
                                this.$message('Feature not yet implemented!')
                            },
                            label: 'Edit'
                        }
                    ]
                },
                selectedRow: []
            }
        },
        mounted: function () {
            this.loaded = false;
            let baseUrl = "http://127.0.0.1:5000"
            let userUrl = baseUrl + "/api/getUsers?isMaster=" + this.$store.getters.isMasterAdmin;
            var that = this;
            axios.get(userUrl).then(function (response) {
                that.data = JSON.parse(response.data);
            }).catch(function (error) {
                console.log(error);
                this.$emit('error', true)
            });
            that.loaded = true;
        },
        methods: {
            handleSelectionChange(val) {
                this.selectedRow = val
            },
            getDate(date) {
                let elDate = new Date(date)
                return elDate.getFullYear() + '-'
                    + (elDate.getMonth() + 1) + '-'
                    + elDate.getDate()
            },
            getBool(value) {
                if (value)
                    return "True"
                else
                    return "False"
            }
        }
    }
</script>