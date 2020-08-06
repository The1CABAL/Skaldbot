<template>
    <div id="UserProfile">
        <div v-if="submitted" v-bind:class="isError ? 'errorMsg' : 'successMsg'">
            <p style="font-weight: bold;">{{msg}}</p>
            <button class="close" @click="closeNotification">x</button>
        </div>
        <button type="button" class="btn-button" v-on:click="goBack">Go Back</button>
        <button type="button" class="btn-button" v-on:click="changePassword">Change Password</button>
        <ChangePassword v-if="showChangePassword" @close="closeChangePassword"></ChangePassword>
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
                    <label for="discordUserId">Discord User ID:</label>
                    <input type="text" id="discordUserId" name="discordUserId" v-model="userData.DiscordUserId" />
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
                    <hr />
                    <button type="submit" class="btn-button">Save</button>
                    <button type="button" v-on:click="openHelp" class="btn-button">Help</button>
                    <HelpDocumentation v-if="showHelp" @close="closeChangePassword"></HelpDocumentation>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
    import HelpDocumentation from '../../components/HelpDocumentation'
    import ChangePassword from '../../account/ChangePassword'

    export default {
        name: "UserProfile",
        props: {
            userId: {
                type: String,
                required: true
            }
        },
        components: {
            HelpDocumentation,
            ChangePassword
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
                prevRoute: {},
                helpContentKey: 'RegisterHelp',
                showHelp: false,
                showChangePassword: false
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
                    var postData = [];
                    if (this.selectedRole != this.userData.r[0].Role) {
                        this.userData.r[0].Role = this.selectedRole
                    }
                    postData.push(this.userData)

                    this.$store.dispatch('updateUser', postData).then(() => {
                        var returnVal = this.$store.getters.authStatus;
                        if (returnVal == "Success") {
                            this.success = true;
                            this.setNotification(this.success);
                            this.getData()
                        }
                        else {
                            this.success = false;
                            this.setNotification(this.success);
                            this.getData()
                        }
                    })
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
                var userId = this.userId

                this.$store.dispatch('getUser', userId).then(() => {
                    this.userData = { ...this.$store.getters.getUser };
                    this.oldUserData = { ...this.$store.getters.getUser };
                    this.selectedRole = this.$store.getters.getUser.r[0].Role;
                }).catch(err => {
                    console.log(err);
                    this.$message("Error getting user data");
                })

                this.$store.dispatch('getAllRoles').then(() => {
                    this.roles = this.$store.getters.getAllRoles;
                }).catch(err => {
                    console.log(err);
                })
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
                    if (this.$store.getters.isMasterAdmin || this.$store.getters.isAdmin) {
                        this.isAdmin = true
                    }
                });
            },
            goBack() {
                this.$router.push(this.prevRoute.path)
            },
            openHelp() {
                this.showHelp = true;
            },
            closeHelp() {
                this.showHelp = false;
            },
            changePassword() {
                this.showChangePassword = true;
            },
            closeChangePassword() {
                this.showChangePassword = false;
            }
        }
    }
</script>

<style scoped>
</style>