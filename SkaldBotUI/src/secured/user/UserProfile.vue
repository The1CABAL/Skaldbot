<template>
    <div id="UserProfile">
        <div v-if="submitted" v-bind:class="isError ? 'errorMsg' : 'successMsg'">
            <p style="font-weight: bold;">{{msg}}</p>
            <vue-button varient="close" @click="closeNotification">x</vue-button>
        </div>
        <div class="w-full space-x-2">
            <vue-button @click="goBack">Go Back</vue-button>
            <vue-button varient="secondary" @click="changePassword">Change Password</vue-button>
        </div>
        <ChangePassword v-if="showChangePassword" @close="closeChangePassword"></ChangePassword>
        <div class="panel">
            <div class="panel-heading"><h4 class="font-bold tracking-wide">User Profile</h4></div>
            <div class="panel-body">
                <h4 class="font-bold tracking-wide">{{userData.FirstName}} {{userData.LastName}}</h4>
                <hr />
                <form v-on:submit="formSubmit">
                    <vue-input id="userName" name="userName" v-model="userData.Username" :is-disabled="true">User Name</vue-input>
                    <vue-input id="firstName" name="firstName" v-model="userData.FirstName">First Name</vue-input>
                    <vue-input id="lastName" name="lastName" v-model="userData.LastName">Last Name</vue-input>
                    <vue-input id="discordUserId" name="discordUserId" v-model="userData.DiscordUserId">Discord User Id</vue-input>
                    <vue-input id="createDate" name="createDate" :is-disabled="true" :value="getDate(userData.CreateDate)">Date Created</vue-input>
                    <div v-if="admin">
                        <div>
                            <hr class="mb-3" />
                            <h4 class="font-bold tracking-wide">Admin Options</h4>
                            <vue-checkbox id="isActive" name="isActive" v-model="userData.IsActive">Is User Active</vue-checkbox>
                            <vue-checkbox id="isLocked" name="isLocked" v-model="userData.IsLocked">Is User Locked</vue-checkbox>
                        </div>
                        <div>
                            <hr class="mt-3 mb-3" />
                            <h4 class="font-bold tracking-wide">Permissions</h4>
                            <div>
                                <div v-for="item in roles" :key="item.Role">
                                    <vue-checkbox :id="item.Role" :name="item.Role" :value="isPermissionSelected(item.Role)" @change="updateSelectedRole(item.Role)">{{item.RoleName}}</vue-checkbox>
                                </div>
                            </div>
                        </div>
                    </div>
                    <hr class="mt-3 mb-3" />
                    <div class="space-x-2">
                        <vue-button type="submit">Save</vue-button>
                        <vue-button varient="secondary" type="secondary" @click="openHelp">Help</vue-button>
                    </div>
                    <HelpDocumentation v-if="showHelp" :HelpContentKey="helpContentKey" @close="closeHelp"></HelpDocumentation>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
    import HelpDocumentation from '../../components/HelpDocumentation'
    import ChangePassword from '../../account/ChangePassword'
    import fieldButton from '@/components/CustomFields/fieldButton'
    import fieldInput from '@/components/CustomFields/fieldInput'
    import fieldCheckbox from '@/components/CustomFields/fieldCheckbox'
    import PageMixin from '@/mixins/page-mixin'
    import UtilMixin from '@/mixins/util-mixin'

    export default {
        name: "UserProfile",
        props: {
            userId: {
                type: String,
                required: true
            }
        },
        mixins: [PageMixin, UtilMixin],
        components: {
            HelpDocumentation,
            ChangePassword,
            'vue-button': fieldButton,
            'vue-input': fieldInput,
            'vue-checkbox': fieldCheckbox
        },

        data() {
            return {
                userData: [],
                oldUserData: [],
                roles: [],
                selectedRole: '',
                msg: '',
                isError: true,
                submitted: false,
                success: false,
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

        beforeMount() {
            this.pageMounting();
        },

        mounted() {
            this.pageMounted().then(() => {
                if (!this.masterAdmin && !this.admin && this.$store.getters.userId !== this.userId) {
                    this.$router.push('/unauthorized')
                }

                this.getData();
                this.pageReady();
            })
        },

        methods: {
            isPermissionSelected(permission) {
                return this.selectedRole === permission;
            },

            updateSelectedRole(e) {
                this.selectedRole = e
            },

            formSubmit() {
                event.preventDefault();
                if (this.areEquivalent(this.userData, this.oldUserData) || this.isPermissionSelected(this.userData.r[0].Role)) {
                    this.setNotification(false);
                    return;
                }

                var postData = [];

                if (!this.isPermissionSelected(this.userData.r[0].Role)) {
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
                this.getUser();
                this.getRoles();
            },

            getUser() {
                this.$store.dispatch('getUser', this.userId).then(() => {
                    this.userData = this.$store.getters.getUser;
                    this.oldUserData = this.cloneModel(this.$store.getters.getUser);
                    this.selectedRole = this.$store.getters.getRole;
                }).catch(err => {
                    this.$message("Error getting user data");
                })
            },

            getRoles() {
                if (this.admin) {
                    this.$store.dispatch('getAllRoles').then(() => {
                        this.roles = this.$store.getters.getAllRoles;
                    }).catch(err => {
                        this.$message("Error getting user roles");
                    })
                }
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