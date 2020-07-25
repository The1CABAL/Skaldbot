<template>
    <div id="UserProfile">
        <div v-if="submitted" v-bind:class="isError ? 'errorMsg' : 'successMsg'">
            <p style="font-weight: bold;">{{msg}}</p>
            <button class="close" @click="closeNotification">x</button>
        </div>
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
                    <button type="submit">Update</button>
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
                success: false
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
        mounted: function () {
            this.getData();
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
                console.log(this.userData)
                console.log(this.oldUserData);
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
                console.log("Success value: " + success)
                if (success) {
                    this.submitted = true;
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

                if (this.$store.getters.isAdmin || this.$store.getters.isMasterAdmin) {
                    this.isAdmin = true;
                }
            },
            objectsAreSame(x, y) {
                var objectsAreSame = true;
                for (var propertyName in x) {
                    if (propertyName == 'r') {
                        if (x[propertyName][0].Role != y[propertyName][0].Role)
                        {
                            objectsAreSame = false;
                        }
                    }
                    else if (x[propertyName] != y[propertyName]) {
                        objectsAreSame = false;
                    }
                }

                return objectsAreSame;
            }
        }
    }
</script>

<style scoped>
    .close {
        position: absolute;
        font-size: 15px;
        top: 1px;
        right: 0;
        border: 0;
        padding-right: 5px;
        background-color: rgba(0,0,0,0.0);
    }

    .successMsg {
        position: relative;
        display: inline-block;
        width: 100%;
        height: auto;
        background: #93FFA1;
        border-radius: 10px 10px 10px 10px;
        overflow: hidden;
        padding-left: 10px;
    }

    .errorMsg {
        position: relative;
        display: inline-block;
        width: 100%;
        height: auto;
        background: #FF9393;
        border-radius: 10px 10px 10px 10px;
        overflow: hidden;
        padding-left: 10px;
    }

    .panel {
        margin-top: 5px;
        margin-bottom: 20px;
        border: 1px solid transparent;
        border-radius: 4px;
        -webkit-box-shadow: 0 1px 1px rgba(0, 0, 0, .05);
        box-shadow: 0 1px 1px rgba(0, 0, 0, .05);
        border-color: #ddd;
    }

    .panel-heading {
        color: #333;
        background-color: #f5f5f5;
        border-color: #ddd;
        padding: 5px 15px;
        border-bottom: 1px solid transparent;
        border-top-left-radius: 3px;
        border-top-right-radius: 3px;
    }

    .panel-body {
        padding: 15px;
        background-color: #fff;
    }

    input[type=text] {
        width: 100%;
        padding: 12px 20px;
        margin: 8px 0;
        display: inline-block;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-sizing: border-box;
    }

    .sectionHeading {
        color: #00b1b1;
    }
</style>