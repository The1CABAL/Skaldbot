<template>
    <div id="AccountProfile">
        <div class="pb-3">
            <vue-button @click="goBack">Go Back</vue-button>
        </div>
        <div v-if="submitted" v-bind:class="isError ? 'errorMsg' : 'successMsg'">
            <p style="font-weight: bold;">{{msg}}</p>
            <vue-button varient="close" @click="closeNotification">x</vue-button>
        </div>
        <tabs :onSelect="activeTab">
            <tab title="Account Information">
                <div class="panel">
                    <div class="panel-heading"><h4 class="font-bold tracking-wide">Account Profile</h4></div>
                    <div class="panel-body">
                        <h4 class="font-bold tracking-wide">{{accountData.AccountName}}</h4>
                        <hr class="mt-3" />
                        <form v-on:submit="formSubmit">
                            <vue-input name="accountName" id="accountName" v-model="accountData.AccountName">Account Name</vue-input>
                            <vue-input name="createDate" id="createDate" :value="getDate(accountData.CreateDate)" :is-disabled="true">Date Created</vue-input>
                            <vue-checkbox v-model="accountData.IsActive">Is Active</vue-checkbox>
                            <vue-button type="submit">Save</vue-button>
                        </form>
                    </div>
                </div>
            </tab>
            <tab title="Users" class="panel p-3">
                <vue-button v-on:click="registerUser">Add User</vue-button>
                <vue-table-filtered v-if="isViewingUsers"
                                    :hidden-columns="['Id']"
                                    showPerPage
                                    showSearchField
                                    showPagination
                                    :model="model"
                                    :columns="titles"
                                    :searchFunction="getAccountUsers"
                                    @editClick="handleSelectionChange">
                </vue-table-filtered>
            </tab>
        </tabs>
    </div>
</template>

<script>
    import fieldButton from '../../components/CustomFields/fieldButton'
    import fieldCheckbox from '../../components/CustomFields/fieldCheckbox'
    import fieldInput from '../../components/CustomFields/fieldInput'
    import vueTableFiltered from '../../components/Tables/vueTableFiltered'
    import vueTableColumn from '../../components/Tables/vueTableColumn'
    import PageMixin from '@/mixins/page-mixin.js'
    import UtilMixin from '@/mixins/util-mixin.js'

    export default {
        name: "AccountProfile",

        props: {
            accountId: {
                type: String,
                required: true
            }
        },

        mixins: [PageMixin, UtilMixin],

        components: {
            'vue-button': fieldButton,
            'vue-checkbox': fieldCheckbox,
            'vue-input': fieldInput,
            'vue-table-filtered': vueTableFiltered,
            'vue-table-column': vueTableColumn
        },

        data() {
            return {
                accountData: [],
                accountUsers: [],
                msg: '',
                isError: true,
                submitted: false,
                success: false,
                currentTab: 'account',
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
                        label: "User Active",
                        sortable: true
                    },
                    {
                        prop: "IsLocked",
                        label: "User Locked",
                        sortable: true
                    },
                    {
                        prop: "CreateDate",
                        label: "Date Created",
                        sortable: true
                    }
                ],
                model: {
                    accountId: this.accountId,
                    masterAdmin: false
                }
            }
        },

        watch: {
            submitted() {
                if (this.submitted) {
                    setTimeout(this.closeNotification, 5000);
                }
            }
        },

        beforeMount() {
            this.pageMounting();
        },

        mounted() {
            this.pageMounted().then(() => {
                if (!this.masterAdmin && !this.admin && !this.clientAdmin) {
                    this.$router.push('/unauthorized')
                }

                this.model.masterAdmin = this.masterAdmin;
                this.getAccountInformation();
                this.pageReady();
            });
        },

        computed: {
            hasAccountUsers() {
                return this.accountUsers.length > 0;
            },

            isViewingUsers() {
                return this.currentTab === 'users'
            }
        },

        methods: {
            activeTab(e, i) {
                this.currentTab = i === 0 ? "account" : "users";
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

            getAccountInformation() {
                this.$store.dispatch('getAccountInformation', this.model.accountId).then(() => {
                    this.accountData = this.cloneModel(this.$store.getters.accountInformation);
                });
            },

            async getAccountUsers(model) {
                await this.$store.dispatch('getAccountUsers', model);

                return this.$store.getters.accountUsers;
            },

            objectsAreSame(x, y) {
                return this.areEquivalient(x, y)
            },

            goBack() {
                this.redirectUser(this.prevRoute.path)
            },

            handleSelectionChange(val) {
                this.redirectUser(`/userprofile/${val}`)
            },

            registerUser() {
                this.redirectUser(`/registerUser/${this.accountId}`);
            }
        }
    }
</script>

<style scoped>
</style>