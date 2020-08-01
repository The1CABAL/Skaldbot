<template>
    <div id="UserProfile">
        <div v-if="submitted" v-bind:class="isError ? 'errorMsg' : 'successMsg'">
            <p style="font-weight: bold;">{{msg}}</p>
            <button class="close" @click="closeNotification">x</button>
        </div>
        <button type="button" class="btn-button" v-on:click="goBack">Go Back</button>
        <button type="submit" class="btn-button">Save</button>
        <div class="panel">
            <div class="panel-heading"><h4>User Profile</h4></div>
            <div class="panel-body">
                <h4 class="sectionHeading">{{userData.FirstName}} {{userData.LastName}}</h4>
                <hr />
                <form v-on:submit="formSubmit">
                    <label for="userName">Username:</label>
                    <input type="text" id="userName" name="userName" v-model="userData.Username" disabled />
                    <label for="firstName">First Name:</label>
                    <input type="text" id="firstName" name="firstName" v-model="userData.FirstName" />
                    <label for="lastName">Last Name:</label>
                    <input type="text" id="lastName" name="lastName" v-model="userData.LastName" />
                    <label for="createDate">Date Created:</label>
                    <input type="text" id="createDate" name="createDate" disabled :value="getDate(userData.CreateDate)" />
                    <div v-if="isAdmin">
                        <div>
                            <hr />
                            <h4 class="sectionHeading">Admin Options</h4>
                            <div>
                                <label for="isActive">Is User Active:</label>
                                <input type="checkbox" id="isActive" name="isActive" v-model="userData.IsActive" />
                            </div>
                            <div>
                                <label for="isLocked">Is User Locked:</label>
                                <input type="checkbox" id="isLocked" name="isLocked" v-model="userData.IsLocked" />
                            </div>
                        </div>
                        <div>
                            <hr />
                            <h4 class="sectionHeading">Permissions</h4>
                            <div>
                                <div v-for="item in roles" :key="item.Role">
                                    <label for="item.Role">{{item.RoleName}}</label>
                                    <input type="checkbox" :name="item.Role" :value="item.Role" :checked="item.Role == selectedRole ? true : false" @change="updateSelectedRole" />
                                </div>
                            </div>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import { BaseUrl } from '../../helpers/constants';

    export default {
        name: "UserProfile",
        props: {
            userId: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                isAdmin: false,
                userData: [],
                oldUserData: [],
                roles: [],
                selectedRole: '',
                msg: '',
                isError: true,
                submitted: false,
                success: false,
                prevRoute: {}
            }
        },
        watch: {
            submitted: function () {
                if (this.submitted) {
                    setTimeout(
                        this.closeNotification, 5000);
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
                if (!this.$store.getters.isMasterAdmin && !this.$store.getters.isAdmin) {
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
            updateSelectedRole(e) {
                this.selectedRole = ''
                if (e.target.checked) {
                    this.selectedRole = (e.target.value);
                }
            },
            formSubmit() {
                event.preventDefault();
                if (!this.objectsAreSame(this.userData, this.oldUserData)) {
                    var url = BaseUrl + 'getUser'
                    var postData = [];
                    let that = this;
                    if (this.selectedRole != this.userData.r[0].Role) {
                        this.userData.r[0].Role = this.selectedRole
                    }
                    postData.push(this.userData)

                    axios.post(url, postData).then(function (response) {
                        var returnVal = response.data;
                        if (returnVal.Message.toString() == "Success") {
                            that.success = true
                            that.setNotification(that.success)
                            that.getData()
                        }
                        else {
                            that.success = false
                            that.setNotification(that.success)
                            that.getData()
                        }
                    });
                }
                else {
                    this.setNotification(false)
                }
            },
            closeNotification() {
                this.msg = '';
                this.submitted = false;
                this.isError = false;
            },
            setNotification(success) {
                if (success) {
                    this.submitted = true;
                    this.isError = false;
                    this.msg = "Successfully updated the user!";
                }
                else {
                    this.submitted = true;
                    this.isError = true;
                    this.msg = "There was an error updating the user. Please try again.";
                }
            },
            getData() {
                let url = BaseUrl + 'getUser?userId=' + this.userId;
                let roleUrl = BaseUrl + 'getRoles'
                let that = this;
                axios.get(url).then(function (response) {
                    var data = response.data[0];
                    that.userData = JSON.parse(data);
                    that.userData = that.userData[0]
                    that.oldUserData = JSON.parse(data);
                    that.oldUserData = that.oldUserData[0]
                    that.selectedRole = (that.userData.r[0].Role)
                }).catch(function (error) {
                    console.log(error);
                });

                axios.get(roleUrl).then(function (response) {
                    that.roles = JSON.parse(response.data)
                }).catch(function (error) {
                    console.log(error);
                });
            },
            objectsAreSame(x, y) {
                var objectsAreSame = true;
                for (var propertyName in x) {
                    if (propertyName == 'r') {
                        if (x[propertyName][0].Role != y[propertyName][0].Role) {
                            objectsAreSame = false;
                        }
                    }
                    else if (x[propertyName] != y[propertyName]) {
                        objectsAreSame = false;
                    }
                }

                return objectsAreSame;
            },
            reloadAuthentication() {
                this.$store.dispatch('loadRoles').then(() => {
                    if (!this.$store.getters.isMasterAdmin && !this.$store.getters.isAdmin) {
                        this.$router.push('/unauthorized')
                    }
                    else {
                        if (this.$store.getters.isMasterAdmin || this.$store.getters.isAdmin) {
                            this.isAdmin = true
                        }
                    }
                });
            },
            goBack() {
                this.$router.push(this.prevRoute.path)
            }
        }
    }
</script>

<style scoped>
</style>