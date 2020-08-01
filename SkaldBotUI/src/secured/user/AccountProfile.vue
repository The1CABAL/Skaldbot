<template>
    <div id="AccountProfile">
        <div v-if="submitted" v-bind:class="isError ? 'errorMsg' : 'successMsg'">
            <p style="font-weight: bold;">{{msg}}</p>
            <button class="close" @click="closeNotification">x</button>
        </div>
        <tabs>
            <tab title="Account Information">
                <div class="panel">
                    <div class="panel-heading"><h4>Account Profile</h4></div>
                    <div class="panel-body">
                        <h4 class="sectionHeading">{{accountData.AccountName}}</h4>
                        <hr />
                        <form v-on:submit="formSubmit">
                            <label for="accountName">Account Name:</label>
                            <input type="text" id="accountName" name="accountName" v-model="accountData.AccountName" />
                            <label for="createDate">Date Created:</label>
                            <input type="text" id="createDate" name="createDate" :value="getDate(accountData.CreateDate)" disabled />
                            <label for="isActive">Is Active:</label>
                            <input type="checkbox" id="isActive" name="isActive" v-model="accountData.IsActive" />
                            <br />
                            <button type="submit" class="btn-button">Save</button>
                        </form>
                    </div>
                </div>
            </tab>
            <tab title="Users">
                <button type="button" class="btn-button" v-on:click="registerUser">Add User</button>
                <div style="margin-bottom: 10px">
                    <el-row>
                        <el-col :span="6">
                            <el-input placeholder="Search Username" v-model="filters[0].value"></el-input>
                        </el-col>
                    </el-row>
                </div>

                <data-tables :data="accountUsers" :action-col="actionCol" :filters="filters" @selection-change="handleSelectionChange">
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
            </tab>
        </tabs>
    </div>
</template>

<script>
    export default {
        name: "AccountProfile",
        props: {
            accountId: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                accountData: [],
                accountUsers: [],
                prevRoute: {},
                msg: '',
                isError: true,
                submitted: false,
                success: false,
                masterAdmin: false,
                admin: false,
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
        watch: {
            submitted: function () {
                if (this.submitted) {
                    setTimeout(this.closeNotification, 5000);
                }
            }
        },
        beforeRouteEnter(to, from, next) {
            next((vm) => {
                vm.prevRoute = from
            })
        },
        mounted: function () {
            this.getData();
        },
        created: function () {
            if (this.$store.getters.isLoggedIn) {
                this.reloadAuthentication();
            }
            else {
                if (!this.$store.getters.isMasterAdmin && !this.$store.getters.isAdmin && !this.$store.getters.isClientAdmin) {
                    this.$router.push('/unauthorized')
                }
                else {
                    this.getData();
                }
            }
        },
        methods: {
            getDate(date) {
                let elDate = new Date(date)
                return (elDate.getMonth() + 1) + '-'
                    + elDate.getDate() + '-'
                    + elDate.getFullYear()
            },
            formSubmit() {
                event.preventDefault();
                if (!this.objectsAreSame(this.accountData, this.$store.getters.accountInformation)) {
                    let that = this;
                    this.$store.dispatch('updateAccountInformation', this.accountData).then(() => {
                        that.success = true
                        that.setNotification(that.success);
                        that.getData()
                    }).catch(err => {
                        that.success = false;
                        that.setNotification(that.success)
                        that.getData()
                        console.log(err);
                    })
                }
                else {
                    this.setNotification(false);
                }
            },
            setNotification(success) {
                if (success) {
                    this.submitted = true;
                    this.isError = false;
                    this.msg = "Successfully updated the account!";
                }
                else {
                    this.submitted = true;
                    this.isError = true;
                    this.msg = "There was an error updating the account. Please try again.";
                }
            },
            closeNotification() {
                this.msg = '';
                this.submitted = false;
                this.isError = false;
            },
            getData() {
                let that = this;
                this.$store.dispatch('getAccountInformation', this.accountId).then(() => {
                    that.accountData = { ...this.$store.getters.accountInformation };
                    that.accountUsers = this.$store.getters.accountUsers;
                }).catch(err => {
                    that.$message('Error loading account data!');
                    console.log(err);
                })
            },
            objectsAreSame(x, y) {
                var objectsAreSame = true;
                for (var propertyName in x) {
                    if (x[propertyName] != y[propertyName]) {
                        objectsAreSame = false;
                    }
                }

                return objectsAreSame;
            },
            goBack() {
                this.$router.push(this.prevRoute.path)
            },
            reloadAuthentication() {
                this.$store.dispatch('loadRoles').then(() => {
                    if (this.$store.getters.isMasterAdmin) {
                        this.masterAdmin = true;
                        this.admin = true;
                    }
                    else if (this.$store.getters.isAdmin) {
                        this.admin = true;
                    }
                });
            },
            handleSelectionChange(val) {
                this.selectedRow = val
            },
            getBool(value) {
                if (value)
                    return "True"
                else
                    return "False"
            },
            registerUser() {
                this.$router.push('/registerUser/' + this.accountId)
            }
        }
    }
</script>

<style scoped>
</style>